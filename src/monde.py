from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

from src import personnage, zone, pnjs


class Monde:
    def __init__(self, rpg: "CyrilRpg", perso: personnage.Personnage):
        self.zones: dict[str, zone.Zone] = {
            "Desert": zone.Desert(rpg, perso)
        }

        self.personnage_courant = perso
        perso.monde = self

        # Ajout des différents obstacles des zones
        # self.zones["Marais"].ajouter_obstacles([
        #     pygame.Rect(640, 325, 640, 240),
        #     pygame.Rect(0, 0, 394, 417),
        #     pygame.Rect(0, 710, 411, 370),
        #     pygame.Rect(786, 876, 163, 155),
        #     pygame.Rect(1054, 23, 154, 158),
        #     pygame.Rect(1410, 50, 163, 155),
        #     pygame.Rect(1587, 278, 163, 155),
        #     pygame.Rect(1465, 658, 154, 158)
        # ])
        #
        # self.zones["Marais corrompu"].ajouter_obstacles([
        #     pygame.Rect(0, 0, 1920, 140),
        #     pygame.Rect(0, 140, 175, 800),
        #     pygame.Rect(0, 940, 1920, 140)
        # ])

    def get_zone_courante(self) -> zone.Zone:
        return self.zones[self.personnage_courant.zone]

    def get_monstres_zone_courante(self) -> list[pnjs.Pnj]:
        return self.zones[self.personnage_courant.zone].get_pnjs_hostiles()

    def draw(self, surface):
        self.zones[self.personnage_courant.zone].draw(surface)

    def update(self, game):
        self.zones[self.personnage_courant.zone].update(game)

    def handle_event(self, game, event):
        self.zones[self.personnage_courant.zone].handle_event(game, event)
