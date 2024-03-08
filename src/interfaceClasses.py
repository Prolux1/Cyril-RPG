import pygame
from data import Color


class BasicInterfaceElement:
    def __init__(self, x, y, surf, center=False):
        self.surface = surf
        self.rect = self.surface.get_rect()

        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.surface, self.rect.topleft)

    def update_surf(self, new_surf):
        self.surface = new_surf
        self.rect.size = self.surface.get_size()

    def update(self, game):
        pass

    def handle_event(self, game, event):
        pass


class BasicInterfaceTextElement(BasicInterfaceElement):
    def __init__(self, x, y, text, text_font, text_color, center=False):
        super().__init__(x, y, text_font.render(text, True, text_color), center)
        self.text = text
        self.text_font = text_font
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
        super().__init__(pygame.surface.Surface(size))
        self.surface.fill(color)


class Button(BasicInterfaceTextElement):
    def __init__(self, x, y, text, text_font, color, border_radius, center=False):
        super().__init__(x, y, text, text_font, color, center)
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

    def draw(self, surface):
        if self.pressed:
            surface.blit(self.surface_pressed, self.rect.topleft)
        elif self.mouse_over:
            surface.blit(self.surface_mouse_over, self.rect.topleft)
        else:
            surface.blit(self.surface, self.rect.topleft)

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
    def __init__(self, x, y, text_font, text_color, border_color=Color.BLACK, border_radius=2, center=False):
        char_name_surf = text_font.render("Character name", True, Color.GREY)

        initial_surf = pygame.Surface((max(char_name_surf.get_width(), 200), char_name_surf.get_height() + 50), pygame.SRCALPHA)
        initial_surf.blit(char_name_surf, [initial_surf.get_width() / 2 - char_name_surf.get_width() / 2, 0])

        self.x = x - initial_surf.get_width() / 2
        self.y = y - initial_surf.get_height() - 40

        self.input_field_rect = pygame.Rect(0, char_name_surf.get_height(), 200, 50)
        self.input_field_window_rect = pygame.Rect(x + self.input_field_rect.x, y + self.input_field_rect.y, self.input_field_rect.width, self.input_field_rect.height)
        self.input_field_rect_border_width = 3
        pygame.draw.rect(initial_surf, border_color, self.input_field_rect, self.input_field_rect_border_width, 4)

        initial_surf.convert_alpha()

        self.text = ""
        self.text_surface = BasicInterfaceTextElement(0, 0, "", text_font, text_color)
        # self.text_surface = self.text_font.render(self.text, True, border_color)
        self.initial_surf_with_text = initial_surf.copy()

        super().__init__(x, y, self.initial_surf_with_text, center)

        self.pressed = False
        self.last_time_blink = None
        self.cooldown = False

        self.blink_surf = pygame.Surface((3, 30))

    def update(self, game):
        surf_with_text = self.initial_surf_with_text.copy()
        self.text_surface.draw(surf_with_text)
        # surf_with_text.blit(self.text_surface, self.text_surface.get_rect(center=self.input_field_rect.center))
        self.update_surf(surf_with_text)  # reset surf

        # make a blinking bar that indicates that the input field has been pressed
        if self.pressed:
            if self.last_time_blink is None:
                self.last_time_blink = game.time

            if self.cooldown:
                if self.last_time_blink + 1 < game.time:
                    self.cooldown = False
                    self.last_time_blink = None

            elif self.last_time_blink + 0.5 > game.time:
                self.surface.blit(self.blink_surf, self.blink_surf.get_rect(center=(self.input_field_rect.centerx + self.text_surface.rect.width / 2, self.input_field_rect.centery)))
            else:
                self.cooldown = True

        else:
            self.last_time_blink = None
            self.cooldown = False

    def handle_event(self, game, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # on click pressure
            if event.button == 1:  # left click
                if self.input_field_window_rect.collidepoint(game.mouse_pos):
                    self.pressed = True
                else:
                    self.pressed = False

        # handle key inputs only if pressed
        if self.pressed:
            if event.type == pygame.KEYDOWN:
                # event.key from 97 -> 'a' to 122 -> 'z'
                if pygame.K_a <= event.key <= pygame.K_z:
                    if self.text_surface.rect.width + 24 < self.input_field_rect.width:
                        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                            self.text += chr(event.key - 32)
                        else:
                            self.text += chr(event.key)
                        self.update_text_surface()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # remove last character
                    self.update_text_surface()

    def update_text_surface(self):
        self.last_time_blink = None
        self.cooldown = False
        self.text_surface.update_text(self.text)







