import pygame
import os
import pickle
import random
import math
import datetime

from config import *
from src import *
from data import *


class CyrilRpg:

    def __init__(self):
        pygame.init()  # Initialization of pygame module
        pygame.mixer.init()  # Initialization of sound module for pygame
        pygame.display.set_caption("Cyril RPG")  # Window title
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        self.mouse_pos = pygame.mouse.get_pos()
        self.components = []
        self.clock = pygame.time.Clock()
        self.time = pygame.time.get_ticks() / 1000

        self.player = None

        self.lac_sud = obstacle.Obstacle(pygame.image.load("./assets/obstacles/lac_sud.png").convert_alpha())
        self.zones = {
            "Spawn": zone.Zone("Spawn", 15),
            "Desert": zone.Zone("Desert", 15),
            "Marais": zone.Zone("Marais", 15),
            "Marais corrompu": zone.Zone("Marais corrompu", 1)
        }
        self.monde = ["Marais corrompu", "Marais", "Desert"]

        # Ajout des différents obstacles des zones
        self.zones["Marais"].ajouter_obstacles([
            pygame.Rect(640, 325, 640, 240),
            pygame.Rect(0, 0, 394, 417),
            pygame.Rect(0, 710, 411, 370),
            pygame.Rect(786, 876, 163, 155),
            pygame.Rect(1054, 23, 154, 158),
            pygame.Rect(1410, 50, 163, 155),
            pygame.Rect(1587, 278, 163, 155),
            pygame.Rect(1465, 658, 154, 158)
        ])

        self.zones["Marais corrompu"].ajouter_obstacles([
            pygame.Rect(0, 0, 1920, 140),
            pygame.Rect(0, 140, 175, 800),
            pygame.Rect(0, 940, 1920, 140)
        ])

    def run(self):
        # self.load_data()
        self.convert_images()

        self.main_menu()

        while 1:
            self.update()
            self.handle_events()
            self.draw()
            pygame.display.flip()

    def update(self):
        self.clock.tick(60)
        self.time = pygame.time.get_ticks() / 1000
        self.mouse_pos = pygame.mouse.get_pos()
        for c in self.components:
            c.update(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    self.save_screenshot()
                elif event.key == pygame.K_ESCAPE:  # To remove
                    self.quit()

            for c in self.components:
                c.handle_event(self, event)

    def draw(self):
        self.window.fill(Color.BLACK)
        for c in self.components:
            c.draw(self.window)

    def quit(self):
        # self.save_data()
        pygame.quit()
        exit()

    def load_data(self):
        """
        All data will be pickle and saved in save/data.pkl.
        """
        # We load data only if save directory exists,
        # else we create it
        if os.path.isdir("save"):
            # If the data.pkl file exist, we load the data
            # else we do nothing because we have nothing to load
            if os.path.isfile("save/save.pkl"):
                with open("save/save.pkl", "rb") as save_file:
                    data = pickle.load(save_file)
                    # Todo: change the structure of data to be a list like data["player"] to get player data
                    self.player = data
        else:
            os.mkdir(os.path.join("save"))

    def save_data(self):
        if not os.path.isdir("save"):
            os.mkdir(os.path.join("save"))

        with open("save/save.pkl", "wb") as save_file:
            pickle.dump(self.player, save_file)

    def convert_images(self):
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
            Image.CHARACTER_POSTURES[p] = Image.CHARACTER_POSTURES[p].convert_alpha()

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


    def save_screenshot(self):
        if not os.path.isdir("screenshots"):
            os.mkdir(os.path.join("screenshots"))

        screenshot_date = datetime.datetime.today().isoformat(" ")
        screenshot_date = screenshot_date.replace(":", "-")
        screenshot_date = screenshot_date.replace(".", "-")
        pygame.image.save(self.window, f"screenshots/{screenshot_date}.png")

    def main_menu(self):
        self.components = [
            interfaceClasses.BackgroundImage(Image.BACKGROUND_MENU),
            interfaceClasses.StaticImage(WINDOW_WIDTH / 2, 110, Image.FOND_MARBRE_TITRE, center=True),
            interfaceClasses.StaticImage(WINDOW_WIDTH / 2 + 135, 110, Image.OEIL_BLEU),
            interfaceClasses.BasicInterfaceTextElement(WINDOW_WIDTH / 2, 110, "Cyril RPG", Font.TITLE, Color.BLACK, center=True),
            interface.PlayButton(Image.SILVER_WOOD_BUTTONS[2], WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3, "Play", Font.ARIAL_40, Color.GREY),
            interface.SettingsButton(Image.SILVER_WOOD_BUTTONS[1], WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2.25, "Settings", Font.ARIAL_40, Color.GREY, center=True),
            interface.QuitButton(Image.SILVER_WOOD_BUTTONS[0], WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.8, "Quit", Font.ARIAL_40, Color.GREY, center=True)
        ]

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps(), WINDOW_WIDTH, 0))
            # for i in range(3000):  # Todo: I WOKE UP IN A NEW BUGATTI
            #     lol = interface.FpsViewer(self.clock.get_fps())
            #     lol.rect.topleft = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
            #     self.components.append(lol)

    def character_creation_menu(self):
        self.components = [
            interfaceClasses.BackgroundColor((WINDOW_WIDTH, WINDOW_HEIGHT), Color.DARK_GREY),
            interface.CharacterNameInput(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100, Font.ARIAL_23, Color.WHITE)
        ]

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps(), WINDOW_WIDTH, 0))

    def character_selection_menu(self):
        self.components = [
            interfaceClasses.BackgroundColor((WINDOW_WIDTH, WINDOW_HEIGHT), Color.DARK_GREY)
        ]

        # Adding all the characters to a list to select one of them
        for i, c in enumerate(self.player.characters):
            self.components.append(
                interface.CharacterSelectionButton(Image.SILVER_WOOD_BUTTONS[0], WINDOW_WIDTH / 2, 200 + (100 * (i+1)), c, Font.ARIAL_23, Color.GREY)
            )

        # Adding a button to create new character
        self.components.append(interface.CharacterCreationButton(Image.SILVER_WOOD_BUTTONS[1], WINDOW_WIDTH / 2, WINDOW_HEIGHT - Image.SILVER_WOOD_BUTTONS[1].get_height(),"Create character", Font.ARIAL_23, Color.GREY))

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps(), WINDOW_WIDTH, 0))

    def settings_menu(self):
        self.components = [
            interfaceClasses.BackgroundColor((WINDOW_WIDTH, WINDOW_HEIGHT), Color.DARK_GREY)
        ]

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps(), WINDOW_WIDTH, 0))

    def enter_world(self, character):
        self.zones[character.zone].add_character(character)
        self.components = [
            self.zones[character.zone],
            gui.GameUserInterface(character)
        ]

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps(), WINDOW_WIDTH, 0))


    def info_classe_guerrier(self):
        # affichage des différentes informations de la classe guerrier
        affiche_info_nom_classe = self.police.render("Guerrier lvl 1", True, self.Noir)
        self.window.blit(affiche_info_nom_classe, [900, 300])

        affiche_info_hp = self.police.render("150 PV", True, self.Noir)
        self.window.blit(affiche_info_hp, [750, 400])

        affiche_info_style_combat = self.police.render("Style de combat au corps à corps", True, self.Noir)
        self.window.blit(affiche_info_style_combat, [750, 500])

        affiche_info_classe_l1 = self.police_description.render("Le guerrier est un combattant hors pair", True, self.Noir)
        affiche_info_classe_l2 = self.police_description.render("équipée d'une armure lourde et d'une grande", True, self.Noir)
        affiche_info_classe_l3 = self.police_description.render("épée. Il utilise sa rage pour pourfendre", True, self.Noir)
        affiche_info_classe_l4 = self.police_description.render("les adversaires les plus coriaces.", True, self.Noir)
        self.window.blit(affiche_info_classe_l1, [1300, 400])
        self.window.blit(affiche_info_classe_l2, [1300, 430])
        self.window.blit(affiche_info_classe_l3, [1300, 460])
        self.window.blit(affiche_info_classe_l4, [1300, 490])

        self.window.blit(self.epee_info, [1220, 430])

    def info_classe_chasseur(self):
        # affichage des différentes informations de la classe chasseur
        affiche_info_nom_classe = self.police.render("Chasseur lvl 1", True, self.Noir)
        self.window.blit(affiche_info_nom_classe, [900, 300])

        affiche_info_hp = self.police.render("137 PV", True, self.Noir)
        self.window.blit(affiche_info_hp, [750, 400])

        affiche_info_style_combat = self.police.render("Style de combat à distance", True, self.Noir)
        self.window.blit(affiche_info_style_combat, [750, 500])

        affiche_info_classe_l1 = self.police_description.render("Le guerrier est un combattant hors pair", True, self.Noir)
        affiche_info_classe_l2 = self.police_description.render("équipée d'une armure lourde et d'une grande", True, self.Noir)
        affiche_info_classe_l3 = self.police_description.render("épée. Il utilise sa rage pour pourfendre", True, self.Noir)
        affiche_info_classe_l4 = self.police_description.render("les adversaires les plus coriaces.", True, self.Noir)
        self.window.blit(affiche_info_classe_l1, [1300, 400])
        self.window.blit(affiche_info_classe_l2, [1300, 430])
        self.window.blit(affiche_info_classe_l3, [1300, 460])
        self.window.blit(affiche_info_classe_l4, [1300, 490])

        self.window.blit(self.arbalete_info, [1120, 430])

    def info_classe_mage(self):
        # affichage des différentes informations de la classe mage
        affiche_info_nom_classe = self.police.render("Mage lvl 1", True, self.Noir)
        self.window.blit(affiche_info_nom_classe, [900, 300])

        affiche_info_hp = self.police.render("124 PV", True, self.Noir)
        self.window.blit(affiche_info_hp, [750, 400])

        affiche_info_style_combat = self.police.render("Style de combat à distance", True, self.Noir)
        self.window.blit(affiche_info_style_combat, [750, 500])

        affiche_info_classe_l1 = self.police_description.render("Le guerrier est un combattant hors pair", True, self.Noir)
        affiche_info_classe_l2 = self.police_description.render("équipée d'une armure lourde et d'une grande", True, self.Noir)
        affiche_info_classe_l3 = self.police_description.render("épée. Il utilise sa rage pour pourfendre", True, self.Noir)
        affiche_info_classe_l4 = self.police_description.render("les adversaires les plus coriaces.", True, self.Noir)
        self.window.blit(affiche_info_classe_l1, [1300, 400])
        self.window.blit(affiche_info_classe_l2, [1300, 430])
        self.window.blit(affiche_info_classe_l3, [1300, 460])
        self.window.blit(affiche_info_classe_l4, [1300, 490])

        self.window.blit(self.baton_info, [1130, 350])

    def affichage_menu_jouer_perso(self):
        # affichage d'une flèche si on veut retourner au menu principal
        if 10 < self.mouse_pos[0] < 110 and 10 < self.mouse_pos[1] < 75:
            self.window.blit(self.fleche_2, [10, 10])
        else:
            self.window.blit(self.fleche, [10, 10])

        # affiche un message d'aide indiquant qu'il faut utiliser les fleches du clavier pour parcourir les différents perso
        affiche_info_fleches = self.police.render("Utilise les flèches haut et bas du clavier", True, self.Noir)
        affiche_info_fleches2 = self.police.render("pour parcourir tes différents personnage", True, self.Noir)
        self.window.blit(affiche_info_fleches, [100, 500])
        self.window.blit(affiche_info_fleches2, [100, 530])

        # affichage des boutons fleche du haut et bas pour indiquer comment parcourir les différents perso
        self.window.blit(self.bouton_fleche_haut, [200, 600])
        self.window.blit(self.bouton_fleche_bas, [200, 632])

        # affichage du nombre de perso du joueur (max 3 persos)
        affiche_nombre_persos = self.police.render("Nombre de personnages : " + str(len(self.joueur.personnages)) + " / 3", True, self.Noir)
        self.window.blit(affiche_nombre_persos, [750, 300])

        # affichage du tableau (image) où va apparaître les différents personnages
        self.window.blit(self.tableau_perso, [660, 350])

        # affichage des différents personnages du joueur
        espacement = 0
        for personnage in self.joueur.personnages:
            if personnage.classe == "Guerrier":
                self.window.blit(self.epee_logo, [670, 350 + espacement])
            elif personnage.classe == "Chasseur":
                self.window.blit(self.arbalete_logo, [670, 350 + espacement])
            else:
                self.window.blit(self.baton_logo, [700, 360 + espacement])
            affiche_perso_courant = self.police.render(personnage.nom + " lvl " + str(personnage.lvl), True, self.Noir)
            self.window.blit(affiche_perso_courant, [750, 400 + espacement])
            espacement += 150

        # affichage du bouton pour entrer dans le jeu
        if 1475 < self.mouse_pos[0] < 1760 and 785 < self.mouse_pos[1] < 850:
            pygame.draw.rect(self.window, self.Gris_clair, [1477, 787, 281, 61])  # le background du bouton
        else:
            pygame.draw.rect(self.window, self.Gris, [1477, 787, 281, 61])
        pygame.draw.rect(self.window, self.Noir, [1475, 785, 285, 65], 3)
        affiche_entrer_jeu = self.police.render("Entrer dans le jeu", True, self.Noir)
        self.window.blit(affiche_entrer_jeu, [1500, 800])


    def affichage_menu_parametre(self):
        # Titre
        affiche_titre = self.police.render("Paramètres", True, self.Noir)
        self.window.blit(affiche_titre, [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10])

    def affichage_menu_creation_perso(self):
        # affichage classe guerrier
        if 400 < self.mouse_pos[0] < 510 and 483 < self.mouse_pos[1] < 510:
            affiche_classe_guerrier = self.police_2.render("Guerrier", True, self.Noir)
        else:
            affiche_classe_guerrier = self.police.render("Guerrier", True, self.Noir)
        self.window.blit(affiche_classe_guerrier, [400, 480])

        # affichage classe chasseur
        if 400 < self.mouse_pos[0] < 530 and 583 < self.mouse_pos[1] < 610:
            affiche_classe_chasseur = self.police_2.render("Chasseur", True, self.Noir)
        else:
            affiche_classe_chasseur = self.police.render("Chasseur", True, self.Noir)
        self.window.blit(affiche_classe_chasseur, [400, 580])

        # affichage classe mage
        if 400 < self.mouse_pos[0] < 475 and 683 < self.mouse_pos[1] < 710:
            affiche_classe_mage = self.police_2.render("Mage", True, self.Noir)
        else:
            affiche_classe_mage = self.police.render("Mage", True, self.Noir)
        self.window.blit(affiche_classe_mage, [400, 680])

        # affiche une case où l'on peut rentrer le nom de son personnage
        affiche_texte_nom = self.police.render("Nom :", True, self.Noir)
        self.window.blit(affiche_texte_nom, [950, 800])

        affiche_creer = self.police.render("Créer le personnage", True, self.Noir)
        self.window.blit(affiche_creer, [880, 920])

        pygame.draw.rect(self.window, self.Noir, [900, 850, 200, 50], 2)

        # affichage d'une flèche si on veut retourner au menu principal
        if 10 < self.mouse_pos[0] < 110 and 10 < self.mouse_pos[1] < 75:
            self.window.blit(self.fleche_2, [10, 10])
        else:
            self.window.blit(self.fleche, [10, 10])

        # affichage d'aide pour le nom
        affiche_nom_info = self.police.render("Le nom du personnage ne doit pas contenir d'espaces", True, self.Rouge)
        affiche_nom_info_2 = self.police.render("Les espaces présents seront automatiquement", True, self.Rouge)
        affiche_nom_info_3 = self.police.render("supprimés lors de la création du personnage", True, self.Rouge)
        self.window.blit(affiche_nom_info, [1150, 700])
        self.window.blit(affiche_nom_info_2, [1150, 730])
        self.window.blit(affiche_nom_info_3, [1150, 760])

    def menu_creer_perso(self):
        classe_select = 'Guerrier'
        execution = True
        while execution:
            self.horloge.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()  # récupère la position de la souris
            self.temps = pygame.time.get_ticks() / 1000
            self.window.fill(self.Blanc)
            evenements = pygame.event.get()
            for event in evenements:  # à chaque événement provoqué par l'utilisateur
                if event.type == pygame.QUIT:  # si un des événements évoque la fermeture d'une fenêtre (par exemple cliquez sur la croix rouge en haut a droite ou appuyez alt+F4) ferme le jeu
                    pygame.quit()
                    exit()
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 10 < self.mouse_pos[0] < 110 and 10 < self.mouse_pos[1] < 75:  # si on clique sur la fleche, retour au menu
                        execution = False
                    if 400 < self.mouse_pos[0] < 510 and 483 < self.mouse_pos[1] < 510:  # Info Guerrier
                        classe_select = 'Guerrier'
                    if 400 < self.mouse_pos[0] < 530 and 583 < self.mouse_pos[1] < 610:  # Info Chasseur
                        classe_select = 'Chasseur'
                    if 400 < self.mouse_pos[0] < 475 and 683 < self.mouse_pos[1] < 710:  # Info Mage
                        classe_select = 'Mage'
                    if 900 < self.mouse_pos[0] < 1100 and 850 < self.mouse_pos[1] < 900:  # si on clique sur la case où l'on peut écrire on lance l'écriture
                        ecrire_pseudo = True
                    else:
                        ecrire_pseudo = False
                    if 900 < self.mouse_pos[0] < 1160 and 920 < self.mouse_pos[1] < 947:  # si on clique sur créer un nouveau personnage
                        if len(self.joueur.personnages) < 3:
                            pass
                            # nom_personnage.value = nom_personnage.value.replace(" ", "")
                            # if len(nom_personnage.value) > 0:
                            #     # print("Le nom du personnage est " + nom_personnage.value + " et sa classe est " + classe_select)
                            #     # nouveau_personnage = Personnage(nom_personnage.value, classe_select)
                            #     # self.joueur.personnages.append(nouveau_personnage)
                            #     self.joueur.nouveau_personnage(src.personnage.Personnage(nom_personnage.value, classe_select))
                            #     execution = False

            if classe_select == 'Guerrier':
                self.info_classe_guerrier()
            elif classe_select == 'Chasseur':
                self.info_classe_chasseur()
            elif classe_select == 'Mage':
                self.info_classe_mage()

            self.affichage_menu_creation_perso()
            # self.fenetre.blit(nom_personnage.surface, [908, 858])

            pygame.display.flip()

    def menu(self):
        execution = True
        background_decalage = 0
        background_decalage_sens_inverse = False
        self.music_menu.play(-1)
        while execution:
            self.horloge.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()  # récupère la position de la souris
            self.window.fill(self.Blanc)
            for event in pygame.event.get():  # à chaque événement provoqué par l'utilisateur
                if event.type == pygame.QUIT:  # si un des événements évoque la fermeture d'une fenêtre (par exemple cliquez sur la croix rouge en haut a droite ou appuyez alt+F4) ferme le jeu
                    execution = False
                if event.type == pygame.K_ESCAPE:
                    execution = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 5 < self.mouse_pos[0] < 45 and 5 < self.mouse_pos[1] < 45:  # si on clique sur la croix, arrêt du jeu
                        pygame.quit()
                        exit()
                    if 900 < self.mouse_pos[0] < 980 and 353 < self.mouse_pos[1] < 383:  # si on clique sur jouer
                        self.music_menu.stop()
                        self.menu_jouer_perso()
                        self.music_menu.play(-1)
                    if 800 < self.mouse_pos[0] < 1090 and 433 < self.mouse_pos[1] < 463:  # si on crée un nouveau perso
                        self.music_menu.stop()
                        self.menu_creer_perso()
                        self.music_menu.play(-1)

            self.affichage_menu(background_decalage)

            if background_decalage == -530:
                background_decalage_sens_inverse = True
            elif background_decalage == 0:
                background_decalage_sens_inverse = False

            if background_decalage_sens_inverse:
                background_decalage += 0.5
            else:
                background_decalage -= 0.5

            pygame.display.flip()  # Permet de mettre à jour la fenêtre

    def menu_jouer_perso(self):
        espacement = 0
        execution = True
        while execution:
            self.horloge.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()  # récupère la position de la souris
            self.window.fill(self.Blanc)
            for event in pygame.event.get():  # à chaque événement provoqué par l'utilisateur
                if event.type == pygame.QUIT: # si un des événements évoque la fermeture d'une fenêtre (par exemple cliquez sur la croix rouge en haut a droite ou appuyez alt+F4) ferme le jeu
                    pygame.quit()  # on ferme le module pygame
                    exit()  # on termine immédiatement tous les processus
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if 10 < self.mouse_pos[0] < 110 and 10 < self.mouse_pos[1] < 75:  # si on clique sur la fleche, retour au menu
                        execution = False
                    if 1475 < self.mouse_pos[0] < 1760 and 785 < self.mouse_pos[1] < 850:  # si on clique sur entrer dans le jeu
                        if len(self.joueur.personnages) > 0:
                            perso_select = self.joueur.personnages[espacement // 150]
                            self.music_zone1.play(-1)
                            self.zones[perso_select.zone].personnages_zone.append(perso_select)
                            #donnees_perso = {"nom": perso_select.nom, "id": perso_select.id, "classe": perso_select.classe, "lvl": perso_select.lvl, "PV": perso_select.PV, "PV_max": perso_select.PV_max, "orientation": perso_select.orientation, "x": perso_select.x, "y": perso_select.y}
                            #envoyer_donnees_perso = pickle.dumps(donnees_perso)
                            #envoyer_donnees_perso = bytes(f'{len(envoyer_donnees_perso)}', "utf-8") + envoyer_donnees_perso
                            #self.reseau.envoyer(envoyer_donnees_perso)
                            self.jeu(perso_select)
                if len(self.joueur.personnages) > 1:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.window.blit(self.bouton_fleche_haut_presse, [250, 632])
                            if espacement == 0:
                                pass
                            else:
                                espacement -= 150
                        if event.key == pygame.K_DOWN:
                            self.window.blit(self.bouton_fleche_bas_presse, [250, 632])
                            if espacement + 150 == 150 * len(self.joueur.personnages):
                                pass
                            else:
                                espacement += 150

            if len(self.joueur.personnages) > 0:
                # affiche une fleche qui indique quel perso est sélectionné
                affiche_bouton_select = self.police_2.render("→", True, self.Noir)
                self.window.blit(affiche_bouton_select, [600, 386 + espacement])

                # affichage du nom du perso sélectionner
                perso_select = self.joueur.personnages[espacement // 150]
                affiche_perso_select = self.police.render(perso_select.nom + " lvl " + str(perso_select.lvl), True, self.Noir)
                self.window.blit(affiche_perso_select, [1500, 750])

            self.affichage_menu_jouer_perso()

            pygame.display.flip()  # Permet de mettre à jour la fenêtre

    def jeu(self, personnage):
        """
        Lance le jeu avec le personnage passé en paramètre.
        :param personnage:
        :return:
        """
        execution = True
        temps_regen = None  # Temps à attendre entre chaque regen de PV
        affiche_zone_effet_s1 = True
        affiche_zone_effet_s2 = False
        xp_obtenu = 0
        mob_spawn_timer = None
        level_up, level_up_alpha = False, 51
        dic_menu = {"Inventaire": False, "Personnage": False}  # État des différents menus de l'interface du joueur
        pygame.key.set_repeat(200, 30)
        personnage.connecte = True
        sort_lancer = None
        temps_attaques_tourbillon = [None, 0]  # liste indiquant le temps à attendre et le nombre d'attaques effectuer
        # Stuff de départ lvl 22 cheaté :)
        #for i in range(30):
        #    personnage.ajouter_item_inventaire(generation_equipement_alea(22, True))
        #personnage.ajouter_item_inventaire(generation_arme_alea(22, True))
        while execution:
            self.horloge.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()  # récupère la position de la souris
            self.temps = pygame.time.get_ticks() / 1000
            self.window.fill(self.Blanc)
            mobs_zone = self.zones[personnage.zone].monstres_zone

            self.affichage_jeu(personnage)
            self.affichage_interface_jeu(personnage, dic_menu)

            # affiche la barre des sorts (3 emplacements de sorts pour l'instant)

            for mob in mobs_zone:
                if mob.est_mort():
                    temps_affiche_xp = self.temps.__round__()

            # affiche l'xp obtenu suite aux monstres tués
            if xp_obtenu != 0:
                if temps_affiche_xp + 2 > self.temps.__round__():
                    affiche_xp_obtenu = self.police.render("+ " + str(xp_obtenu) + " XP", True, self.Violet)
                    self.window.blit(affiche_xp_obtenu, [personnage.x + 100, personnage.y + 50])
                else:
                    xp_obtenu = 0

            # Affiche un message indiquant que le joueur à level up
            # if level_up:
            #     if temps_affiche_level_up + 2 > self.temps:
            #         if temps_affiche_level_up + level_up_alpha / 255 < self.temps:
            #             if level_up_alpha != 255:
            #                 level_up_alpha += 51
            #         self.images_level_up[(level_up_alpha // 51) - 1].set_alpha(level_up_alpha)
            #         self.window.blit(self.images_level_up[(level_up_alpha // 51) - 1], [personnage.x - 80, personnage.y - 240])
            #     else:
            #         level_up = False
            #         level_up_alpha = 51

            # Si le personnage s'approche des bordures d'une zone, il change de zone
            if personnage.x <= 20 and self.monde.index(personnage.zone) != 0:
                self.zones[personnage.zone].personnages_zone.remove(personnage)
                personnage.zone = self.monde[self.monde.index(personnage.zone) - 1]
                self.zones[personnage.zone].personnages_zone.append(personnage)
                personnage.x = 1750
            elif personnage.x >= 1800 and self.monde.index(personnage.zone) != len(self.monde) - 1:
                zone_quitte = personnage.zone
                self.zones[personnage.zone].personnages_zone.remove(personnage)
                personnage.zone = self.monde[self.monde.index(personnage.zone) + 1]
                self.zones[personnage.zone].personnages_zone.append(personnage)
                if zone_quitte == "Marais corrompu":
                    personnage.x = 50
                    personnage.y = 450
                else:
                    personnage.x = 50

            pygame.display.flip()  # Permet de mettre à jour la fenêtre


if __name__ == "__main__":
    noms_random_joueurs = [
        "ShadowHunter", "QuantumGamer", "MysticFury", "CyberNinjaX", "VelocityRaptor",
        "StarlightStriker", "BlazePhoenix", "EchoPulse", "FrostByte", "VortexVoyager",
        "ZenithSpectre", "MirageWanderer", "ThunderVolt", "CelestialSorcerer", "RogueReaper",
        "InfernoProwler", "FrostbiteFalcon", "LunaLurker", "OmegaOracle"
    ]

    noms_random_personnages = [
        "Aldric l'Intrépide", "Elena l'Enchanteresse", "Garrick le Gardien", "Isolde la Sombre",
        "Thrain le Vaillant", "Lyria l'Étoilée", "Cedric l'Éclair", "Faelan le Mystique",
        "Elara la Furtive", "Darius le Défenseur", "Sylas le Silencieux", "Vivienne la Vindicative",
        "Gwendolyn la Glorieuse", "Xander le Xénophobe", "Seraphina la Sérénade", "Kael le Courageux",
        "Luna la Légendaire", "Roland le Rédempteur", "Morgana la Maléfique", "Thorin le Tonnerre"
    ]

    joueur_test = joueur.Joueur(random.choice(noms_random_joueurs))
    jeu = CyrilRpg()
    jeu.player = joueur_test

    # Création d'un personnage de test
    personnage_test = personnage.Personnage(random.choice(noms_random_personnages), "Guerrier")
    jeu.player.add_character(personnage_test)



    jeu.run()
