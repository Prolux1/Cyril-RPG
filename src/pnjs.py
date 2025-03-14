from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

import pygame, random, math

from data import Image, Color, Font

from src import utils, personnage, quetes, cercle
from config import WINDOW_WIDTH, WINDOW_HEIGHT


class Pnj:
    def __init__(self, rpg: "CyrilRpg", lvl, pv, degat, nom, orientation, frames: dict[str, dict[str, pygame.Surface]],
                 x, y, xp: int, perso: "personnage.Personnage", est_boss=False, est_world_boss=False, se_deplace_aleatoirement=True, interactions=None):
        if interactions is None:
            interactions = []
        self.rpg = rpg
        self.personnage = perso
        self.lvl = lvl
        self.PV = pv
        self.PV_max = pv
        self.degat = degat
        self.nom = nom
        etat = "Lidle"
        self.image = frames[etat][orientation]
        self.x = x
        self.y = y
        self.offset: pygame.Vector2 = perso.offset

        self.xp = xp

        self.etat = etat
        self.orientation = orientation
        self.frames = frames  # Frames d'un mob sous forme de dico
        self.direction = None
        self.vitesse_de_base = 2  # 2 par défaut
        self.vitesse_marche = self.vitesse_de_base
        self.vitesse_course = self.vitesse_marche * 2
        self.dist_parcouru = 0
        self.temps_attendre_depla = 2
        self.frame_courante = 0
        self.est_boss = est_boss  # Booléen indiquant si le mob est un boss ou pas (False de base)
        self.est_world_boss = est_world_boss

        self.rect = self.image.get_rect()
        self.update_rect_pos()

        self.hovered_by_mouse = False

        self.enervee = False
        self.cercle_aggro = cercle.Cercle(self.rect.center, 400)

        self.temps_prochaine_attaque = self.rpg.time
        self.vitesse_attaque = 2.5  # Temps entre les attaques, plus cette valeure est faible, plus le pnj attaquera vite.

        self.dx_dy_directions = {"Gauche": (-1, 0), "Droite": (1, 0), "Dos": (0, -1), "Face": (0, 1)}
        self.temps_prochains_changements_frames = {"Lidle": 1.7, "Marcher": 0.7 / self.vitesse_marche, "Mourir": 0.7}


        self.temps_prochain_changement_frame = self.rpg.time
        self.se_deplace_aleatoirement = se_deplace_aleatoirement

        self.interactions = [] if interactions is None else interactions

        self.temps_decomposition = None
        self.duree_avant_decomposition = 60  # durée en secondes avant que le corps du pnj ne disparaisse après qu'il soit mort (60 par défaut)

        self.items_lootables = []

    def draw(self, surface):
        # pygame.draw.rect(surface, Color.BLACK, pygame.Rect((self.rect.topleft - self.offset), self.rect.size), 2)

        # pygame.draw.rect(surface, Color.BLACK, pygame.Rect((self.x, self.y) - self.offset, (2, 2)), 1)

        # Afficher le cerlce d'aggression du pnj
        # pygame.draw.circle(surface, Color.BLACK, self.cercle_aggro.centre - self.offset, self.cercle_aggro.rayon, 2)

        if self.personnage.hovered_pnj == self:
            # regarde si la souris passe sur un pnj, si c'est le cas, on le montre visuellement en le coloriant en :
            #   - rouge si c'est un pnj attaquable (Pnj hostile ou Pnj neutre)
            #   - vert si c'est un pnj amical
            #   TODO : mettre plutot un contour rouge autour du monstre aulieu de le colorié en entier
            image_copy = self.image.copy()
            image_copy.fill(Color.RED_HOVER if self.est_attaquable() else Color.GREEN_HOVER, None, pygame.BLEND_RGB_ADD)
            surface.blit(image_copy, self.rect.topleft - self.offset)
        else:
            surface.blit(self.image, self.rect.topleft - self.offset)

        if self.personnage.selected_mob == self or self.personnage.hovered_pnj == self:
            # si le pnj est sélectionner, on affiche un cadre au dessus de sa tête qui indique :
            #   - son nom
            #   - son niveau
            #   - ses points de vies courant / ses points de vies max
            taille_nom_lvl_x, taille_nom_lvl_y = Font.ARIAL_23.size(f"{self.nom} lvl {self.lvl}")
            taille_pv_sur_pv_max_x, taille_pv_sur_pv_max_y = Font.ARIAL_23.size(f"{utils.convert_number(self.PV)} / {utils.convert_number(self.PV_max)}")
            taille_pv_sur_pv_max_x += 10  # un ptit 10


            mob_info_surf = pygame.Surface((max(taille_nom_lvl_x, taille_pv_sur_pv_max_x), 100), pygame.SRCALPHA)  # 200, 100
            mob_info_surf_rect = mob_info_surf.get_rect()
            mob_info_surf_rect.midbottom = self.rect.midtop
            # pygame.draw.rect(mob_info_surf, Color.BLACK, pygame.Rect(0, 0, mob_info_surf.get_width(), mob_info_surf.get_height()), 2)

            # Affiche le nom et le niveau du monstre
            name_lvl_surf = Font.ARIAL_23.render(f"{self.nom} lvl {self.lvl}", True, Color.BLACK)
            mob_info_surf.blit(name_lvl_surf, (mob_info_surf_rect.width / 2 - name_lvl_surf.get_width() / 2, 0))

            mob_frame_rect = pygame.Rect(0, mob_info_surf_rect.height / 2 - 40 / 2, mob_info_surf_rect.width, 40)

            perc_hp_left = self.PV / self.PV_max
            if perc_hp_left >= 0.5:
                color_mob_hp_bar_rect = (24 + 216 * (1 - perc_hp_left ** 2), 240, 10)
            else:
                color_mob_hp_bar_rect = (240, 240 * (2 * perc_hp_left), 10)

            pygame.draw.rect(mob_info_surf, color_mob_hp_bar_rect,
                             pygame.Rect(0, mob_frame_rect.y, mob_frame_rect.width * perc_hp_left,
                                         mob_frame_rect.height))
            pygame.draw.rect(mob_info_surf, Color.BLACK, mob_frame_rect, 2)  # Draws the border

            hp_hp_max_surf = Font.ARIAL_23.render(
                f"{utils.convert_number(self.PV)} / {utils.convert_number(self.PV_max)}", True, Color.BLACK)
            mob_info_surf.blit(hp_hp_max_surf, (mob_info_surf_rect.width / 2 - hp_hp_max_surf.get_width() / 2,
                                                mob_info_surf_rect.height / 2 - hp_hp_max_surf.get_height() / 2))

            surface.blit(mob_info_surf, mob_info_surf_rect.topleft - self.offset)

    def update(self, game, zone):
        if self.est_decompose():
            zone.pnjs.remove(self)
        else:
            if not self.est_mort():
                self.cercle_aggro.update_centre(self.rect.center)

                self.vitesse_marche = self.vitesse_de_base * 60 / max(game.fps, 1)
                if self.est_enervee_contre(self.personnage) and not self.personnage.est_mort():
                    self.fumer_perso()
                elif self.se_deplace_aleatoirement:
                    self.deplacement_aleatoire(game)

            self.animation()
            self.update_rect_pos()

            self.hovered_by_mouse = pygame.Rect(self.rect.topleft - self.offset, self.rect.size).collidepoint(game.mouse_pos)

        # if self.rect.collidepoint(game.mouse_pos):
        #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        # else:
        #     if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
        #         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_event(self, game, event: pygame.event.Event):
        pass

    def est_mort(self) -> bool:
        return self.PV <= 0

    def est_decompose(self) -> bool:
        """
        Après que le pnj meurt, il y a un temps où son cadavre reste visible sur le sol, si ce temps atteinte sa limite,
        cette fonction renvoie True.
        """
        if self.temps_decomposition is not None:
            return self.est_mort() and self.rpg.time >= self.temps_decomposition
        return False

    def est_enervee_contre(self, perso: "personnage.Personnage") -> bool:
        return False

    def fumer_perso(self) -> None:
        # Le Pnj peut attaquer le personnage s'il est assez proche de celui-ci et s'il n'a pas attaqué recemment, c'est à
        # dire si le timer avant qu'il puisse lancer sa prochaine attaque a été atteint.
        if self.est_a_proximite_de(self.personnage):
            if self.rpg.time >= self.temps_prochaine_attaque:
                self.attaquer(self.personnage)
        else:  # Sinon le pnj se déplace vers le perso
            self.deplacement_vers_perso()

    def deplacement_vers_perso(self) -> None:
        dx = 0
        dy = 0

        if self.y > self.personnage.y + self.personnage.rect.height / 2:
            dy = -1
        elif self.y < self.personnage.y - self.personnage.rect.height / 2:
            dy = 1

        if self.x > self.personnage.x + self.personnage.rect.width / 2:
            self.orientation = "Gauche"
            dx = -1
        elif self.x < self.personnage.x - self.personnage.rect.width / 2:
            self.orientation = "Droite"
            dx = 1

        # Fait avancer le monstre en fonction de sa direction
        self.x = self.x + round(dx * math.sqrt(2 * (self.vitesse_course ** 2)) / 2)
        self.y = self.y + round(dy * math.sqrt(2 * (self.vitesse_course ** 2)) / 2)

    def deplacement_aleatoire(self, game: "CyrilRpg") -> None:
        """
        Déplace un pnj d'une position vers sa direction petit à petit par son facteur vitesse.
        """
        if self.direction is None and game.time >= self.temps_attendre_depla:
            # choisi une direction aléatoire vers où se déplacer
            self.direction = random.choice(list(self.dx_dy_directions.keys()))

            self.dist_parcouru = 0
            self.temps_attendre_depla = game.time + 4
            self.changer_etat("Marcher")
        elif self.direction is not None and self.dist_parcouru <= 200:
            self.orientation = self.direction

            # Fait avancer le monstre en fonction de sa direction
            dx, dy = self.dx_dy_directions[self.direction]
            self.x, self.y = self.x + (dx * self.vitesse_marche), self.y + (dy * self.vitesse_marche)

            self.dist_parcouru += self.vitesse_marche
        elif self.direction is not None:
            self.changer_etat("Lidle")
            self.direction = None
        else:
            if self.est_world_boss:
                self.image = self.frames[self.orientation][0]  # TODO : C'est quoi cette merde

    def est_a_proximite_de(self, perso: "personnage.Personnage") -> bool:
        assez_proche_du_personnage = (perso.x - perso.rect.width / 1.5 < self.x < perso.x + perso.rect.width / 1.5
                                      and perso.y - perso.rect.height / 1.5 < self.y < perso.y + perso.rect.height / 1.5 )
        return assez_proche_du_personnage

    def animation(self) -> None:
        """
        Anime le pnj en fonction de :
            - sa vitesse
            - son orientation
            - sa frame courante
        """
        if self.rpg.time >= self.temps_prochain_changement_frame:
            nb_frames_etat_courant = self.get_nb_frames_etat(self.etat, self.orientation)

            # On ne continue plus à animer si le pnj est mort et que sa dernière frame a été affiché
            if self.etat != "Mourir" or self.frame_courante != nb_frames_etat_courant - 1:
                largeur_frame_sheet_courante, hauteur_frame_sheet_courante = self.frames[self.etat][self.orientation].get_size()

                self.frame_courante = (self.frame_courante + 1) % max(1, nb_frames_etat_courant)

                indice_frame = self.frame_courante / max(1, nb_frames_etat_courant)

                rect_frame_courante = pygame.Rect(
                    largeur_frame_sheet_courante * indice_frame,
                    0,
                    largeur_frame_sheet_courante / max(1, nb_frames_etat_courant),
                    hauteur_frame_sheet_courante
                )

                self.image = self.frames[self.etat][self.orientation].subsurface(rect_frame_courante)
                self.rect = self.image.get_rect()

                self.temps_prochain_changement_frame = self.rpg.time + (self.temps_prochains_changements_frames[self.etat] / max(1, nb_frames_etat_courant))

    def changer_etat(self, nouvelle_etat: str) -> None:
        self.etat = nouvelle_etat
        self.temps_prochain_changement_frame = 0
        self.frame_courante = 0

    def update_rect_pos(self):
        self.rect.midbottom = (self.x, self.y)

    def est_attaquer(self) -> bool:
        return self.PV != self.PV_max

    def attaquer(self, perso: "personnage.Personnage") -> None:
        """
        Prends en paramètre un personnage à attaquer et lui inflige des dégâts.
        """
        perso.receive_damage(self.degat)
        self.temps_prochaine_attaque = self.rpg.time + self.vitesse_attaque

    def prendre_cher(self, perso: "personnage.Personnage", degats: int):
        """
        Cette fonction ne doit être appelé qu'une seule fois quand le pnj meurt.
        """
        self.PV = max(0, self.PV - degats)

        if self.est_mort():
            # Quand le pnj meurt on donne immédiatement l'xp au personnage puis il a un peu de temps pour le looter
            # avant que le corps disparaisse
            xp_a_donner_au_personnage = int(self.lvl / perso.lvl * self.xp * perso.xp_multiplier)
            if xp_a_donner_au_personnage > 0:
                perso.gain_xp(xp_a_donner_au_personnage)

            # Si le pnj meurt on regarde si le personnage qui l'a tué avait une quete où il devait le buter
            for quete in perso.get_quetes_actives_tuer_pnjs():
                if quete.pnj_match(self):
                    quete.incrementer_objectif_tuer_pnj(self)

            self.temps_decomposition = self.rpg.time + self.duree_avant_decomposition
            self.changer_etat("Mourir")

            # Génère du loot
            self.generer_loot()

        # Ancienne version d'attaque qui auto répliquait à chaque attaque du joueur
        # self.attaquer(perso)

    def generer_loot(self) -> None:
        self.items_lootables.clear()

        # à une chance d'ajouter à l'inventaire du personnage, un équipement de type aléatoire
        # et en adéquation avec le lvl du mob si le mob est un boss,
        # il y a génération d'un équipement à tous les coups
        if self.est_world_boss:
            weapon_drop_chance = 50  # chance basique : 50 %
            for i in range(3):
                self.items_lootables.append(utils.generation_equipement_alea(self.lvl, False, True))
        elif self.est_boss:
            weapon_drop_chance = 100 / 3  # chance basique : 33.3333333333 %
            self.items_lootables.append(utils.generation_equipement_alea(self.lvl, True))
        else:
            equipment_drop_chance = 100  # equipment % drop chance (basic : 20%)
            weapon_drop_chance = 50  # weapon % drop chance (basic : 10 %)

            if random.random() < equipment_drop_chance / 100:
                self.items_lootables.append(utils.generation_equipement_alea(self.lvl))

        if random.random() < weapon_drop_chance / 100:
            self.items_lootables.append(utils.generation_arme_alea(self.lvl, self.est_boss, self.est_world_boss))


        # Tests génération de plein d'items pour les loots
        for i in range(random.randint(5, 10)):
            if random.random() < 0.25:
                self.items_lootables.append(utils.generation_arme_alea(self.lvl, self.est_boss, self.est_world_boss))
            else:
                self.items_lootables.append(utils.generation_equipement_alea(self.lvl, self.est_boss, self.est_world_boss))


    def est_attaquable(self) -> bool:
        return isinstance(self, PnjHostile) or isinstance(self, PnjNeutre)

    def est_interactible(self) -> bool:
        return len(self.interactions) > 0

    @staticmethod
    def get_nom() -> str:
        return "?"

    @staticmethod
    def get_dict_nb_frames_etats() -> dict[str, int | dict[str, int]]:
        return {"Lidle": 0, "Marcher": 0, "Mourir": 0}

    def get_nb_frames_etat(self, etat: str, orientation: str) -> int:
        dict_ou_int_nb_frames_etats = self.get_dict_nb_frames_etats()[etat]
        if isinstance(dict_ou_int_nb_frames_etats, dict):
            return dict_ou_int_nb_frames_etats[orientation]
        else:
            return dict_ou_int_nb_frames_etats


class PnjHostile(Pnj):
    def __init__(self, rpg: "CyrilRpg", lvl: int, pv: int, degats: int, nom: str, orientation: str,
                 frames: dict[str, dict[str, pygame.Surface]], x: int | float, y: int | float, xp, perso: "personnage.Personnage", est_boss=False,
                 est_world_boss=False, se_deplace_aleatoirement=True):

        super().__init__(rpg, lvl, pv, degats, nom, orientation, frames, x, y, xp, perso, est_boss, est_world_boss, se_deplace_aleatoirement)

    def est_enervee_contre(self, perso: "personnage.Personnage") -> bool:
        return self.cercle_aggro.collidepoint((perso.x, perso.y))



class PnjNeutre(Pnj):
    # Pour la fonction "est_enervee_contre", on pourra dire qu'elle renvoie True si le personnage a attaquer le Pnj
    pass


class PnjAmical(Pnj):
    def __init__(self, rpg: "CyrilRpg", lvl: int, pv: int, degats: int, nom: str, orientation: str,
                 frames: dict[str, dict[str, pygame.Surface]], x: int | float, y: int | float, xp, perso: "personnage.Personnage", est_boss=False,
                 est_world_boss=False, se_deplace_aleatoirement=True, interactions=None):

        super().__init__(rpg, lvl, pv, degats, nom, orientation, frames, x, y, xp, perso, est_boss, est_world_boss, se_deplace_aleatoirement, interactions)


class PnjCompanion(PnjAmical):
    """
    Un companion loup pour un personnage de classe chasseur par exemple.
    """
    pass







class RatGeant(PnjHostile):
    def __init__(self, rpg: "CyrilRpg", perso: "personnage.Personnage"):
        lvl_mob = random.randint(1, 5)
        mob_x = random.choice((random.randint(-WINDOW_WIDTH, 0), random.randint(WINDOW_WIDTH, WINDOW_WIDTH * 2)))
        mob_y = random.choice((random.randint(-WINDOW_HEIGHT, 0), random.randint(WINDOW_HEIGHT, WINDOW_HEIGHT * 2)))
        super().__init__(
            rpg,
            lvl_mob,
            59 + 9 * lvl_mob,
            3 + lvl_mob,
            self.get_nom(),
            random.choice(Image.POSITIONS),
            Image.FRAMES_MOB_RAT,
            mob_x,
            mob_y,
            random.randint(40, 60),
            perso
        )

    @staticmethod
    def get_nom() -> str:
        return "Rat géant"

    @staticmethod
    def get_dict_nb_frames_etats() -> dict[str, int | dict[str, int]]:
        return {"Lidle": 1, "Marcher": 4, "Mourir": {"Face": 3, "Gauche": 4, "Droite": 4, "Dos": 3}}










class Ratcaille(PnjHostile):
    def __init__(self, rpg: "CyrilRpg", perso: "personnage.Personnage"):
        lvl_mob = random.randint(1, 5)

        # on s'assure que le mob spawn en dehors de l'écran car sinon pas beau
        mob_x = random.choice((random.randint(-WINDOW_WIDTH, 0), random.randint(WINDOW_WIDTH, WINDOW_WIDTH * 2)))
        mob_y = random.choice((random.randint(-WINDOW_HEIGHT, 0), random.randint(WINDOW_HEIGHT, WINDOW_HEIGHT * 2)))
        super().__init__(
            rpg,
            lvl_mob,
            623,
            24,
            self.get_nom(),
            random.choice(Image.POSITIONS),
            Image.FRAMES_RATCAILLE,
            mob_x,
            mob_y,
            random.randint(800, 900),
            perso,
            True
        )

    @staticmethod
    def get_nom() -> str:
        return "Ratcaille"

    @staticmethod
    def get_dict_nb_frames_etats() -> dict[str, int | dict[str, int]]:
        return {"Lidle": 1, "Marcher": 4, "Mourir": {"Face": 3, "Gauche": 4, "Droite": 4, "Dos": 3}}











class MarechalMcBride(PnjAmical):
    def __init__(self, rpg: "CyrilRpg", perso: "personnage.Personnage"):
        super().__init__(
            rpg,
            20,
            1361,
            78,
            "Maréchal McBride",
            "Face",
            Image.GUERRIER_FRAMES,
            WINDOW_WIDTH / 1.5,
            WINDOW_HEIGHT / 1.5,
            0,
            perso,
            se_deplace_aleatoirement=False,
            interactions=[
                quetes.QueteTuerPnjs(
                    "Satanés rongeurs",
                    f"Salutations {perso.nom}, le désert est infesté de rats géants. Il faut réduire "
                    f"leur nombre au plus vite avant qu'ils ne nous submerge!",
                    [(RatGeant, 7)],

                    description_rendu="Ça c'est ce qu'on appelle faire du ménage! Votre contribution ne sera pas oublié héros."

                )
            ]
        )

    @staticmethod
    def get_nom() -> str:
        return "Maréchal McBride"

    @staticmethod
    def get_dict_nb_frames_etats() -> dict[str, int | dict[str, int]]:
        return {"Lidle": 5, "Marcher": 8, "Mourir": {"Face": 5, "Gauche": 5, "Droite": 5, "Dos": 6}}
















