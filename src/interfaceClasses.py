import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import CyrilRpg

from data import Color, Font


class BasicInterfaceElement:
    def __init__(self, x, y, surf, center=False):
        self.surface = surf
        self.x = x
        self.y = y
        self.center = center
        self.rect: pygame.Rect = self.surface.get_rect()

        if self.center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.surface, self.rect.topleft)

    def update(self, game):
        pass

    def handle_event(self, game, event: pygame.event.Event):
        pass

    def update_surf(self, new_surf):
        self.surface = new_surf
        self.rect.size = self.surface.get_size()

        self.update_rect()

    def update_rect(self):
        if self.center:
            self.rect.center = (self.x, self.y)
        else:
            self.rect.topleft = (self.x, self.y)

    def maj_surf_et_draw(self, surface_sur_laquelle_afficher: pygame.Surface, new_surf: pygame.Surface) -> None:
        self.update_surf(new_surf)
        surface_sur_laquelle_afficher.blit(self.surface, self.rect.topleft)


class Label(BasicInterfaceElement):
    def __init__(self, text: str, text_font, text_color, x, y, center=False):
        super().__init__(x, y, text_font.render(text, True, text_color), center)
        self.text = text
        self.text_font: pygame.font.Font = text_font
        self.text_color = text_color

    def update_text(self, new_text):
        self.text = new_text
        self.update_surf(self.text_font.render(self.text, True, self.text_color))

    def update_text_color(self, new_text_color):
        self.text_color = new_text_color


class StaticImage(BasicInterfaceElement):
    def __init__(self, x, y, img, center=False):
        super().__init__(x, y, img, center)


class BackgroundImage(StaticImage):
    def __init__(self, surf):
        super().__init__(0, 0, surf)


class BackgroundColor(BackgroundImage):
    def __init__(self, size, color):
        super().__init__(pygame.surface.Surface(size, pygame.SRCALPHA))
        self.surface.fill(color)


class Button(Label):
    def __init__(self, x, y, text, text_font, color, border_radius, center=False):
        super().__init__(text, text_font, color, x, y, center)
        self.border_radius = border_radius

        text_surf = self.surface.copy()
        surf_size = pygame.math.Vector2(text_surf.get_width() + int(text_surf.get_height() / 1), text_surf.get_height() + int(text_surf.get_height() / 2))

        self.surface = pygame.Surface(surf_size)
        self.surface.fill((34, 34, 34))
        self.surface.blit(text_surf, (surf_size.x / 2 - self.rect.w / 2, surf_size.y / 2 - self.rect.h / 2))

        self.rect = pygame.Rect(0, 0, self.surface.get_width(), self.surface.get_height())

        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)

        pygame.draw.rect(self.surface, color, [0, 0, self.rect.width, self.rect.height], border_radius)
        self.surface.blit(text_surf, [(self.rect.width / 2) - (text_surf.get_width() / 2), (self.rect.height / 2) - (text_surf.get_height() / 2)])

        self.surface_mouse_over = pygame.Surface(surf_size)
        self.surface_mouse_over.fill((68, 68, 68))
        pygame.draw.rect(self.surface_mouse_over, color, [0, 0, self.rect.width, self.rect.height], border_radius)
        self.surface_mouse_over.blit(text_surf, [(self.rect.width / 2) - (text_surf.get_width() / 2), (self.rect.height / 2) - (text_surf.get_height() / 2)])

        self.surface_pressed = pygame.Surface(surf_size)
        self.surface_pressed.fill((51, 51, 51))
        pygame.draw.rect(self.surface_pressed, color, [0, 0, self.rect.width, self.rect.height], border_radius)
        self.surface_pressed.blit(text_surf, [(self.rect.width / 2) - (text_surf.get_width() / 2), (self.rect.height / 2) - (text_surf.get_height() / 2)])
        self.temp_blackalpha_surf = pygame.Surface(surf_size)
        self.temp_blackalpha_surf.set_alpha(100)
        self.surface_pressed.blit(self.temp_blackalpha_surf, [0, 0])

        self.pressed = False
        self.mouse_over = False

    def update(self, game):
        self.mouse_over = self.collide_with_point(game.mouse_pos)

    def draw(self, surface, dx: int = 0, dy: int = 0):
        """
        On peut spécifier un décalage en x et en y qui permet d'afficher à la position du rectangle décaler par ces dx, dy.
        """
        if self.pressed:
            surface.blit(self.surface_pressed, self.rect.move(dx, dy))
        elif self.mouse_over:
            surface.blit(self.surface_mouse_over, self.rect.move(dx, dy))
        else:
            surface.blit(self.surface, self.rect.move(dx, dy))

    def handle_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # on click pressure
            if event.button == pygame.BUTTON_LEFT:  # left click
                self.pressed = self.collide_with_point(game.mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:  # on click release
            if event.button == pygame.BUTTON_LEFT:
                if self.pressed:
                    self.pressed = False
                    if self.collide_with_point(game.mouse_pos):
                        self.get_clicked(game)

    def collide_with_point(self, coord):
        return self.rect.collidepoint(coord)

    def get_clicked(self, game):
        pass


class ButtonImage(Button):
    def __init__(self, img, x, y, text, text_font, text_color, center=False):
        super().__init__(x, y, text, text_font, text_color, 0, center)
        surf_temp = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        surf_temp.blit(img, (0, 0))

        text_surf = text_font.render(text, True, text_color)
        surf_temp.blit(text_surf, (surf_temp.get_width() / 2 - text_surf.get_width() / 2,
                                   surf_temp.get_height() / 2 - text_surf.get_height() / 2))

        self.surface = surf_temp

        self.rect = self.surface.get_rect()
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)


        self.surface_mouse_over = self.surface.copy()
        self.surface_mouse_over.fill((32, 32, 32), None, pygame.BLEND_RGB_ADD)

        self.surface_pressed = self.surface.copy()
        self.surface_pressed.fill((0, 0, 0), None, pygame.BLEND_RGB_ADD)
        self.surface.fill((8, 8, 8), None, pygame.BLEND_RGB_ADD)


class InputField(BasicInterfaceElement):
    def __init__(self, jeu:"CyrilRpg", x: float, y: float, largeur: float, hauteur: float, police_input_text=Font.ARIAL_23, couleur_input_text=Color.BLACK, couleur_input_rect=Color.BLACK, largeur_bordure_input_rect=2, rayon_bordure_input_rect=1, center=False):
        self.jeu = jeu

        self.input_field_sans_texte = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        pygame.draw.rect(self.input_field_sans_texte, couleur_input_rect, self.input_field_sans_texte.get_rect(), largeur_bordure_input_rect, rayon_bordure_input_rect)
        super().__init__(x, y, self.input_field_sans_texte.copy(), center)

        self.text = ""
        self.text_surface = Label(self.text, police_input_text, couleur_input_text, self.rect.w / 2, self.rect.h / 2, center=True)
        self.text_surface.draw(self.surface)

        self.focused = False
        self.next_time_blink = 0
        self.cooldown = False

        self.blink_surf = pygame.Surface((3, 30))

    def update(self, game):
        # make a blinking bar that indicates that the input field has been pressed
        if self.focused:
            if self.jeu.time >= self.next_time_blink:
                self.update_input_surface()
            elif self.jeu.time + 0.5 >= self.next_time_blink:
                self.remove_blink()
        else:
            self.remove_blink()

    def handle_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # on click pressure
            if event.button == pygame.BUTTON_LEFT:  # left click
                self.focused = self.rect.collidepoint(game.mouse_pos)

        # handle key inputs only if pressed
        if self.focused:
            if event.type == pygame.KEYDOWN:
                # event.key from 97 -> 'a' to 122 -> 'z'
                if pygame.K_a <= event.key <= pygame.K_z:
                    lettre = chr(event.key - 32) if pygame.key.get_pressed()[pygame.K_LSHIFT] else chr(event.key)
                    if self.text_surface.rect.width + self.text_surface.text_font.size(lettre)[0] < self.rect.width:
                        self.text += lettre
                        self.update_input_surface()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # remove last character
                    self.update_input_surface()

    def update_input_surface(self):
        self.text_surface.update_text(self.text)
        self.reset_input_field()
        self.text_surface.draw(self.surface)
        self.blink()

    def blink(self):
        self.surface.blit(self.blink_surf, self.blink_surf.get_rect(
            center=(self.rect.w / 2 + self.text_surface.rect.width / 2, self.rect.h / 2)))
        self.next_time_blink = self.jeu.time + 1

    def remove_blink(self):
        self.text_surface.update_text(self.text)
        self.reset_input_field()
        self.text_surface.draw(self.surface)

    def reset_input_field(self):
        self.update_surf(self.input_field_sans_texte.copy())







