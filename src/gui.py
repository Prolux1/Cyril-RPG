
from data import Font, Color
from config import WINDOW_WIDTH, WINDOW_HEIGHT


from src import interface




class GameUserInterface:
    def __init__(self, character):
        self.components = [
            interface.CharacterFrame(character, 10, 10, Font.ARIAL_30, Color.BLACK),
            interface.CharacterXpBar(character, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.025, Font.ARIAL_23, Color.DARK_PURPLE),
            interface.CharacterSpells(character, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.1, Font.ARIAL_23, Color.WHITE),
            interface.GUIMenusPanel(character, WINDOW_WIDTH / 1.075, WINDOW_HEIGHT / 1.055, Font.ARIAL_23, Color.WHITE),
            interface.CharacterDead(character)
        ]

    def draw(self, surface):
        for c in self.components:
            c.draw(surface)

    def update(self, game):
        for c in self.components:
            c.update(game)

    def handle_event(self, game, event):
        for c in self.components:
            c.handle_event(game, event)
