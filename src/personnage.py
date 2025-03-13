from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

import pygame
import math
import random
import copy

from data import Image, Color, Sound
from src import sorts, inventory, items, utils, quetes, pnjs
from config import WINDOW_WIDTH, WINDOW_HEIGHT


class Personnage:
    def __init__(self, rpg: "CyrilRpg", nom: str, classe: str):
        self.rpg = rpg
        self.monde = None  # est affecté dès que le Monde est instancié
        self.nom = nom
        self.id = random.randint(1, 10**100)
        self.classe = classe
        self.lvl = 1
        self.xp = 0
        self.xp_requis = 400  # xp requis pour le lvl suivant
        self.xp_requis_lvl_precedent = 400  # xp requis au lvl d'avant
        self.xp_multiplier = 10

        # TODO : implémenter d'autres classes (Chasseur, Mage, ...)
        pvs_classes = {
            "Guerrier": 150,  # 150
            "Chasseur": 137,
            "Mage": 124
        }

        sorts_classes = {
            "Guerrier": [
                sorts.Spell("Cleave", 150, 0.5, "cleave", (150, 50))
                # Spell("Trancher", 4, Image.SPELL_TRANCHER_ICON, 0.3, (150, 50))
            ],
            "Chasseur": [],
            "Mage": []
        }

        self.PV = pvs_classes[self.classe]
        self.PV_de_base = self.PV

        self.spells = sorts_classes[self.classe]


        self.armure = 0
        self.reduction_degats = 0
        self.force_de_base = 25  # 3 by default
        self.force = self.force_de_base
        self.PV_max = self.PV
        #if classe == "Guerrier":

        self.orientation = "Face"
        self.etat = "Lidle"  # L'état dans lequel se trouve le personnage par exemple "Courir", s'il ne fait rien "Lidle"
        self.frame_courante = 0
        self.nb_frames_etats = {"Lidle": 5, "Courir": 8, "Attaquer1": 6, "Attaquer2": 6, "Attaquer3": 5}
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
        self.nom_zone_courante = "Desert"  # nom de la zone dans laquelle le joueur se trouve, par défaut, il est dans le désert

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
        self.hovered_pnj = None

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

        # pygame.draw.rect(surface, Color.GREEN, pygame.Rect((self.rect.topleft - self.offset), self.rect.size), 2)
        # pygame.draw.rect(surface, Color.BLACK, self.rect, 2)
        # pygame.draw.rect(surface, Color.BLACK, pygame.Rect(self.x, self.y, 2, 2), 1)

        # circle reach of first spell of the character
        # pygame.draw.circle(surface, Color.BLACK, self.rect.center, self.spells[0].reach, 2)

    def update(self, game: "CyrilRpg", zone):
        self.update_stats()

        # Ajouter masse équipement à l'inventaire pour tests
        # if int(str(game.time).split('.')[1]) % 2 == 0:
        #     if random.random() < 0.2:
        #         self.ajouter_item_inventaire(utils.generation_arme_alea(random.randint(1, 100)))
        #     else:
        #         self.ajouter_item_inventaire(utils.generation_equipement_alea(random.randint(1, 100)))

        self.movement_speed = self.vitesse_de_deplacement_de_base * 60 / self.rpg.fps
        if not self.est_mort():
            # On met à jours l'état, l'orientation, la position et l'offset du personnage s'il se déplace
            self.maj_deplacements()

            # si le personnage n'est pas mort, on regen 1 % de ses PVs max toutes les 2 secondes
            if self.PV < self.PV_max:
                if self.passive_regen_timer is None:
                    self.passive_regen_timer = self.rpg.time + 2
                else:
                    if self.rpg.time >= self.passive_regen_timer:
                        self.regen()
                        self.passive_regen_timer = self.rpg.time + 2
            else:
                self.passive_regen_timer = None

            self.hovered_pnj = self.chercher_hovered_pnj()

        # On anime le personnage
        self.animation()

    def handle_event(self, game: "CyrilRpg", event: pygame.event.Event):
        if not self.est_mort():
            if event.type == pygame.MOUSEBUTTONUP:
                if self.hovered_pnj is not None:
                    self.selected_mob = self.hovered_pnj

            # Character spells casting
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if self.spells[0].ready(self.rpg.time):
                        Sound.SONS_ATTAQUE_PERSO[random.randint(0, len(Sound.SONS_ATTAQUE_PERSO) - 1)].play()
                        self.attaquer(self.monde.get_pnjs_attaquables_zone_courante(), self.spells[0])
                        self.spells[0].set_timer(self.rpg.time)

                        # affiche_zone_effet_s1 = True

                # Pour heal le perso instant à des fins de tests (en appuyant sur 'H')
                if event.key == pygame.K_h:
                    self.PV = self.PV_max
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
        # # Si on appuie sur '←-' (Backspace), supprime l'objet à l'emplacement ciblé par la souris
        # if event.key == pygame.K_BACKSPACE:
        #     if dic_menu["Inventaire"]:
        #         for i in range(len(self.inventaire)):
        #             for j in range(len(self.inventaire[0])):
        #                 if 1417 + 52 * j < self.mouse_pos[0] < 1417 + 52 * j + 39 and 533 + 52 * i < \
        #                         self.mouse_pos[1] < 533 + 52 * i + 39:
        #                     self.inventaire[i][j] = None

    def chercher_hovered_pnj(self) -> pnjs.Pnj | None:
        hovered_pnj = None

        pnjs_en_y = sorted(self.monde.get_pnjs_zone_courante(), key=lambda entite_i: entite_i.y, reverse=True)

        i = 0
        while not hovered_pnj and i < len(pnjs_en_y):
            if pnjs_en_y[i].hovered_by_mouse:
                hovered_pnj = pnjs_en_y[i]
            i += 1
        return hovered_pnj

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

    def equiper(self, piece_equipement: items.Equipment):
        if isinstance(piece_equipement, items.Weapon):
            # si la case d'arme est vide, on équipe l'arme
            if not self.arme:
                self.arme = piece_equipement
            # sinon, on ajoute d'abord la pièce équipée à l'inventaire puis
            # on rappelle la fonction vu que la case d'équipement est désormais libre
            else:
                self.unequip(self.arme)
                self.equiper(piece_equipement)
        elif isinstance(piece_equipement, items.Armor):
            # same for armor
            if not self.equipment[piece_equipement.type]:
                self.equipment[piece_equipement.type] = piece_equipement
            else:
                self.unequip(self.equipment[piece_equipement.type])
                self.equiper(piece_equipement)
            Sound.EQUIPER_ARMURE_LOURDE.play()

    def unequip(self, equipment_piece):
        if not self.inventory.is_full():
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
        return self.PV <= 0

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

    def maj_deplacements(self):
        touches_pressees = pygame.key.get_pressed()
        deplacements_possibles = self.get_deplacements_possibles(self.monde.get_obstacles_zone_courante())

        if touches_pressees[pygame.K_z] and touches_pressees[pygame.K_d]:
            if "Haut" in deplacements_possibles and "Droite" in deplacements_possibles:
                self.orientation = "Droite"
                self.y -= math.sqrt(2 * (self.movement_speed ** 2)) / 2
                self.x += math.sqrt(2 * (self.movement_speed ** 2)) / 2
        elif touches_pressees[pygame.K_z] and touches_pressees[pygame.K_q]:
            if "Haut" in deplacements_possibles and "Gauche" in deplacements_possibles:
                self.orientation = "Gauche"
                self.y -= math.sqrt(2 * (self.movement_speed ** 2)) / 2
                self.x -= math.sqrt(2 * (self.movement_speed ** 2)) / 2
        elif touches_pressees[pygame.K_s] and touches_pressees[pygame.K_q]:
            if "Bas" in deplacements_possibles and "Gauche" in deplacements_possibles:
                self.orientation = "Gauche"
                self.y += math.sqrt(2 * (self.movement_speed ** 2)) / 2
                self.x -= math.sqrt(2 * (self.movement_speed ** 2)) / 2
        elif touches_pressees[pygame.K_s] and touches_pressees[pygame.K_d]:
            if "Bas" in deplacements_possibles and "Droite" in deplacements_possibles:
                self.orientation = "Droite"
                self.y += math.sqrt(2 * (self.movement_speed ** 2)) / 2
                self.x += math.sqrt(2 * (self.movement_speed ** 2)) / 2
        elif touches_pressees[pygame.K_z]:
            if "Haut" in deplacements_possibles:
                self.orientation = "Dos"
                self.y -= self.movement_speed
        elif touches_pressees[pygame.K_s]:
            if "Bas" in deplacements_possibles:
                self.orientation = "Face"
                self.y += self.movement_speed
        elif touches_pressees[pygame.K_q]:
            if "Gauche" in deplacements_possibles:
                self.orientation = "Gauche"
                self.x -= self.movement_speed
        elif touches_pressees[pygame.K_d]:
            if "Droite" in deplacements_possibles:
                self.orientation = "Droite"
                self.x += self.movement_speed
        else:
            # Si on ne se déplace pas on Lidle et on return, ça nous évite de mettre self.etat = "Courir" dans chaque if
            if not self.etat.startswith("Attaquer") and not self.etat == "Lidle":
                self.changer_etat("Lidle")
            return

        self.rect.midbottom = (self.x, self.y)
        if not self.etat.startswith("Attaquer") and not self.etat == "Courir":
            self.changer_etat("Courir")

        self.x, self.y = round(self.x), round(self.y)
        self.offset.update(self.x - WINDOW_WIDTH / 2, self.y - (WINDOW_HEIGHT / 2 + self.rect.height / 2))

    def get_deplacements_possibles(self, rects_obstacles: list[pygame.Rect]):
        """
        Prends une liste de rects correspondants aux obstacles passé en paramètre et renvoie les directions possibles
        du personnage en prenant en compte ces obstacles.
        """
        directions_possibles = ["Gauche", "Droite", "Haut", "Bas"]

        hits_boxs_avec_deplacement = {
            "Gauche": pygame.Rect(self.x - self.movement_speed, self.y, self.rect.width + self.movement_speed, self.rect.height),
            "Droite": pygame.Rect(self.x, self.y, self.rect.width + self.movement_speed, self.rect.height),
            "Haut": pygame.Rect(self.x, self.y - self.movement_speed, self.rect.width, self.rect.height + self.movement_speed),
            "Bas": pygame.Rect(self.x, self.y, self.rect.width, self.rect.height + self.movement_speed)
        }

        # hit_box_avec_deplacement = [self.x - self.vitesse_deplacement, self.y - self.vitesse_deplacement, self.hit_box[2] + self.vitesse_deplacement, self.hit_box[3] + self.vitesse_deplacement]
        for rect in rects_obstacles:
            for direction in hits_boxs_avec_deplacement:
                if rect.colliderect(hits_boxs_avec_deplacement[direction]):
                    directions_possibles.remove(direction)

        return directions_possibles

    def changer_etat(self, nouvelle_etat: str) -> None:
        self.etat = nouvelle_etat
        self.temps_prochain_changement_frame = 0
        self.frame_courante = 0

    def animation(self):
        if self.rpg.time >= self.temps_prochain_changement_frame:
            nb_frames_etat_courant = self.nb_frames_etats[self.etat]

            if not self.etat.startswith("Attaquer") or self.frame_courante != nb_frames_etat_courant - 1:

                self.frame_courante += 1

                temps_prochains_changements_frames = {
                    "Lidle": 1.7,
                    "Courir": 0.7 / self.vitesse_de_deplacement,
                    "Attaquer1": 0.7,
                    "Attaquer2": 0.7,
                    "Attaquer3": 0.7,
                }
                self.temps_prochain_changement_frame = self.rpg.time + (temps_prochains_changements_frames[self.etat] / self.nb_frames_etats[self.etat])
            else:
                # On a afficher toutes les frames de l'attaque
                self.changer_etat("Lidle")

    def receive_damage(self, degats: int):
        degats_reels = round(degats * (1 - self.reduction_degats))
        self.PV = max(0, self.PV - degats_reels)

    def regen(self):
        # Regen 1 % des hps max du personnage
        self.PV = min(self.PV_max, round(self.PV + self.PV_max / 100))

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
                    self.changer_etat("Attaquer1")

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


