import pygame

from data import Font, Color
from src.interfaceClasses import *
from src import utils


class FpsViewer(BasicInterfaceTextElement):
    def __init__(self, fps: float):
        super().__init__(0, 0, str(fps), Font.ARIAL_30, Color.BLACK)

    def update(self, game):
        self.update_text(str(round(game.clock.get_fps())))


class BackgroundImage(Image):
    def __init__(self, surf):
        super().__init__(0, 0, surf)


class BackgroundColor(BackgroundImage):
    def __init__(self, size, color):
        super().__init__(pygame.surface.Surface(size))
        self.surface.fill(color)


class PlayButton(ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.character_selection_menu()


class SettingsButton(ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.settings_menu()


class QuitButton(ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.quit()


class CharacterSelectionButton(ButtonImage):
    def __init__(self, img, x, y, character, text_font, text_color, center=True):
        self.character = character
        super().__init__(img, x, y, self.character.nom, text_font, text_color, center)


    def get_clicked(self, game):
        game.enter_world(self.character)



class CharacterCreationButton(ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.character_creation_menu()


class CharacterNameInput(InputField):
    def __init__(self, x, y, text_font, text_color, border_color=Color.BLACK, border_radius=2, center=True):
        super().__init__(x, y, text_font, text_color, border_color, border_radius, center)


class CharacterXpBar(BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=True):
        self.empty_surface = pygame.Surface((400, 35), pygame.SRCALPHA)
        super().__init__(x, y, self.empty_surface.copy(), center)
        self.character = character

        self.char_xp_text = BasicInterfaceTextElement(
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


class CharacterSpells(BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=True):
        self.empty_surface = pygame.Surface((800, 80))
        super().__init__(x, y, self.empty_surface.copy(), center)
        self.character = character


class CharacterMenus(BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=False):
        self.empty_surface = pygame.Surface((300, 50))
        super().__init__(x, y, self.empty_surface.copy(), center)
        self.character = character








