import random
import pygame


from data import Color, Font

from src import utils


class Monstre:
    def __init__(self, lvl, PV, degat, nom, orientation, frames, x, y, xp, offset, est_boss=False, est_world_boss=False):
        self.lvl = lvl
        self.PV = PV
        self.PV_max = PV
        self.degat = degat
        self.nom = nom
        self.image = frames[orientation][0]
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x, self.y)
        self.offset = offset

        self.xp = xp

        self.orientation = "Face"
        self.frames = frames  # Frames d'un mob sous forme de dico
        self.direction = None
        self.dist_parcouru = 0
        self.temps_attendre_depla = 0
        self.frame_courante = 0
        self.est_boss = est_boss  # Booléen indiquant si le mob est un boss ou pas (False de base)
        self.est_world_boss = est_world_boss

        self.movement_speed = 1

        self.selected = False
        self.hovered_by_mouse = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft - self.offset)
        # pygame.draw.rect(surface, "black", self.rect, 2)

        if self.hovered_by_mouse:
            # check if the mouse of the player is colliding with a mob
            # if it is, then we show it visually by drawing a red mob image
            # shaped surface over it
            image_copy = self.image.copy()
            image_copy.fill(Color.RED_HOVER, None, pygame.BLEND_RGB_ADD)
            surface.blit(image_copy, self.rect.topleft - self.offset)

        if self.selected or self.hovered_by_mouse:
            # if this mob is selected, we indicate the quantity a multitude of information
            # like his name, his lvl, his hp / his max hp
            mob_info_surf = pygame.Surface((200, 100), pygame.SRCALPHA)
            mob_info_surf_rect = mob_info_surf.get_rect()
            mob_info_surf_rect.midbottom = self.rect.midtop
            # pygame.draw.rect(mob_info_surf, Color.BLACK, pygame.Rect(0, 0, mob_info_surf.get_width(), mob_info_surf.get_height()), 2)

            # Draw the name and lvl of the mob
            name_lvl_surf = Font.ARIAL_23.render(self.nom + " lvl " + str(self.lvl), True, Color.BLACK)
            mob_info_surf.blit(name_lvl_surf, (mob_info_surf_rect.width / 2 - name_lvl_surf.get_width() / 2, 0))

            mob_frame_rect = pygame.Rect(0, mob_info_surf_rect.height / 2 - 40 / 2, mob_info_surf_rect.width, 40)


            perc_hp_left = self.PV / self.PV_max
            if perc_hp_left >= 0.5:
                color_mob_hp_bar_rect = (24 + 216 * (1 - perc_hp_left ** 2), 240, 10)
            else:
                color_mob_hp_bar_rect = (240, 240 * (2 * perc_hp_left), 10)

            pygame.draw.rect(mob_info_surf, color_mob_hp_bar_rect, pygame.Rect(0, mob_frame_rect.y, mob_frame_rect.width * perc_hp_left, mob_frame_rect.height))
            pygame.draw.rect(mob_info_surf, Color.BLACK, mob_frame_rect, 2)  # Draws the border


            hp_hp_max_surf = Font.ARIAL_23.render(utils.convert_number(self.PV) + " / " + utils.convert_number(self.PV_max), True, Color.BLACK)
            mob_info_surf.blit(hp_hp_max_surf, (mob_info_surf_rect.width / 2 - hp_hp_max_surf.get_width() / 2, mob_info_surf_rect.height / 2 - hp_hp_max_surf.get_height() / 2))


            surface.blit(mob_info_surf, mob_info_surf_rect.topleft - self.offset)

    def update(self, game, zone):
        if self.is_dead():
            zone.entities_in_zone.remove(self)
        else:
            self.deplacement(self.movement_speed / 10)
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.x, self.y)

            self.hovered_by_mouse = pygame.Rect(self.rect.topleft - self.offset, self.rect.size).collidepoint(game.mouse_pos)

        # if self.rect.collidepoint(game.mouse_pos):
        #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        # else:
        #     if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
        #         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_event(self, game, event):
        pass


    def is_dead(self):
        if self.PV <= 0:
            return True
        return False

    def deplacement(self, vitesse):
        """
        Déplace un mob d'une position (x, y) à une autre position aléatoire.
        :return:
        """
        if self.direction is None and self.temps_attendre_depla == 120:
            direction_alea = [-2, -1, 1, 2]
            if self.x - 200 < 0:
                direction_alea.remove(-1)
            if self.y - self.rect.height - 200 < 0:
                direction_alea.remove(-2)
            if self.x + 200 > 1920:
                direction_alea.remove(1)
            if self.y + 200 > 1080:
                direction_alea.remove(2)
            self.direction = random.choice(direction_alea)
            self.dist_parcouru = 0
            self.temps_attendre_depla = 0
        elif self.direction is not None:
            if self.dist_parcouru <= 200:
                if self.direction == -1:
                    self.orientation = "Gauche"
                    self.x -= 2
                    self.dist_parcouru += 2
                elif self.direction == 1:
                    self.orientation = "Droite"
                    self.x += 2
                    self.dist_parcouru += 2
                elif self.direction == -2:
                    self.orientation = "Dos"
                    self.y -= 2
                    self.dist_parcouru += 2
                elif self.direction == 2:
                    self.orientation = "Face"
                    self.y += 2
                    self.dist_parcouru += 2
                self.animation(vitesse)
            else:
                self.direction = None
        else:
            if self.est_world_boss:
                if self.orientation == "Gauche":
                    self.image = self.frames["Gauche"][0]
                elif self.orientation == "Droite":
                    self.image = self.frames["Droite"][0]
                elif self.orientation == "Face":
                    self.image = self.frames["Face"][0]
                elif self.orientation == "Dos":
                    self.image = self.frames["Dos"][0]

            self.temps_attendre_depla += 1

    def animation(self, vitesse):
        """
        Anime le mob à l'aide de ses frames et en fonction de son orientation.
        :return:
        """
        if int(self.frame_courante) < len(self.frames[self.orientation]):
            self.image = self.frames[self.orientation][int(self.frame_courante)]
            self.frame_courante += vitesse
        else:
            self.frame_courante = vitesse

    def est_attaquer(self):
        if self.PV != self.PV_max:
            return True

    def attaquer(self, personnage):
        """
        Prends en paramètre un personnage attaquant le mob et l'attaque.
        :param personnage:
        :return:
        """
        if self.est_attaquer():
            personnage.receive_damage(self.degat)

    def take_damage(self, character, amount):
        if self.PV - amount < 0:
            self.PV = 0
        else:
            self.PV -= amount

        if self.is_dead():
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

        # The mob automatically fight back
        # souffrance = 5
        # for i in range(souffrance):
        #     self.attaquer(character)
        self.attaquer(character)


