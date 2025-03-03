from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

import pygame, random

from data import Image, Color, Font

from src import utils, interfaceClasses, personnage


class Pnj:
    def __init__(self, rpg: "CyrilRpg", lvl, pv, degat, nom, orientation, frames: dict[str, dict[str, pygame.Surface]], x, y, xp, offset, est_boss=False, est_world_boss=False):
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
        self.nb_frames_etats = {"Lidle": 1, "Marcher": 4}
        self.temps_prochains_changements_frames = {"Lidle": 1.7, "Marcher": 0.7 / self.vitesse}
        self.temps_prochain_changement_frame = (rpg.time + self.temps_prochains_changements_frames[self.etat]) / self.nb_frames_etats[self.etat]


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft - self.offset)
        # pygame.draw.rect(surface, "black", self.rect, 2)

        if self.hovered_by_mouse:
            # regarde si la souris passe sur un monstre, si c'est le cas, on le montre visuellement en le coloriant en
            # rouge le monstre TODO : mettre plutot un contour rouge autour du monstre aulieu de le colorié en entier
            image_copy = self.image.copy()
            image_copy.fill(Color.RED_HOVER, None, pygame.BLEND_RGB_ADD)
            surface.blit(image_copy, self.rect.topleft - self.offset)

        if self.selected or self.hovered_by_mouse:
            # si le monstre est sélectionner, on affiche un cadre au dessus de sa tête qui indique :
            #   - son nom
            #   - son niveau
            #   - ses points de vies courant / ses points de vies max
            mob_info_surf = pygame.Surface((200, 100), pygame.SRCALPHA)
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
            self.deplacement(game)
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.x, self.y)

            self.hovered_by_mouse = pygame.Rect(self.rect.topleft - self.offset, self.rect.size).collidepoint(
                game.mouse_pos)

        # if self.rect.collidepoint(game.mouse_pos):
        #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        # else:
        #     if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
        #         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_event(self, game, event):
        pass

    def est_mort(self):
        return self.PV <= 0

    def deplacement(self, game: "CyrilRpg"):
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
            self.animation()
        elif self.direction is not None:
            self.etat = "Lidle"
            self.direction = None
            self.temps_prochain_changement_frame = 0
            self.frame_courante = 0
            self.animation()
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

    def prendre_cher(self, character: "personnage.Personnage", degats: int):
        self.PV = max(0, self.PV - degats)

        if self.est_mort():
            xp_given_to_player = int(self.lvl / character.lvl * self.xp * character.xp_multiplier)
            if xp_given_to_player > 0:
                character.gain_xp(xp_given_to_player)

            character.selected_mob = None

            # à une chance d'ajouter à l'inventaire du personnage, un équipement de type aléatoire
            # et en adéquation avec le lvl du mob si le mob est un boss,
            # il y a génération d'un équipement à tous les coups
            if self.est_world_boss:
                weapon_drop_chance = 50  # chance basique : 50 %
                for i in range(3):
                    character.inventory.add(utils.generation_equipement_alea(self.lvl, False, True))
            elif self.est_boss:
                weapon_drop_chance = 100 / 3  # chance basique : 33.3333333333 %
                character.inventory.add(utils.generation_equipement_alea(self.lvl, True))
            else:
                equipment_drop_chance = 100  # equipment % drop chance (basic : 20%)
                weapon_drop_chance = 50  # weapon % drop chance (basic : 10 %)

                if random.random() < equipment_drop_chance / 100:
                    character.inventory.add(utils.generation_equipement_alea(self.lvl))

            if random.random() < weapon_drop_chance / 100:
                character.inventory.add(utils.generation_arme_alea(self.lvl, self.est_boss, self.est_world_boss))

        # Le monstre attaque automatiquement en retour
        # souffrance = 5
        # for i in range(souffrance):
        #     self.attaquer(character)
        self.attaquer(character)



class PnjHostile(Pnj):
    def __init__(self, rpg: "CyrilRpg", lvl: int, pv: int, degats: int, nom: str, orientation: str,
                 frames: dict[str, dict[str, pygame.Surface]], x: int | float, y: int | float, xp, offset, est_boss=False,
                 est_world_boss=False):
        super().__init__(rpg, lvl, pv, degats, nom, orientation, frames, x, y, xp, offset, est_boss, est_world_boss)


class PnjNeutre(Pnj):
    pass


class PnjAmical(Pnj):
    def __init__(self, rpg: "CyrilRpg", lvl: int, pv: int, degats: int, nom: str, orientation: str,
                 frames: dict[str, dict[str, pygame.Surface]], x: int | float, y: int | float, xp, offset, est_boss=False,
                 est_world_boss=False):
        super().__init__(rpg, lvl, pv, degats, nom, orientation, frames, x, y, xp, offset, est_boss, est_world_boss)


class PnjCompanion(PnjAmical):
    """
    Un companion loup pour un personnage de classe chasseur par exemple.
    """




class Rat(PnjHostile):
    pass
























