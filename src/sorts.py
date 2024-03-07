import pygame


from src import CircleClass


class Spell:
    def __init__(self, nom, perc_char_dmg, temps_rechargement, zone_effet=None, reach=16/9 * 100):
        self.nom = nom
        self.zone_effet = zone_effet  # un tuple (x, y) qui représente la taille de la zone d'effet
        self.perc_char_dmg = perc_char_dmg  # If perc_char_dmg = 100, this means that this spell will do 100% of the character damage
        self.temps_rechargement = temps_rechargement
        self.last_time_used = None

        self.reach = reach

    def ready(self, game_time):
        if self.last_time_used is None:
            return True
        else:
            return game_time - self.last_time_used >= self.temps_rechargement

    def set_timer(self, time):
        self.last_time_used = time

    def check_reach(self, caster_center, dest):
        """
        Check if this spell is in reach with the rect passed in parameter.
        This returns True if the center of the rect is inside the circle of
        ray reach.
        """
        c = CircleClass.Circle(caster_center, self.reach)
        return c.collide_point(dest)
