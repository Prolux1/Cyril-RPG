from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

from src import personnage, zone, pnjs


class Monde:
    def __init__(self, rpg: "CyrilRpg", perso: personnage.Personnage):
        self.rpg = rpg

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

    def draw(self, surface):
        self.get_zone_courante().draw(surface)

    def update(self, game):
        self.get_zone_courante().update(game)

    def handle_event(self, game, event):
        self.get_zone_courante().handle_event(game, event)

    def get_zone_courante(self) -> zone.Zone:
        return self.zones[self.personnage_courant.nom_zone_courante]

    def get_pnjs_attaquables_zone_courante(self) -> list[pnjs.PnjHostile | pnjs.PnjNeutre]:
        return self.get_zone_courante().get_pnjs_attaquables()

    def get_pnjs_zone_courante(self) -> list[pnjs.Pnj]:
        return self.get_zone_courante().get_pnjs()

    def get_pnjs_interactibles_zone_courante(self) -> list[pnjs.Pnj]:
        return self.get_zone_courante().get_pnjs_interactibles()

    def get_obstacles_zone_courante(self) -> list:
        return self.get_zone_courante().obstacles
