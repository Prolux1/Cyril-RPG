
from data import Font, Color
from config import WINDOW_WIDTH, WINDOW_HEIGHT


from src import interface, personnage, monde




class GameUserInterface:
    def __init__(self, perso: personnage.Personnage, m: monde.Monde):
        self.personnage = perso

        self.components = [
            interface.CharacterFrame(perso, 10, 10, Font.ARIAL_30, Color.BLACK),
            interface.CharacterXpBar(perso, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.025, Font.ARIAL_23, Color.DARK_PURPLE),
            interface.CharacterSpells(perso, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.1, Font.ARIAL_23, Color.WHITE),
            interface.JournalDeQuetes(perso, WINDOW_WIDTH / 1.2, WINDOW_HEIGHT / 8),
            interface.GUIMenusPanel(perso, WINDOW_WIDTH / 1.075, WINDOW_HEIGHT / 1.055, Font.ARIAL_23, Color.WHITE),
            interface.InteractionsPnj(perso, m, WINDOW_WIDTH / 8, WINDOW_HEIGHT / 2),
            interface.FenetreLoot(perso, m, WINDOW_WIDTH / 1.5, WINDOW_HEIGHT / 1.5)
        ]

        self.character_dead_interface = interface.CharacterDead(perso)

    def draw(self, surface):
        for c in self.components:
            c.draw(surface)

        if self.personnage.est_mort():
            self.character_dead_interface.draw(surface)

    def update(self, game):
        for c in self.components:
            c.update(game)

        if self.personnage.est_mort():
            self.character_dead_interface.update(game)

    def handle_event(self, game, event):
        if not self.personnage.est_mort():
            for c in self.components:
                c.handle_event(game, event)
        else:
            self.character_dead_interface.handle_event(game, event)
