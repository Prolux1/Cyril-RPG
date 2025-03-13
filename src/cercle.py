import pygame
from math import hypot

from data import Color

class Cercle:
    def __init__(self, centre: tuple[int | float, int | float], rayon: int | float):
        self.centre = centre
        self.centrex, self.centrey = centre
        self.rayon = rayon
        self.diametre = rayon * 2
        self.selected = False

    def draw(self, surface: pygame.Surface, color: pygame.Color = Color.BLACK, width: int = 2):
        pygame.draw.circle(surface, color, self.centre, self.rayon, width)

    def collidepoint(self, pos: tuple[int | float, int | float]) -> bool:
        dist_x = pos[0] - self.centrex
        dist_y = pos[1] - self.centrey
        return hypot(dist_x, dist_y) < self.rayon

    def collidecircle(self, circle: "Cercle"):
        other_circle_x = circle.centrex
        other_circle_y = circle.centrey
        other_circle_radius = circle.rayon
        distance_between_circles_squared = ((other_circle_x - self.centrex) ** 2) + ((other_circle_y - self.centrey) ** 2)
        radius_circles_sum_squared = (self.rayon + other_circle_radius) ** 2

        return distance_between_circles_squared > radius_circles_sum_squared

    def update_centre(self, new_centre: tuple[int | float, int | float]):
        self.centre = new_centre
        self.centrex, self.centrey = new_centre





