import pygame as pg
class Consts:
    pg.init()
    button_font = pg.font.Font('assets/button_font.ttf', 30)
    main_title_font = pg.font.Font('assets/main_title_font.ttf', 50)
    sub_title_font = pg.font.Font('assets/main_title_font.ttf', 30)
    message_font = pg.font.Font('assets/main_title_font.ttf', 35)
    label_font = pg.font.Font('assets/main_title_font.ttf', 15)

    grass_color = (107, 170, 117)
    river_color = (69, 105, 144)
    trap_color = (173, 52, 62)
    den_color = (242, 175, 41)

    ROWS = 9
    COLS = 7
    BLOCK_SIZE = 50
    GAP = 5

    FPS = 60

    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]