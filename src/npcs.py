import pygame, random

from data import Image, Color, Font

from src import utils, interfaceClasses


class Npc:
    def __init__(self, name: str, lvl: int, hp: int, dmg: int, frames_name: str, x: int | float, y: int | float, is_static: bool):
        self.name = name
        self.lvl = lvl
        self.max_hp = hp
        self.hp = self.max_hp
        self.dmg = dmg

        self.x = x
        self.y = y

        self.is_static = is_static
        self.frames_name = frames_name
        self.facing = "south"
        self.num_current_frame = 0
        self.rect = self.get_current_frame().get_rect()
        self.rect.midbottom = (self.x, self.y)

        self.movement_speed = 1

        self.selected = False
        self.hovered_by_mouse = False

        self.hovered_by_mouse_surf = None
        self.info_surf = None
        self.info_surf_hp_text = None
        self.info_surf_name_lvl = None

    def get_current_frame(self) -> pygame.Surface:
        return Image.FRAMES_NPCS[self.frames_name][self.facing][self.num_current_frame]

    def draw(self, surface: pygame.Surface):
        surface.blit(self.get_current_frame(), self.rect.topleft)
        # pygame.draw.rect(surface, "black", self.rect, 2)

        if self.hovered_by_mouse:
            # check if the mouse is colliding with a mob
            # if it is, then we show it visually by drawing a red mob image
            # shaped surface over it
            if self.hovered_by_mouse_surf is None:
                self.hovered_by_mouse_surf = self.get_current_frame().copy()
                self.hovered_by_mouse_surf.fill(Color.RED_HOVER, None, pygame.BLEND_RGB_ADD)

            surface.blit(self.hovered_by_mouse_surf, self.rect.topleft)
        else:
            self.hovered_by_mouse_surf = None

        if self.selected or self.hovered_by_mouse:
            # if this mob is selected, we indicate its information
            # like his name, his lvl, his hp / his max hp
            if self.info_surf is None:
                self.info_surf = interfaceClasses.BasicInterfaceElement(
                    0, 0,
                    pygame.Surface((200, 100), pygame.SRCALPHA),
                )
                self.info_surf.rect.midbottom = self.rect.midtop

                self.info_surf_hp_text = interfaceClasses.BasicInterfaceTextElement(
                    self.info_surf.rect.width / 2,
                    self.info_surf.rect.height / 2,
                    utils.convert_number(self.hp) + " / " + utils.convert_number(self.max_hp),
                    Font.ARIAL_30,
                    Color.BLACK,
                    True
                )

                self.info_surf_name_lvl = interfaceClasses.BasicInterfaceTextElement(
                    self.info_surf.rect.width / 2,
                    self.info_surf.rect.height / 2,
                    self.name + " lvl " + str(self.lvl),
                    Font.ARIAL_23,
                    Color.BLACK
                )
            else:
                self.info_surf_hp_text.update_text(utils.convert_number(self.hp) + " / " + utils.convert_number(self.max_hp))
                self.info_surf_name_lvl.update_text(self.name + " lvl " + str(self.lvl))

            info_surf_hp_border_rect = pygame.Rect(0, self.info_surf.rect.height / 2 - 40 / 2, self.info_surf.rect.width, 40)

            perc_hp_left = self.hp / self.max_hp
            if perc_hp_left >= 0.5:
                color_hp_bar_rect = (24 + 216 * (1 - perc_hp_left ** 2), 240, 10)
            else:
                color_hp_bar_rect = (240, 240 * (2 * perc_hp_left), 10)

            pygame.draw.rect(
                self.info_surf.surface, color_hp_bar_rect,
                pygame.Rect(0, info_surf_hp_border_rect.y, info_surf_hp_border_rect.width * perc_hp_left, 40))

            pygame.draw.rect(self.info_surf, Color.BLACK, info_surf_hp_border_rect, 2)  # Draws the border

            self.info_surf_hp_text.draw(self.info_surf)

            surface.blit(self.info_surf.surface, self.info_surf.rect.topleft)
        else:
            self.info_surf = None
            self.info_surf_hp_text = None
            self.info_surf_name_lvl = None

    def update(self, game, zone):
        if self.is_dead():
            zone.entities_in_zone.remove(self)
        else:
            if not self.is_static:
                self.deplacement()
                self.rect = self.get_current_frame().get_rect()
                self.rect.midbottom = (self.x, self.y)

            self.hovered_by_mouse = self.rect.collidepoint(game.mouse_pos)

        # if self.rect.collidepoint(game.mouse_pos):
        #     pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        # else:
        #     if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
        #         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_event(self, game, event):
        pass

    def is_dead(self):
        if self.hp <= 0:
            return True
        return False

    def deplacement(self):
        """
        Déplace un mob d'une position (x, y) à une autre position aléatoire.
        :return:
        """
        if self.direction is None and self.temps_attendre_depla == 120:
            direction_alea = ["north", "west", "east", "south"]
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
                self.animate()
            else:
                self.direction = None

            self.temps_attendre_depla += 1

    def animate(self):
        """
        Animate the Npc by changing his current frame
        """
        if int(self.num_current_frame) < len(Image.FRAMES_NPCS[self.frames_name][self.facing]):
            self.num_current_frame += self.movement_speed / 10
        else:
            self.num_current_frame = 0



class HostileNpc(Npc):
    def __init__(self, name: str, lvl: int, hp: int, dmg: int, frames_name: str, x: int | float, y: int | float):
        super().__init__(name, lvl, hp, dmg, frames_name, x, y)


class NeutralNpc(Npc):
    def __init__(self, name: str, lvl: int, hp: int, dmg: int, frames_name: str, x: int | float, y: int | float):
        super().__init__(name, lvl, hp, dmg, frames_name, x, y)


class FriendlyNpc(Npc):
    pass


class CompanionNpc(FriendlyNpc):
    pass




class Rat(HostileNpc):
    pass
























