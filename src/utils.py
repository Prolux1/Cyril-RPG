import pygame
import random
import math
from src import item


def bonus_increment(nombre, lvl):
    for i in range(3, lvl):
        nombre += math.ceil(nombre / 4)
    return nombre


def convert_number(number):
    return f"{number:_}".replace('_', ' ')

    # units = ["K", "M", "B", "T"]



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
    bonus_rarete = {"common": 1, "uncommon": 1.5, "rare": 2, "epic": 3, "legendary": 5}
    if est_boss:
        raretes_possibles = ["uncommon", "rare", "epic"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[50, 10, 1])[0]
    elif est_world_boss:
        raretes_possibles = ["rare", "epic", "legendary"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[10, 3, 1])[0]
    else:
        raretes_possibles = ["common", "uncommon"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[15, 1])[0]
    equipement_choisi_alea = random.choice(equipements_possibles)
    armor_name = equipement_choisi_alea
    armor_icon_name = equipement_choisi_alea

    if rarete_choisi_alea == "legendary":
        armor_icon_name += "_spécial"


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
    return item.Armor(
        armor_name,
        equipement_choisi_alea,
        lvl,
        math.ceil(equipement_drop_armure * bonus_rarete[rarete_choisi_alea]),
        math.ceil(equipement_drop_bonus_pv * bonus_rarete[rarete_choisi_alea]),
        math.ceil(equipement_drop_bonus_force * bonus_rarete[rarete_choisi_alea]),
        rarete_choisi_alea,
        armor_icon_name
    )


def generation_arme_alea(lvl, est_boss=False, est_world_boss=False):
    """
    Prends en paramètre le lvl d'un mob et renvoie une arme de type aléatoire adapté au lvl.
    Renvoie une arme de meilleur qualité si le mob mort était un boss
    :param lvl: int
    :param est_boss: booléen
    :param est_world_boss: booléen
    :return:
    """
    weapon_types = ["sword"]
    bonus_rarete = {"common": 1, "uncommon": 2, "rare": 3, "epic": 5, "legendary": 7}
    if est_boss:
        raretes_possibles = ["uncommon", "rare", "epic"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[50, 10, 1])[0]
    elif est_world_boss:
        raretes_possibles = ["rare", "epic", "legendary"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[10, 5, 1])[0]
    else:
        raretes_possibles = ["common", "uncommon"]
        rarete_choisi_alea = random.choices(raretes_possibles, weights=[50, 1])[0]
    weapon_type = random.choice(weapon_types)
    weapon_name = weapon_type
    weapon_icon_name = f"{rarete_choisi_alea}_{weapon_type}"

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

    return item.Weapon(
        weapon_name,
        weapon_type,
        lvl,
        math.ceil(arme_drop_degat * bonus_rarete[rarete_choisi_alea]),
        math.ceil(arme_drop_bonus_pv * bonus_rarete[rarete_choisi_alea]),
        math.ceil(arme_drop_bonus_force * bonus_rarete[rarete_choisi_alea]),
        rarete_choisi_alea,
        weapon_icon_name
    )


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


def text_surface(text: str, text_font: pygame.font.Font, text_color: tuple[int, int, int] | pygame.Color, surf_width: int | float) -> pygame.Surface:
    """
    Return a surface that contains all the text passed in parameter,
    without exceeding the specified 'surf_width'
    """
    text_surf = text_font.render(text, True, text_color)
    text_size = text_surf.get_size()
    lines = int(math.ceil(text_font.size(text)[0] / surf_width))
    line_height = text_size[1]


    surf_res = pygame.Surface((surf_width, line_height * lines), pygame.SRCALPHA)

    for i in range(lines):
        width_left = text_size[0] - surf_width * i
        surf_res.blit(
            text_surf.subsurface(pygame.Rect(surf_width * i, 0, min(surf_width, width_left), line_height)),
            (0, line_height * i)
        )

    return surf_res


def fibo(n):
    if n == 0 or n == 1:
        return 1
    elif n < 0:
        return None
    else:
        vals = [1, 1]
        for i in range(2, n + 1):
            vals.append(vals[i-1] + vals[i-2])

        return vals[n]




