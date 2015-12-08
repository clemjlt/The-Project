# codind:utf8

"""
rajouter gestion tour/temps
- transformer
- rajouter gestion maximum pour les pions
- rajouter equivalence soif --> boisson, alim --> faim
- voir pour remplacer le scan par mesure de distances- 
- rajouter gestion bords carte

"""

from math import sqrt
from random import randint
import os


class Ressources(object):

    """Objet ressource"""

    def __init__(self, nom, type_source, position, quantite, vitesse_regen):

        self.nom = nom
        self.type = type_source
        self.position = position
        self.quantite = quantite
        self.vitesse_regen = vitesse_regen

    def utilisation_source(self, pion):
        if self.quantite > 0:
            print("avt source : ", pion.besoins)
            pion.besoins[self.type] += self.quantite
            self.quantite -= self.quantite
            print("ap source : ", pion.besoins)
        else:
            print("source vide")

    def __repr__(self):

        return "Source de %s, situee a %s, avec %s de %s" % (
            self.type, self.position, self.quantite, self.nom)

viande1 = Ressources("viande1", "faim", (0, 0), 10, 5)
eau1 = Ressources("eau1", "soif", (2, 2), 10, 10)

ressources_carte = [viande1, eau1]


class Pion(object):

    """ objet pion"""

    def __init__(self, pos_init=[0, 0], vision=2, besoins={}):

        self.pos = pos_init
        self.desination = pos_init
        self.vision = vision
        self.besoins = besoins
        self.besoin_a_combler = min(self.besoins)

    def __repr__(self):
        return "Pion, situé en %s avec %s besoins" % (self.pos, self.besoins)

    def _update_pion(self):
        """fnct qui update la pos du pion a chaque tour"""

        self.besoin_a_combler = min(self.besoins)

        self.pos = [self.posx, self.posy]

    def _get_pos_elem(self):
        self.posy = self.pos[1]
        self.posx = self.pos[0]

    def deplacer_pos(self, new_pos):
        self._get_pos_elem()
        print(self.posx, self.posy)

        self.pos = list(new_pos)


    def deplacer_dist(self, *args):
        self._get_pos_elem()

        if len(args) == 1:
            self.posx += args[0]
            self.posy += args[0]
        elif len(args) == 2:
            self.posx += args[0]
            self.posy += args[1]
        else:
            print("trop d'args")

        self._update_pion(self)


besoins = {"faim": 100, "soif": 150}
pion1 = Pion([5, 5], 5, besoins)


rayon_vision = 2
position_pion = [1, 1]


def analyse_chp_visions(pos, chp_vision, ressources):
    posx = pos[0]
    posy = pos[1]

    limite_inf_x = int(posx - chp_vision)
    limite_sup_x = int(posx + chp_vision)

    limite_sup_y = int(posy + chp_vision)
    limite_inf_y = int(posy - chp_vision)

    ressource_chp_vision = []

    for k in range(limite_inf_x, limite_sup_x):

        for j in range(limite_inf_y, limite_sup_y):

            for elem in ressources:
                if elem.position == (k, j) and elem.position != (posx, posy):

                    ressource_chp_vision.append(elem)

    return ressource_chp_vision


def calcul_distance(res_trouvee, position_pion):
    """renvoie l'indice de la ressource la plus proche du pion parmi une liste"""
    distance = []
    nom = []
    for elem in res_trouvee:
        pos = elem.position
        distance.append(
            int(sqrt((position_pion[0] - pos[0])**2 + (position_pion[1] - pos[1])**2)))
        nom.append(elem.nom)
    # print(distance)
    return distance, nom


while pion1.pos < [10, 10]:

    source_trouvees = analyse_chp_visions(
        pion1.pos, pion1.vision, ressources_carte)

    print("Position : ",  pion1.pos,
          "\nsource trouvees : ", source_trouvees, "\n")

    if source_trouvees != []:

        distances_sources, noms_sources = calcul_distance(
            source_trouvees, pion1.pos)
        for dist, nom in zip(distances_sources, noms_sources):

            print("Source de %s a une distance de %s" % (nom, dist))
        choix_source = distances_sources.index(min(distances_sources))
        source_choisie = source_trouvees[choix_source]
        print("source choisie : ", source_choisie.nom, source_choisie.position, "\n")

        pion1.deplacer_pos(source_choisie.position)

        if source_choisie.quantite > 0:
            source_choisie.utilisation_source(pion1)
            print("Position : ",  pion1.pos)
            a = input("Pause")
        else:
            print("source vide")
            print("Position source vide : ",  pion1.pos)
            a = input("Pause")
    else:
        pion1.deplacer_dist(1)
        print("rien trouve")
