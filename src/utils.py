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




# Fonctions utilitaires pour générer des pseudos de joueurs aléatoires, utiles pour faire des tests

def nom_joueur_random():
    noms_random_joueurs = [
        "ShadowHunter", "QuantumGamer", "MysticFury", "CyberNinjaX", "VelocityRaptor",
        "StarlightStriker", "BlazePhoenix", "EchoPulse", "FrostByte", "VortexVoyager",
        "ZenithSpectre", "MirageWanderer", "ThunderVolt", "CelestialSorcerer", "RogueReaper",
        "InfernoProwler", "FrostbiteFalcon", "LunaLurker", "OmegaOracle"
    ]
    return random.choice(noms_random_joueurs)

def nom_personnage_rp_random():
    noms_random_personnages = [
        "Aldric l'Intrépide", "Elena l'Enchanteresse", "Garrick le Gardien", "Isolde la Sombre",
        "Thrain le Vaillant", "Lyria l'Étoilée", "Cedric l'Éclair", "Faelan le Mystique",
        "Elara la Furtive", "Darius le Défenseur", "Sylas le Silencieux", "Vivienne la Vindicative",
        "Gwendolyn la Glorieuse", "Xander le Xénophobe", "Seraphina la Sérénade", "Kael le Courageux",
        "Luna la Légendaire", "Roland le Rédempteur", "Morgana la Maléfique", "Thorin le Tonnerre"
    ]
    return random.choice(noms_random_personnages)


########

def conversion_format_imgs():
    from data import Image
    Image.BACKGROUND_MENU = Image.BACKGROUND_MENU.convert_alpha()
    Image.FOND_MARBRE_TITRE = Image.FOND_MARBRE_TITRE.convert_alpha()
    Image.OEIL_BLEU = Image.OEIL_BLEU.convert_alpha()
    Image.FLECHE = Image.FLECHE.convert_alpha()
    Image.FLECHE_2 = Image.FLECHE_2.convert_alpha()
    Image.EPEE_INFO = Image.EPEE_INFO.convert_alpha()
    Image.ARBALETE_INFO = Image.ARBALETE_INFO.convert_alpha()
    Image.BATON_INFO = Image.BATON_INFO.convert_alpha()
    Image.TABLEAU_PERSO = Image.TABLEAU_PERSO.convert_alpha()
    Image.EPEE_LOGO = Image.EPEE_LOGO.convert_alpha()
    Image.ARBALETE_LOGO = Image.ARBALETE_LOGO.convert_alpha()
    Image.BATON_LOGO = Image.BATON_LOGO.convert_alpha()
    Image.BOUTON_FLECHE_HAUT = Image.BOUTON_FLECHE_HAUT.convert_alpha()
    Image.BOUTON_FLECHE_HAUT_PRESSE = Image.BOUTON_FLECHE_HAUT_PRESSE.convert_alpha()
    Image.BOUTON_FLECHE_BAS = Image.BOUTON_FLECHE_BAS.convert_alpha()
    Image.BOUTON_FLECHE_BAS_PRESSE = Image.BOUTON_FLECHE_BAS_PRESSE.convert_alpha()
    Image.IMAGE_INVENTORY = Image.IMAGE_INVENTORY.convert_alpha()
    Image.TABLEAU_DESCRIPTION_ITEM = Image.TABLEAU_DESCRIPTION_ITEM.convert_alpha()
    Image.MENU_EQUIPEMENT_PERSONNAGE = Image.MENU_EQUIPEMENT_PERSONNAGE.convert_alpha()
    Image.MENU_DONJONS = Image.MENU_DONJONS.convert_alpha()
    Image.IMAGE_BARRE_DE_SORTS = Image.IMAGE_BARRE_DE_SORTS.convert_alpha()

    ### Converting the wood buttons

    for i in range(len(Image.SILVER_WOOD_BUTTONS)):
        Image.SILVER_WOOD_BUTTONS[i] = Image.SILVER_WOOD_BUTTONS[i].convert_alpha()

    ###

    for i in range(len(Image.IMAGES_LEVEL_UP)):
        Image.IMAGES_LEVEL_UP[i] = Image.IMAGES_LEVEL_UP[i].convert_alpha()
    Image.SPAWN = Image.SPAWN.convert_alpha()
    Image.DESERT = Image.DESERT.convert_alpha()
    Image.MARAIS = Image.MARAIS.convert_alpha()
    Image.MARAIS_CORROMPU = Image.MARAIS_CORROMPU.convert_alpha()
    for p in Image.POSITIONS:
        for i in range(len(Image.FRAMES_MOB_RAT[p])):
            Image.FRAMES_MOB_RAT[p][i] = Image.FRAMES_MOB_RAT[p][i].convert_alpha()
        for i in range(len(Image.FRAMES_MOB_BOSS_RAT[p])):
            Image.FRAMES_MOB_BOSS_RAT[p][i] = Image.FRAMES_MOB_BOSS_RAT[p][i].convert_alpha()
        for i in range(len(Image.FRAMES_MOB_CERF[p])):
            Image.FRAMES_MOB_CERF[p][i] = Image.FRAMES_MOB_CERF[p][i].convert_alpha()
        for i in range(len(Image.FRAMES_MOB_BOSS_CERF[p])):
            Image.FRAMES_MOB_BOSS_CERF[p][i] = Image.FRAMES_MOB_BOSS_CERF[p][i].convert_alpha()
        for i in range(len(Image.FRAMES_MOB_ORC[p])):
            Image.FRAMES_MOB_ORC[p][i] = Image.FRAMES_MOB_ORC[p][i].convert_alpha()
        for i in range(len(Image.FRAMES_MOB_LOUP_HUMAIN[p])):
            Image.FRAMES_MOB_LOUP_HUMAIN[p][i] = Image.FRAMES_MOB_LOUP_HUMAIN[p][i].convert_alpha()
        for i in range(len(Image.FRAMES_MOB_DOTUM[p])):
            Image.FRAMES_MOB_DOTUM[p][i] = Image.FRAMES_MOB_DOTUM[p][i].convert_alpha()
        for i in range(len(Image.FRAMES_MOB_FENRIR[p])):
            Image.FRAMES_MOB_FENRIR[p][i] = Image.FRAMES_MOB_FENRIR[p][i].convert_alpha()

        Image.GUERRIER_COURIR_FRAMES[p] = Image.GUERRIER_COURIR_FRAMES[p].convert_alpha()

    for s in Image.SPELL_ICONS:
        Image.SPELL_ICONS[s] = Image.SPELL_ICONS[s].convert_alpha()

    ### Converting images for the game user interface
    # Icons for the GUIMenusPanel
    Image.BAG_ICON = Image.BAG_ICON.convert_alpha()
    Image.EQUIPMENT_ICON = Image.EQUIPMENT_ICON.convert_alpha()
    Image.DONJONS_ICON = Image.DONJONS_ICON.convert_alpha()

    # Icons for the CharacterFrame
    # Image.CHARACTER_LEVEL_FRAME = Image.CHARACTER_LEVEL_FRAME.convert_alpha()

    ###






