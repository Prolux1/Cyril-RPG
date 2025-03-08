from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

import pygame
import math
import random
import copy

from data import Image, Color, Sound
from src import sorts, inventory, items, utils, quetes
from config import WINDOW_WIDTH, WINDOW_HEIGHT


class Personnage:
    def __init__(self, rpg: "CyrilRpg", nom: str, classe: str):
        self.rpg = rpg
        self.monde = None
        self.nom = nom
        self.id = random.randint(1, 10**100)
        self.classe = classe
        self.lvl = 1
        self.xp = 0
        self.xp_requis = 400  # xp requis pour le lvl suivant
        self.xp_requis_lvl_precedent = 400  # xp requis au lvl d'avant
        self.xp_multiplier = 10


        if self.classe == "Guerrier":
            self.PV_de_base = 150
            self.PV = 150
            self.spells = [
                sorts.Spell("Cleave", 150, 0.5, "cleave", (150, 50))
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
        self.force_de_base = 25  # 3 by default
        self.force = self.force_de_base
        self.PV_max = self.PV
        #if classe == "Guerrier":

        self.orientation = "Face"
        self.etat = "Lidle"  # L'état dans lequel se trouve le personnage par exemple "Courir", s'il ne fait rien "Lidle"
        self.frame_courante = 0
        self.nb_frames_etats = {"Lidle": 5, "Courir": 8}
        self.vitesse_de_deplacement = 1
        self.temps_prochain_changement_frame = rpg.time + 1.7 / self.nb_frames_etats["Lidle"]

        self.rect = Image.GUERRIER_FRAMES["Lidle"][self.orientation].subsurface(
            (
                0,
                0,
                Image.GUERRIER_FRAMES["Lidle"][self.orientation].get_width() / self.nb_frames_etats["Lidle"],
                Image.GUERRIER_FRAMES["Lidle"][self.orientation].get_height()
            )
        ).get_rect()

        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2 + self.rect.height / 2
        self.rect.midbottom = (self.x, self.y)
        self.offset = pygame.Vector2(self.x - WINDOW_WIDTH / 2, self.y - (WINDOW_HEIGHT / 2 + self.rect.height / 2))
        self.zone = "Desert"  # nom de la zone dans laquelle le joueur se trouve, par défaut, il est dans le désert

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
            "Artifact": None
        }

        self.inventory = inventory.Inventory(8, 8)

        self.arme = None
        self.vitesse_de_deplacement_de_base = 7
        self.movement_speed = 7

        self.selected_mob = None

        self.passive_regen_timer = None

        self.journal_de_quetes: set[quetes.Quete] = set()  # Les quêtes actives du personnage
        self.quetes_terminees: set[quetes.Quete] = set()  # Les quêtes terminées par le personnage

    def draw(self, surface):
        # surface.blit(Image.CHARACTER_POSTURES[self.orientation], self.rect.topleft - self.offset)

        indice_frame = (self.frame_courante % self.nb_frames_etats[self.etat]) / self.nb_frames_etats[self.etat]
        rect_frame_courante = pygame.Rect(
            Image.GUERRIER_FRAMES[self.etat][self.orientation].get_width() * indice_frame,
            0,
            Image.GUERRIER_FRAMES[self.etat][self.orientation].get_width() / self.nb_frames_etats[self.etat],
            Image.GUERRIER_FRAMES[self.etat][self.orientation].get_height()
        )
        img_courante = Image.GUERRIER_FRAMES[self.etat][self.orientation].subsurface(rect_frame_courante)


        surface.blit(
            img_courante,
            self.rect.topleft - self.offset
        )

        # pygame.draw.rect(surface, Color.BLACK, pygame.Rect((self.rect.topleft - self.offset), self.rect.size), 2)
        # pygame.draw.rect(surface, Color.BLACK, self.rect, 2)
        # pygame.draw.rect(surface, Color.GREEN, pygame.Rect(self.x, self.y, 2, 2), 1)

        # circle reach of first spell of the character
        # pygame.draw.circle(surface, Color.BLACK, self.rect.center, self.spells[0].reach, 2)

    def update(self, game: "CyrilRpg", zone):
        self.update_stats()

        self.movement_speed = self.vitesse_de_deplacement_de_base * 60 / self.rpg.fps
        if not self.est_mort():
            key_pressed = pygame.key.get_pressed()
            deplacements_possibles = self.verifier_personnage_obstacles(zone.obstacles)
            self.etat = "Lidle"
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
                self.etat = "Courir"
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
                self.etat = "Courir"
            elif key_pressed[pygame.K_q]:
                if "Gauche" in deplacements_possibles:
                    self.deplacement_gauche()
                self.rect.midbottom = (self.x, self.y)
                self.etat = "Courir"
            elif key_pressed[pygame.K_d]:
                if "Droite" in deplacements_possibles:
                    self.deplacement_droite()
                self.rect.midbottom = (self.x, self.y)
                self.etat = "Courir"
            self.x, self.y = round(self.x), round(self.y)
            self.offset.update(self.x - WINDOW_WIDTH / 2, self.y - (WINDOW_HEIGHT / 2 + self.rect.height / 2))

            # if character is not dead we regen 1 % of its
            # max hp every 2 seconds

            if self.PV < self.PV_max:
                if self.passive_regen_timer is None:
                    self.passive_regen_timer = self.rpg.time + 2
                else:
                    if self.rpg.time >= self.passive_regen_timer:
                        self.regen()
                        self.passive_regen_timer = self.rpg.time + 2
            else:
                self.passive_regen_timer = None

        # On update la frame courante
        if self.rpg.time >= self.temps_prochain_changement_frame:
            self.frame_courante += 1

            temps_prochains_changements_frames = {
                "Lidle": 1.7,
                "Courir": 0.7 / self.vitesse_de_deplacement
            }
            self.temps_prochain_changement_frame = self.rpg.time + (temps_prochains_changements_frames[self.etat] / self.nb_frames_etats[self.etat])

    def handle_event(self, game: "CyrilRpg", event: pygame.event.Event):
        if not self.est_mort():
            if event.type == pygame.MOUSEBUTTONUP:
                self.select_pnj(self.monde.get_pnjs_zone_courante(), self.rpg.mouse_pos)

            # Character spells casting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if self.spells[0].ready(self.rpg.time):
                        Sound.SONS_ATTAQUE_PERSO[random.randint(0, len(Sound.SONS_ATTAQUE_PERSO) - 1)].play()
                        self.attaquer(self.monde.get_pnjs_attaquables_zone_courante(), self.spells[0])
                        self.spells[0].set_timer(self.rpg.time)
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
        # # Si on appuie sur '←-' (Backspace), supprime l'objet à l'emplacement ciblé par la souris
        # if event.key == pygame.K_BACKSPACE:
        #     if dic_menu["Inventaire"]:
        #         for i in range(len(self.inventaire)):
        #             for j in range(len(self.inventaire[0])):
        #                 if 1417 + 52 * j < self.mouse_pos[0] < 1417 + 52 * j + 39 and 533 + 52 * i < \
        #                         self.mouse_pos[1] < 533 + 52 * i + 39:
        #                     self.inventaire[i][j] = None

    def select_pnj(self, mobs_list, mouse_pos):
        mob_found = False
        for i in range(len(mobs_list)):
            if not mob_found:
                if pygame.Rect(mobs_list[i].rect.topleft - self.offset, mobs_list[i].rect.size).collidepoint(mouse_pos):
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
        return self.arme.damage + self.force if self.arme is not None else self.force

    def update_stats(self):
        """
        Met à jour les stats du joueur en fonction de l'équipement équipée
        """
        armure_total = 0
        pv_max_total = self.PV_de_base
        force_total = self.force_de_base

        if self.arme:
            pv_max_total += self.arme.bonus_hp
            force_total += self.arme.bonus_strength
        for eq in self.equipment.values():
            if eq:
                armure_total += eq.armor
                pv_max_total += eq.bonus_hp
                force_total += eq.bonus_strength
        self.armure = armure_total
        if self.armure <= 500:
            self.reduction_degats = (self.armure / (self.armure + 1000))
        elif self.armure <= 10000:
            self.reduction_degats = (self.armure / ((self.armure + 1000) + (self.armure / 2)))
        else:
            self.reduction_degats = (self.armure / ((self.armure + 1000) + (self.armure / 4)))
        self.PV_max = pv_max_total
        self.force = force_total

        # Si les PV ne peuvent pas dépassé les PV max
        self.PV = min(self.PV, self.PV_max)

    def equip(self, equipment_piece):
        if isinstance(equipment_piece, items.Weapon):
            # si la case d'arme est vide, on équipe l'arme
            if not self.arme:
                self.arme = equipment_piece
            # sinon, on ajoute d'abord la pièce équipée à l'inventaire puis
            # on rappelle la fonction vu que la case d'équipement est désormais libre
            else:
                self.unequip(self.arme)
                self.equip(equipment_piece)
        elif isinstance(equipment_piece, items.Armor):
            # same for armor
            if not self.equipment[equipment_piece.type]:
                self.equipment[equipment_piece.type] = equipment_piece
            else:
                self.unequip(self.equipment[equipment_piece.type])
                self.equip(equipment_piece)
            Sound.EQUIPER_ARMURE_LOURDE.play()

    def unequip(self, equipment_piece):
        if isinstance(equipment_piece, items.Weapon):
            if self.arme:
                self.inventory.add(self.arme)
                self.arme = None
        elif isinstance(equipment_piece, items.Armor):
            if equipment_piece in self.equipment.values():
                self.inventory.add(self.equipment[equipment_piece.type])
                self.equipment[equipment_piece.type] = None

    def ajouter_item_inventaire(self, item: items.Item) -> bool:
        """
        Renvoie True si l'item à pu être ajouter à l'inventaire, False sinon si l'inventaire est plein.
        """
        res = False
        if not self.inventory.is_full():
            self.inventory.add(item)
            res = True
        return res

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
        self.force_de_base += utils.fibo(self.lvl)
        self.PV_de_base += round(self.PV_de_base / 6)

        # updating xp
        self.xp -= self.xp_requis

        # augmentation de l'expérience requise pour le prochain lvl
        self.xp_requis += self.xp_requis_lvl_precedent
        if self.xp_requis != self.xp_requis_lvl_precedent:
            self.xp_requis_lvl_precedent = copy.copy(self.xp_requis) - self.xp_requis_lvl_precedent

    def gain_xp(self, amount):
        self.xp += amount
        has_lvl_up = False
        while self.xp >= self.xp_requis:
            self.lvl_up()
            has_lvl_up = True

        if has_lvl_up:
            Sound.SON_LEVEL_UP.play()

        # temps_affiche_level_up = self.temps.__round__()
        # if self.lvl == 10:
        #     self.spells.append(sorts.Sort("Tourbillon", 3, pygame.image.load(
        #         "./assets/logos_sorts/sort2_guerrier.png").convert_alpha(), 10, (395, 300)))

    def deplacement_haut(self):
        self.orientation = "Dos"
        self.y -= self.movement_speed

    def deplacement_gauche(self):
        self.orientation = "Gauche"
        self.x -= self.movement_speed

    def deplacement_bas(self):
        self.orientation = "Face"
        self.y += self.movement_speed

    def deplacement_droite(self):
        self.orientation = "Droite"
        self.x += self.movement_speed

    def deplacement_haut_gauche(self):
        self.orientation = "Gauche"
        self.y -= math.sqrt(2 * (self.movement_speed**2)) / 2
        self.x -= math.sqrt(2 * (self.movement_speed**2)) / 2

    def deplacement_haut_droite(self):
        self.orientation = "Droite"
        self.y -= math.sqrt(2 * (self.movement_speed**2)) / 2
        self.x += math.sqrt(2 * (self.movement_speed**2)) / 2

    def deplacement_bas_gauche(self):
        self.orientation = "Gauche"
        self.y += math.sqrt(2 * (self.movement_speed**2)) / 2
        self.x -= math.sqrt(2 * (self.movement_speed**2)) / 2

    def deplacement_bas_droite(self):
        self.orientation = "Droite"
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

    def receive_damage(self, amount: int):
        if self.PV - amount < 0:
            self.PV = 0
        else:
            self.PV -= round(amount * (1 - self.reduction_degats))

    def regen(self):
        # Regen 1 % of the max hp of the character
        if self.PV + self.PV_max / 100 < self.PV_max:
            self.PV += self.PV_max / 100
            self.PV = round(self.PV)
        else:
            self.PV = self.PV_max

    def respawn(self):
        self.PV = 1

    def attaquer(self, mobs, sort, attaques_multiples=False):
        """
        Attaque le mob sélectionné

        :param mobs: liste de pnjs
        :param sort: sort avec lequel il faut attaquer les pnjs
        :param attaques_multiples: si le sort attaque en plusieurs les ennemis n'attaques qu'une fois
        :return:
        """
        if self.selected_mob is not None:
            if self.selected_mob.est_attaquable() and not self.selected_mob.est_mort():
                if sort.check_reach(self.rect.center, self.selected_mob.rect.center):
                    self.selected_mob.prendre_cher(self, round(self.get_damage() * sort.perc_char_dmg / 100))

    def est_quete_terminee(self, quete: quetes.Quete) -> bool:
        return quete in self.quetes_terminees

    def est_quete_active(self, quete: quetes.Quete) -> bool:
        return quete in self.journal_de_quetes

    def peut_quete_etre_terminee(self, quete: quetes.Quete) -> bool:
        return self.est_quete_active(quete) and quete.peut_etre_terminee()

    def accepter_quete(self, quete: quetes.Quete) -> bool:
        """
        Peut renvoyer False si le journal de quetes est plein (pour l'instant pas de limite, c'est pas comme ci
        y alait avoir 500 000 quetes mdrrr)
        """
        self.journal_de_quetes.add(quete)
        return True

    def abandonner_quete(self, quete: quetes.Quete) -> None:
        quete.abandonner()
        self.journal_de_quetes.remove(quete)

    def terminer_quete(self, quete: quetes.Quete) -> None:
        self.quetes_terminees.add(quete)
        self.journal_de_quetes.remove(quete)

    def get_quetes_actives_tuer_pnjs(self, toutes: bool = False) -> list[quetes.QueteTuerPnjs]:
        """
        Renvoie par défaut toutes les quetes actives dans le journal de quêtes où il faut tuer des pnjs ET dont les
        objectifs ne sont pas encore remplit.
        On peut décider de renvoyer également celles dont les objectifs sont remplis en mettant le paramètre "toutes" à True.
        """
        return [quete for quete in self.journal_de_quetes if isinstance(quete, quetes.QueteTuerPnjs) and (not quete.peut_etre_terminee() or toutes)]


