import pygame
from math import hypot


class Cercle:
    def __init__(self, center: tuple, radius: int or float):
        self.center = center
        self.centerx = center[0]
        self.centery = center[1]
        self.radius = radius
        self.diameter = radius * 2
        self.selected = False

    def collide_point(self, pos):
        dist_x = pos[0] - self.centerx
        dist_y = pos[1] - self.centery
        return hypot(dist_x, dist_y) < self.radius

    def collide_circle(self, circle):
        other_circle_x = circle.centerx
        other_circle_y = circle.centery
        other_circle_radius = circle.radius
        distance_between_circles_squared = ((other_circle_x - self.centerx) ** 2) + ((other_circle_y - self.centery) ** 2)
        radius_circles_sum_squared = (self.radius + other_circle_radius) ** 2

        return distance_between_circles_squared > radius_circles_sum_squared

    def draw(self, surface, color=(0, 0, 0), width=2):
        pygame.draw.circle(surface, color, self.center, self.radius, width)



