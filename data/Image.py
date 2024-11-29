import pygame.image
from data import Color

from src import utils


# chargement de diverses images
BACKGROUND_MENU = pygame.image.load("./assets/map/menu.png")
FOND_MARBRE_TITRE = pygame.image.load("./assets/autres/fond_marbre_titre.png")
OEIL_BLEU = pygame.image.load("./assets/autres/oeil_bleu.png")
FLECHE = pygame.image.load("./assets/fleche.png")
FLECHE_2 = pygame.image.load("./assets/fleche_2.png")
EPEE_INFO = pygame.image.load("./assets/épée_info.png")
ARBALETE_INFO = pygame.image.load("./assets/arbalète_info.png")
BATON_INFO = pygame.image.load("./assets/baton_info.png")
TABLEAU_PERSO = pygame.image.load("./assets/tableau_perso.png")
EPEE_LOGO = pygame.image.load("./assets/logo_armes/épée_logo.png")
ARBALETE_LOGO = pygame.image.load("./assets/logo_armes/arbalète_logo.png")
BATON_LOGO = pygame.image.load("./assets/logo_armes/baton_logo.png")
BOUTON_FLECHE_HAUT = pygame.image.load("./assets/boutons/fleche_haut.png")
BOUTON_FLECHE_HAUT_PRESSE = pygame.image.load("./assets/boutons/fleche_haut_pressé.png")
BOUTON_FLECHE_BAS = pygame.image.load("./assets/boutons/fleche_bas.png")
BOUTON_FLECHE_BAS_PRESSE = pygame.image.load("./assets/boutons/fleche_bas_pressé.png")


# chargement des images de l'interface
IMAGE_INVENTORY = pygame.image.load("./assets/interface_joueur/inventaire.png")
TABLEAU_DESCRIPTION_ITEM = pygame.image.load("./assets/interface_joueur/tableau_description_item.png")
MENU_EQUIPEMENT_PERSONNAGE = pygame.image.load("./assets/interface_joueur/menu_equipement_personnage.png")
MENU_DONJONS = pygame.image.load("./assets/interface_joueur/menu_donjons.png")
IMAGE_BARRE_DE_SORTS = pygame.image.load("./assets/interface_joueur/barre_de_sorts.png")

### Loading the wood buttons
SILVER_WOOD_BUTTONS = [pygame.image.load(f"./assets/interface_joueur/silver_wood_button_{i+1}.png") for i in range(4)]
GOLD_WOOD_BUTTONS = []

###

### Load images for the game user interface
# Icons for the GUIMenusPanel
BAG_ICON = pygame.image.load("./assets/interface_joueur/sac.png")
EQUIPMENT_ICON = pygame.image.load("./assets/interface_joueur/gui_equipment_menu_icon.png")
DONJONS_ICON = pygame.image.load("./assets/interface_joueur/gui_donjons_menu_icon.png")

# Icons for the CharacterFrame
# CHARACTER_LEVEL_FRAME = pygame.image.load("./assets/interface_joueur/character_level_frame.png")


# images lorsque le perso level up
IMAGES_LEVEL_UP = [
    pygame.image.load(f"./assets/level_up/level_up{i}.png") for i in range(1, 6)
]




# chargement des images des zones
SPAWN = pygame.image.load("./assets/map/spawn.png")
DESERT = pygame.image.load("./assets/map/desert.png")
MARAIS = pygame.image.load("./assets/map/marais.png")
MARAIS_CORROMPU = pygame.image.load("./assets/map/marais corrompu.png")

# On enregistre les frames d'un mob sous la forme d'un dictionnaire où les clés sont les positions du mob et les valeurs les différentes animations dans la position souhaiter
POSITIONS = ["Face", "Gauche", "Droite", "Dos"]
POSITIONS_IN_ENGLISH = ["Down", "Left", "Right", "UP"]

FRAMES_MOB_RAT = {}
FRAMES_MOB_BOSS_RAT = {}
FRAMES_MOB_CERF = {}
FRAMES_MOB_BOSS_CERF = {}
FRAMES_MOB_ORC = {}
for p in POSITIONS:
    FRAMES_MOB_RAT[p] = [pygame.image.load(f"./assets/mobs/rat/rat_{p}/rat_{p}_frame_{i}.png") for i in range(1, 5)]
    FRAMES_MOB_BOSS_RAT[p] = [pygame.image.load(f"./assets/mobs/boss_rat/rat_{p}/rat_{p}_frame_{i}.png") for i in range(1, 5)]
    FRAMES_MOB_CERF[p] = [pygame.image.load(f"./assets/mobs/cerf/cerf_{p}/cerf_{p}_frame_{i}.png") for i in range(1, 5)]
    FRAMES_MOB_BOSS_CERF[p] = [pygame.image.load(f"./assets/mobs/boss_cerf/cerf_{p}/cerf_{p}_frame_{i}.png") for i in range(1, 5)]
    FRAMES_MOB_ORC[p] = [pygame.image.load(f"./assets/mobs/Orc/Orc_{p}/Orc_{p}_frame_{i}.png") for i in range(1, 3)]

FRAMES_MOB_LOUP_HUMAIN = utils.frame(pygame.image.load(f"./assets/mobs/Loup humain/Loup humain_{p}/Loup humain_frames_{p}.png"), 30, 44, 4, 9, Color.BLACK)
FRAMES_MOB_DOTUM = utils.frame(pygame.image.load("./assets/mobs/Dotum/Walk.png"), 64, 70, 8, 9, Color.BLACK)
FRAMES_MOB_FENRIR = utils.frame(pygame.image.load("./assets/mobs/Fenrir/Walk.png"), 64, 70, 12, 9, Color.BLACK)

# Charge les différentes frames pour les images quand le guerrier cours en fonction de la direction également
GUERRIER_COURIR_FRAMES = {}
GUERRIER_LIDLE_FRAMES = {}
for i,p in enumerate(POSITIONS_IN_ENGLISH):
    GUERRIER_COURIR_FRAMES[POSITIONS[i]] = pygame.transform.scale_by(
        pygame.image.load(f"assets/personnage/guerrier/{p}/Png/Warrior{p}Walk.png"), 4
    )

    GUERRIER_LIDLE_FRAMES[POSITIONS[i]] = pygame.transform.scale_by(
        pygame.image.load(f"assets/personnage/guerrier/{p}/Png/Warrior{p}Idle.png"), 4
    )


# Spells Icons
SPELL_ICONS = {
    "cleave": pygame.image.load("./assets/logos_sorts/sort1_guerrier.png")
}


# Items Icons
ITEMS_ICONS = {}
rarity_types = ["common", "uncommon", "rare", "epic", "legendary"]
armor_types = ["Casque", "Épaulières", "Plastron", "Gants", "Ceinture", "Jambières", "Bottes"]
for at in armor_types:
    ITEMS_ICONS[at] = pygame.image.load(f"./assets/items/equipement/{at}/{at}_simple.png")
    ITEMS_ICONS[at + "_spécial"] = pygame.image.load(f"./assets/items/equipement/{at}/{at}_spécial.png")

weapon_types = ["sword"]
for wt in weapon_types:
    for rt in rarity_types:
        ITEMS_ICONS[f"{rt}_{wt}"] = pygame.image.load(f"./assets/items/armes/{wt}/{rt}_{wt}.png")













