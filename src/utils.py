import pygame
import random
import math

from data import Color, Image, Font

from src import items, personnage


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
    return items.Armor(
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
    weapon_types_match_nom_icone = {"Épée": "sword"}
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
    weapon_type = random.choice(list(weapon_types_match_nom_icone))
    weapon_name = weapon_type
    weapon_icon_name = f"{rarete_choisi_alea}_{weapon_types_match_nom_icone[weapon_type]}"

    # Défini les différents bonus de l'arme gagnés en fonction du lvl du mob tuée
    if lvl <= 3:
        if lvl == 3:
            arme_drop_degat = 11
            arme_drop_bonus_pv = 3
            arme_drop_bonus_force = 6
        else:
            arme_drop_degat = 5 + 2 * lvl
            arme_drop_bonus_pv = lvl
            arme_drop_bonus_force = 3 + lvl
    else:
        arme_drop_degat = bonus_increment(11, lvl)
        arme_drop_bonus_pv = bonus_increment(3, lvl)
        arme_drop_bonus_force = bonus_increment(6, lvl)

    return items.Weapon(
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
    Renvoie une surface qui contient tout le texte passé en paramètre afficher sur plusieurs lignes (sans dépassé
    la "surf_width" mentionné).
    """

    mots = [mot.split(' ') for mot in text.splitlines()]
    largeur_espace = text_font.size(' ')[0]
    hauteur_ligne = text_font.get_linesize()

    x = 0
    hauteur_total = hauteur_ligne
    for ligne in mots:
        for mot in ligne:
            largeur_mot, hauteur_mot = text_font.size(mot)
            if x + largeur_mot > surf_width:
                x = 0
                hauteur_total += hauteur_ligne
            x += largeur_mot

    surf_res = pygame.Surface((surf_width, hauteur_total), pygame.SRCALPHA)

    y_courant = 0
    for ligne in mots:
        x_courant = 0

        for mot in ligne:
            largeur_mot, hauteur_mot = text_font.size(mot)
            if x_courant + largeur_mot > surf_width:
                x_courant = 0
                y_courant += hauteur_ligne

            surf_res.blit(text_font.render(mot, True, text_color), (x_courant, y_courant))
            x_courant += largeur_mot + largeur_espace

        y_courant += hauteur_ligne

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
    Image.FLECHE_RETOUR = Image.FLECHE_RETOUR.convert_alpha()
    Image.FLECHE_RETOUR_FOCUS = Image.FLECHE_RETOUR_FOCUS.convert_alpha()
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
        for etat in Image.FRAMES_MOB_RAT:
            Image.FRAMES_MOB_RAT[etat][p] = Image.FRAMES_MOB_RAT[etat][p].convert_alpha()

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

        for etat in Image.TRADUCTIONS_ETATS:
            Image.GUERRIER_FRAMES[etat][p] = Image.GUERRIER_FRAMES[etat][p].convert_alpha()

        for i in range(1, 4):
            Image.GUERRIER_FRAMES[f"Attaquer{i}"][p] = Image.GUERRIER_FRAMES[f"Attaquer{i}"][p].convert_alpha()

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

def scale_frames(frames: dict[str, dict[str, pygame.Surface]], ratio: float) -> dict[str, dict[str, pygame.Surface]]:
    """
    Renvoie le dictionnaire de frames passé en paramètre avec les frames mise à l'échelle par le ratio spécifié.
    """
    nouvelles_frames = {"Lidle": {}, "Marcher": {}, "Mourir": {}}

    for etat in frames:
        for position in frames[etat]:
            nouvelles_frames[etat][position] = pygame.transform.scale_by(frames[etat][position], ratio)

    return nouvelles_frames

def charger_frames(chemin: str, nom: str) -> dict[str, dict[str, pygame.Surface]]:
    """
    Charge des frames avec le nom spécifié en paramètre.

    ATTENTION : le format est très important et doit respecter les règles suivantes :
        - Chemin est le dossier contenant les frames (ex: "./assets/pnjs/rat")
        - Ce dossier doit contenir 3 sous dossiers : "Lidle", "Marcher", "Mourir"
        - Ces sous dossiers doivent contenir 4 images au format png ayant exactement ce nom
          "{nom}_Dos.png", "{nom}_Droite.png", "{nom}_Dos.png", "{nom}_Gauche.png" (en remplaçant "{nom}" par un vrai
          nom ex: "rat_Droite.png")
    """
    positions = ["Face", "Gauche", "Droite", "Dos"]
    frames = {"Lidle": {}, "Marcher": {}, "Mourir": {}}

    for etat in frames:
        for p in positions:
            frames[etat][p] = pygame.image.load(f"{chemin}/{etat}/{nom}_{p}.png")

    return frames



def images_to_sprite_sheet(dossier_contenant_les_images: str, nom_sprite_sheet: str):
    from PIL import Image
    import os

    # Load all images from a folder
    image_folder = dossier_contenant_les_images  # ex : "assets/pnjs/rat/rat_Dos"
    output_file = f"{dossier_contenant_les_images}/{nom_sprite_sheet}"  # ex "assets/pnjs/rat/rat_Dos/rat_Dos.png"

    images = [Image.open(os.path.join(image_folder, img)) for img in os.listdir(image_folder) if
              img.endswith((".png", ".jpg"))]

    # Determine max sprite size
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)

    # Standardize size by padding
    def pad_image(img, target_width, target_height):
        padded = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))  # Transparent background
        x_offset = (target_width - img.width) // 2
        y_offset = (target_height - img.height) // 2
        padded.paste(img, (x_offset, y_offset))
        return padded

    padded_images = [pad_image(img, max_width, max_height) for img in images]

    # Arrange into a sprite sheet (1 row)
    sprite_sheet_width = max_width * len(padded_images)
    sprite_sheet_height = max_height

    sprite_sheet = Image.new("RGBA", (sprite_sheet_width, sprite_sheet_height), (0, 0, 0, 0))

    # Paste images
    for index, img in enumerate(padded_images):
        sprite_sheet.paste(img, (index * max_width, 0))

    # Save sprite sheet
    sprite_sheet.save(output_file)
    print(f"Sprite sheet saved as {output_file}")



def couleur_stat_diff(stat1: int, stat2: int | None) -> pygame.color.Color:
    """
    Cette fonction compare la stat1 et la stat2 passé en paramètre (généralement celles d'équipements), et renvoie
    la couleur :
        - Color.WHITE si la stat1 est égale à la stat2
        - Color.GREEN si la stat1 est plus grande que la stat2
        - Color.RED si la stat1 est inférieur à la stat2

    Cette fonction est utile pour afficher les stats d'un équipement survolé dans l'inventaire d'une certaine
    couleur en fonction de si la stat est meilleur que celle de l'équipement équipé.
    C'est pour cela que dans "stat2" on peut passé None s'il n'y a pas d'équipement équipé (on renvoie Color.WHITE dans ce cas).
    """
    couleur_res = Color.WHITE
    if stat2 is not None:
        if stat1 > stat2:
            couleur_res = Color.GREEN
        elif stat1 < stat2:
            couleur_res = Color.RED

    return couleur_res




def item_info_surf(item: items.Item, perso: "personnage.Personnage" = None) -> pygame.Surface:
    """
    Renvoie une surface permettant d'afficher une multitude d'informations par rapport à l'item passé en paramètre.

    Si un personnage est renseigné, les stats de l'équipement est comparé avec l'équipement de même type équipé par
    le personnage, cela se traduit par la couleur du texte des stats de l'équipement changé par rapport à la fonction
    "couleur_stat_diff".
    """
    surf_res = Image.TABLEAU_DESCRIPTION_ITEM.copy()

    # Traiter les autres types d'items

    if isinstance(item, items.Equipment):
        # Si c'est un équipement on affiche le type suivi du lvl et la couleur du texte en fonction de sa rareté
        surf_res.blit(Font.ARIAL_23.render(f"{item.type} {item.rarity} lvl {item.lvl}", True,
                                                 Color.RARITY_COLORS[item.rarity]), (5, 5))

        # Si c'est une arme, on affiche les dégâts de celle-ci
        if isinstance(item, items.Weapon):
            if perso is not None:
                couleur_info_stat = couleur_stat_diff(item.damage, perso.arme.damage if perso.arme is not None else None)
            else:
                couleur_info_stat = Color.WHITE

            surf_res.blit(Font.ARIAL_23.render(f"{item.damage} dégât{'s' if item.damage > 1 else ''}", True, couleur_info_stat), (10, 50))

            if perso is not None:
                couleur_info_stat_pv = couleur_stat_diff(item.bonus_hp, perso.arme.bonus_hp if perso.arme is not None else None)
                couleur_info_stat_force = couleur_stat_diff(item.bonus_strength, perso.arme.bonus_strength if perso.arme is not None else None)
            else:
                couleur_info_stat_pv = Color.WHITE
                couleur_info_stat_force = Color.WHITE

        elif isinstance(item, items.Armor):  # L'équipement est une Armure (Si on ajoute des types d'équipements différents il faudras rajouter des branches conditionnelles)
            if perso is not None:
                couleur_info_stat = couleur_stat_diff(item.armor, perso.equipment[item.type].armor if perso.equipment[item.type] is not None else None)
            else:
                couleur_info_stat = Color.WHITE

            surf_res.blit(Font.ARIAL_23.render(f"{item.armor} armure", True, couleur_info_stat), (10, 50))

            if perso is not None:
                couleur_info_stat_pv = couleur_stat_diff(item.bonus_hp, perso.equipment[item.type].bonus_hp if perso.equipment[item.type] is not None else None)
                couleur_info_stat_force = couleur_stat_diff(item.bonus_strength, perso.equipment[item.type].bonus_strength if perso.equipment[item.type] is not None else None)
            else:
                couleur_info_stat_pv = Color.WHITE
                couleur_info_stat_force = Color.WHITE
        else:
            couleur_info_stat_pv = Color.WHITE
            couleur_info_stat_force = Color.WHITE

        surf_res.blit(Font.ARIAL_23.render(f"+ {item.bonus_hp} PV", True, couleur_info_stat_pv), (10, 80))
        surf_res.blit(Font.ARIAL_23.render(f"+ {item.bonus_strength} force", True, couleur_info_stat_force), (10, 110))





    return surf_res



