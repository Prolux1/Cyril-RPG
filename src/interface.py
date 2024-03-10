import pygame

from data import Font, Color, Image
from src import interfaceClasses, utils
from config import WINDOW_WIDTH, WINDOW_HEIGHT


class FpsViewer(interfaceClasses.BasicInterfaceTextElement):
    def __init__(self, fps: float):
        super().__init__(0, 0, str(fps), Font.ARIAL_30, Color.BLACK)

    def update(self, game):
        self.update_text(str(round(game.clock.get_fps())))


class PlayButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.character_selection_menu()


class SettingsButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.settings_menu()


class QuitButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.quit()


class CharacterSelectionButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, character, text_font, text_color, center=True):
        self.character = character
        super().__init__(img, x, y, self.character.nom, text_font, text_color, center)


    def get_clicked(self, game):
        game.enter_world(self.character)



class CharacterCreationButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.character_creation_menu()


class CharacterNameInput(interfaceClasses.InputField):
    def __init__(self, x, y, text_font, text_color, border_color=Color.BLACK, border_radius=2, center=True):
        super().__init__(x, y, text_font, text_color, border_color, border_radius, center)


class CharacterXpBar(interfaceClasses.BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=True):
        self.empty_surface = pygame.Surface((400, 35), pygame.SRCALPHA)
        super().__init__(x, y, self.empty_surface.copy(), center)
        self.character = character

        self.char_xp_text = interfaceClasses.BasicInterfaceTextElement(
            self.rect.width / 2,
            self.rect.height / 2,
            str(self.character.xp) + " / " + str(self.character.xp_requis),
            text_font,
            text_color,
            True
        )

        pygame.draw.rect(self.surface, Color.PURPLE, pygame.Rect(0, 0, self.surface.get_width() * (self.character.xp / self.character.xp_requis), self.surface.get_height()))

        pygame.draw.rect(self.surface, Color.GREY_LIGHTEN, self.surface.get_rect(), 2)

        self.char_xp_text.draw(self.surface)

    def update(self, game):
        self.char_xp_text.update_text(str(self.character.xp) + " / " + str(self.character.xp_requis))

        updated_surf = self.empty_surface.copy()
        pygame.draw.rect(updated_surf, Color.PURPLE, pygame.Rect(0, 0, updated_surf.get_width() * (self.character.xp / self.character.xp_requis), updated_surf.get_height()))
        pygame.draw.rect(updated_surf, Color.GREY_LIGHTEN, updated_surf.get_rect(), 2)
        self.char_xp_text.draw(updated_surf)

        self.update_surf(updated_surf)


class CharacterSpells(interfaceClasses.BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=True):
        self.empty_surface = pygame.Surface((800, 80))
        super().__init__(x, y, self.empty_surface.copy(), center)
        self.character = character


class GUIMenusPanel(interfaceClasses.BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=False):
        self.character = character
        self.components = [
            GUIMenusItemBag(self.character),
            GUIMenusItemEquipment(self.character),
            GUIMenusItemDonjons(self.character)
        ]

        width_needed = 0
        height_needed = 0
        self.gap_between_icons = 15
        for c in self.components:
            width_needed += c.rect.width
            if c.rect.height > height_needed:
                height_needed = c.rect.height

        self.empty_surface = pygame.Surface((width_needed + self.gap_between_icons * len(self.components), height_needed), pygame.SRCALPHA)
        super().__init__(x, y, self.empty_surface.copy(), center)

        self.rect.x -= self.rect.width

        total_width_taken = 0
        for i in range(len(self.components)):
            total_width_taken += self.components[i].rect.width
            self.surface.blit(self.components[i].surface, (self.rect.width - total_width_taken, height_needed - self.components[i].rect.height))

            self.components[i].rect.topleft = (
                self.rect.topright[0] - total_width_taken,
                self.rect.topright[1] + height_needed - self.components[i].rect.height
            )

            total_width_taken += self.gap_between_icons

    def draw(self, surface):
        # pygame.draw.rect(surface, Color.BLACK, self.rect, 2)
        # for c in self.components:
        #     pygame.draw.rect(surface, Color.BLACK, c.rect, 2)
        surface.blit(self.surface, self.rect.topleft)

        for c in self.components:
            c.draw(surface)

    def update(self, game):
        for c in self.components:
            c.update(game)

    def handle_event(self, game, event):
        for c in self.components:
            c.handle_event(game, event)


class GUIMenusItem(interfaceClasses.ButtonImage):
    def __init__(self, character, key, icon, menu, text, text_font, text_color, center=False):
        self.character = character
        self.key = key
        super().__init__(icon, 0, 0, text, text_font, text_color, center)

        self.menu = menu

        self.show_menu = False

    def draw(self, surface):
        if self.show_menu:
            self.menu.draw(surface)

    def handle_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # on click pressure
            if event.button == 1:  # left click
                self.pressed = self.collide_with_point(game.mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:  # on click release
            if event.button == 1:
                if self.pressed:
                    self.pressed = False
                    if self.collide_with_point(game.mouse_pos):
                        self.get_clicked(game)

        if event.type == pygame.KEYDOWN:
            if event.key == self.key:
                self.get_clicked(game)

    def get_clicked(self, game):
        self.show_menu = not self.show_menu









class GUIMenusItemBag(GUIMenusItem):
    def __init__(self, character):
        super().__init__(character, pygame.K_b, Image.BAG_ICON, GUIInventoryMenu(character.inventory), "", Font.ARIAL_23, Color.WHITE)


class GUIInventoryMenu(interfaceClasses.StaticImage):
    def __init__(self, inventory):
        self.inventory = inventory
        super().__init__(WINDOW_WIDTH / 1.2, WINDOW_HEIGHT / 1.5, Image.IMAGE_INVENTORY, center=True)










class GUIMenusItemEquipment(GUIMenusItem):
    def __init__(self, character):
        super().__init__(character, pygame.K_c, Image.EQUIPMENT_ICON, GUIEquipmentMenu(character.equipment), "", Font.ARIAL_23, Color.WHITE)


class GUIEquipmentMenu(interfaceClasses.StaticImage):
    def __init__(self, equipment):
        self.equipment = equipment
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, Image.MENU_EQUIPEMENT_PERSONNAGE, center=True)












class GUIMenusItemDonjons(GUIMenusItem):
    def __init__(self, character):
        super().__init__(character, pygame.K_v, Image.DONJONS_ICON, GUIDonjonsMenu(None), "", Font.ARIAL_23, Color.WHITE)


class GUIDonjonsMenu(interfaceClasses.StaticImage):
    def __init__(self, donjons):
        self.donjons = donjons
        super().__init__(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2, Image.MENU_DONJONS, center=True)






