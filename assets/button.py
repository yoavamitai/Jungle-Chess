import pygame as pg

class Button:
    def __init__(self, color, x, y, w, h, border_radius=0, text='', font=None, outline=None, outline_thickness=0):
        hex = color[1:]
        self.color = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.font = font
        self.outline = outline
        self.outline_thickness = outline_thickness
        self.border_radius = border_radius

    def draw(self, window):
        if self.outline:
            pg.draw.rect(window, self.outline, (self.x - self.outline_thickness, self.y - self.outline_thickness,
                                                self.w + self.outline_thickness * 2,
                                                self.h + self.outline_thickness * 2),
                         border_radius=self.border_radius)

        pg.draw.rect(window, self.color, (self.x, self.y, self.w, self.h), border_radius=self.border_radius)

        if self.text != '':

            text = self.font.render(self.text, True, (7, 9, 15))

            window.blit(text, (self.x + (self.w / 2 - text.get_width() / 2), self.y + (self.h / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h