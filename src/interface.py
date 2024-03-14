import pygame

from data import Font, Color, Image
from src import interfaceClasses, utils
from src.item import *
from config import WINDOW_WIDTH, WINDOW_HEIGHT


class FpsViewer(interfaceClasses.BasicInterfaceTextElement):
    def __init__(self, fps: float, x, y):
        super().__init__(x, y, str(round(fps)), Font.ARIAL_30, Color.BLACK)

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
        game.enter_world(self.character)



class CharacterCreationButton(interfaceClasses.ButtonImage):
    def __init__(self, img, x, y, text, text_font, text_color, center=True):
        super().__init__(img, x, y, text, text_font, text_color, center)

    def get_clicked(self, game):
        game.character_creation_menu()


class CharacterNameInput(interfaceClasses.InputField):
    def __init__(self, x, y, text_font, text_color, border_color=Color.BLACK, border_radius=2, center=True):
        super().__init__(x, y, text_font, text_color, border_color, border_radius, center)


class CharacterXpBar(interfaceClasses.BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=True):
        self.empty_surface = pygame.Surface((400, 35), pygame.SRCALPHA)
        super().__init__(x, y, self.empty_surface.copy(), center)
        self.character = character

        self.char_xp_text = interfaceClasses.BasicInterfaceTextElement(
            self.rect.width / 2,
            self.rect.height / 2,
            str(self.character.xp) + " / " + str(self.character.xp_requis),
            text_font,
            text_color,
            True
        )

        pygame.draw.rect(self.surface, Color.PURPLE, pygame.Rect(0, 0, self.surface.get_width() * (self.character.xp / self.character.xp_requis), self.surface.get_height()))

        pygame.draw.rect(self.surface, Color.GREY_LIGHTEN, self.surface.get_rect(), 2)

        self.char_xp_text.draw(self.surface)

    def update(self, game):
        self.char_xp_text.update_text(str(self.character.xp) + " / " + str(self.character.xp_requis))

        updated_surf = self.empty_surface.copy()
        pygame.draw.rect(updated_surf, Color.PURPLE, pygame.Rect(0, 0, updated_surf.get_width() * (self.character.xp / self.character.xp_requis), updated_surf.get_height()))
        pygame.draw.rect(updated_surf, Color.GREY_LIGHTEN, updated_surf.get_rect(), 2)
        self.char_xp_text.draw(updated_surf)

        self.update_surf(updated_surf)


class CharacterSpells(interfaceClasses.BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=True):
        self.empty_surface = pygame.Surface((800, 80), pygame.SRCALPHA)
        super().__init__(x, y, self.empty_surface.copy(), center)
        pygame.draw.rect(self.surface, Color.BLACK, self.surface.get_rect(), 2)
        self.character = character


class GUIMenusPanel(interfaceClasses.BasicInterfaceElement):
    def __init__(self, character, x, y, text_font, text_color, center=False):
        self.character = character
        self.components = [
            GUIMenusItemBag(self.character),
            GUIMenusItemEquipment(self.character),
            GUIMenusItemDonjons(self.character)
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

    def draw(self, surface):
        if self.show_menu:
            self.menu.draw(surface)

    def handle_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # on click pressure
            if event.button == 1:  # left click
                self.pressed = self.collide_with_point(game.mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:  # on click release
            if event.button == 1:
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
    def __init__(self, character):
        super().__init__(character, pygame.K_b, Image.BAG_ICON, GUIInventoryMenu(character), "", Font.ARIAL_23, Color.WHITE)


class GUIInventoryMenu(interfaceClasses.StaticImage):
    def __init__(self, character):
        self.character = character
        super().__init__(WINDOW_WIDTH / 1.2, WINDOW_HEIGHT / 1.5, Image.IMAGE_INVENTORY, center=True)
        self.origin_surface = self.surface.copy()

    def update(self, game):
        updated_surf = self.origin_surface.copy()

        item_info = None
        # affichage des différents objets de l'inventaire
        for index, item in enumerate(self.character.inventory):
            if item is not None:
                i = index // self.character.inventory.cols
                j = index % self.character.inventory.cols

                # Affichage d'un cadre autour de l'objet indiquant sa rareté
                item_rect = pygame.Rect(4 + 52 * j, 3 + 52 * i, 48, 48)
                pygame.draw.rect(
                    updated_surf,
                    Color.RARITY_COLORS[item.rarity],
                    item_rect,
                    2
                )

                updated_surf.blit(
                    Image.ITEMS_ICONS[item.icon_name],
                    (
                        item_rect.x + item_rect.width / 2 - Image.ITEMS_ICONS[item.icon_name].get_width() / 2,
                        item_rect.y + item_rect.height / 2 - Image.ITEMS_ICONS[item.icon_name].get_height() / 2
                    )
                )

                if not item_info:
                    current_item_real_rect = pygame.Rect(self.rect.x + item_rect.x, self.rect.y + item_rect.y, item_rect.width, item_rect.height)
                    # Affiche un menu indicatif de l'item survolé par la souris s'il existe
                    if current_item_real_rect.collidepoint(game.mouse_pos):
                        item_info = item

        if item_info:
            item_info_surf = Image.TABLEAU_DESCRIPTION_ITEM.copy()

            item_info_surf.blit(Font.ARIAL_23.render(
                item_info.type + " " + item_info.rarity + " lvl " + str(item_info.lvl),
                True, Color.RARITY_COLORS[item_info.rarity]), (5, 5))

            # If it's a weapon we display the damage of the weapon
            if isinstance(item_info, Weapon):
                item_info_surf.blit(Font.ARIAL_23.render(str(item_info.damage) + " Damage", True, Color.WHITE),
                                    (10, 50))

            elif isinstance(item_info, Armor):
                item_info_surf.blit(Font.ARIAL_23.render(str(item_info.armor) + " Armor", True, Color.WHITE), (10, 50))

            if isinstance(item_info, Equipment):
                item_info_surf.blit(Font.ARIAL_23.render("+ " + str(item_info.bonus_hp) + " HP", True, Color.WHITE), (10, 80))

                item_info_surf.blit(Font.ARIAL_23.render("+ " + str(item_info.bonus_strength) + " Strength", True, Color.WHITE), (10, 110))

            item_info_surf_rect = item_info_surf.get_rect()
            item_info_surf_rect.topright = (game.mouse_pos[0] - self.rect.x + item_info_surf_rect.width, game.mouse_pos[1] - self.rect.y)

            if item_info_surf_rect.right > self.rect.width:
                item_info_surf_rect.right = self.rect.width

            if item_info_surf_rect.bottom > self.rect.height:
                item_info_surf_rect.bottom = self.rect.height

            updated_surf.blit(item_info_surf, item_info_surf_rect.topleft)

        self.update_surf(updated_surf)

    def handle_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                # équipe la pièce d'équipement sélectionner si le joueur fait un clique droit dessus depuis l'inventaire
                for index, item in enumerate(self.character.inventory):
                    if item is not None:
                        i = index // self.character.inventory.cols
                        j = index % self.character.inventory.cols

                        current_item_real_rect = pygame.Rect(self.rect.x + 4 + 52 * j, self.rect.y + 3 + 52 * i, 48, 48)

                        if current_item_real_rect.collidepoint(game.mouse_pos):
                            if isinstance(item, Equipment):
                                self.character.equip(item)
                                self.character.inventory[index] = None











class GUIMenusItemEquipment(GUIMenusItem):
    def __init__(self, character):
        super().__init__(character, pygame.K_c, Image.EQUIPMENT_ICON, GUIEquipmentMenu(character), "", Font.ARIAL_23, Color.WHITE)




class GUIEquipmentMenu(interfaceClasses.StaticImage):
    def __init__(self, character):
        self.character = character
        super().__init__(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, Image.MENU_EQUIPEMENT_PERSONNAGE, center=True)
        self.origin_surface = self.surface.copy()

        self.char_strength_surf = interfaceClasses.BasicInterfaceTextElement(
            10,
            self.rect.height,
            "Strength : " + str(self.character.force),
            Font.ARIAL_23,
            Color.WHITE
        )
        self.char_strength_surf.y -= self.char_strength_surf.rect.height + 5

        self.char_armor_surf = interfaceClasses.BasicInterfaceTextElement(
            10,
            self.rect.height,
            "Armor : " + str(self.character.armure),
            Font.ARIAL_23,
            Color.WHITE
        )
        self.char_armor_surf.y -= self.char_strength_surf.rect.height + self.char_armor_surf.rect.height + 5

        self.char_max_hp_surf = interfaceClasses.BasicInterfaceTextElement(
            10,
            self.rect.height,
            "Hp : " + str(self.character.PV_max),
            Font.ARIAL_23,
            Color.WHITE
        )
        self.char_max_hp_surf.y -= self.char_strength_surf.rect.height + self.char_armor_surf.rect.height + self.char_max_hp_surf.rect.height + 5

        self.char_strength_surf.draw(self.surface)
        self.char_armor_surf.draw(self.surface)
        self.char_max_hp_surf.draw(self.surface)

    def update(self, game):
        # Updating the stats surfaces of the character to show in the menu
        self.char_strength_surf.update_text("Strength : " + str(self.character.force))
        self.char_armor_surf.update_text("Armor : " + str(self.character.armure))
        self.char_max_hp_surf.update_text("Hp : " + str(self.character.PV_max))

        updated_surf = self.origin_surface.copy()

        self.char_strength_surf.draw(updated_surf)
        self.char_armor_surf.draw(updated_surf)
        self.char_max_hp_surf.draw(updated_surf)

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
            item_info_surf = Image.TABLEAU_DESCRIPTION_ITEM.copy()

            item_info_surf.blit(Font.ARIAL_23.render(
                item_info.type + " " + item_info.rarity + " lvl " + str(item_info.lvl),
                True, Color.RARITY_COLORS[item_info.rarity]), (5, 5))

            # If it's a weapon we display the damage of the weapon
            if isinstance(item_info, Weapon):
                item_info_surf.blit(Font.ARIAL_23.render(str(item_info.damage) + " Damage", True, Color.WHITE),
                                    (10, 50))

            elif isinstance(item_info, Armor):
                item_info_surf.blit(Font.ARIAL_23.render(str(item_info.armor) + " Armor", True, Color.WHITE), (10, 50))

            if isinstance(item_info, Equipment):
                item_info_surf.blit(Font.ARIAL_23.render("+ " + str(item_info.bonus_hp) + " HP", True, Color.WHITE), (10, 80))

                item_info_surf.blit(Font.ARIAL_23.render("+ " + str(item_info.bonus_strength) + " Strength", True, Color.WHITE), (10, 110))

            item_info_surf_rect = item_info_surf.get_rect()
            item_info_surf_rect.topright = (game.mouse_pos[0] - self.rect.x + item_info_surf_rect.width, game.mouse_pos[1] - self.rect.y)

            if item_info_surf_rect.right > self.rect.width:
                item_info_surf_rect.right = self.rect.width

            if item_info_surf_rect.bottom > self.rect.height:
                item_info_surf_rect.bottom = self.rect.height

            updated_surf.blit(item_info_surf, item_info_surf_rect.topleft)

        self.update_surf(updated_surf)

    def handle_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # right click
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
        self.empty_surface = pygame.Surface((250, 80), pygame.SRCALPHA)
        super().__init__(x, y, self.empty_surface.copy(), center)
        self.character = character

        self.char_hp_text = interfaceClasses.BasicInterfaceTextElement(
            self.rect.width / 2,
            self.rect.height / 2,
            str(self.character.PV) + " / " + str(self.character.PV_max),
            text_font,
            text_color,
            True
        )

        pygame.draw.rect(self.surface, Color.PURPLE, pygame.Rect(0, 0, self.surface.get_width() * (self.character.PV / self.character.PV_max), self.surface.get_height()))

        pygame.draw.rect(self.surface, Color.GREY_LIGHTEN, self.surface.get_rect(), 2)

        self.char_hp_text.draw(self.surface)

    def update(self, game):
        self.char_hp_text.update_text(str(self.character.PV) + " / " + str(self.character.PV_max))

        perc_hp_left = self.character.PV / self.character.PV_max

        updated_surf = self.empty_surface.copy()

        if perc_hp_left >= 0.5:
            color_char_hp_bar_rect = (24 + 216 * (1 - perc_hp_left ** 2), 240, 10)
        else:
            color_char_hp_bar_rect = (240, 240 * (2 * perc_hp_left), 10)

        pygame.draw.rect(updated_surf, color_char_hp_bar_rect, pygame.Rect(0, 0, updated_surf.get_width() * perc_hp_left, updated_surf.get_height()))
        pygame.draw.rect(updated_surf, Color.BLACK, updated_surf.get_rect(), 2)
        self.char_hp_text.draw(updated_surf)

        self.update_surf(updated_surf)


