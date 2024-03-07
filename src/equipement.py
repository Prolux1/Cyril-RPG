import pygame


class Equipement:

    def __init__(self, type_equipement, lvl, armure, bonus_PV, bonus_force, rarete):
        self.type_equipement = type_equipement
        self.lvl = lvl
        self.armure = armure
        self.bonus_PV = bonus_PV
        self.bonus_force = bonus_force
        self.rarete = rarete
        self.equipee = False  # L'équipement est-il équipée sur un personnage ou pas
        if rarete == "Légendaire":
            self.logo_objet = pygame.image.load("./assets/items/equipement/" + type_equipement + "/" + type_equipement + "_spécial.png").convert_alpha()
        else:
            self.logo_objet = pygame.image.load("./assets/items/equipement/" + type_equipement + "/" + type_equipement + "_simple.png").convert_alpha()

    def __getitem__(self, item):
        return True

    def equipe_item(self):
        self.equipee = True

    def desequipe_item(self):
        self.equipee = False
