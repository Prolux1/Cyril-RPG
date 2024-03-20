import pygame

from data import Image, Color, Font

from src import utils, interfaceClasses


class Npc:
    def __init__(self, name: str, lvl: int, hp: int, dmg: int, frames_name: str, x: int | float, y: int | float):
        self.name = name
        self.lvl = lvl
        self.max_hp = hp
        self.hp = self.max_hp
        self.dmg = dmg

        self.x = x
        self.y = y

        self.frames_name = frames_name
        self.facing = "south"
        self.num_current_frame = 0
        self.rect = Image.FRAMES_NPCS[self.frames_name][self.facing][self.num_current_frame].get_rect()
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

                perc_hp_left = self.hp / self.max_hp
                if perc_hp_left >= 0.5:
                    color_hp_bar_rect = (24 + 216 * (1 - perc_hp_left ** 2), 240, 10)
                else:
                    color_hp_bar_rect = (240, 240 * (2 * perc_hp_left), 10)

                pygame.draw.rect(self.info_surf, color_hp_bar_rect,
                                 pygame.Rect(0, mob_frame_rect.y, mob_frame_rect.width * perc_hp_left,
                                             mob_frame_rect.height))
                pygame.draw.rect(self.info_surf, Color.BLACK, mob_frame_rect, 2)  # Draws the border

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

            surface.blit(self.info_surf.surface, self.info_surf.rect.topleft)
        else:
            self.info_surf = None
            self.info_surf_hp_text = None
            self.info_surf_name_lvl = None

            # Draw the name and lvl of the mob
            name_lvl_surf = Font.ARIAL_23.render(self.nom + " lvl " + str(self.lvl), True, Color.BLACK)
            mob_info_surf.blit(name_lvl_surf, (mob_info_surf_rect.width / 2 - name_lvl_surf.get_width() / 2, 0))

            mob_frame_rect = pygame.Rect(0, mob_info_surf_rect.height / 2 - 40 / 2, mob_info_surf_rect.width, 40)

            pygame.draw.rect(mob_info_surf, color_mob_hp_bar_rect,
                             pygame.Rect(0, mob_frame_rect.y, mob_frame_rect.width * perc_hp_left,
                                         mob_frame_rect.height))
            pygame.draw.rect(mob_info_surf, Color.BLACK, mob_frame_rect, 2)  # Draws the border

            hp_hp_max_surf = Font.ARIAL_23.render(
                utils.convert_number(self.hp) + " / " + utils.convert_number(self.max_hp), True, Color.BLACK)
            mob_info_surf.blit(hp_hp_max_surf, (mob_info_surf_rect.width / 2 - hp_hp_max_surf.get_width() / 2,
                                                mob_info_surf_rect.height / 2 - hp_hp_max_surf.get_height() / 2))

            surface.blit(mob_info_surf, mob_info_surf_rect.topleft)


class HostileNpc(Npc):
    pass


class FriendlyNpc(Npc):
    pass







class Rat(HostileNpc):
    pass
























