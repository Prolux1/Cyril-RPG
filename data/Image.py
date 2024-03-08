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
IMAGE_INVENTAIRE = pygame.image.load("./assets/interface_joueur/inventaire.png")
TABLEAU_DESCRIPTION_ITEM = pygame.image.load("./assets/interface_joueur/tableau_description_item.png")
IMAGE_MENU_EQUIPEMENT_PERSONNAGE = pygame.image.load("./assets/interface_joueur/menu_equipement_personnage.png")
IMAGE_BARRE_DE_SORTS = pygame.image.load("./assets/interface_joueur/barre_de_sorts.png")
SILVER_WOOD_BUTTON_1 = pygame.image.load("./assets/interface_joueur/silver_wood_button_1.png")
SILVER_WOOD_BUTTON_2 = pygame.image.load("./assets/interface_joueur/silver_wood_button_2.png")
SILVER_WOOD_BUTTON_3 = pygame.image.load("./assets/interface_joueur/silver_wood_button_3.png")

# Load images for the game user interface
bag_sprite_sheet = pygame.image.load("./assets/interface_joueur/sac.png")
bag_sprite_sheet_rect = bag_sprite_sheet.get_rect()
image_bag_closed_rect = bag_sprite_sheet_rect.copy()
IMAGE_BAG_CLOSE = bag_sprite_sheet.subsurface((0, 0, bag_sprite_sheet.get_width() / 2, bag_sprite_sheet.get_height()))
Image_BAG_OPEN = bag_sprite_sheet.subsurface((bag_sprite_sheet.get_width() / 2, 0, bag_sprite_sheet.get_width() / 2, bag_sprite_sheet.get_height()))



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

# Images of the character depending on its orientation

CHARACTER_POSTURES = {
    "Face": pygame.image.load("./assets/personnage/guerrier_devant.png"),
    "Droite": pygame.image.load("./assets/personnage/guerrier_droite.png"),
    "Gauche": pygame.image.load("./assets/personnage/guerrier_gauche.png"),
    "Dos": pygame.image.load("./assets/personnage/guerrier_retourné.png")
}

# Spells Icons

SPELL_TRANCHER_ICON = pygame.image.load("./assets/logos_sorts/sort1_guerrier.png")













