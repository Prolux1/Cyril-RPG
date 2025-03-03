from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

import random

import pygame

from data import Image

from src import personnage, pnjs, monde
from config import WINDOW_WIDTH, WINDOW_HEIGHT



class Zone:
    def __init__(self, rpg: "CyrilRpg", perso: personnage.Personnage, nom, nb_max_monstres):
        self.rpg = rpg
        self.personnage = perso
        self.nom = nom  # nom de la zone
        self.nb_max_monstres = nb_max_monstres


        self.pnjs = [perso]  # contains both pnjs and characters
        self.obstacles = []  # liste de rect


        self.time_last_respawn = 0
        self.mob_respawn_timer = 1

    def draw(self, surface: pygame.Surface):
        # surface.blit(Image.DESERT, (0, 0))
        surface.fill((198, 146, 73))

        # On affiche les entitées présente dans la zone de manière
        # horizontale pour avoir une sensation de dimension
        self.pnjs.sort(key=lambda mob_i: mob_i.y)
        for entity in self.pnjs:
            entity.draw(surface)

    def update(self, game):
        if game.time >= self.time_last_respawn + (self.mob_respawn_timer * self.rpg.interval_spawn_mobs):
            if self.get_nb_mobs() < self.nb_max_monstres:
                self.generate_random_mob(game)
            else:
                self.time_last_respawn = game.time

        for entity in self.pnjs:
            entity.update(game, self)

    def handle_event(self, game, event):
        for entity in self.pnjs:
            entity.handle_event(game, event)

    def get_pnjs_hostiles(self):
        return [pnj for pnj in self.pnjs if isinstance(pnj, pnjs.PnjHostile)]

    def get_personnage(self) -> personnage.Personnage:
        return self.personnage

    def get_nb_mobs(self):
        return len(self.get_pnjs_hostiles())

    def generate_random_mob(self, game):
        """
        Renvoie un mob en fonction du nom de la zone passé en paramètre
        """
        mob = None

        if self.nom == "Desert":
            proba_boss = random.randint(1, 20)
            # on s'assure que le mob spawn en dehors de l'écran car sinon pas très sympa
            orientation = random.choice(Image.POSITIONS)
            mob_x = random.choice((random.randint(-WINDOW_WIDTH, 0), random.randint(WINDOW_WIDTH, WINDOW_WIDTH * 2)))
            mob_y = random.choice((random.randint(-WINDOW_HEIGHT, 0), random.randint(WINDOW_HEIGHT, WINDOW_HEIGHT * 2)))
            if proba_boss == 1:
                lvl_mob = 8

                mob = pnjs.PnjHostile(self.rpg, lvl_mob, 623, 24, "Boss Rat", orientation,
                                   Image.FRAMES_MOB_BOSS_RAT, mob_x, mob_y, random.randint(800, 900),
                                   self.personnage.offset, True)
            else:
                lvl_mob = random.randint(1, 5)
                mob = pnjs.PnjHostile(self.rpg, lvl_mob, 59 + 9 * lvl_mob, 3 + lvl_mob, "Rat", orientation,
                                   Image.FRAMES_MOB_RAT, mob_x, mob_y, random.randint(40, 60), self.personnage.offset)
                # mob = Monstre(lvl_mob, 59 + 9 * lvl_mob, 3 + lvl_mob, "Loup humain", self.frames_mob_loup_humain["Face"][0], self.frames_mob_loup_humain, mob_x, mob_y, randint(40, 60) * xp_multiplier, [mob_x, mob_y + 40, 35 * 4, 44 * 4])






        # elif self.nom == "Marais":
        #     proba_boss = random.randint(1, 20)
        #     if proba_boss == 1:
        #         lvl_mob = 20
        #         mob_x, mob_y = random.randint(300, 1800), random.randint(200, 900)
        #         mob = pnjs.Monstre(lvl_mob, 27138, 107, "Boss Cerf", Image.FRAMES_MOB_BOSS_CERF["Face"][0],
        #                            Image.FRAMES_MOB_BOSS_CERF, mob_x, mob_y, random.randint(800, 900) * lvl_mob,
        #                            self.get_player_character().offset, True)
        #     else:
        #         lvl_mob = random.randint(11, 18)
        #         mob_x, mob_y = random.randint(300, 1800), random.randint(200, 900)
        #         mob = pnjs.Monstre(lvl_mob, 47 + 111 * lvl_mob, 6 * lvl_mob, "Cerf", Image.FRAMES_MOB_CERF["Face"][0],
        #                            Image.FRAMES_MOB_CERF, mob_x, mob_y, random.randint(40, 60) * lvl_mob,
        #                            self.get_player_character().offset)
        # elif self.nom == "Marais corrompu":
        #     lvl_mob = 25
        #     mob_x, mob_y = random.randint(300, 1800), random.randint(200, 900)
        #     mob = pnjs.Monstre(lvl_mob, 120000, 250, "Orc", Image.frames_mob_orc["Face"][0], Image.frames_mob_orc, mob_x,
        #                        mob_y, random.randint(1500, 1700) * lvl_mob, self.get_player_character().offset, False, True)

        # lvl_mob = 30
        # mob_x, mob_y = randint(300, 1600), randint(100, 800)
        # mob = Monstre(lvl_mob, 126*10**3, 300, "Dotum", self.frames_mob_Dotum["Face"][0], self.frames_mob_Dotum, mob_x, mob_y, randint(15000, 18000), [mob_x - 40, mob_y + 20, 25 * 8, 42 * 8], False, True)

        # lvl_mob = 40
        # mob_x, mob_y = 399, 399
        # mob = Monstre(lvl_mob, 897 * 10 ** 3, 1250, "Fenrir", self.frames_mob_fenrir["Face"][0], self.frames_mob_fenrir, mob_x, mob_y, randint(90000, 110000), [mob_x - 40, mob_y + 20, 25 * 12, 42 * 12], False, True)

        self.pnjs.append(mob)
        self.time_last_respawn = game.time

    def ajouter_obstacles(self, liste_obstacle):
        """
        Prends en paramètre une liste d'obstacles chaque obstacle étant sous forme d'un rect (liste de taille 4)
        """
        for obstacle in liste_obstacle:
            self.obstacles.append(obstacle)





class Desert(Zone):
    def __init__(self, rpg: "CyrilRpg", perso: personnage.Personnage):
        super().__init__(rpg, perso, "Desert", 250)

        # Ajout des pnjs amicaux de la zone Desert
        # self.pnjs.extend(
        #     [
        #         pnjs.PnjAmical(20, 1361, 78, "Maréchal McBride", "Face", Image.GUERRIER_FRAMES, 100, 100, 0, self.get_personnage().offset)
        #     ]
        # )


