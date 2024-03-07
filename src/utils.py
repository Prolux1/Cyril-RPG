import pygame
import random
import math
from src import equipement, arme


def regen(entite):
    """
    Regen une entité ayant des PV à hauteur d'1% de ses PV max
    :param entite:
    :return:
    """
    if entite.PV + entite.PV_max / 100 > entite.PV_max:
        return entite.PV_max
    return entite.PV + entite.PV_max / 100


def bonus_increment(nombre, lvl):
    for i in range(3, lvl):
        nombre += math.ceil(nombre / 4)
    return nombre


def conversion_nombre(nombre):
    table = ["K", "M", "B", "T"]
    nombre_str = str(nombre)
    nombre_str_reverse = nombre_str[::-1]
    nombre_convertis = ""
    nb_chiffres = 0

    if len(nombre_str) <= 5:
        for i in range(len(nombre_str)):
            nb_chiffres += 1
            nombre_convertis += nombre_str_reverse[i]
            if nb_chiffres % 3 == 0 and i != len(nombre_str) - 1:
                nombre_convertis += " "

    else:
        nb_milliers = 0
        for i in range(len(nombre_str)):
            nb_chiffres += 1
            if nb_chiffres % 3 == 0:
                nb_milliers += 1

        if nb_milliers >= 6:
            nombre_convertis += table[3] + " "
            nombre_convertis += nombre_str_reverse[(3 * 5) - len(nombre_str) - 3:]
        else:
            nombre_convertis += table[nb_milliers - 2] + " "
            nombre_convertis += nombre_str_reverse[(3 * nb_milliers) - len(nombre_str) - 3:]

            table_nombre = [str(i) for i in range(10)]
            compt_0 = 0
            nombre_convertis_final = ""
            for carac in nombre_convertis:
                if carac in table_nombre:
                    compt_0 += 1
                nombre_convertis_final += carac
                if compt_0 == 3:
                    nombre_convertis_final += " "
                    compt_0 = 0

            if nombre_convertis_final[-1] == " ":
                return nombre_convertis_final[::-1][1:]
            return nombre_convertis_final[::-1]
        #print(nb_milliers)

    return nombre_convertis[::-1]


def generation_equipement_alea(lvl, est_boss=False, est_world_boss=False):
    """
    Prends en paramètre le lvl d'un mob et renvoie un équipement de type aléatoire adapté au lvl.
    Renvoie un équipement de meilleur qualité si le mob mort était un boss
    :param lvl: int
    :param est_boss: booléen
    :param est_world_boss: booléen
    :return:
    """
    equipements_possibles = ["Casque", "Épaulières", "Plastron", "Gants", "Ceinture", "Jambières", "Bottes"]
    bonus_rarete = {"Ordinaire": 1, "Peu commun": 1.5, "Rare": 2, "Épique": 3, "Légendaire": 5}
    if est_boss:
        raretes_possibles = ["Peu commun", "Rare", "Épique"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[50, 10, 1])[0]
    elif est_world_boss:
        raretes_possibles = ["Rare", "Épique", "Légendaire"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[10, 3, 1])[0]
    else:
        raretes_possibles = ["Ordinaire", "Peu commun"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[15, 1])[0]
    equipement_choisi_alea = random.choice(equipements_possibles)

    # Défini les différents bonus de l'équipement gagné en fonction du lvl du mob tuée
    if lvl <= 3:
        if lvl == 3:
            equipement_drop_armure = 10
            equipement_drop_bonus_pv = 3
            equipement_drop_bonus_force = 5
        else:
            equipement_drop_armure = 3 + 2 * lvl
            equipement_drop_bonus_pv = lvl
            equipement_drop_bonus_force = 1 + lvl
    else:
        equipement_drop_armure = bonus_increment(10, lvl)
        equipement_drop_bonus_pv = bonus_increment(3, lvl)
        equipement_drop_bonus_force = bonus_increment(5, lvl)
    return equipement.Equipement(equipement_choisi_alea, lvl, math.ceil(equipement_drop_armure * bonus_rarete[rarete_choisi_alea]), math.ceil(equipement_drop_bonus_pv * bonus_rarete[rarete_choisi_alea]), math.ceil(equipement_drop_bonus_force * bonus_rarete[rarete_choisi_alea]), rarete_choisi_alea)


def generation_arme_alea(lvl, est_boss=False, est_world_boss=False):
    """
    Prends en paramètre le lvl d'un mob et renvoie une arme de type aléatoire adapté au lvl.
    Renvoie une arme de meilleur qualité si le mob mort était un boss
    :param lvl: int
    :param est_boss: booléen
    :param est_world_boss: booléen
    :return:
    """
    bonus_rarete = {"Ordinaire": 1, "Peu commun": 2, "Rare": 3, "Épique": 5, "Légendaire": 7}
    if est_boss:
        raretes_possibles = ["Peu commun", "Rare", "Épique"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[50, 10, 1])[0]
    elif est_world_boss:
        raretes_possibles = ["Rare", "Épique", "Légendaire"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[10, 5, 1])[0]
    else:
        raretes_possibles = ["Ordinaire", "Peu commun"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[50, 1])[0]

    # Défini les différents bonus de l'arme gagnés en fonction du lvl du mob tuée
    if lvl <= 3:
        if lvl == 3:
            arme_drop_degat = 11
            arme_drop_bonus_pv = 3
            arme_drop_bonus_force = 6
        else:
            arme_drop_degat = 5 + 2*lvl
            arme_drop_bonus_pv = lvl
            arme_drop_bonus_force = 3 + lvl
    else:
        arme_drop_degat = bonus_increment(11, lvl)
        arme_drop_bonus_pv = bonus_increment(3, lvl)
        arme_drop_bonus_force = bonus_increment(6, lvl)

    return arme.Arme(lvl, math.ceil(arme_drop_degat * bonus_rarete[rarete_choisi_alea]), math.ceil(arme_drop_bonus_pv * bonus_rarete[rarete_choisi_alea]), math.ceil(arme_drop_bonus_force * bonus_rarete[rarete_choisi_alea]), rarete_choisi_alea)


def frame(frame_sheet, largeur, hauteur, taille, nb_frames, couleur=None):
    """
    :param frame_sheet: une image contenant toutes les frames d'un mob
    :param largeur: largeur de la frame
    :param hauteur: hauteur de la frame
    :param taille: taille de la frame
    :param  nb_frames: nombres de frames dans la frame_sheet
    :param couleur: couleur (R, G, B) du fond de la frame à enlevé s'il y en a un
    :return: frame
    """
    frames_mob = {"Dos": [], "Gauche": [], "Face": [], "Droite": []}
    for j, orientation in enumerate(frames_mob):
        liste_frames_position = []
        for i in range(nb_frames):
            image_frame = pygame.Surface((largeur, hauteur))
            image_frame.blit(frame_sheet, (0, 0), pygame.rect.Rect(largeur * i, hauteur * j, largeur, hauteur))
            image_frame = pygame.transform.scale(image_frame, (largeur * taille, hauteur * taille))
            if couleur:
                image_frame.set_colorkey(couleur)
            liste_frames_position.append(image_frame)
        frames_mob[orientation] = liste_frames_position

    return frames_mob
















