import pygame


class Arme:

    def __init__(self, lvl, degat, bonus_PV, bonus_force, rarete):
        self.type_equipement = "Arme"
        self.lvl = lvl
        self.degat = degat
        self.bonus_PV = bonus_PV
        self.bonus_force = bonus_force
        self.rarete = rarete
        self.equipee = False  # L'équipement est-il équipée sur un personnage ou pas
        self.logo_objet = pygame.image.load("./assets/items/armes/épées/épée_" + rarete + ".png").convert_alpha()

    def __getitem__(self, item):
        return True

    def equipe_item(self):
        self.equipee = True

    def desequipe_item(self):
        self.equipee = False
