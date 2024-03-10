import pygame
import math
import random
import copy

from data import Image, Color, Sound

from src import sorts, inventory


class Personnage:

    def __init__(self, nom, classe):
        self.nom = nom
        self.id = random.randint(1, 10**100)
        self.classe = classe
        self.lvl = 1
        self.xp = 0
        self.xp_requis = 400  # xp requis pour le lvl suivant
        self.xp_requis_lvl_precedent = 400  # xp requis au lvl d'avant




        if self.classe == "Guerrier":
            self.PV_de_base = 150
            self.PV = 150
            self.spells = [
                sorts.Spell("Trancher", 150, 0.3, (150, 50))
            ]
            # Spell("Trancher", 4, Image.SPELL_TRANCHER_ICON, 0.3, (150, 50))
        elif self.classe == "Chasseur":
            self.PV_de_base = 137
            self.PV = 137
        elif self.classe == "Mage":
            self.PV_de_base = 124
            self.PV = 124





        self.armure = 0
        self.reduction_degats = 0
        self.force_de_base = 3000000000  # 3 by default
        self.force = self.force_de_base
        self.PV_max = self.PV
        #if classe == "Guerrier":

        self.orientation = "Face"
        self.x = 960
        self.y = 540
        self.rect = pygame.Rect(0, 0, 105, 217)
        self.rect.midbottom = (self.x, self.y)
        self.zone = "Desert"  # nom de la zone dans laquelle le joueur se trouve, par défaut, il est au spawn

        self.equipment = {
            "Casque": None,
            "Épaulières": None,
            "Cape": None,
            "Plastron": None,
            "Ceinture": None,
            "Gants": None,
            "Jambières": None,
            "Bottes": None,
            "Bague 1": None,
            "Bague 2": None,
            "Bijou 1": None,
            "Bijou 2": None
        }

        self.inventory = inventory.Inventory(8, 8)

        self.arme = None
        self.movement_speed = 7

        self.selected_mob = None

    def draw(self, surface):
        surface.blit(Image.CHARACTER_POSTURES[self.orientation], self.rect.topleft)
        # pygame.draw.rect(surface, "black", self.rect, 2)

        # circle reach of first spell of the character
        # pygame.draw.circle(surface, Color.BLACK, self.rect.center, self.spells[0].reach, 2)

    def update(self, game, zone):
        if not self.est_mort():
            key_pressed = pygame.key.get_pressed()
            deplacements_possibles = self.verifier_personnage_obstacles(zone.obstacles)
            if key_pressed[pygame.K_z]:
                if key_pressed[pygame.K_d]:
                    if "Haut" in deplacements_possibles and "Droite" in deplacements_possibles:
                        self.deplacement_haut_droite()
                elif key_pressed[pygame.K_q]:
                    if "Haut" in deplacements_possibles and "Gauche" in deplacements_possibles:
                        self.deplacement_haut_gauche()
                else:
                    if "Haut" in deplacements_possibles:
                        self.deplacement_haut()
                self.rect.midbottom = (self.x, self.y)
            elif key_pressed[pygame.K_s]:
                if key_pressed[pygame.K_q]:
                    if "Bas" in deplacements_possibles and "Gauche" in deplacements_possibles:
                        self.deplacement_bas_gauche()
                elif key_pressed[pygame.K_d]:
                    if "Bas" in deplacements_possibles and "Droite" in deplacements_possibles:
                        self.deplacement_bas_droite()
                else:
                    if "Bas" in deplacements_possibles:
                        self.deplacement_bas()
                self.rect.midbottom = (self.x, self.y)
            elif key_pressed[pygame.K_q]:
                if "Gauche" in deplacements_possibles:
                    self.deplacement_gauche()
                self.rect.midbottom = (self.x, self.y)
            elif key_pressed[pygame.K_d]:
                if "Droite" in deplacements_possibles:
                    self.deplacement_droite()
                self.rect.midbottom = (self.x, self.y)

    def handle_event(self, game, event):



        if event.type == pygame.MOUSEBUTTONUP:
            self.select_mob(game.zones[self.zone].get_all_mobs(), game.mouse_pos)

        # Character spells casting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if self.spells[0].ready(game.time):
                    Sound.SONS_ATTAQUE_PERSO[random.randint(0, len(Sound.SONS_ATTAQUE_PERSO) - 1)].play()
                    self.attaquer(game.zones[self.zone].get_all_mobs(), self.spells[0])
                    self.spells[0].set_timer(game.time)
                    # affiche_zone_effet_s1 = True
        #
        # # Si le personnage lance le sort 2
        # if event.key == pygame.K_2:
        #     if len(self.sorts) >= 2:
        #         if self.sorts[1].temps_restant_rechargement == 0:
        #             self.sons_attaque_perso[random.randint(0, len(self.sons_attaque_perso) - 1)].play()
        #             self.attaquer(mobs_zone, self.sorts[1])
        #             self.sorts[1].temps_restant_rechargement = self.sorts[1].temps_rechargement
        #             # affiche_zone_effet_s2 = True
        #             sort_lancer = "Tourbillon"
        #
        # # Si le joueur appuie sur 2, son perso est heal de 50 PV
        # if event.key == pygame.K_3:
        #     if self.PV <= self.PV_max - 50:
        #         self.PV += 50
        #     else:
        #         self.PV = self.PV_max
        #
        # # Si on ouvre l'inventaire avec 'i'
        # if event.key == pygame.K_i:
        #     # Permet d'alterner entre ouvert et fermer lorsqu'on appuie sur "i" pour ouvrir l'inventaire
        #     if dic_menu["Inventaire"] is False:
        #         dic_menu["Inventaire"] = True
        #     else:
        #         dic_menu["Inventaire"] = False
        #
        # # Si on ouvre le menu d'équipement du personnage avec 'c'
        # if event.key == pygame.K_c:
        #     if dic_menu["Personnage"] is False:
        #         dic_menu["Personnage"] = True
        #     else:
        #         dic_menu["Personnage"] = False
        #
        # # Si on appuie sur '←-' (Backspace), supprime l'object à l'emplacment cibler par la souris
        # if event.key == pygame.K_BACKSPACE:
        #     if dic_menu["Inventaire"]:
        #         for i in range(len(self.inventaire)):
        #             for j in range(len(self.inventaire[0])):
        #                 if 1417 + 52 * j < self.mouse_pos[0] < 1417 + 52 * j + 39 and 533 + 52 * i < \
        #                         self.mouse_pos[1] < 533 + 52 * i + 39:
        #                     self.inventaire[i][j] = None

    def select_mob(self, mobs_list, mouse_pos):
        mob_found = False
        for i in range(len(mobs_list)):
            if not mob_found:
                if mobs_list[i].rect.collidepoint(mouse_pos):
                    self.selected_mob = mobs_list[i]
                    self.selected_mob.selected = True
                    mob_found = True
                else:
                    mobs_list[i].selected = False
            else:
                mobs_list[i].selected = False

        if not mob_found:
            self.selected_mob = None

    def get_damage(self):
        total = 0
        if self.arme:
            total += self.arme.degat

        total += self.force

        return total

    def mise_a_jour_stats(self):
        """
        Met à jour les stats du joueur en fonction de l'équipement équipée
        """
        armure_total = 0
        PV_max_total = self.PV_de_base
        force_total = self.force_de_base

        if self.arme:
            PV_max_total += self.arme.bonus_PV
            force_total += self.arme.bonus_force
        for equipement in self.equipment.values():
            if equipement:
                armure_total += equipement.armure
                PV_max_total += equipement.bonus_PV
                force_total += equipement.bonus_force
        self.armure = armure_total
        if self.armure <= 500:
            self.reduction_degats = (self.armure / (self.armure + 1000))
        elif self.armure <= 10000:
            self.reduction_degats = (self.armure / ((self.armure + 1000) + (self.armure / 2)))
        else:
            self.reduction_degats = (self.armure / ((self.armure + 1000) + (self.armure / 4)))
        self.PV_max = PV_max_total
        self.force = force_total

        #Si les PV sont supérieur aux PV max, on change cela
        if self.PV > self.PV_max:
            self.PV = self.PV_max

    def equiper_object(self, equipement, i, j):
        """
        Equipe la pièce d'équipement passé en paramètre sur le stuff du personnage
        :return:
        """
        # si la case d'équipement est vide, on ajoute l'équipement
        if not self.equipment[equipement.type_equipement]:
            equipement.equipee = True
            self.equipment[equipement.type_equipement] = equipement
            self.equipment[i][j] = None
        # sinon on ajoute d'abord la pièce équipée à l'inventaire puis on rapelle la fonction vu que la case d'équipement est désormais libre
        else:
            self.desequiper_object(self.equipment[equipement.type_equipement])
            self.equiper_object(equipement, i, j)

    def equiper_arme(self, arme, i, j):
        """
        Equipe l'arme passé en paramètre sur le stuff du personnage
        :return:
        """
        # si la case d'arme est vide on équipe l'arme
        if not self.arme:
            arme.equipee = True
            self.arme = arme
            self.inventory[i][j] = None
        # sinon on ajoute d'abord la pièce équipée à l'inventaire puis on rapelle la fonction vu que la case d'équipement est désormais libre
        else:
            self.desequiper_arme(self.arme)
            self.equiper_arme(arme, i, j)

    def desequiper_arme(self, arme):
        """
        Déséquipe l'arme passé en paramètre du stuff du personnage
        :return:
        """
        if self.arme:
            self.inventory.add(self.arme)
            self.arme.equipee = False
            self.arme = None

    def desequiper_object(self, equipement):
        """
        Déséquipe la pièce d'équipement passé en paramètre du stuff du personnage
        :return:
        """
        if equipement in self.equipment.values():
            self.inventory.add(self.equipment[equipement.type_equipement])
            self.equipment[equipement.type_equipement].equipee = False
            self.equipment[equipement.type_equipement] = None

    def est_mort(self):
        """
        Renvoie True si le perso est mort False sinon.
        :return:
        """
        if self.PV <= 0:
            return True
        return False

    def lvl_up(self):
        self.lvl += 1
        force_gagne = round(self.force_de_base / 2)
        if force_gagne == 0:
            force_gagne = 1
        self.force_de_base += force_gagne
        self.PV_de_base += round(self.PV_de_base / 6)

        # updating xp
        self.xp -= self.xp_requis

        # augmentation de l'expérience requise pour le prochain lvl
        self.xp_requis += self.xp_requis_lvl_precedent
        if self.xp_requis != self.xp_requis_lvl_precedent:
            self.xp_requis_lvl_precedent = copy.copy(self.xp_requis) - self.xp_requis_lvl_precedent

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_requis:
            self.lvl_up()

    def deplacement_haut(self):
        self.orientation = "Dos"
        if self.y - self.rect.height > 5:
            self.y -= self.movement_speed

    def deplacement_gauche(self):
        self.orientation = "Gauche"
        if self.x - self.rect.width / 2 > 5:
            self.x -= self.movement_speed

    def deplacement_bas(self):
        self.orientation = "Face"
        if self.y < 1075:
            self.y += self.movement_speed

    def deplacement_droite(self):
        self.orientation = "Droite"
        if self.x + self.rect.width / 2 < 1915:
            self.x += self.movement_speed

    def deplacement_haut_gauche(self):
        self.orientation = "Gauche"
        if self.x - self.rect.width / 2 > 5 and self.y - self.rect.height > 5:

            self.y -= math.sqrt(2 * (self.movement_speed**2)) / 2
            self.x -= math.sqrt(2 * (self.movement_speed**2)) / 2

    def deplacement_haut_droite(self):
        self.orientation = "Droite"
        if self.x + self.rect.width / 2 < 1915 and self.y - self.rect.height > 5:
            self.y -= math.sqrt(2 * (self.movement_speed**2)) / 2
            self.x += math.sqrt(2 * (self.movement_speed**2)) / 2

    def deplacement_bas_gauche(self):
        self.orientation = "Gauche"
        if self.y < 1075 and self.x - self.rect.width / 2 > 5:
            self.y += math.sqrt(2 * (self.movement_speed**2)) / 2
            self.x -= math.sqrt(2 * (self.movement_speed**2)) / 2

    def deplacement_bas_droite(self):
        self.orientation = "Droite"
        if self.y < 1075 and self.x + self.rect.width / 2 < 1915:
            self.y += math.sqrt(2 * (self.movement_speed**2)) / 2
            self.x += math.sqrt(2 * (self.movement_speed**2)) / 2

    def verifier_personnage_obstacles(self, obstacles):
        """
        Prends une liste d'obstacles en paramètre et renvoie les directions possibles du personnage
        en prenants en compte ses obstacles.
        """
        directions_possibles = ["Gauche", "Droite", "Haut", "Bas"]

        hit_box_avec_deplacement_gauche = [self.x - self.movement_speed, self.y, self.rect.width + self.movement_speed, self.rect.height]
        hit_box_avec_deplacement_droite = [self.x, self.y, self.rect.width + self.movement_speed, self.rect.height]
        hit_box_avec_deplacement_haut = [self.x, self.y - self.movement_speed, self.rect.width, self.rect.height + self.movement_speed]
        hit_box_avec_deplacement_bas = [self.x, self.y, self.rect.width, self.rect.height + self.movement_speed]
        #hit_box_avec_deplacement = [self.x - self.vitesse_deplacement, self.y - self.vitesse_deplacement, self.hit_box[2] + self.vitesse_deplacement, self.hit_box[3] + self.vitesse_deplacement]
        for rect in obstacles:
            if rect.colliderect(hit_box_avec_deplacement_gauche):
                directions_possibles.remove("Gauche")
            if rect.colliderect(hit_box_avec_deplacement_droite):
                directions_possibles.remove("Droite")
            if rect.colliderect(hit_box_avec_deplacement_haut):
                directions_possibles.remove("Haut")
            if rect.colliderect(hit_box_avec_deplacement_bas):
                directions_possibles.remove("Bas")

        return directions_possibles

    def attaquer(self, mobs, sort, attaques_multiples=False):
        """

        :param mobs: liste de mobs
        :param sort: sort avec lequel il faut attaquer les mobs
        :param attaques_multiples: si le sort attaque en plusieurs les ennemis n'attaques qu'une fois
        :return:
        """
        if self.selected_mob:
            if sort.check_reach(self.rect.center, self.selected_mob.rect.center):
                self.selected_mob.take_damage(self, (self.get_damage() * sort.perc_char_dmg / 100))




        # for mob in mobs:
        #     mob_toucher = False
        #     rect_hit_box_mob = pygame.Rect(mob.hit_box)
        #     if sort.nom == "Trancher":
        #         if self.orientation == "Face":
        #             if rect_hit_box_mob.colliderect([self.x - 25, self.y + 220, sort.zone_effet[0], sort.zone_effet[1]]):
        #                 mob_toucher = True
        #         elif self.orientation == "Droite":
        #             if rect_hit_box_mob.colliderect([self.x + 110, self.y + 40, sort.zone_effet[1], sort.zone_effet[0]]):
        #                 mob_toucher = True
        #         elif self.orientation == "Gauche":
        #             if rect_hit_box_mob.colliderect([self.x - 45, self.y + 40, sort.zone_effet[1], sort.zone_effet[0]]):
        #                 mob_toucher = True
        #         elif self.orientation == "Dos":
        #             if rect_hit_box_mob.colliderect([self.x - 25, self.y - 60, sort.zone_effet[0], sort.zone_effet[1]]):
        #                 mob_toucher = True
        #     elif sort.nom == "Tourbillon":
        #         if rect_hit_box_mob.colliderect([self.x - 145, self.y - 50, sort.zone_effet[0], sort.zone_effet[1]]):
        #             mob_toucher = True
        #
        #     if mob_toucher:
        #         if self.arme:
        #             mob.PV -= (self.get_damage() * sort.perc_char_dmg / 100) + self.arme.degat
        #         else:
        #             mob.PV -= (self.get_damage() * sort.perc_char_dmg / 100)
        #
        #         if not attaques_multiples:
        #             self.PV -= mob.degat - (mob.degat * self.reduction_degats)  # Quand le joueur fait des dégâts à un mob il réplique immédiatement
        #             if self.PV < 0:
        #                 self.PV = 0
        #
        #         if mob.PV < 0:
        #             mob.PV = 0
