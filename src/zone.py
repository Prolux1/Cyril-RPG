from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

import random

import pygame


from src import personnage, pnjs



class Zone:
    def __init__(self, rpg: "CyrilRpg", perso: personnage.Personnage, nom, nb_max_monstres):
        self.rpg = rpg
        self.personnage = perso
        self.nom = nom  # nom de la zone
        self.nb_max_monstres = nb_max_monstres


        self.pnjs: list[pnjs.Pnj] = []  # contains both pnjs and characters
        self.obstacles = []  # liste de rect


        self.time_last_respawn = 0
        self.mob_respawn_timer = 1

    def draw(self, surface: pygame.Surface):
        # surface.blit(Image.DESERT, (0, 0))
        surface.fill((198, 146, 73))

        # On affiche les entitées présente dans la zone de manière
        # horizontale pour avoir une sensation de dimension
        for entite in sorted(self.pnjs + [self.personnage], key=lambda entite_i: entite_i.rect.y):
            entite.draw(surface)

    def update(self, game):
        if game.time >= self.time_last_respawn + (self.mob_respawn_timer * self.rpg.interval_spawn_mobs):
            if len(self.get_pnjs_attaquables()) < self.nb_max_monstres:
                self.generate_random_mob(game)
            else:
                self.time_last_respawn = game.time

        for entite in self.pnjs + [self.personnage]:
            entite.update(game, self)

    def handle_event(self, game, event):
        for entite in self.pnjs + [self.personnage]:
            entite.handle_event(game, event)

    def get_pnjs_attaquables(self):
        return [pnj for pnj in self.pnjs if isinstance(pnj, pnjs.PnjHostile) or isinstance(pnj, pnjs.PnjNeutre)]

    def get_pnjs_interactibles(self):
        return [pnj for pnj in self.pnjs if pnj.est_interactible()]

    def get_pnjs(self):
        return self.pnjs

    def generate_random_mob(self, game):
        """
        Renvoie un mob en fonction du nom de la zone passé en paramètre
        """
        mob = None

        if self.nom == "Desert":
            proba_boss = random.randint(1, 20)
            if proba_boss == 1:
                mob = pnjs.Ratcaille(self.rpg, self.personnage)
            else:
                mob = pnjs.RatGeant(self.rpg, self.personnage)
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
        super().__init__(rpg, perso, "Desert", 100)

        # Ajout des pnjs amicaux de la zone Desert
        self.pnjs.extend(
            [
                pnjs.MarechalMcBride(rpg, perso)
            ]
        )


