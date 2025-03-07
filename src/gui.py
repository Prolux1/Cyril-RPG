
from data import Font, Color
from config import WINDOW_WIDTH, WINDOW_HEIGHT


from src import interface, personnage, monde




class GameUserInterface:
    def __init__(self, perso: personnage.Personnage, m: monde.Monde):
        self.components = [
            interface.CharacterFrame(perso, 10, 10, Font.ARIAL_30, Color.BLACK),
            interface.CharacterXpBar(perso, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.025, Font.ARIAL_23, Color.DARK_PURPLE),
            interface.CharacterSpells(perso, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.1, Font.ARIAL_23, Color.WHITE),
            interface.JournalDeQuetes(perso, WINDOW_WIDTH / 1.2, WINDOW_HEIGHT / 8),
            interface.GUIMenusPanel(perso, WINDOW_WIDTH / 1.075, WINDOW_HEIGHT / 1.055, Font.ARIAL_23, Color.WHITE),
            interface.InteractionsPnj(perso, m, WINDOW_WIDTH / 8, WINDOW_HEIGHT / 2),
            interface.CharacterDead(perso)
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
