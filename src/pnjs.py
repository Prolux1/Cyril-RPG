from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

import pygame, random

from data import Image, Color, Font

from src import utils, interfaceClasses, personnage
from config import WINDOW_WIDTH, WINDOW_HEIGHT


class Pnj:
    def __init__(self, rpg: "CyrilRpg", lvl, pv, degat, nom, orientation, frames: dict[str, dict[str, pygame.Surface]],
                 x, y, xp, offset, est_boss=False, est_world_boss=False, se_deplace_aleatoirement=True, interactions=None):
        if interactions is None:
            interactions = []
        self.rpg = rpg
        self.lvl = lvl
        self.PV = pv
        self.PV_max = pv
        self.degat = degat
        self.nom = nom
        etat = "Lidle"
        self.image = frames[etat][orientation]
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x, self.y)
        self.offset: pygame.Vector2 = offset

        self.xp = xp

        self.etat = etat
        self.orientation = orientation
        self.frames = frames  # Frames d'un mob sous forme de dico
        self.direction = None
        self.vitesse_de_base = 2  # 2 par défaut
        self.vitesse = self.vitesse_de_base
        self.dist_parcouru = 0
        self.temps_attendre_depla = 2
        self.frame_courante = 0
        self.est_boss = est_boss  # Booléen indiquant si le mob est un boss ou pas (False de base)
        self.est_world_boss = est_world_boss

        self.selected = False
        self.hovered_by_mouse = False

        self.dx_dy_directions = {"Gauche": (-1, 0), "Droite": (1, 0), "Dos": (0, -1), "Face": (0, 1)}
        if nom == "Maréchal McBride":
            self.nb_frames_etats = {"Lidle": 5, "Courir": 8}
        else:
            self.nb_frames_etats = {"Lidle": 1, "Marcher": 4}
        self.temps_prochains_changements_frames = {"Lidle": 1.7, "Marcher": 0.7 / self.vitesse}
        self.temps_prochain_changement_frame = (rpg.time + self.temps_prochains_changements_frames[self.etat]) / self.nb_frames_etats[self.etat]
        self.se_deplace_aleatoirement = se_deplace_aleatoirement

        self.interactions = [] if interactions is None else interactions


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft - self.offset)
        # pygame.draw.rect(surface, "black", self.rect, 2)

        if self.hovered_by_mouse:
            # regarde si la souris passe sur un pnj, si c'est le cas, on le montre visuellement en le coloriant en :
            #   - rouge si c'est un pnj attaquable (Pnj hostile ou Pnj neutre)
            #   - vert si c'est un pnj amical
            #   TODO : mettre plutot un contour rouge autour du monstre aulieu de le colorié en entier
            image_copy = self.image.copy()
            image_copy.fill(Color.RED_HOVER if self.est_attaquable() else Color.GREEN_HOVER, None, pygame.BLEND_RGB_ADD)
            surface.blit(image_copy, self.rect.topleft - self.offset)

        if self.selected or self.hovered_by_mouse:
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
        if self.est_mort():
            zone.pnjs.remove(self)
        else:
            self.vitesse = self.vitesse_de_base * 60 / max(game.fps, 1)
            if self.se_deplace_aleatoirement:
                self.deplacement_aleatoire(game)
            self.animation()
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.x, self.y)

            self.hovered_by_mouse = pygame.Rect(self.rect.topleft - self.offset, self.rect.size).collidepoint(game.mouse_pos)

        # if self.rect.collidepoint(game.mouse_pos):
        #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        # else:
        #     if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
        #         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_event(self, game, event: pygame.event.Event):
        pass

    def est_mort(self):
        return self.PV <= 0

    def deplacement_aleatoire(self, game: "CyrilRpg"):
        """
        Déplace un pnj d'une position vers sa direction petit à petit par son facteur vitesse.
        """
        if self.direction is None and game.time >= self.temps_attendre_depla:
            # choisi une direction aléatoire vers où se déplacer
            self.direction = random.choice(list(self.dx_dy_directions.keys()))

            self.dist_parcouru = 0
            self.temps_attendre_depla = game.time + 4
            self.etat = "Marcher"
            self.temps_prochain_changement_frame = 0
            self.frame_courante = 0
        elif self.direction is not None and self.dist_parcouru <= 200:
            self.orientation = self.direction

            # Fait avancer le monstre en fonction de sa direction
            dx, dy = self.dx_dy_directions[self.direction]
            self.x, self.y = self.x + (dx * self.vitesse), self.y + (dy * self.vitesse)

            self.dist_parcouru += self.vitesse
        elif self.direction is not None:
            self.etat = "Lidle"
            self.direction = None
            self.temps_prochain_changement_frame = 0
            self.frame_courante = 0
        else:
            if self.est_world_boss:
                self.image = self.frames[self.orientation][0]

    def animation(self):
        """
        Anime le mob à l'aide en fonction de :
            - sa vitesse
            - son orientation
            - sa frame courante
        :return:
        """
        if self.rpg.time >= self.temps_prochain_changement_frame:
            self.frame_courante = (self.frame_courante + 1) % self.nb_frames_etats[self.etat]

            indice_frame = self.frame_courante / self.nb_frames_etats[self.etat]
            rect_frame_courante = pygame.Rect(
                self.frames[self.etat][self.orientation].get_width() * indice_frame,
                0,
                self.frames[self.etat][self.orientation].get_width() / self.nb_frames_etats[self.etat],
                self.frames[self.etat][self.orientation].get_height()
            )

            self.image = self.frames[self.etat][self.orientation].subsurface(rect_frame_courante)
            # self.frame_courante = (self.frame_courante + self.vitesse / 20) % len(self.frames[self.etat])

            self.temps_prochain_changement_frame = self.rpg.time + (self.temps_prochains_changements_frames[self.etat] / self.nb_frames_etats[self.etat])


    def est_attaquer(self) -> bool:
        return self.PV != self.PV_max

    def attaquer(self, pers: "personnage.Personnage") -> None:
        """
        Prends en paramètre un personnage à attaquer et lui inflige des dégâts.
        """
        pers.receive_damage(self.degat)

    def prendre_cher(self, perso: "personnage.Personnage", degats: int):
        self.PV = max(0, self.PV - degats)

        if self.est_mort():
            xp_given_to_player = int(self.lvl / perso.lvl * self.xp * perso.xp_multiplier)
            if xp_given_to_player > 0:
                perso.gain_xp(xp_given_to_player)

            perso.selected_mob = None

            # à une chance d'ajouter à l'inventaire du personnage, un équipement de type aléatoire
            # et en adéquation avec le lvl du mob si le mob est un boss,
            # il y a génération d'un équipement à tous les coups
            if self.est_world_boss:
                weapon_drop_chance = 50  # chance basique : 50 %
                for i in range(3):
                    perso.inventory.add(utils.generation_equipement_alea(self.lvl, False, True))
            elif self.est_boss:
                weapon_drop_chance = 100 / 3  # chance basique : 33.3333333333 %
                perso.inventory.add(utils.generation_equipement_alea(self.lvl, True))
            else:
                equipment_drop_chance = 100  # equipment % drop chance (basic : 20%)
                weapon_drop_chance = 50  # weapon % drop chance (basic : 10 %)

                if random.random() < equipment_drop_chance / 100:
                    perso.inventory.add(utils.generation_equipement_alea(self.lvl))

            if random.random() < weapon_drop_chance / 100:
                perso.inventory.add(utils.generation_arme_alea(self.lvl, self.est_boss, self.est_world_boss))

            # Si le pnj meurt on regarde si le personnage qui l'a tué avait une quete où il devait le buter
            for quete in perso.get_quetes_actives_tuer_pnjs():
                if quete.pnj_match(self):
                    quete.incrementer_objectif_tuer_pnj(self)

        # Le monstre attaque automatiquement en retour
        # souffrance = 5
        # for i in range(souffrance):
        #     self.attaquer(character)
        self.attaquer(perso)

    def est_attaquable(self) -> bool:
        return isinstance(self, PnjHostile) or isinstance(self, PnjNeutre)

    def est_interactible(self) -> bool:
        return len(self.interactions) > 0

    @staticmethod
    def get_nom() -> str:
        return "?"


class PnjHostile(Pnj):
    def __init__(self, rpg: "CyrilRpg", lvl: int, pv: int, degats: int, nom: str, orientation: str,
                 frames: dict[str, dict[str, pygame.Surface]], x: int | float, y: int | float, xp, offset, est_boss=False,
                 est_world_boss=False, se_deplace_aleatoirement=True):

        super().__init__(rpg, lvl, pv, degats, nom, orientation, frames, x, y, xp, offset, est_boss, est_world_boss, se_deplace_aleatoirement)


class PnjNeutre(Pnj):
    pass


class PnjAmical(Pnj):
    def __init__(self, rpg: "CyrilRpg", lvl: int, pv: int, degats: int, nom: str, orientation: str,
                 frames: dict[str, dict[str, pygame.Surface]], x: int | float, y: int | float, xp, offset, est_boss=False,
                 est_world_boss=False, se_deplace_aleatoirement=True, interactions=None):

        super().__init__(rpg, lvl, pv, degats, nom, orientation, frames, x, y, xp, offset, est_boss, est_world_boss, se_deplace_aleatoirement, interactions)


class PnjCompanion(PnjAmical):
    """
    Un companion loup pour un personnage de classe chasseur par exemple.
    """




class Rat(PnjHostile):
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
            Image.FRAMES_MOB_RAT, mob_x, mob_y,
            random.randint(40, 60),
            perso.offset
        )

    @staticmethod
    def get_nom() -> str:
        return "Rat"





















