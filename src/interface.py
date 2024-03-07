from data import Font, Color
from src.interfaceClasses import *


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










