from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

import pygame

from data import Font, Color, Image
from src import interfaceClasses, utils, personnage, monde, pnjs, quetes, items
from config import WINDOW_WIDTH, WINDOW_HEIGHT


class FpsViewer(interfaceClasses.Label):
    def __init__(self, fps: float, x, y):
        super().__init__(str(round(fps)), Font.ARIAL_30, Color.BLACK, x, y)

    def update(self, game):
        self.update_text(str(round(game.clock.get_fps())))
        self.rect.topright = (self.x, self.y)


class PlayButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.character_selection_menu()


class SettingsButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.settings_menu()


class QuitButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.quit()


class CharacterSelectionButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, character, text_font, text_color, center=True):
        self.character = character
        super().__init__(img, x, y, self.character.nom, text_font, text_color, center)


    def get_clicked(self, game):
        game.entrer_dans_le_monde(self.character)



class CharacterCreationButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.character_creation_menu()


class CharacterNameInput(interfaceClasses.InputField):
    def __init__(self, jeu, x, y, text_font, text_color, border_color=Color.BLACK, border_radius=2, center=True):
        super().__init__(jeu, x, y, text_font, text_color, border_color, border_radius, center)


class CharacterXpBar(interfaceClasses.BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=True):
        self.empty_surface = pygame.Surface((400, 35), pygame.SRCALPHA)
        super().__init__(x, y, self.empty_surface.copy(), center)
        self.character = character

        self.char_xp_text = interfaceClasses.Label(
            utils.convert_number(self.character.xp) + " / " + utils.convert_number(self.character.xp_requis),
            text_font,
            text_color,
            self.rect.width / 2,
            self.rect.height / 2,
            True
        )

        pygame.draw.rect(self.surface, Color.PURPLE, pygame.Rect(0, 0, self.surface.get_width() * (self.character.xp / self.character.xp_requis), self.surface.get_height()))

        pygame.draw.rect(self.surface, Color.GREY_LIGHTEN, self.surface.get_rect(), 2)

        self.char_xp_text.draw(self.surface)

    def update(self, game):
        self.char_xp_text.update_text(utils.convert_number(self.character.xp) + " / " + utils.convert_number(self.character.xp_requis))

        updated_surf = self.empty_surface.copy()
        pygame.draw.rect(updated_surf, Color.PURPLE, pygame.Rect(0, 0, updated_surf.get_width() * (self.character.xp / self.character.xp_requis), updated_surf.get_height()))
        pygame.draw.rect(updated_surf, Color.GREY_LIGHTEN, updated_surf.get_rect(), 2)
        self.char_xp_text.draw(updated_surf)

        self.update_surf(updated_surf)


class CharacterSpells(interfaceClasses.BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=True):
        self.character = character
        self.text_font = text_font
        self.text_color = text_color
        self.origin_surf = pygame.Surface((800, 54), pygame.SRCALPHA)
        super().__init__(x, y, self.origin_surf.copy(), center)
        pygame.draw.rect(self.surface, Color.BLACK, self.surface.get_rect(), 2)

        self.spell_info_surf = None
        self.spell_info_surf_rect = None

    def draw(self, surface):
        surface.blit(self.surface, self.rect.topleft)
        if self.spell_info_surf:
            surface.blit(self.spell_info_surf, self.spell_info_surf_rect.topleft)

    def update(self, game):
        updated_surf = self.origin_surf.copy()

        pygame.draw.rect(updated_surf, Color.BLACK, updated_surf.get_rect(), 2)

        spell_info = None

        total_width_taken = 0
        for i, s in enumerate(self.character.spells):
            spell_icon_rect = Image.SPELL_ICONS[s.icon_name].get_rect()
            spell_icon_rect.x = 2 + total_width_taken
            spell_icon_rect.y = updated_surf.get_height() / 2 - spell_icon_rect.height / 2
            updated_surf.blit(Image.SPELL_ICONS[s.icon_name], (spell_icon_rect.x, spell_icon_rect.y))

            # The spell of index i is casted using the i+1 keyboard key, we indicate this
            spell_key_surf = self.text_font.render(str(i+1), True, self.text_color)
            updated_surf.blit(spell_key_surf, (spell_icon_rect.x + spell_icon_rect.width - spell_key_surf.get_width(), spell_icon_rect.y + spell_icon_rect.height - spell_key_surf.get_height()))

            # If the spell is reloading, displays the remaining
            # time before the spell can be cast again
            if not s.ready(game.time):
                spell_time_remaining = s.last_time_used + s.temps_rechargement - game.time
                spell_time_remaining_surf = self.text_font.render(str(round(spell_time_remaining, 1)), True, Color.RED)
                updated_surf.blit(spell_time_remaining_surf, (spell_icon_rect.centerx - spell_time_remaining_surf.get_width() / 2, spell_icon_rect.centery - spell_time_remaining_surf.get_height() / 2))


            # if mouse hovers the spell, display information about it
            if spell_info is None:
                spell_icon_real_rect = pygame.Rect(self.rect.x + spell_icon_rect.x, self.rect.y + spell_icon_rect.y, spell_icon_rect.width, spell_icon_rect.height)
                if spell_icon_real_rect.collidepoint(game.mouse_pos):
                    spell_info = s

            total_width_taken += Image.SPELL_ICONS[s.icon_name].get_width()

        if spell_info:
            spell_info_surf = Image.TABLEAU_DESCRIPTION_ITEM.copy()
            spell_info_surf_rect = spell_info_surf.get_rect()

            spell_info_surf.blit(utils.text_surface(
                spell_info.nom + " inflicts "
                + utils.convert_number(round(self.character.get_damage() * spell_info.perc_char_dmg / 100))
                + " damage to the enemy",
                self.text_font,
                self.text_color,
                spell_info_surf_rect.width - 10
            ), (5, 0))

            spell_info_surf_rect.topleft = (game.mouse_pos[0] + 12, game.mouse_pos[1] + 12)

            spell_info_surf_rect.right = min(spell_info_surf_rect.right, game.window.get_width())
            spell_info_surf_rect.bottom = min(spell_info_surf_rect.bottom, game.window.get_height())

            self.spell_info_surf = spell_info_surf
            self.spell_info_surf_rect = spell_info_surf_rect
        else:
            self.spell_info_surf, self.spell_info_surf_rect = None, None

        self.update_surf(updated_surf)


    def handle_event(self, game, event):
        pass



class BoutonAccepterQuete(interfaceClasses.Button):
    def __init__(self, menu_interactions_pnj: "InteractionsPnj", x: int, y: int):
        self.menu_interactions_pnj = menu_interactions_pnj
        super().__init__(x, y, "Accepter", Font.ARIAL_23, Color.WHITE, 2)

        self.rect.move_ip(self.menu_interactions_pnj.rect.x, -self.rect.h + self.menu_interactions_pnj.rect.y)

    def get_clicked(self, game):
        self.menu_interactions_pnj.personnage.accepter_quete(self.menu_interactions_pnj.interaction_selectionnee)
        self.menu_interactions_pnj.retour_liste_interactions()

    def draw(self, surface, dx: int = 0, dy: int = 0):
        # Il faut bouger le rectangle du bouton en fonction de quand on l'affiche dans le menu d'interactions des pnjs
        # et quand on veut gérer "handle_event" et les "update" par rapport à la surface de la fenêtre principale.
        super().draw(surface, -self.menu_interactions_pnj.rect.x, -self.menu_interactions_pnj.rect.y)


class BoutonAbandonnerQuete(interfaceClasses.Button):
    def __init__(self, menu_interactions_pnj: "InteractionsPnj", x: int, y: int):
        self.menu_interactions_pnj = menu_interactions_pnj
        super().__init__(x, y, "Abandonner", Font.ARIAL_23, Color.WHITE, 2)

        self.rect.move_ip(self.menu_interactions_pnj.rect.x, -self.rect.h + self.menu_interactions_pnj.rect.y)

    def get_clicked(self, game):
        self.menu_interactions_pnj.personnage.abandonner_quete(self.menu_interactions_pnj.interaction_selectionnee)
        self.menu_interactions_pnj.retour_liste_interactions()

    def draw(self, surface, dx: int = 0, dy: int = 0):
        # Il faut bouger le rectangle du bouton en fonction de quand on l'affiche dans le menu d'interactions des pnjs
        # et quand on veut gérer "handle_event" et les "update" par rapport à la surface de la fenêtre principale.
        super().draw(surface, -self.menu_interactions_pnj.rect.x, -self.menu_interactions_pnj.rect.y)


class BoutonTerminerQuete(interfaceClasses.Button):
    def __init__(self, menu_interactions_pnj: "InteractionsPnj", x: int, y: int):
        self.menu_interactions_pnj = menu_interactions_pnj
        super().__init__(x, y, "Terminer", Font.ARIAL_23, Color.WHITE, 2)

        self.rect.move_ip(self.menu_interactions_pnj.rect.x, -self.rect.h + self.menu_interactions_pnj.rect.y)

    def get_clicked(self, game):
        self.menu_interactions_pnj.personnage.terminer_quete(self.menu_interactions_pnj.interaction_selectionnee)
        self.menu_interactions_pnj.retour_liste_interactions()

    def draw(self, surface, dx: int = 0, dy: int = 0):
        # Il faut bouger le rectangle du bouton en fonction de quand on l'affiche dans le menu d'interactions des pnjs
        # et quand on veut gérer "handle_event" et les "update" par rapport à la surface de la fenêtre principale.
        super().draw(surface, -self.menu_interactions_pnj.rect.x, -self.menu_interactions_pnj.rect.y)


class InteractionsPnj(interfaceClasses.BasicInterfaceElement):
    def __init__(self, perso: personnage.Personnage, m: monde.Monde, x, y):
        self.personnage = perso
        self.monde = m

        # self.pnj_selectionnee gère le pnj avec qui on est entrain d'intéragir mais c'est aussi avec lui qu'on va
        # savoir si on affiche des trucs ou pas. Par exemple s'il est à None, on va pas afficher le menu d'interactions
        # sinon on va l'afficher avec les interactions qu'il a (ses quetes, ses dialogues, etc...)
        self.pnj_selectionnee = None

        # liste de tuples du style (interaction, rect_interaction)
        # qui va contenir pour chaque intéractions son rectangle associé pour qu'on puisse cliqué et affiché le contenu de l'intéraction
        self.pnj_selectionnee_tuple_interactions_rects = []

        # L'intéraction sélectionnée par le joueur
        self.interaction_selectionnee = None

        largeur_origin_surface, hauteur_origin_surface = (400, 800)
        self.origin_surface = pygame.Surface((largeur_origin_surface, hauteur_origin_surface))
        self.origin_surface.fill(Color.FOND_INTERACTIONS)


        super().__init__(x, y, self.origin_surface.copy(), center=True)


        # Un rectangle qui défini la zone (en haut à droite du menu d'intéractions) qui permet de fermer le menu d'intéractions
        # Le rectangle avec "dans_surf" à la fin est utilisé pour le dessiner plus facilement dans la surface tandis
        # que l'autre est utilisé pour les collisions.
        self.rect_fermeture_menu_dans_surf = pygame.Rect(largeur_origin_surface - 30, 0, 30, 30)
        self.rect_fermeture_menu = self.rect_fermeture_menu_dans_surf.copy().move(self.rect.x, self.rect.y)

        # Un rectangle qui défini la zone (en bas à gauche du menu d'intéractions) qui permet d'accepter une quete
        self.rect_accepter_quete_dans_surf = pygame.Rect(0, hauteur_origin_surface - 30, 100, 30)
        self.rect_accepter_quete = self.rect_accepter_quete_dans_surf.copy().move(self.rect.x, self.rect.y)

        self.bouton_accepter_quete = BoutonAccepterQuete(self, 0, hauteur_origin_surface)
        self.bouton_abandonner_quete = BoutonAbandonnerQuete(self, 0, hauteur_origin_surface)
        self.bouton_terminer_quete = BoutonTerminerQuete(self, 0, hauteur_origin_surface)

    def draw(self, surface):
        new_surf = self.origin_surface.copy()

        # Les trucs communs à afficher si on est entrain de consulter les intéractions d'un pnj ou si on est sur
        # une d'entre elle (typiquement le bouton pour tout fermer)
        if self.pnj_selectionnee is not None:
            # Dessine le fond du bouton pour tout fermer
            pygame.draw.rect(new_surf, Color.RED, self.rect_fermeture_menu_dans_surf)

            # TODO : Dessiner une croix en plus

            # Dessine le contour du bouton pour tout fermer
            pygame.draw.rect(new_surf, Color.BLACK, self.rect_fermeture_menu_dans_surf, 2)


        if self.interaction_selectionnee is not None:


            if isinstance(self.interaction_selectionnee, quetes.Quete):
                espacement_titre = 10
                espacement_cote_droit = espacement_titre
                x_courant = espacement_titre
                y_courant = espacement_titre

                texte_nom_quete = Font.NOM_QUETE.render(self.interaction_selectionnee.nom, True, Color.BLACK)
                new_surf.blit(texte_nom_quete, (x_courant, y_courant))
                y_courant += texte_nom_quete.get_height() + espacement_titre

                # Affichage de la description de la quete en fonction de si :
                #   - elle n'a pas encore été accepté
                #   - elle est active mais les objectifs ne sont pas encore remplis
                #   - elle est active et les objectifs ont été remplis
                if self.personnage.peut_quete_etre_terminee(self.interaction_selectionnee):  # si la quete peut etre terminée c'est à dire si tout les objectifs ont été remplis
                    texte_description_quete = utils.text_surface(self.interaction_selectionnee.description_rendu, Font.ARIAL_16, Color.BLACK, new_surf.get_width() - x_courant - espacement_cote_droit)
                elif self.personnage.est_quete_active(self.interaction_selectionnee):  # si la quete est active dans le journal de quete du joueur mais que les objectifs n'ont pas encore été remplis
                    texte_description_quete = utils.text_surface(self.interaction_selectionnee.description_intermediaire, Font.ARIAL_16, Color.BLACK, new_surf.get_width() - x_courant - espacement_cote_droit)
                else:  # si on arrive ici c'est que la quete n'est pas dans le journal de quete du joueur
                    texte_description_quete = utils.text_surface(self.interaction_selectionnee.description, Font.ARIAL_16, Color.BLACK, new_surf.get_width() - x_courant - espacement_cote_droit)
                new_surf.blit(texte_description_quete, (x_courant, y_courant))
                y_courant += texte_description_quete.get_height() + espacement_titre

                y_courant += 250  # séparation entre la description et les objectifs

                # Affichage des objectifs de la quete. Il existe différents type de quêtes donc faut faire gaffe
                if isinstance(self.interaction_selectionnee, quetes.QueteTuerPnjs):
                    espacement_objectifs = 5
                    # Pour chaque objectif de dézingage de pnjs on affiche :
                    #   - le nombre de pnjs à tuer pour chaque type

                    texte_objectifs = Font.ARIAL_23.render("Objectifs :", True, Color.BLACK)
                    new_surf.blit(texte_objectifs, (x_courant, y_courant))

                    y_courant += texte_objectifs.get_height() + espacement_titre

                    for i in range(len(self.interaction_selectionnee.pnjs_a_tuers)):
                        type_pnj_a_tuer, nb_pnjs_a_tuer = self.interaction_selectionnee.pnjs_a_tuers[i]

                        if nb_pnjs_a_tuer > 1:
                            str_objectif_courant = f"- Tuer {nb_pnjs_a_tuer} {type_pnj_a_tuer.get_nom()}"
                        else:
                            str_objectif_courant = f"- Tuer {type_pnj_a_tuer.get_nom()}"

                        # Si la quete est active on affiche la progression actuelle pour chaque objectif de pnjs à tuer
                        if self.personnage.est_quete_active(self.interaction_selectionnee):
                            str_objectif_courant += f" {self.interaction_selectionnee.pnjs_tuers[i]} / {nb_pnjs_a_tuer}"

                        texte_objectif_courant = utils.text_surface(str_objectif_courant, Font.ARIAL_16, Color.BLACK, new_surf.get_width() - x_courant - espacement_cote_droit)

                        new_surf.blit(texte_objectif_courant, (x_courant, y_courant))
                        y_courant += texte_objectif_courant.get_height() + espacement_objectifs

                # Affichage d'un bouton :
                #   - pour accepter la quete si elle n'est pas déjà dans le journal de quetes du personnage
                #   - pour terminer la quete si elle est dans le journal de quetes du personnage ET qu'elle peut être terminée
                #   - pour abandonner sinon
                if self.personnage.est_quete_active(self.interaction_selectionnee):
                    if self.interaction_selectionnee.peut_etre_terminee():
                        self.bouton_terminer_quete.draw(new_surf)
                    else:
                        self.bouton_abandonner_quete.draw(new_surf)
                else:
                    self.bouton_accepter_quete.draw(new_surf)


                

            self.maj_surf_et_draw(surface, new_surf)
        elif self.pnj_selectionnee is not None:

            espacement = 5
            y_courant = espacement
            for interaction in self.pnj_selectionnee.interactions:
                x_courant = espacement
                if isinstance(interaction, quetes.Quete):
                    # On affiche uniquement les quetes qui n'ont pas déjà été terminé par le personnage
                    if not self.personnage.est_quete_terminee(interaction):
                        if interaction.peut_etre_terminee():
                            texte_indicateur_statut_quete = Font.ARIAL_23.render("?", True, Color.YELLOW_ORANGE)
                        elif self.personnage.est_quete_active(interaction):
                            texte_indicateur_statut_quete = Font.ARIAL_23.render("?", True, Color.GREY)
                        else:
                            texte_indicateur_statut_quete = Font.ARIAL_23.render("!", True, Color.YELLOW_ORANGE)

                        texte_nom_quete = Font.ARIAL_23.render(interaction.nom, True, Color.BLACK)

                        new_surf.blit(texte_indicateur_statut_quete, (x_courant, y_courant))
                        x_courant += texte_indicateur_statut_quete.get_width() + espacement

                        new_surf.blit(texte_nom_quete, (x_courant, y_courant))





            self.maj_surf_et_draw(surface, new_surf)

    def update(self, game):
        if self.interaction_selectionnee is not None:
            if isinstance(self.interaction_selectionnee, quetes.Quete):
                if self.personnage.est_quete_active(self.interaction_selectionnee):
                    if self.interaction_selectionnee.peut_etre_terminee():
                        self.bouton_terminer_quete.update(game)
                    else:
                        self.bouton_abandonner_quete.update(game)
                else:
                    self.bouton_accepter_quete.update(game)

    def handle_event(self, game: "CyrilRpg", event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_RIGHT:
                self.charger_infos_pnj(self.trouver_pnj_avec_qui_interagir())

            if event.button == pygame.BUTTON_LEFT:
                if self.pnj_selectionnee is not None:
                    if self.rect_fermeture_menu.collidepoint(game.mouse_pos):
                        self.fermer()


                    for interaction, rect_interaction in self.pnj_selectionnee_tuple_interactions_rects:
                        if rect_interaction.collidepoint(game.mouse_pos):
                            self.interaction_selectionnee = interaction

        if self.interaction_selectionnee is not None:
            if isinstance(self.interaction_selectionnee, quetes.Quete):
                if self.personnage.est_quete_active(self.interaction_selectionnee):
                    if self.interaction_selectionnee.peut_etre_terminee():
                        self.bouton_terminer_quete.handle_event(game, event)
                    else:
                        self.bouton_abandonner_quete.handle_event(game, event)
                else:
                    self.bouton_accepter_quete.handle_event(game, event)

    def charger_infos_pnj(self, pnj_interactible: pnjs.Pnj | None) -> None:
        self.pnj_selectionnee = pnj_interactible
        self.pnj_selectionnee_tuple_interactions_rects = []

        if pnj_interactible is not None:
            espacement = 5
            y_courant = self.rect.y + espacement
            for interaction in pnj_interactible.interactions:
                largeur_zone_interaction = 0
                hauteur_zone_interaction = 0

                # Il y a aussi une petit icone indiquant si l'interaction est une "Quete" / "Marchant" / "Dialogue"
                # a prendre en compte dans le rectangle
                if isinstance(interaction, quetes.Quete):
                    if not self.personnage.est_quete_terminee(interaction):
                        largeur_point_dint, hauteur_point_fint = Font.ARIAL_23.size("!")
                        largeur_zone_interaction += largeur_point_dint + espacement
                        hauteur_zone_interaction = max(hauteur_point_fint, hauteur_zone_interaction)
                    else:  # si la quete a déjà été terminé, il ne faut pas la compté comme étant une intéraction possible donc -> on skip l'intéraction (tout ce qui a en dessous)
                        continue


                # Toutes les intéractions quelles soient de type "Quete" / "Marchant" / "Dialogue" doivent avoir un
                # attribut "nom"
                largeur_nom_interaction, hauteur_nom_interaction = Font.ARIAL_23.size(interaction.nom)
                largeur_zone_interaction += largeur_nom_interaction

                hauteur_zone_interaction = max(hauteur_nom_interaction, hauteur_zone_interaction)

                self.pnj_selectionnee_tuple_interactions_rects.append(
                    (interaction, pygame.Rect(self.rect.x + espacement, y_courant, largeur_zone_interaction, hauteur_zone_interaction))
                )

                y_courant += hauteur_zone_interaction + espacement

    def trouver_pnj_avec_qui_interagir(self) -> pnjs.Pnj | None:
        for pnj in self.monde.get_pnjs_interactibles_zone_courante():
            if pnj.hovered_by_mouse:
                if self.pnj_selectionnee is None or not self.rect.collidepoint(pnj.rpg.mouse_pos):
                    return pnj
        return None

    def retour_liste_interactions(self) -> None:
        self.interaction_selectionnee = None
        self.charger_infos_pnj(self.pnj_selectionnee)

    def fermer(self) -> None:
        self.pnj_selectionnee = None
        self.pnj_selectionnee_tuple_interactions_rects.clear()
        self.interaction_selectionnee = None






class FenetreLoot(interfaceClasses.BasicInterfaceElement):
    def __init__(self, perso: personnage.Personnage, m: monde.Monde, x: int, y: int):
        self.personnage = perso
        self.monde = m
        self.rpg = m.rpg

        self.origin_surface = pygame.Surface((200, 300))

        self.origin_surface.fill(Color.DARK_GREY)
        pygame.draw.rect(self.origin_surface, Color.BLACK, self.origin_surface.get_rect(), 2)

        super().__init__(x, y, self.origin_surface.copy(), center=True)

        self.espacement_x = 5
        self.espacement_y = 5

        self.pnj_a_looter = None
        self.items_lootables = []
        self.items_lootables_rects = []

    def draw(self, surface):
        new_surf = self.origin_surface.copy()

        item_info_surf = None
        item_info_surf_rect = None

        if self.pnj_a_looter is not None:

            x_courant = self.espacement_x
            y_courant = self.espacement_y
            for i in range(len(self.items_lootables)):
                item_courant = self.items_lootables[i]
                rect_item_courant = self.items_lootables_rects[i]

                icone_item_courant = Image.ITEMS_ICONS[item_courant.icon_name]
                rect_icone_item_courant = icone_item_courant.get_rect()
                hauteur_icone_item_courant_sur_2 = rect_icone_item_courant.height / 2

                new_surf.blit(icone_item_courant, (x_courant, y_courant))

                couleur_rarete_item_courant = Color.RARITY_COLORS[item_courant.rarity]

                # Affiche un rectangle autour de l'item pour indiqué la rareté
                pygame.draw.rect(new_surf, couleur_rarete_item_courant, rect_icone_item_courant.move(x_courant, y_courant), 2)

                # Affichage du nom de l'item
                texte_nom_item_courant = Font.ARIAL_20.render(item_courant.nom, True, couleur_rarete_item_courant)
                hauteur_texte_nom_item_courant_sur_2 = texte_nom_item_courant.get_height() / 2

                x_courant += rect_icone_item_courant.width + self.espacement_x

                y_courant += hauteur_icone_item_courant_sur_2 - hauteur_texte_nom_item_courant_sur_2
                new_surf.blit(texte_nom_item_courant, (x_courant, y_courant))
                y_courant -= hauteur_icone_item_courant_sur_2 - hauteur_texte_nom_item_courant_sur_2

                x_courant -= rect_icone_item_courant.width + self.espacement_x
                y_courant += rect_icone_item_courant.height + self.espacement_y

                if rect_item_courant.collidepoint(self.rpg.mouse_pos):
                    item_info_surf = utils.item_info_surf(item_courant, perso=self.personnage)

                    item_info_surf_rect = item_info_surf.get_rect()
                    item_info_surf_rect.topleft = (self.rpg.mouse_pos[0] + 12, self.rpg.mouse_pos[1] + 12)

                    item_info_surf_rect.right = min(item_info_surf_rect.right, WINDOW_WIDTH)
                    item_info_surf_rect.bottom = min(item_info_surf_rect.bottom, WINDOW_HEIGHT)


            self.maj_surf_et_draw(surface, new_surf)

            if item_info_surf is not None:
                surface.blit(item_info_surf, item_info_surf_rect)

    def update(self, game):
        if self.pnj_a_looter is not None:
            if self.pnj_a_looter.est_decompose() or self.personnage.est_mort():
                self.fermer()

    def handle_event(self, game, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_RIGHT:
                if not self.personnage.est_mort():
                    self.charger_infos_pnj_a_looter(self.trouver_pnj_a_looter())

            if event.button == pygame.BUTTON_LEFT:
                if self.pnj_a_looter is not None:
                    item_trouvee = False
                    i = 0
                    while not item_trouvee and i < len(self.items_lootables):
                        if self.items_lootables_rects[i].collidepoint(game.mouse_pos):
                            item_trouvee = True
                            item = self.items_lootables[i]

                            item_ajouter_avec_succes = self.personnage.ajouter_item_inventaire(item)

                            if item_ajouter_avec_succes:
                                self.pnj_a_looter.items_lootables.remove(item)

                                self.charger_infos_pnj_a_looter(self.pnj_a_looter)

                        i += 1

    def trouver_pnj_a_looter(self) -> pnjs.Pnj | None:
        for pnj in self.monde.get_pnjs_attaquables_zone_courante():
            if pnj.est_mort() and not pnj.est_decompose() and pnj.hovered_by_mouse:
                return pnj
        return None

    def charger_infos_pnj_a_looter(self, pnj_a_looter: pnjs.Pnj | None) -> None:
        self.pnj_a_looter = pnj_a_looter
        self.clear_items_lootables_et_rects()

        if pnj_a_looter is not None:
            self.items_lootables = pnj_a_looter.items_lootables.copy()

            if len(self.items_lootables) > 0:
                x_courant = self.rect.x + self.espacement_x
                y_courant = self.rect.y + self.espacement_y
                for i in range(len(self.items_lootables)):
                    hauteur_icone_item_courant = Image.ITEMS_ICONS[self.items_lootables[i].icon_name].get_height()


                    self.items_lootables_rects.append(pygame.Rect(x_courant, y_courant, self.rect.width - self.espacement_x, hauteur_icone_item_courant))

                    y_courant += hauteur_icone_item_courant + self.espacement_y
            else:  # S'il n'y a rien à looter, on s'embete meme pas a faire tout ça mdrrrr
                self.fermer()

    def fermer(self) -> None:
        self.pnj_a_looter = None
        self.clear_items_lootables_et_rects()

    def clear_items_lootables_et_rects(self) -> None:
        self.items_lootables.clear()
        self.items_lootables_rects.clear()










class JournalDeQuetes(interfaceClasses.BasicInterfaceElement):
    def __init__(self, perso: personnage.Personnage, x, y):
        self.personnage = perso

        self.origin_surface = pygame.Surface((300, 800), pygame.SRCALPHA)

        # taille_bordure_rect_test = 2
        # pygame.draw.rect(self.origin_surface, Color.GREEN, self.origin_surface.get_rect(), taille_bordure_rect_test)

        self.espacement_x = 10
        self.espacement_y = 5

        # Pré rendu des textes statiques
        self.texte_journal_de_quetes = Font.ARIAL_23.render("Journal de quêtes", True, Color.BLACK)
        self.texte_a_rendre = Font.ARIAL_20_ITALIC.render("A rendre", True, Color.GREY_LIGHTEN)

        super().__init__(x, y, self.origin_surface.copy())

    def draw(self, surface):
        new_surf = self.origin_surface.copy()

        x_courant = 0
        y_courant = 0

        # Si le journal de quetes du personnage est vide, meme pas besoin d'afficher le texte "Journal de quetes" mdrrr
        if len(self.personnage.journal_de_quetes) > 0:
            new_surf.blit(self.texte_journal_de_quetes, (x_courant, y_courant))
            y_courant += self.texte_journal_de_quetes.get_height() + self.espacement_y

            for quete in self.personnage.journal_de_quetes:
                # On affiche le nom de toutes les quetes du journal de quetes du personnage
                texte_nom_quete = Font.ARIAL_21.render(quete.nom, True, Color.BLACK)
                new_surf.blit(texte_nom_quete, (x_courant, y_courant))
                y_courant += texte_nom_quete.get_height() + self.espacement_y

                # Indentation supplémentaire pour les objectifs
                x_courant += self.espacement_x

                if quete.peut_etre_terminee():  # Si la quete peut être terminé on affiche direct "A rendre"
                    new_surf.blit(self.texte_a_rendre, (x_courant, y_courant))
                else:  # Sinon on affiche tout les objectifs (séparés par des tirets) de la quete à complété
                    # Traiter les différents type de quetes
                    if isinstance(quete, quetes.QueteTuerPnjs):
                        for i in range(len(quete.pnjs_a_tuers)):
                            type_pnj_a_tuer = quete.pnjs_a_tuers[i][0]
                            nb_pnjs_a_tuer = quete.pnjs_a_tuers[i][1]

                            texte_objectif_courant = Font.ARIAL_20.render(f"- Tuer {nb_pnjs_a_tuer} {type_pnj_a_tuer.get_nom()} : {quete.pnjs_tuers[i]} / {nb_pnjs_a_tuer}", True, Color.GREY_LIGHTEN)

                            new_surf.blit(texte_objectif_courant, (x_courant, y_courant))
                            y_courant += texte_objectif_courant.get_height() + self.espacement_y

                # Séparation supplémentaire entre les quetes
                y_courant += self.espacement_y

                # Reset de l'indentation supplémentaire pour les objectifs
                x_courant -= self.espacement_x

        self.maj_surf_et_draw(surface, new_surf)






class GUIMenusPanel(interfaceClasses.BasicInterfaceElement):
    def __init__(self, perso: personnage.Personnage, x, y, text_font, text_color, center=False):
        self.personnage = perso
        self.components = [
            GUIMenusItemBag(self.personnage),
            GUIMenusItemEquipment(self.personnage),
            GUIMenusItemDonjons(self.personnage)
        ]

        width_needed = 0
        height_needed = 0
        self.gap_between_icons = 15
        for c in self.components:
            width_needed += c.rect.width
            if c.rect.height > height_needed:
                height_needed = c.rect.height

        self.empty_surface = pygame.Surface((width_needed + self.gap_between_icons * len(self.components), height_needed), pygame.SRCALPHA)
        super().__init__(x, y, self.empty_surface.copy(), center)

        self.rect.x -= self.rect.width

        total_width_taken = 0
        for i in range(len(self.components)):
            total_width_taken += self.components[i].rect.width
            self.surface.blit(self.components[i].surface, (self.rect.width - total_width_taken, height_needed - self.components[i].rect.height))

            self.components[i].rect.topleft = (
                self.rect.topright[0] - total_width_taken,
                self.rect.topright[1] + height_needed - self.components[i].rect.height
            )

            total_width_taken += self.gap_between_icons

    def draw(self, surface):
        # pygame.draw.rect(surface, Color.BLACK, self.rect, 2)
        # for c in self.components:
        #     pygame.draw.rect(surface, Color.BLACK, c.rect, 2)
        surface.blit(self.surface, self.rect.topleft)

        for c in self.components:
            c.draw(surface)

    def update(self, game):
        for c in self.components:
            c.update(game)

    def handle_event(self, game, event):
        for c in self.components:
            c.handle_event(game, event)


class GUIMenusItem(interfaceClasses.ButtonImage):
    def __init__(self, character, key, icon, menu, text, text_font, text_color, center=False):
        self.character = character
        self.key = key
        super().__init__(icon, 0, 0, text, text_font, text_color, center)

        self.menu = menu

        self.show_menu = False

    def update(self, game):
        if self.show_menu:
            self.menu.update(game)

    def draw(self, surface, dx: int = 0, dy: int = 0):
        if self.show_menu:
            self.menu.draw(surface)

    def handle_event(self, game, event):
        if not self.character.est_mort():
            if event.type == pygame.MOUSEBUTTONDOWN:  # on click pressure
                if event.button == pygame.BUTTON_LEFT:  # left click
                    self.pressed = self.collide_with_point(game.mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:  # on click release
                if event.button == pygame.BUTTON_LEFT:
                    if self.pressed:
                        self.pressed = False
                        if self.collide_with_point(game.mouse_pos):
                            self.get_clicked(game)

            if event.type == pygame.KEYDOWN:
                if event.key == self.key:
                    self.get_clicked(game)

            if self.show_menu:
                self.menu.handle_event(game, event)

    def get_clicked(self, game):
        self.show_menu = not self.show_menu









class GUIMenusItemBag(GUIMenusItem):
    def __init__(self, perso: personnage.Personnage):
        super().__init__(perso, pygame.K_b, Image.BAG_ICON, GUIInventoryMenu(perso), "", Font.ARIAL_23, Color.WHITE)


class GUIInventoryMenu(interfaceClasses.StaticImage):
    def __init__(self, perso: personnage.Personnage):
        self.personnage = perso
        super().__init__(WINDOW_WIDTH / 1.2, WINDOW_HEIGHT / 1.5, Image.IMAGE_INVENTORY, center=True)
        self.origin_surface = self.surface.copy()

        self.item_info_surf = None
        self.item_info_surf_rect = None

    def draw(self, surface):
        surface.blit(self.surface, self.rect.topleft)
        if self.item_info_surf:
            surface.blit(self.item_info_surf, self.item_info_surf_rect.topleft)

    def update(self, game):
        updated_surf = self.origin_surface.copy()

        item_info = None
        # affichage des différents objets de l'inventaire
        for index, item_courant in enumerate(self.personnage.inventory):
            if item_courant is not None:
                i = index // self.personnage.inventory.cols
                j = index % self.personnage.inventory.cols

                # Affichage d'un cadre autour de l'objet indiquant sa rareté
                item_rect = pygame.Rect(4 + 52 * j, 3 + 52 * i, 48, 48)
                pygame.draw.rect(
                    updated_surf,
                    Color.RARITY_COLORS[item_courant.rarity],
                    item_rect,
                    2
                )

                updated_surf.blit(
                    Image.ITEMS_ICONS[item_courant.icon_name],
                    (
                        item_rect.x + item_rect.width / 2 - Image.ITEMS_ICONS[item_courant.icon_name].get_width() / 2,
                        item_rect.y + item_rect.height / 2 - Image.ITEMS_ICONS[item_courant.icon_name].get_height() / 2
                    )
                )

                if not item_info:
                    current_item_real_rect = pygame.Rect(self.rect.x + item_rect.x, self.rect.y + item_rect.y, item_rect.width, item_rect.height)
                    # Affiche un menu indicatif de l'item survolé par la souris s'il existe
                    if current_item_real_rect.collidepoint(game.mouse_pos):
                        item_info = item_courant

        if item_info:
            item_info_surf = utils.item_info_surf(item_info, perso=self.personnage)

            item_info_surf_rect = item_info_surf.get_rect()
            item_info_surf_rect.topleft = (game.mouse_pos[0] + 12, game.mouse_pos[1] + 12)

            item_info_surf_rect.right = min(item_info_surf_rect.right, game.window.get_width())
            item_info_surf_rect.bottom = min(item_info_surf_rect.bottom, game.window.get_height())

            self.item_info_surf = item_info_surf
            self.item_info_surf_rect = item_info_surf_rect
        else:
            self.item_info_surf = None
            self.item_info_surf_rect = None

        self.update_surf(updated_surf)

    def handle_event(self, game, event):
        if not self.personnage.est_mort():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_RIGHT:
                    # équipe la pièce d'équipement sélectionner si le joueur fait un clique droit dessus depuis l'inventaire
                    item_a_equiper, indice = self.chercher_item_a_equiper(game)

                    if item_a_equiper is not None:
                        self.personnage.inventory[indice] = None
                        self.personnage.equiper(item_a_equiper)


    def chercher_item_a_equiper(self, game) -> (items.Equipment | None, int):
        item_a_equiper = None
        indice = 0
        while not item_a_equiper and indice < len(self.personnage.inventory):
            item_courant = self.personnage.inventory[indice]

            i = indice // self.personnage.inventory.cols
            j = indice % self.personnage.inventory.cols

            rect_item_courant = pygame.Rect(self.rect.x + 4 + 52 * j, self.rect.y + 3 + 52 * i, 48, 48)

            if rect_item_courant.collidepoint(game.mouse_pos) and isinstance(item_courant, items.Equipment):
                item_a_equiper =  item_courant
            else:
                indice += 1


        return item_a_equiper, indice








class GUIMenusItemEquipment(GUIMenusItem):
    def __init__(self, character):
        super().__init__(character, pygame.K_c, Image.EQUIPMENT_ICON, GUIEquipmentMenu(character), "", Font.ARIAL_23, Color.WHITE)




class GUIEquipmentMenu(interfaceClasses.StaticImage):
    def __init__(self, character):
        self.character = character
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, Image.MENU_EQUIPEMENT_PERSONNAGE, center=True)
        self.origin_surface = self.surface.copy()

        self.char_strength_surf = interfaceClasses.Label(
            "Strength : " + str(self.character.force),
            Font.ARIAL_23,
            Color.WHITE,
            10,
            self.rect.height
        )
        self.char_strength_surf.y -= self.char_strength_surf.rect.height + 5

        self.char_armor_surf = interfaceClasses.Label(
            "Armor : " + str(self.character.armure),
            Font.ARIAL_23,
            Color.WHITE,
            10,
            self.rect.height
        )
        self.char_armor_surf.y -= self.char_strength_surf.rect.height + self.char_armor_surf.rect.height + 5

        self.char_max_hp_surf = interfaceClasses.Label(
            "Hp : " + str(self.character.PV_max),
            Font.ARIAL_23,
            Color.WHITE,
            10,
            self.rect.height
        )
        self.char_max_hp_surf.y -= self.char_strength_surf.rect.height + self.char_armor_surf.rect.height + self.char_max_hp_surf.rect.height + 5

        self.char_name_and_level_surf = interfaceClasses.Label(
            self.character.nom + " level " + str(self.character.lvl),
            Font.ARIAL_16,
            Color.WHITE,
            self.rect.width / 2,
            0,
            True
        )
        self.char_name_and_level_surf.y += self.char_name_and_level_surf.rect.height

        self.item_info_surf = None
        self.item_info_surf_rect = None

        self.armor_dmg_reduction_info_surf = None
        self.armor_dmg_reduction_info_surf_rect = None


    def draw(self, surface):
        surface.blit(self.surface, self.rect.topleft)
        if self.item_info_surf:
            surface.blit(self.item_info_surf, self.item_info_surf_rect.topleft)
        if self.armor_dmg_reduction_info_surf:
            surface.blit(self.armor_dmg_reduction_info_surf, self.armor_dmg_reduction_info_surf_rect.topleft)

    def update(self, game):
        # Updating the stats surfaces of the character to show in the menu
        self.char_strength_surf.update_text(f"Strength : {self.character.force}")
        self.char_armor_surf.update_text(f"Armor : {self.character.armure}")
        self.char_max_hp_surf.update_text(f"Hp : {self.character.PV_max}")
        self.char_name_and_level_surf.update_text(f"{self.character.nom} level {self.character.lvl}")

        updated_surf = self.origin_surface.copy()

        self.char_name_and_level_surf.draw(updated_surf)
        self.char_strength_surf.draw(updated_surf)
        self.char_armor_surf.draw(updated_surf)
        self.char_max_hp_surf.draw(updated_surf)

        char_armor_surf_real_rect = pygame.Rect(self.char_armor_surf.rect.x + self.rect.x,
                                                self.char_armor_surf.rect.y + self.rect.y,
                                                self.char_armor_surf.rect.width,
                                                self.char_armor_surf.rect.height)

        if char_armor_surf_real_rect.collidepoint(game.mouse_pos):
            armor_dmg_reduction_info_surf = Image.TABLEAU_DESCRIPTION_ITEM.copy()
            armor_dmg_reduction_info_surf_rect = armor_dmg_reduction_info_surf.get_rect()

            armor_dmg_reduction_info_surf.blit(utils.text_surface(
                f"L'armure réduit les dégats reçus par votre personnage de {str(round(self.character.reduction_degats * 100, 2))} %",
                Font.ARIAL_23,
                Color.WHITE,
                armor_dmg_reduction_info_surf_rect.width - 10
            ), (5, 0))

            armor_dmg_reduction_info_surf_rect.topleft = (game.mouse_pos[0] + 12, game.mouse_pos[1] + 12)

            armor_dmg_reduction_info_surf_rect.right = min(armor_dmg_reduction_info_surf_rect.right, game.window.get_width())
            armor_dmg_reduction_info_surf_rect.bottom = min(armor_dmg_reduction_info_surf_rect.bottom, game.window.get_height())

            self.armor_dmg_reduction_info_surf = armor_dmg_reduction_info_surf
            self.armor_dmg_reduction_info_surf_rect = armor_dmg_reduction_info_surf_rect
        else:
            self.armor_dmg_reduction_info_surf = None
            self.armor_dmg_reduction_info_surf_rect = None

        item_info = None

        # Show character weapon in slot
        if self.character.arme:
            weapon_rect = pygame.Rect(158, 404, 48, 48)
            # Affichage d'un cadre autour de l'objet indiquant sa rareté
            pygame.draw.rect(updated_surf, Color.RARITY_COLORS[self.character.arme.rarity], weapon_rect, 2)

            updated_surf.blit(Image.ITEMS_ICONS[self.character.arme.icon_name], (158 + 48 / 2 - Image.ITEMS_ICONS[self.character.arme.icon_name].get_width() / 2, 404 + 48 / 2 - Image.ITEMS_ICONS[self.character.arme.icon_name].get_height() / 2))

            # Affiche un menu indicatif de l'item de gauche survolé par la souris s'il existe
            weapon_real_rect = weapon_rect.copy()
            weapon_real_rect.x += self.rect.x
            weapon_real_rect.y += self.rect.y
            if weapon_real_rect.collidepoint(game.mouse_pos):
                item_info = self.character.arme

        # affiche les différents pièces d'équipements du personnage
        for i, e in enumerate(self.character.equipment.values()):
            if e:
                # équipements de gauche
                if i < 5:
                    e_rect = pygame.Rect(51, 34 + 74 * i, 48, 48)
                else:
                    e_rect = pygame.Rect(280, 34 + 74 * (i-5), 48, 48)

                pygame.draw.rect(updated_surf, Color.RARITY_COLORS[e.rarity], e_rect, 2)

                updated_surf.blit(
                    Image.ITEMS_ICONS[e.icon_name],
                    (
                        e_rect.x + e_rect.width / 2 - Image.ITEMS_ICONS[e.icon_name].get_width() / 2,
                        e_rect.y + e_rect.height / 2 - Image.ITEMS_ICONS[e.icon_name].get_height() / 2
                    )
                )

                # Affiche un menu indicatif de l'item de gauche survolé par la souris s'il existe
                e_real_rect = e_rect.copy()
                e_real_rect.x += self.rect.x
                e_real_rect.y += self.rect.y
                if e_real_rect.collidepoint(game.mouse_pos):
                    item_info = e

        if item_info:
            item_info_surf = utils.item_info_surf(item_info)

            item_info_surf_rect = item_info_surf.get_rect()
            item_info_surf_rect.topleft = (game.mouse_pos[0] + 12, game.mouse_pos[1] + 12)

            item_info_surf_rect.right = min(item_info_surf_rect.right, game.window.get_width())
            item_info_surf_rect.bottom = min(item_info_surf_rect.bottom, game.window.get_height())

            self.item_info_surf = item_info_surf
            self.item_info_surf_rect = item_info_surf_rect
        else:
            self.item_info_surf = None
            self.item_info_surf_rect = None

        self.update_surf(updated_surf)

    def handle_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_RIGHT:
                if not self.character.est_mort():
                    if self.character.arme:
                        real_weapon_slot_rect = pygame.Rect(158 + self.rect.x, 404 + self.rect.y, 48, 48)
                        if real_weapon_slot_rect.collidepoint(game.mouse_pos):
                            self.character.unequip(self.character.arme)

                    for i, e in enumerate(self.character.equipment.values()):
                        if e:
                            # équipement de gauche
                            if i < 5:
                                real_e_slot_rect = pygame.Rect(51 + self.rect.x, 34 + 74 * i + self.rect.y, 48, 48)
                            # équipement de droite
                            else:
                                real_e_slot_rect = pygame.Rect(280 + self.rect.x, 34 + 74 * (i - 5) + self.rect.y, 48, 48)

                            if real_e_slot_rect.collidepoint(game.mouse_pos):
                                self.character.unequip(e)













class GUIMenusItemDonjons(GUIMenusItem):
    def __init__(self, character):
        super().__init__(character, pygame.K_v, Image.DONJONS_ICON, GUIDonjonsMenu(None), "", Font.ARIAL_23, Color.WHITE)


class GUIDonjonsMenu(interfaceClasses.StaticImage):
    def __init__(self, donjons):
        self.donjons = donjons
        super().__init__(WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2, Image.MENU_DONJONS, center=True)









class CharacterFrame(interfaceClasses.BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=False):
        self.character = character

        self.char_hp_rect = pygame.Rect(
            0,
            0,
            300,
            80
        )

        self.char_hp_text = interfaceClasses.Label(
            utils.convert_number(self.character.PV) + " / " + utils.convert_number(self.character.PV_max),
            text_font,
            text_color,
            self.char_hp_rect.width / 2,
            self.char_hp_rect.height / 2,
            True
        )

        self.char_level_frame_surf = pygame.Surface((40, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(self.char_level_frame_surf, Color.BACKGROUND_SHADOW, pygame.Rect(0, 0, self.char_level_frame_surf.get_width(), self.char_level_frame_surf.get_height()))
        pygame.draw.ellipse(self.char_level_frame_surf, Color.BLACK, pygame.Rect(0, 0, self.char_level_frame_surf.get_width(), self.char_level_frame_surf.get_height()), 2)

        self.char_lvl_text = interfaceClasses.Label(
            str(self.character.lvl),
            Font.CHARACTER_LEVEL,
            Color.YELLOW_ORANGE,
            self.char_hp_rect.right + self.char_level_frame_surf.get_width() / 2,
            self.char_level_frame_surf.get_height() / 2.5 + self.char_hp_rect.height,
            True
        )

        self.origin_surf = pygame.Surface((self.char_hp_rect.width + self.char_level_frame_surf.get_width(), self.char_hp_rect.height + self.char_level_frame_surf.get_height()), pygame.SRCALPHA)
        super().__init__(x, y, self.origin_surf.copy(), center)

    def update(self, game):
        self.char_hp_text.update_text(utils.convert_number(self.character.PV) + " / " + utils.convert_number(self.character.PV_max))
        self.char_lvl_text.update_text(str(self.character.lvl))

        perc_hp_left = self.character.PV / self.character.PV_max

        updated_surf = self.origin_surf.copy()

        if perc_hp_left >= 0.5:
            color_char_hp_bar_rect = (24 + 216 * (1 - perc_hp_left ** 2), 240, 10)
        else:
            color_char_hp_bar_rect = (240, 240 * (2 * perc_hp_left), 10)

        pygame.draw.rect(updated_surf, color_char_hp_bar_rect, pygame.Rect(0, 0, self.char_hp_rect.width * perc_hp_left, self.char_hp_rect.height))
        pygame.draw.rect(updated_surf, Color.BLACK, self.char_hp_rect, 2)
        self.char_hp_text.draw(updated_surf)

        updated_surf.blit(self.char_level_frame_surf, self.char_hp_rect.bottomright)
        self.char_lvl_text.draw(updated_surf)

        self.update_surf(updated_surf)



class CharacterRespawnButton(interfaceClasses.ButtonImage):
    def __init__(self, character, img, x, y, text, text_font, text_color, center=True):
        self.character = character
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        self.character.respawn()


class CharacterDead(interfaceClasses.BackgroundColor):
    def __init__(self, character):
        self.character = character
        super().__init__((WINDOW_WIDTH, WINDOW_HEIGHT), Color.BACKGROUND_SHADOW)
        self.origin_surf = self.surface.copy()

        self.respawn_button = CharacterRespawnButton(character, Image.SILVER_WOOD_BUTTONS[3], self.rect.width / 2, self.rect.height / 2, "Respawn", Font.ARIAL_23, Color.GREY)

        self.character_is_dead_text = interfaceClasses.Label(
            "You died",
            Font.ARIAL_40,
            Color.RED,
            self.rect.width / 2,
            self.rect.height / 2 - self.respawn_button.rect.height,
            True
        )


    def draw(self, surface):
        if self.character.est_mort():
            surface.blit(self.surface, self.rect.topleft)

    def update(self, game):
        if self.character.est_mort():
            self.respawn_button.update(game)

            updated_surf = self.origin_surf.copy()
            self.respawn_button.draw(updated_surf)
            self.character_is_dead_text.draw(updated_surf)
            self.update_surf(updated_surf)

    def handle_event(self, game, event):
        if self.character.est_mort():
            self.respawn_button.handle_event(game, event)



class FlecheRetour(interfaceClasses.BasicInterfaceElement):
    def __init__(self, on_click_func, x, y, center=False):
        self.on_click_func = on_click_func
        super().__init__(x, y, Image.FLECHE_RETOUR, center)

        self.survolee_par_souris = False

    def update(self, game: "CyrilRpg"):
        self.survolee_par_souris = self.rect.collidepoint(game.mouse_pos)

        if self.survolee_par_souris:
            self.update_surf(Image.FLECHE_RETOUR_FOCUS)
        else:
            self.update_surf(Image.FLECHE_RETOUR)

    def handle_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                if self.rect.collidepoint(game.mouse_pos):
                    self.on_click_func()



