import os, pygame, datetime

from config import *
from src import *
from data import *


class CyrilRpg:
    def __init__(self):
        pygame.mixer.init()  # Initialisation du son du jeu
        pygame.display.set_caption("Cyril RPG")  # Titre de la fenêtre de mon jeu de coiffeur qui sait coiffer sans son peigne
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        self.mouse_pos = pygame.mouse.get_pos()
        self.components = []
        self.clock = pygame.time.Clock()
        self.time = pygame.time.get_ticks() / 1000
        self.fps_max = 60  # 60 par défaut, 0 -> pas de limite
        self.fps = 1

        save: sauvegarde.Sauvegarde = sauvegarde.charger_sauvegarde()
        self.joueur: joueur.Joueur = save.joueur

        if self.joueur is None:
            self.joueur = joueur.Joueur(utils.nom_joueur_random())  # Création d'un joueur de test

            # Ajout d'un personnage de test (un joueur peu avoir plusieurs personnages)
            self.joueur.add_character(personnage.Personnage(self, utils.nom_personnage_rp_random(), "Guerrier"))

        # constantes internes
        self.interval_spawn_mobs = 0.01  # gère le taux d'apparition des pnjs 1 par défaut. Une valeur plus petite -> + de pnjs

    def run(self):
        # self.load_data()
        utils.conversion_format_imgs()

        self.main_menu()

        while 1:  # C'est extrêmement insolent de faire ça en python
            self.clock.tick(self.fps_max)
            self.fps = max(self.clock.get_fps(), 1)
            self.time = pygame.time.get_ticks() / 1000
            self.mouse_pos = pygame.mouse.get_pos()

            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()

    def update(self):
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
        # sauvegarde.ecrire_sauvegarde(self)
        pygame.quit()
        exit()

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
            interfaceClasses.Label("Cyril RPG", Font.TITLE, Color.BLACK, WINDOW_WIDTH / 2, 110, center=True),
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
            interfaceClasses.Label("Character name", Font.ARIAL_23, "white", WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100, center=True),
            interfaceClasses.InputField(self, WINDOW_WIDTH / 2, WINDOW_HEIGHT - 75 + Font.ARIAL_23.get_height(), 250, 50, center=True),
            interface.FlecheRetour(self.character_selection_menu, 15, 15)
        ]

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps(), WINDOW_WIDTH, 0))

    def character_selection_menu(self):
        self.components = [
            interfaceClasses.BackgroundColor((WINDOW_WIDTH, WINDOW_HEIGHT), Color.DARK_GREY),
            interface.FlecheRetour(self.main_menu, 15, 15)
        ]

        # Adding all the characters to a list to select one of them
        for i, c in enumerate(self.joueur.characters):
            self.components.append(
                interface.CharacterSelectionButton(Image.SILVER_WOOD_BUTTONS[0], WINDOW_WIDTH / 2, 200 + (100 * (i+1)), c, Font.ARIAL_23, Color.GREY)
            )

        # Ajout d'un bouton pour créer un nouveau personnage
        self.components.append(interface.CharacterCreationButton(Image.SILVER_WOOD_BUTTONS[1], WINDOW_WIDTH / 2, WINDOW_HEIGHT - Image.SILVER_WOOD_BUTTONS[1].get_height(),"Create character", Font.ARIAL_23, Color.GREY))

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps(), WINDOW_WIDTH, 0))

    def settings_menu(self):
        self.components = [
            interfaceClasses.BackgroundColor((WINDOW_WIDTH, WINDOW_HEIGHT), Color.DARK_GREY),
            interface.FlecheRetour(self.main_menu, 15, 15)
        ]

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps(), WINDOW_WIDTH, 0))

    def entrer_dans_le_monde(self, perso: "personnage.Personnage"):
        m = monde.Monde(self, perso)
        self.components = [
            m,
            gui.GameUserInterface(perso, m)
        ]

        if SHOW_FPS:
            self.components.append(interface.FpsViewer(self.clock.get_fps(), WINDOW_WIDTH, 0))


    def info_classe_guerrier(self):
        # affichage des différentes informations de la classe guerrier
        affiche_info_nom_classe = Font.ARIAL_23.render("Guerrier lvl 1", True, Color.BLACK)
        self.window.blit(affiche_info_nom_classe, [900, 300])

        affiche_info_hp = Font.ARIAL_23.render("150 PV", True, Color.BLACK)
        self.window.blit(affiche_info_hp, [750, 400])

        affiche_info_style_combat = Font.ARIAL_23.render("Style de combat au corps à corps", True, Color.BLACK)
        self.window.blit(affiche_info_style_combat, [750, 500])

        affiche_info_classe_l1 = Font.ARIAL_16.render("Le guerrier est un combattant hors pair", True, Color.BLACK)
        affiche_info_classe_l2 = Font.ARIAL_16.render("équipée d'une armure lourde et d'une grande", True, Color.BLACK)
        affiche_info_classe_l3 = Font.ARIAL_16.render("épée. Il utilise sa rage pour pourfendre", True, Color.BLACK)
        affiche_info_classe_l4 = Font.ARIAL_16.render("les adversaires les plus coriaces.", True, Color.BLACK)
        self.window.blit(affiche_info_classe_l1, [1300, 400])
        self.window.blit(affiche_info_classe_l2, [1300, 430])
        self.window.blit(affiche_info_classe_l3, [1300, 460])
        self.window.blit(affiche_info_classe_l4, [1300, 490])

        self.window.blit(self.epee_info, [1220, 430])

    def info_classe_chasseur(self):
        # affichage des différentes informations de la classe chasseur
        affiche_info_nom_classe = Font.ARIAL_23.render("Chasseur lvl 1", True, Color.BLACK)
        self.window.blit(affiche_info_nom_classe, [900, 300])

        affiche_info_hp = Font.ARIAL_23.render("137 PV", True, Color.BLACK)
        self.window.blit(affiche_info_hp, [750, 400])

        affiche_info_style_combat = Font.ARIAL_23.render("Style de combat à distance", True, Color.BLACK)
        self.window.blit(affiche_info_style_combat, [750, 500])

        affiche_info_classe_l1 = Font.ARIAL_16.render("Le guerrier est un combattant hors pair", True, Color.BLACK)
        affiche_info_classe_l2 = Font.ARIAL_16.render("équipée d'une armure lourde et d'une grande", True, Color.BLACK)
        affiche_info_classe_l3 = Font.ARIAL_16.render("épée. Il utilise sa rage pour pourfendre", True, Color.BLACK)
        affiche_info_classe_l4 = Font.ARIAL_16.render("les adversaires les plus coriaces.", True, Color.BLACK)
        self.window.blit(affiche_info_classe_l1, [1300, 400])
        self.window.blit(affiche_info_classe_l2, [1300, 430])
        self.window.blit(affiche_info_classe_l3, [1300, 460])
        self.window.blit(affiche_info_classe_l4, [1300, 490])

        self.window.blit(self.arbalete_info, [1120, 430])

    def info_classe_mage(self):
        # affichage des différentes informations de la classe mage
        affiche_info_nom_classe = Font.ARIAL_23.render("Mage lvl 1", True, Color.BLACK)
        self.window.blit(affiche_info_nom_classe, [900, 300])

        affiche_info_hp = Font.ARIAL_23.render("124 PV", True, Color.BLACK)
        self.window.blit(affiche_info_hp, [750, 400])

        affiche_info_style_combat = Font.ARIAL_23.render("Style de combat à distance", True, Color.BLACK)
        self.window.blit(affiche_info_style_combat, [750, 500])

        affiche_info_classe_l1 = Font.ARIAL_16.render("Le guerrier est un combattant hors pair", True, Color.BLACK)
        affiche_info_classe_l2 = Font.ARIAL_16.render("équipée d'une armure lourde et d'une grande", True, Color.BLACK)
        affiche_info_classe_l3 = Font.ARIAL_16.render("épée. Il utilise sa rage pour pourfendre", True, Color.BLACK)
        affiche_info_classe_l4 = Font.ARIAL_16.render("les adversaires les plus coriaces.", True, Color.BLACK)
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
        affiche_info_fleches = Font.ARIAL_23.render("Utilise les flèches haut et bas du clavier", True, Color.BLACK)
        affiche_info_fleches2 = Font.ARIAL_23.render("pour parcourir tes différents personnage", True, Color.BLACK)
        self.window.blit(affiche_info_fleches, [100, 500])
        self.window.blit(affiche_info_fleches2, [100, 530])

        # affichage des boutons fleche du haut et bas pour indiquer comment parcourir les différents perso
        self.window.blit(self.bouton_fleche_haut, [200, 600])
        self.window.blit(self.bouton_fleche_bas, [200, 632])

        # affichage du nombre de perso du joueur (max 3 persos)
        affiche_nombre_persos = Font.ARIAL_23.render("Nombre de personnages : " + str(len(self.joueur.personnages)) + " / 3", True, Color.BLACK)
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
            affiche_perso_courant = Font.ARIAL_23.render(personnage.nom + " lvl " + str(personnage.lvl), True, Color.BLACK)
            self.window.blit(affiche_perso_courant, [750, 400 + espacement])
            espacement += 150

        # affichage du bouton pour entrer dans le jeu
        if 1475 < self.mouse_pos[0] < 1760 and 785 < self.mouse_pos[1] < 850:
            pygame.draw.rect(self.window, Color.GREY_LIGHTEN, [1477, 787, 281, 61])  # le background du bouton
        else:
            pygame.draw.rect(self.window, Color.GREY, [1477, 787, 281, 61])
        pygame.draw.rect(self.window, Color.BLACK, [1475, 785, 285, 65], 3)
        affiche_entrer_jeu = Font.ARIAL_23.render("Entrer dans le jeu", True, Color.BLACK)
        self.window.blit(affiche_entrer_jeu, [1500, 800])


    def affichage_menu_parametre(self):
        # Titre
        affiche_titre = Font.ARIAL_23.render("Paramètres", True, Color.BLACK)
        self.window.blit(affiche_titre, [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10])

    def affichage_menu_creation_perso(self):
        # affichage classe guerrier
        if 400 < self.mouse_pos[0] < 510 and 483 < self.mouse_pos[1] < 510:
            affiche_classe_guerrier = Font.ARIAL_23_2.render("Guerrier", True, Color.BLACK)
        else:
            affiche_classe_guerrier = Font.ARIAL_23.render("Guerrier", True, Color.BLACK)
        self.window.blit(affiche_classe_guerrier, [400, 480])

        # affichage classe chasseur
        if 400 < self.mouse_pos[0] < 530 and 583 < self.mouse_pos[1] < 610:
            affiche_classe_chasseur = Font.ARIAL_23_2.render("Chasseur", True, Color.BLACK)
        else:
            affiche_classe_chasseur = Font.ARIAL_23.render("Chasseur", True, Color.BLACK)
        self.window.blit(affiche_classe_chasseur, [400, 580])

        # affichage classe mage
        if 400 < self.mouse_pos[0] < 475 and 683 < self.mouse_pos[1] < 710:
            affiche_classe_mage = Font.ARIAL_23_2.render("Mage", True, Color.BLACK)
        else:
            affiche_classe_mage = Font.ARIAL_23.render("Mage", True, Color.BLACK)
        self.window.blit(affiche_classe_mage, [400, 680])

        # affiche une case où l'on peut rentrer le nom de son personnage
        affiche_texte_nom = Font.ARIAL_23.render("Nom :", True, Color.BLACK)
        self.window.blit(affiche_texte_nom, [950, 800])

        affiche_creer = Font.ARIAL_23.render("Créer le personnage", True, Color.BLACK)
        self.window.blit(affiche_creer, [880, 920])

        pygame.draw.rect(self.window, Color.BLACK, [900, 850, 200, 50], 2)

        # affichage d'une flèche si on veut retourner au menu principal
        if 10 < self.mouse_pos[0] < 110 and 10 < self.mouse_pos[1] < 75:
            self.window.blit(self.fleche_2, [10, 10])
        else:
            self.window.blit(self.fleche, [10, 10])

        # affichage d'aide pour le nom
        affiche_nom_info = Font.ARIAL_23.render("Le nom du personnage ne doit pas contenir d'espaces", True, Color.RED)
        affiche_nom_info_2 = Font.ARIAL_23.render("Les espaces présents seront automatiquement", True, Color.RED)
        affiche_nom_info_3 = Font.ARIAL_23.render("supprimés lors de la création du personnage", True, Color.RED)
        self.window.blit(affiche_nom_info, [1150, 700])
        self.window.blit(affiche_nom_info_2, [1150, 730])
        self.window.blit(affiche_nom_info_3, [1150, 760])

    def menu_creer_perso(self):
        classe_select = 'Guerrier'
        execution = True
        while execution:
            self.clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()  # récupère la position de la souris
            self.temps = pygame.time.get_ticks() / 1000
            self.window.fill(Color.WHITE)
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
                            #     self.joueur.nouveau_personnage(src.personnage.Personnage(self, nom_personnage.value, classe_select))
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
            self.clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()  # récupère la position de la souris
            self.window.fill(Color.WHITE)
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
            self.clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()  # récupère la position de la souris
            self.window.fill(Color.WHITE)
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
                            self.monde.set_personnage(perso_select)
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
                affiche_bouton_select = Font.ARIAL_23_2.render("→", True, Color.BLACK)
                self.window.blit(affiche_bouton_select, [600, 386 + espacement])

                # affichage du nom du perso sélectionner
                perso_select = self.joueur.personnages[espacement // 150]
                affiche_perso_select = Font.ARIAL_23.render(perso_select.nom + " lvl " + str(perso_select.lvl), True, Color.BLACK)
                self.window.blit(affiche_perso_select, [1500, 750])

            self.affichage_menu_jouer_perso()

            pygame.display.flip()  # Permet de mettre à jour la fenêtre

    def jeu(self, perso):
        """
        Lance le jeu avec le personnage passé en paramètre.
        :param perso:
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
        perso.connecte = True
        sort_lancer = None
        temps_attaques_tourbillon = [None, 0]  # liste indiquant le temps à attendre et le nombre d'attaques effectuer
        # Stuff de départ lvl 22 cheaté :)
        #for i in range(30):
        #    perso.ajouter_item_inventaire(generation_equipement_alea(22, True))
        #perso.ajouter_item_inventaire(generation_arme_alea(22, True))
        while execution:
            self.clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()  # récupère la position de la souris
            self.temps = pygame.time.get_ticks() / 1000
            self.window.fill(Color.WHITE)
            mobs_zone = self.monde.get_pnjs_attaquables_zone_courante()

            self.affichage_jeu(perso)
            self.affichage_interface_jeu(perso, dic_menu)

            # affiche la barre des sorts (3 emplacements de sorts pour l'instant)

            for mob in mobs_zone:
                if mob.est_mort():
                    temps_affiche_xp = self.temps.__round__()

            # affiche l'xp obtenu suite aux monstres tués
            if xp_obtenu != 0:
                if temps_affiche_xp + 2 > self.temps.__round__():
                    affiche_xp_obtenu = Font.ARIAL_23.render(f"+ {xp_obtenu} XP", True, Color.PURPLE)
                    self.window.blit(affiche_xp_obtenu, [perso.x + 100, perso.y + 50])
                else:
                    xp_obtenu = 0

            # Affiche un message indiquant que le joueur à level up
            # if level_up:
            #     if temps_affiche_level_up + 2 > self.temps:
            #         if temps_affiche_level_up + level_up_alpha / 255 < self.temps:
            #             if level_up_alpha != 255:
            #                 level_up_alpha += 51
            #         self.images_level_up[(level_up_alpha // 51) - 1].set_alpha(level_up_alpha)
            #         self.window.blit(self.images_level_up[(level_up_alpha // 51) - 1], [perso.x - 80, perso.y - 240])
            #     else:
            #         level_up = False
            #         level_up_alpha = 51

            pygame.display.flip()  # Permet de mettre à jour la fenêtre


if __name__ == "__main__":
    # Pour voir les perfs et optimisé : $ py -m cProfile -s time main.py | more

    # Le jeu ce joue en plein écran 1920 x 1080, si l'écran du joueur n'est pas de ce format
    # On lui indique de modifié la résolution de son écran
    pygame.init()
    info = pygame.display.Info()
    largeur_ecran, hauteur_ecran = info.current_w, info.current_h  # info.current_w, info.current_h ou pour test la fenetre d'erreur 1280, 720
    if largeur_ecran != 1920 or hauteur_ecran != 1080:
        import tkinter as tk
        from tkinter import messagebox

        def show_error():
            root = tk.Tk()
            root.withdraw()  # Hide the main root window
            messagebox.showerror("Mauvaise résolution fréro",
                                 "Le jeu ce joue uniquement en résolution d'écran 1920x1080.")
            root.destroy()

        show_error()


        pygame.quit()
    else:
        jeu = CyrilRpg()
        jeu.run()
