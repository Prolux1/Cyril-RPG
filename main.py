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
        Image.IMAGE_MENU_EQUIPEMENT_PERSONNAGE = Image.IMAGE_MENU_EQUIPEMENT_PERSONNAGE.convert_alpha()
        Image.IMAGE_BARRE_DE_SORTS = Image.IMAGE_BARRE_DE_SORTS.convert_alpha()
        Image.SILVER_WOOD_BUTTON_1 = Image.SILVER_WOOD_BUTTON_1.convert_alpha()
        Image.SILVER_WOOD_BUTTON_2 = Image.SILVER_WOOD_BUTTON_2.convert_alpha()
        Image.SILVER_WOOD_BUTTON_3 = Image.SILVER_WOOD_BUTTON_3.convert_alpha()
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

        Image.SPELL_TRANCHER_ICON = Image.SPELL_TRANCHER_ICON.convert_alpha()

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
            interface.PlayButton(Image.SILVER_WOOD_BUTTON_3, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3, "Play", Font.ARIAL_40, Color.GREY),
            interface.SettingsButton(Image.SILVER_WOOD_BUTTON_2, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2.25, "Settings", Font.ARIAL_40, Color.GREY, center=True),
            interface.QuitButton(Image.SILVER_WOOD_BUTTON_1, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.8, "Quit", Font.ARIAL_40, Color.GREY, center=True)
        ]

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps()))
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
            self.components.append(interface.FpsViewer(self.clock.get_fps()))

    def character_selection_menu(self):
        self.components = [
            interfaceClasses.BackgroundColor((WINDOW_WIDTH, WINDOW_HEIGHT), Color.DARK_GREY)
        ]

        # Adding all the characters to a list to select one of them
        for i, c in enumerate(self.player.characters):
            self.components.append(
                interface.CharacterSelectionButton(Image.SILVER_WOOD_BUTTON_1, WINDOW_WIDTH / 2, 200 + (100 * (i+1)), c, Font.ARIAL_23, Color.GREY)
            )

        # Adding a button to create new character
        self.components.append(interface.CharacterCreationButton(Image.SILVER_WOOD_BUTTON_2, WINDOW_WIDTH / 2, WINDOW_HEIGHT - Image.SILVER_WOOD_BUTTON_2.get_height(),"Create character", Font.ARIAL_23, Color.GREY))


        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps()))

    def settings_menu(self):
        self.components = [
            interfaceClasses.BackgroundColor((WINDOW_WIDTH, WINDOW_HEIGHT), Color.DARK_GREY)
        ]

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps()))

    def enter_world(self, character):
        self.zones[character.zone].add_character(character)
        self.components = [
            self.zones[character.zone],
            gui.GameUserInterface(character)
        ]


        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps()))


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

    def affichage_jeu(self, personnage):
        # affichage du background du spawn
        self.window.blit(self.zones[personnage.zone].image, [0, 0])

        # affichage des rect des obstacles de la zone
        #for obstacle in self.zones[personnage.zone].obstacles:
        #    pygame.draw.rect(self.fenetre, self.Noir, obstacle, 2)

        # affichage d'un message si le joueur meurt
        if personnage.est_mort():
            affiche_mort_perso = self.police_2.render("Vous êtes mort", True, self.Noir)
            pygame.draw.rect(self.window, self.Noir, [780, 390, 380, 80], 2)
            self.window.blit(affiche_mort_perso, [800, 400])

            # affichage d'un bouton pour respawn
            affiche_respawn_perso = self.police.render("Réapparaître", True, self.Noir)
            pygame.draw.ellipse(self.window, self.Noir, [820, 493, 300, 50], 3)
            pygame.draw.ellipse(self.window, self.Gris, [823, 496, 294, 44])
            if 820 < self.mouse_pos[0] < 1120 and 493 < self.mouse_pos[1] < 543:
                pygame.draw.ellipse(self.window, self.Gris_clair, [823, 496, 294, 44])
            else:
                pygame.draw.ellipse(self.window, self.Gris, [823, 496, 294, 44])
            self.window.blit(affiche_respawn_perso, [880, 500])

    def affichage_personnages(self, personnage):
        # affichage des personnages dans la zone
        for perso in self.zones[personnage.zone].personnages_zone:
            if not perso.est_mort():
                self.window.blit(perso.postures[perso.orientation], [perso.x, perso.y])

                # affichage du nom et du lvl du personnage
                affiche_nom_lvl_perso = self.police.render(perso.nom + " lvl " + str(perso.lvl), True, self.Noir)
                self.window.blit(affiche_nom_lvl_perso, [perso.x - 10, perso.y - 50])

                # affichage de la hit_box du personnage
                personnage.hit_box[0] = personnage.x
                personnage.hit_box[1] = personnage.y
                #pygame.draw.rect(self.fenetre, self.Noir, personnage.hit_box, 2)

    def affichage_mob_image_orientation(self, mob):
        """
        Positionnement de l'image du monstre personnaliser en fonction de l'orientation du monstre
        :return:
        """
        if mob.orientation == "Gauche":
            if mob.nom == "Rat" or mob.nom == "Boss Rat":
                self.window.blit(mob.image, [mob.x - 40, mob.y + 40])
            elif mob.nom == "Cerf" or mob.nom == "Boss Cerf":
                self.window.blit(mob.image, [mob.x - 40, mob.y])
            elif mob.nom == "Orc":
                self.window.blit(mob.image, [mob.x - 10, mob.y])
            elif mob.nom == "Loup humain":
                self.window.blit(mob.image, [mob.x, mob.y])
            elif mob.nom == "Dotum":
                self.window.blit(mob.image, [mob.x - 22 * 8, mob.y - 10 * 8])
            elif mob.nom == "Fenrir":
                self.window.blit(mob.image, [mob.x - 24 * 12, mob.y - 10 * 12])

        elif mob.orientation == "Droite":
            if mob.nom == "Rat" or mob.nom == "Boss Rat":
                self.window.blit(mob.image, [mob.x - 80, mob.y + 40])
            elif mob.nom == "Cerf" or mob.nom == "Boss Cerf":
                self.window.blit(mob.image, [mob.x - 40, mob.y])
            elif mob.nom == "Orc":
                self.window.blit(mob.image, [mob.x, mob.y])
            elif mob.nom == "Loup humain":
                self.window.blit(mob.image, [mob.x, mob.y])
            elif mob.nom == "Dotum":
                self.window.blit(mob.image, [mob.x - 26 * 8, mob.y + 3 * 8])
            elif mob.nom == "Fenrir":
                self.window.blit(mob.image, [mob.x - 30 * 12, mob.y + 3 * 12])

        elif mob.orientation == "Dos":
            if mob.nom == "Rat" or mob.nom == "Boss Rat":
                self.window.blit(mob.image, [mob.x, mob.y + 40])
            elif mob.nom == "Cerf" or mob.nom == "Boss Cerf":
                self.window.blit(mob.image, [mob.x, mob.y])
            elif mob.nom == "Orc":
                self.window.blit(mob.image, [mob.x - 30, mob.y])
            elif mob.nom == "Loup humain":
                self.window.blit(mob.image, [mob.x, mob.y])
            elif mob.nom == "Dotum":
                self.window.blit(mob.image, [mob.x - 24 * 8, mob.y - 17 * 8])
            elif mob.nom == "Fenrir":
                self.window.blit(mob.image, [mob.x - 28 * 12, mob.y - 17 * 12])

        else:
            if mob.nom == "Rat" or mob.nom == "Boss Rat":
                self.window.blit(mob.image, [mob.x, mob.y])
            elif mob.nom == "Cerf" or mob.nom == "Boss Cerf":
                self.window.blit(mob.image, [mob.x, mob.y])
            elif mob.nom == "Orc":
                self.window.blit(mob.image, [mob.x - 30, mob.y])
            elif mob.nom == "Loup humain":
                self.window.blit(mob.image, [mob.x, mob.y])
            elif mob.nom == "Dotum":
                self.window.blit(mob.image, [mob.x - 25 * 8, mob.y - 5 * 8])
            elif mob.nom == "Fenrir":
                self.window.blit(mob.image, [mob.x - 27 * 12, mob.y - 5 * 12])

    def affichage_mobs(self, mobs_zone):
        # affichage de touts les mobs présents dans la zone du joueur ainsi que de leurs PV au-dessus d'eux
        for mob in mobs_zone:
            if mob.nom == "Fenrir":
                mob.deplacement(0.18)
            else:
                mob.deplacement(0.1)

            # Positionnement de l'image du monstre personnaliser en fonction de l'orientation du monstre
            self.affichage_mob_image_orientation(mob)

            # affichage du nom du mob et de son lvl
            affiche_nom_lvl_mob = self.police.render(mob.nom + " lvl " + str(mob.lvl), True, self.Noir)
            self.window.blit(affiche_nom_lvl_mob, [mob.x + 39 - len(mob.nom + " lvl " + str(mob.lvl)) * 5, mob.y - 80])

            pygame.draw.rect(self.window, self.Noir, [mob.x - 50, mob.y - 50, 210, 50], 2)
            if mob.PV >= mob.PV_max / 2:
                pygame.draw.rect(self.window, (24 + 216 * (1 - (mob.PV / mob.PV_max) ** 2), 240, 10), [mob.x - 48, mob.y - 48, (207 * mob.PV) / mob.PV_max, 47])
            else:
                pygame.draw.rect(self.window, (240, 240 * (2 * mob.PV / mob.PV_max), 10), [mob.x - 48, mob.y - 48, (207 * mob.PV) / mob.PV_max, 47])

            # affichage du nombre de PV du mob au dessus de sa tête
            if len(str(mob.PV) + " / " + str(mob.PV_max)) <= 13:
                affiche_PV_mob = self.police.render(utils.conversion_nombre(mob.PV) + " / " + utils.conversion_nombre(mob.PV_max), True, self.Noir)
                self.window.blit(affiche_PV_mob, [mob.x + 80 - len(str(mob.PV) + " / " + str(mob.PV_max)) * 10, mob.y - 40])
            else:
                affiche_PV_mob = self.police_3.render(utils.conversion_nombre(mob.PV) + " / " + utils.conversion_nombre(mob.PV_max), True, self.Noir)
                self.window.blit(affiche_PV_mob, [mob.x + 45 - len(str(mob.PV) + " / " + str(mob.PV_max)) * 5, mob.y - 38])

            # affiche la hit box du mob
            #pygame.draw.rect(self.fenetre, self.Noir, mob.hit_box, 2)

    def affichage_interface_jeu(self, personnage, dic_menu):
        """
        Prends en paramètre un dictionnaire contenant le nom du menu et son état ex: {"Inventaire: True"} signifie que l'inventaire est ouvert
        Prends également en paramètre le personnage pour affiche les objets de son inventaire
        Affichage de l'interface du jeu
        """

        # affichage des PV + rectangle de couleur verte représentant la vie du personnage
        pygame.draw.rect(self.window, self.Noir, [10, 10, 210, 50], 2)
        if personnage.PV >= personnage.PV_max / 2:
            pygame.draw.rect(self.window, (24 + 216 * (1 - (personnage.PV / personnage.PV_max) ** 2), 240, 10), [12, 12, (207 * personnage.PV) / personnage.PV_max, 47])
        else:
            pygame.draw.rect(self.window, (240, 240 * (2 * personnage.PV / personnage.PV_max), 10), [12, 12, (207 * personnage.PV) / personnage.PV_max, 47])
        affiche_PV_perso = self.police.render(str(math.ceil(personnage.PV)) + " / " + str(personnage.PV_max), True, self.Noir)
        self.window.blit(affiche_PV_perso, [50, 17])

        # affichage de la barre de sorts
        self.window.blit(self.image_barre_de_sorts, [700, 1009])
        for i in range(len(personnage.sorts)):
            self.window.blit(personnage.sorts[i].image, [711 + 74 * i, 1020])

            # affichage du temps restants avant le rechargement de la compétence
            if personnage.sorts[i].temps_restant_rechargement != 0:
                affiche_temps_restant_rechargement = self.police_3.render(str(round(personnage.sorts[i].temps_restant_rechargement, 1)), True, self.Noir)
                self.window.blit(affiche_temps_restant_rechargement, [720 + 74 * i , 980])

            # affichage d'un menu indicatif si on passe la souris sur un sort
            if 711 + 74 * i <= self.mouse_pos[0] <= 761 + 74 * i and 1020 <= self.mouse_pos[1] <= 1070:
                affiche_nom_sort = self.police_3.render(personnage.sorts[i].nom, True, self.Noir)
                affiche_degats_total_sort1 = self.police_3.render("Inflige ", True, self.Noir)
                if personnage.arme:
                    affiche_degats_total_sort2 = self.police_3.render(str(personnage.sorts[i].degats + personnage.arme.degat + personnage.force), True, self.Jaune_Orange)
                else:
                    affiche_degats_total_sort2 = self.police_3.render(str(personnage.sorts[i].degats + personnage.force), True, self.Jaune_Orange)
                affiche_degats_total_sort3 = self.police_3.render(" points de dégâts", True, self.Noir)

                self.window.blit(self.tableau_description_item, [self.mouse_pos[0], self.mouse_pos[1] - 100])
                self.window.blit(affiche_nom_sort, [self.mouse_pos[0] + 5, self.mouse_pos[1] - 95])
                self.window.blit(affiche_degats_total_sort1, [self.mouse_pos[0] + 5, self.mouse_pos[1] - 65])
                self.window.blit(affiche_degats_total_sort2, [self.mouse_pos[0] + 70, self.mouse_pos[1] - 65])
                self.window.blit(affiche_degats_total_sort3, [self.mouse_pos[0] + 70 + 12 * len(str(personnage.sorts[i].degats + personnage.force)), self.mouse_pos[1] - 65])
                if personnage.sorts[i].zone_effet:
                    affiche_zone_effet = self.police_3.render("Dégâts de zone", True, self.Noir)
                    self.window.blit(affiche_zone_effet, [self.mouse_pos[0] + 5, self.mouse_pos[1] - 35])

        selectionner = False
        # affichage de l'inventaire s'il est ouvert
        if dic_menu["Inventaire"]:
            self.window.blit(self.image_inventaire, [1400, 500])

            # affichage des différents objets de l'inventaire ainsi qu'un cadre autour de l'objet indiquant sa rareté
            for i in range(len(personnage.inventaire)):
                for j in range(len(personnage.inventaire[0])):
                    if personnage.inventaire[i][j]:
                        pygame.draw.rect(self.window, self.raretes_couleur[personnage.inventaire[i][j].rarete], [1417 + 52 * j, 533 + 52 * i, 39, 39], 2)
                        self.window.blit(personnage.inventaire[i][j].logo_objet, [1421 + 52 * j, 537 + 52 * i])
                        #self.fenetre.blit(self.logo_equipement_ceinture_simple, [1421 + 52 * j, 537 + 52 * i])

                        # Affiche un menu indicatif de l'item survolé par la souris s'il existe
                        if 1417 + 52 * j < self.mouse_pos[0] < 1417 + 52 * j + 39 and 533 + 52 * i < self.mouse_pos[1] < 533 + 52 * i + 39:
                            selectionner = True
                            i_item = i
                            j_item = j

                            affiche_type_rarete_lvl_equipement = self.police_3.render(personnage.inventaire[i][j].type_equipement + " " + personnage.inventaire[i][j].rarete + " lvl " + str(personnage.inventaire[i][j].lvl), True, self.raretes_couleur[personnage.inventaire[i][j].rarete])
                            if personnage.inventaire[i][j].type_equipement == "Arme":
                                affiche_degat_arme = self.police_3.render(str(personnage.inventaire[i][j].degat) + " Dégâts", True, self.Noir)
                            else:
                                affiche_armure_equipement = self.police_3.render(str(personnage.inventaire[i][j].armure) + " Armure", True, self.Noir)
                            affiche_bonus_PV_equipement = self.police_3.render("+ " + str(personnage.inventaire[i][j].bonus_PV) + " PV", True, self.Noir)
                            affiche_bonus_force_equipement = self.police_3.render("+ " + str(personnage.inventaire[i][j].bonus_force) + " Force", True, self.Noir)

            # Si un équipement est sélectionner on l'affiche tout a la fin pour superposer les écritures et le menu indicatif sur les autres items
            if selectionner:
                self.window.blit(self.tableau_description_item, [self.mouse_pos[0], self.mouse_pos[1]])
                self.window.blit(affiche_type_rarete_lvl_equipement, [self.mouse_pos[0] + 5, self.mouse_pos[1] + 5])
                if personnage.inventaire[i_item][j_item].type_equipement == "Arme":
                    self.window.blit(affiche_degat_arme, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 50])
                else:
                    self.window.blit(affiche_armure_equipement, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 50])
                self.window.blit(affiche_bonus_PV_equipement, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 80])
                self.window.blit(affiche_bonus_force_equipement, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 110])
                if personnage.inventaire[i_item][j_item].equipee:
                    affiche_equipee_equipement = self.police_3.render("équipée", True, self.Noir)
                    self.window.blit(affiche_equipee_equipement, [self.mouse_pos[0] + 100, self.mouse_pos[1] + 20])

        selectionner = False
        selectionner_arme = False
        info_armure = False
        # affichage du menu d'équipement du personnage s'il est ouvert
        if dic_menu["Personnage"]:
            self.window.blit(self.image_menu_equipement_personnage, [800, 200])

            # Affiche les stats du personnage
            affiche_stat_nom_lvl = self.police_3.render(personnage.nom + " lvl " + str(personnage.lvl), True, self.Noir)
            affiche_stat_PV_max = self.police_3.render("PV max : " + str(personnage.PV_max), True, self.Noir)
            affiche_stat_armure = self.police_3.render("Armure : " + str(personnage.armure), True, self.Noir)
            affiche_stat_force = self.police_3.render("Force : " + str(personnage.force), True, self.Noir)

            self.window.blit(affiche_stat_nom_lvl, [930, 210])
            self.window.blit(affiche_stat_PV_max, [825, 690])
            self.window.blit(affiche_stat_armure, [825, 720])
            self.window.blit(affiche_stat_force, [825, 750])

            # affiche l'arme du personnage
            if personnage.arme:
                pygame.draw.rect(self.window, self.raretes_couleur[personnage.arme.rarete], [956, 602, 53, 53], 2)
                self.window.blit(personnage.arme.logo_objet, [966, 612])

                if 956 < self.mouse_pos[0] < 1009 and 602 < self.mouse_pos[1] < 655:
                    selectionner = True
                    selectionner_arme = True

                    affiche_type_rarete_lvl_equipement = self.police_3.render(personnage.arme.type_equipement + " " + personnage.arme.rarete + " lvl " + str(personnage.arme.lvl), True, self.raretes_couleur[personnage.arme.rarete])
                    affiche_degat_arme = self.police_3.render(str(personnage.arme.degat) + " Dégâts", True, self.Noir)
                    affiche_bonus_PV_equipement = self.police_3.render("+ " + str(personnage.arme.bonus_PV) + " PV", True, self.Noir)
                    affiche_bonus_force_equipement = self.police_3.render("+ " + str(personnage.arme.bonus_force) + " Force", True, self.Noir)
                    affiche_equipee_equipement = self.police_3.render("équipée", True, self.Noir)


            # affiche les différents pièces d'équipements du personnage
            i = 0
            for object_equiper in personnage.equipement.values():
                if object_equiper:

                    # équipements de gauche
                    if object_equiper.type_equipement == "Casque":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [849, 232, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [859, 242])
                    elif object_equiper.type_equipement == "Épaulières":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [849, 306, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [859, 316])
                    elif object_equiper.type_equipement == "Cape":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [849, 380, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [859, 390])
                    elif object_equiper.type_equipement == "Plastron":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [849, 454, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [859, 464])
                    elif object_equiper.type_equipement == "Ceinture":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [849, 528, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [859, 538])

                    # équipements de droite
                    elif object_equiper.type_equipement == "Gants":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [1078, 232, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [1088, 242])
                    elif object_equiper.type_equipement == "Jambières":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [1078, 306, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [1088, 316])
                    elif object_equiper.type_equipement == "Bottes":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [1078, 380, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [1088, 390])
                    elif object_equiper.type_equipement == "Bague":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [1078, 454, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [1088, 464])
                    elif object_equiper.type_equipement == "Bague":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [1078, 528, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [1088, 538])
                    elif object_equiper.type_equipement == "Bijou":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [1078, 602, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [1088, 612])
                    elif object_equiper.type_equipement == "Bijou":
                        pygame.draw.rect(self.window, self.raretes_couleur[object_equiper.rarete], [1078, 676, 53, 53], 2)
                        self.window.blit(object_equiper.logo_objet, [1088, 686])

                    # Affiche un menu indicatif de l'item de gauche survolé par la souris s'il existe
                    if i <= 4:
                        if 849 < self.mouse_pos[0] < 902 and 232 + 74 * i < self.mouse_pos[1] < 285 + 74 * i:
                            selectionner = True

                            affiche_type_rarete_lvl_equipement = self.police_3.render(object_equiper.type_equipement + " " + object_equiper.rarete + " lvl " + str(object_equiper.lvl), True, self.raretes_couleur[object_equiper.rarete])
                            affiche_armure_equipement = self.police_3.render(str(object_equiper.armure) + " Armure", True, self.Noir)
                            affiche_bonus_PV_equipement = self.police_3.render("+ " + str(object_equiper.bonus_PV) + " PV", True, self.Noir)
                            affiche_bonus_force_equipement = self.police_3.render("+ " + str(object_equiper.bonus_force) + " Force", True, self.Noir)
                            affiche_equipee_equipement = self.police_3.render("équipée", True, self.Noir)
                    # Affiche un menu indicatif de l'item de droite survolé par la souris s'il existe
                    else:
                        if 1078 < self.mouse_pos[0] < 1131 and 232 + 74 * (i - 5) < self.mouse_pos[1] < 285 + 74 * (i - 5):
                            selectionner = True

                            affiche_type_rarete_lvl_equipement = self.police_3.render(object_equiper.type_equipement + " " + object_equiper.rarete + " lvl " + str(object_equiper.lvl), True, self.raretes_couleur[object_equiper.rarete])
                            affiche_armure_equipement = self.police_3.render(str(object_equiper.armure) + " Armure", True, self.Noir)
                            affiche_bonus_PV_equipement = self.police_3.render("+ " + str(object_equiper.bonus_PV) + " PV", True, self.Noir)
                            affiche_bonus_force_equipement = self.police_3.render("+ " + str(object_equiper.bonus_force) + " Force", True, self.Noir)
                            affiche_equipee_equipement = self.police_3.render("équipée", True, self.Noir)

                # Affiche un menu indicatif si on survole l'armure pour indiquer au joueur que ça réduit les dégats reçus par un pourcentage x
                if 825 < self.mouse_pos[0] < 900 and 720 < self.mouse_pos[1] < 745:
                    info_armure = True

                    affiche_info_armure1 = self.police_3.render("L'armure réduit les dégats", True, self.Noir)
                    affiche_info_armure2 = self.police_3.render("reçus par votre personnage", True, self.Noir)
                    affiche_info_armure3 = self.police_3.render("Réduction de dégats : " + str(round(personnage.reduction_degats * 100, 2)) + " %", True, self.Noir)
                i += 1

            # Si un équipement est sélectionner on l'affiche tout a la fin pour superposer les écritures et le menu indicatif sur les autres items
            if selectionner:
                self.window.blit(self.tableau_description_item, [self.mouse_pos[0], self.mouse_pos[1]])
                self.window.blit(affiche_type_rarete_lvl_equipement, [self.mouse_pos[0] + 5, self.mouse_pos[1] + 5])
                if selectionner_arme:
                    self.window.blit(affiche_degat_arme, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 50])
                else:
                    self.window.blit(affiche_armure_equipement, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 50])
                self.window.blit(affiche_bonus_PV_equipement, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 80])
                self.window.blit(affiche_bonus_force_equipement, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 110])
                self.window.blit(affiche_equipee_equipement, [self.mouse_pos[0] + 220, self.mouse_pos[1] + 125])

            # S'il faut afficher le menu info armure, on l'affiche tout à la fin pour superposer le menu sur tout
            if info_armure:
                self.window.blit(self.tableau_description_item, [self.mouse_pos[0], self.mouse_pos[1]])
                self.window.blit(affiche_info_armure1, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 10])
                self.window.blit(affiche_info_armure2, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 40])
                self.window.blit(affiche_info_armure3, [self.mouse_pos[0] + 10, self.mouse_pos[1] + 70])

    def menu_parametre(self):
        execution = True
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
                    pass

            self.affichage_menu_parametre()

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
        xp_multiplier = 1
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

            # S'il y a un world boss dans la zone et que le son de boss n'est pas déjà joué on le joue
            world_boss_present = False
            for mob in mobs_zone:
                if mob.est_world_boss:
                    world_boss_present = True

            if world_boss_present and self.music_boss.get_num_channels() == 0:
                if self.music_zone1.get_num_channels() != 0:
                    self.music_zone1.set_volume(0)
                self.music_boss.play()
            elif not world_boss_present and self.music_boss.get_num_channels() != 0:
                self.music_boss.stop()
                self.music_zone1.set_volume(self.volume_son)

            for event in pygame.event.get():  # à chaque événement provoqué par l'utilisateur
                if event.type == pygame.QUIT:  # si un des événements évoque la fermeture d'une fenêtre (par exemple cliquez sur la croix rouge en haut a droite ou appuyez alt+F4) ferme le jeu
                    personnage.connecte = False
                    execution = False
                if event.type == pygame.K_ESCAPE:
                    personnage.connecte = False
                    execution = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

                    # équipe la pièce d'équipement sélectionner si le joueur fait un clique droit dessus depuis l'inventaire
                    if dic_menu["Inventaire"]:
                        for i in range(len(personnage.inventaire)):
                            for j in range(len(personnage.inventaire[0])):
                                if personnage.inventaire[i][j]:
                                    if 1417 + 52 * j < self.mouse_pos[0] < 1417 + 52 * j + 39 and 533 + 52 * i < self.mouse_pos[1] < 533 + 52 * i + 39:
                                        if personnage.inventaire[i][j].type_equipement == "Arme":
                                            if not personnage.inventaire_est_plein() or not personnage.arme:
                                                personnage.equiper_arme(personnage.inventaire[i][j], i, j)
                                        elif personnage.inventaire[i][j].type_equipement in personnage.equipement.keys():
                                            if not personnage.inventaire_est_plein() or not personnage.equipement[personnage.inventaire[i][j].type_equipement]:
                                                personnage.equiper_object(personnage.inventaire[i][j], i, j)
                                                self.son_equiper_armure_lourde.play()

                    # déséquipe la pièce d'équipement sélectionner si le joueur fait un clique droit dessus depuis le menu de personnage
                    if dic_menu["Personnage"]:
                        if not personnage.inventaire_est_plein():
                            if personnage.arme:
                                if 956 < self.mouse_pos[0] < 1009 and 602 < self.mouse_pos[1] < 655:
                                    personnage.desequiper_arme(personnage.arme)

                            i = 0
                            for object_equiper in personnage.equipement.values():
                                if object_equiper:
                                    if i <= 4:
                                        if 849 < self.mouse_pos[0] < 902 and 232 + 74 * i < self.mouse_pos[1] < 285 + 74 * i:
                                            personnage.desequiper_object(object_equiper)
                                            self.son_equiper_armure_lourde.play()
                                    else:
                                        if 1078 < self.mouse_pos[0] < 1131 and 232 + 74 * (i - 5) < self.mouse_pos[1] < 285 + 74 * (i - 5):
                                            personnage.desequiper_object(object_equiper)
                                            self.son_equiper_armure_lourde.play()
                                i += 1

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if personnage.est_mort():
                        if 820 < self.mouse_pos[0] < 1120 and 493 < self.mouse_pos[1] < 543:
                            personnage.PV = 1
                    for i in range(len(personnage.sorts)):
                        if 711 + 74 * i <= self.mouse_pos[0] <= 761 + 74 * i and 1020 <= self.mouse_pos[1] <= 1070:
                            if personnage.sorts[i].temps_restant_rechargement == 0:
                                self.sons_attaque_perso[random.randint(0, len(self.sons_attaque_perso) - 1)].play()
                                personnage.attaquer(mobs_zone, personnage.sorts[i])
                                personnage.sorts[i].temps_restant_rechargement = personnage.sorts[i].temps_rechargement
                                if personnage.sorts[i].nom == "Tourbillon":
                                    sort_lancer = "Tourbillon"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        personnage.connecte = False
                        execution = False
                        self.music_zone1.stop()
                        self.music_boss.stop()
                        self.zones[personnage.zone].personnages_zone.remove(personnage)
                    if not personnage.est_mort():
                        # liste de booléens indiquant toutes les touches pressées
                        touches_presses = pygame.key.get_pressed()
                        deplacements_possibles = personnage.verifier_personnage_obstacles(self.zones[personnage.zone].obstacles)
                        if touches_presses[pygame.K_z] and touches_presses[pygame.K_d]:
                            if "Haut" in deplacements_possibles and "Droite" in deplacements_possibles:
                                personnage.deplacement_haut_droite()
                        elif touches_presses[pygame.K_z] and touches_presses[pygame.K_q]:
                            if "Haut" in deplacements_possibles and "Gauche" in deplacements_possibles:
                                personnage.deplacement_haut_gauche()
                        elif touches_presses[pygame.K_s] and touches_presses[pygame.K_q]:
                            if "Bas" in deplacements_possibles and "Gauche" in deplacements_possibles:
                                personnage.deplacement_bas_gauche()
                        elif touches_presses[pygame.K_s] and touches_presses[pygame.K_d]:
                            if "Bas" in deplacements_possibles and "Droite" in deplacements_possibles:
                                personnage.deplacement_bas_droite()
                        elif event.key == pygame.K_z:
                            if "Haut" in deplacements_possibles:
                                personnage.deplacement_haut()
                        elif event.key == pygame.K_q:
                            if "Gauche" in deplacements_possibles:
                                personnage.deplacement_gauche()
                        elif event.key == pygame.K_s:
                            if "Bas" in deplacements_possibles:
                                personnage.deplacement_bas()
                        elif event.key == pygame.K_d:
                            if "Droite" in deplacements_possibles:
                                personnage.deplacement_droite()

                        # Si le personnage lance le sort 1
                        if event.key == pygame.K_1:
                            if personnage.sorts[0].temps_restant_rechargement == 0:
                                self.sons_attaque_perso[random.randint(0, len(self.sons_attaque_perso) - 1)].play()
                                personnage.attaquer(mobs_zone, personnage.sorts[0])
                                personnage.sorts[0].temps_restant_rechargement = personnage.sorts[0].temps_rechargement
                                #affiche_zone_effet_s1 = True

                        # Si le personnage lance le sort 2
                        if event.key == pygame.K_2:
                            if len(personnage.sorts) >= 2:
                                if personnage.sorts[1].temps_restant_rechargement == 0:
                                    self.sons_attaque_perso[random.randint(0, len(self.sons_attaque_perso) - 1)].play()
                                    personnage.attaquer(mobs_zone, personnage.sorts[1])
                                    personnage.sorts[1].temps_restant_rechargement = personnage.sorts[1].temps_rechargement
                                    #affiche_zone_effet_s2 = True
                                    sort_lancer = "Tourbillon"

                        # Si le joueur appuie sur 2, son perso est heal de 50 PV
                        if event.key == pygame.K_3:
                            if personnage.PV <= personnage.PV_max - 50:
                                personnage.PV += 50
                            else:
                                personnage.PV = personnage.PV_max

                        # Si on ouvre l'inventaire avec 'i'
                        if event.key == pygame.K_i:
                            # Permet d'alterner entre ouvert et fermer lorsqu'on appuie sur "i" pour ouvrir l'inventaire
                            if dic_menu["Inventaire"] is False:
                                dic_menu["Inventaire"] = True
                            else:
                                dic_menu["Inventaire"] = False

                        # Si on ouvre le menu d'équipement du personnage avec 'c'
                        if event.key == pygame.K_c:
                            if dic_menu["Personnage"] is False:
                                dic_menu["Personnage"] = True
                            else:
                                dic_menu["Personnage"] = False

                        # Si on appuie sur '←-' (Backspace), supprime l'object à l'emplacment cibler par la souris
                        if event.key == pygame.K_BACKSPACE:
                            if dic_menu["Inventaire"]:
                                for i in range(len(personnage.inventaire)):
                                    for j in range(len(personnage.inventaire[0])):
                                        if 1417 + 52 * j < self.mouse_pos[0] < 1417 + 52 * j + 39 and 533 + 52 * i < self.mouse_pos[1] < 533 + 52 * i + 39:
                                            personnage.inventaire[i][j] = None

            for sort in personnage.sorts:
                if sort.temps_restant_rechargement != 0:
                    if sort.temps_restant_rechargement > 0:
                        sort.temps_restant_rechargement -= 0.01
                    if sort.temps_restant_rechargement < 0:
                        sort.temps_restant_rechargement = 0

            if sort_lancer == "Tourbillon":
                if temps_attaques_tourbillon[1] == 3:
                    sort_lancer = None
                    temps_attaques_tourbillon = [None, 0]
                elif temps_attaques_tourbillon[0] is None:
                    temps_attaques_tourbillon[0] = self.temps

                elif temps_attaques_tourbillon[0]:
                    if self.temps >= temps_attaques_tourbillon[0] + 0.2:
                        personnage.attaquer(mobs_zone, personnage.sorts[1], True)
                        self.sons_attaque_perso[random.randint(0, len(self.sons_attaque_perso) - 1)].play()
                        temps_attaques_tourbillon[0] = None
                        temps_attaques_tourbillon[1] += 1

            if not personnage.est_mort():
                if personnage.PV < personnage.PV_max:
                    if temps_regen is None:
                        temps_regen = self.temps.__round__()

                if temps_regen:
                    if self.temps.__round__() == temps_regen + 2:
                        personnage.PV = utils.regen(personnage)
                        temps_regen = None
            elif temps_regen is not None:
                temps_regen = None

            # Ajoute un mob aléatoire dans la zone du joueur
            if len(mobs_zone) < self.zones[personnage.zone].nb_max_monstres:
                if mob_spawn_timer is None:
                    mob_spawn_timer = self.temps.__round__()
                elif self.temps.__round__() == mob_spawn_timer + 2:
                    mobs_zone.append(self.generer_mob(personnage.zone))
                    mob_spawn_timer = None

            if personnage.xp >= personnage.xp_requis:
                personnage.xp -= personnage.xp_requis
                self.son_level_up.play()
                level_up = True
                temps_affiche_level_up = self.temps.__round__()
                personnage.lvl_up()

                if personnage.lvl == 10:
                    personnage.sorts.append(sorts.Sort("Tourbillon", 3, pygame.image.load("./assets/logos_sorts/sort2_guerrier.png").convert_alpha(), 10, (395, 300)))

            personnage.mise_a_jour_stats()

            self.affichage_jeu(personnage)
            self.affichage_mobs(mobs_zone)
            self.affichage_personnages(personnage)
            self.affichage_interface_jeu(personnage, dic_menu)

            personnage.mise_a_jour_stats()

            # affichage d'une barre d'expérience tout en bas qui se remplis en tuant des mobs
            pygame.draw.rect(self.window, self.Noir, [1500, 1070, 420, 10], 2)
            pygame.draw.rect(self.window, self.Violet, [1502, 1072, 417 * (personnage.xp / personnage.xp_requis), 7])

            # affiche la quantité d'expérience / quantité d'expérience requise
            affiche_xp_xp_requis = self.police.render(utils.conversion_nombre(personnage.xp) + " / " + utils.conversion_nombre(personnage.xp_requis), True, self.Violet)
            self.window.blit(affiche_xp_xp_requis, [1650, 1030])

            # affiche la barre des sorts (3 emplacements de sorts pour l'instant)

            for mob in mobs_zone:
                if mob.est_mort():
                    personnage.xp += mob.xp * xp_multiplier
                    xp_obtenu += mob.xp * xp_multiplier

                    # à une chance d'ajouter à l'inventaire du personnage, un équipement de type aléatoire et en adéquation avec le lvl du mob
                    # si le mob est un boss il y a génération d'un équipement à tout les coups
                    chance_drop_equipement = random.randint(1, 5)  # chance basique : 1/5
                    chance_drop_arme = random.randint(1, 10)  # chance basique : 1/10
                    if mob.est_boss:
                        personnage.ajouter_item_inventaire(utils.generation_equipement_alea(mob.lvl, True))
                        chance_drop_arme = random.randint(1, 3) # chance basique : 1/3
                        if chance_drop_arme == 1:
                            personnage.ajouter_item_inventaire(utils.generation_arme_alea(mob.lvl, True))
                    elif mob.est_world_boss:
                        for i in range(3):
                            personnage.ajouter_item_inventaire(utils.generation_equipement_alea(mob.lvl, False, True))
                        chance_drop_arme = random.randint(1, 2)  # chance basique : 1/2
                        if chance_drop_arme == 1:
                            personnage.ajouter_item_inventaire(utils.generation_arme_alea(mob.lvl, False, True))
                    else:
                        if chance_drop_equipement == 1:
                            personnage.ajouter_item_inventaire(utils.generation_equipement_alea(mob.lvl))
                        if chance_drop_arme == 1:
                            personnage.ajouter_item_inventaire(utils.generation_arme_alea(mob.lvl))
                    mobs_zone.remove(mob)
                    temps_affiche_xp = self.temps.__round__()

            # affiche l'xp obtenu suite aux monstres tués
            if xp_obtenu != 0:
                if temps_affiche_xp + 2 > self.temps.__round__():
                    affiche_xp_obtenu = self.police.render("+ " + str(xp_obtenu) + " XP", True, self.Violet)
                    self.window.blit(affiche_xp_obtenu, [personnage.x + 100, personnage.y + 50])
                else:
                    xp_obtenu = 0

            # Affiche un message indiquant que le joueur à level up
            if level_up:
                if temps_affiche_level_up + 2 > self.temps:
                    if temps_affiche_level_up + level_up_alpha / 255 < self.temps:
                        if level_up_alpha != 255:
                            level_up_alpha += 51
                    self.images_level_up[(level_up_alpha // 51) - 1].set_alpha(level_up_alpha)
                    self.window.blit(self.images_level_up[(level_up_alpha // 51) - 1], [personnage.x - 80, personnage.y - 240])
                else:
                    level_up = False
                    level_up_alpha = 51

            # affichage d'un message si le joueur meurt
            if personnage.est_mort():
                affiche_mort_perso = self.police_2.render("Vous êtes mort", True, self.Noir)
                pygame.draw.rect(self.window, self.Noir, [780, 390, 380, 80], 2)
                self.window.blit(affiche_mort_perso, [800, 400])

                # affichage d'un bouton pour respawn
                affiche_respawn_perso = self.police.render("Réapparaître", True, self.Noir)
                pygame.draw.ellipse(self.window, self.Noir, [820, 493, 300, 50], 3)
                pygame.draw.ellipse(self.window, self.Gris, [823, 496, 294, 44])
                if 820 < self.mouse_pos[0] < 1120 and 493 < self.mouse_pos[1] < 543:
                    pygame.draw.ellipse(self.window, self.Gris_clair, [823, 496, 294, 44])
                else:
                    pygame.draw.ellipse(self.window, self.Gris, [823, 496, 294, 44])
                self.window.blit(affiche_respawn_perso, [880, 500])

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
