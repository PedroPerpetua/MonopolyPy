import pygame as pg
from lib.assets import Colors, Assets

SIDE_LARGE = 98
SIDE_SMALL = 56
BORDER_SIZE = 1
PLAYER_OFFSETS = ("Dummy", [(-8, -8)], [(-16, -8), (0, -8)], [(-16, -16), (0, -16), (-8, 0)], [(-16, -16), (0, -16), (-16, 0), (0, 0)],
                [(-16, -16), (0, -16), (-16, 0), (0, 0), (-8, -8)], [(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -8), (0, -8)],
                [(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -16), (0, -16), (-8, 0)], 
                [(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -16), (0, -16), (-16, 0), (0, 0)])
VISIT_OFFSETS = ("Dummy", [(-16, 0)], [(-16, -48), (+32, 0)], [(-16, -76), (-16, -20), (+32, 0)], [(-16, -76), (-16, 20), (+4, 0), (+60, 0)],
                [(-16, -76), (-16, 20), (+4, 0), (+60, 0), (-16, 0)], [(-16, -76), (-16, 20), (+4, 0), (+60, 0), (-16, -48), (+32, 0)],
                [(-16, -76), (-16, 20), (+4, 0), (+60, 0), (-16, -76), (-16, -20), (+32, 0)],
                [(-16, -76), (-16, 20), (+4, 0), (+60, 0), (-16, -76), (-16, 20), (+4, 0), (+60, 0)]
)

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.box = None
        self.inner_box = None
        self.info = None
        self.hovered = None
    def update(self, info):
        self.info = info
        self.hovered = False
        if self.box.collidepoint(pg.mouse.get_pos()):
            self.hovered = True
    def draw_players(self, window, centerx, centery, player_list):
        position_vector = PLAYER_OFFSETS[len(player_list)]
        for i, icon in enumerate(player_list):
            posx, posy = position_vector[i]
            window.blit(Assets.ICONS["SMALL"][icon], (centerx + posx, centery + posy))

class VerticalTile(Tile):
    def __init__(self, x, y, side):
        super().__init__(x, y)
        self.box = pg.rect.Rect((x, y), (SIDE_SMALL, SIDE_LARGE))
        self.inner_box = pg.rect.Rect((x + BORDER_SIZE, y + BORDER_SIZE), (SIDE_SMALL - 2*BORDER_SIZE, SIDE_LARGE - 2*BORDER_SIZE))
        self.side = side
    def draw(self, window, selected=False):
        if selected:
            pg.draw.rect(window, Colors.SELECTED, self.box)
        else:
            pg.draw.rect(window, Colors.BLACK, self.box)
        if self.info is not None:
            pg.draw.rect(window, self.info["color"], self.inner_box)
            if self.info["type"] == "icon":
                window.blit(self.info["image"], (self.box.centerx - 16, self.box.centery - 16))
                self.draw_players(window, self.box.centerx, self.box.centery, self.info["players"])
            if self.info["type"] == "property":
                if self.side == "T":
                    basex, basey = self.inner_box.left + 1, self.inner_box.bottom - 13
                    centerx, centery = self.inner_box.centerx, self.inner_box.centery - int(13/2)
                elif self.side == "B":
                    basex, basey = self.inner_box.left + 1, self.inner_box.top
                    centerx, centery = self.inner_box.centerx, self.inner_box.centery + int(13/2)
                if self.info["houses"] == 5:
                    window.blit(Assets.HOTEL_HORIZONTAL, (basex, basey))
                else:
                    for i in range(4):
                        if i < self.info["houses"]:
                            window.blit(Assets.HOUSE_FILLED, (basex + i * 13, basey))
                        else:
                            window.blit(Assets.HOUSE_EMPTY, (basex + i * 13, basey))
                if self.info["mortaged"]:
                    window.blit(Assets.MORTAGED, (centerx - 16, centery - 16))
                self.draw_players(window, centerx, centery, self.info["players"])

class HorizontalTile(Tile):
    def __init__(self, x, y, side):
        super().__init__(x, y)
        self.box = pg.rect.Rect((x, y), (SIDE_LARGE, SIDE_SMALL))
        self.inner_box = pg.rect.Rect((x + BORDER_SIZE, y + BORDER_SIZE), (SIDE_LARGE - 2*BORDER_SIZE, SIDE_SMALL - 2*BORDER_SIZE))
        self.side = side
    def draw(self, window, selected=False):
        if selected:
            pg.draw.rect(window, Colors.SELECTED, self.box)
        else:
            pg.draw.rect(window, Colors.BLACK, self.box)
        if self.info is not None:
            pg.draw.rect(window, self.info["color"], self.inner_box)
            if self.info["type"] == "icon":
                window.blit(self.info["image"], (self.box.centerx - 16, self.box.centery - 16))
                self.draw_players(window, self.box.centerx, self.box.centery, self.info["players"])
            if self.info["type"] == "property":
                if self.side == "L":
                    basex, basey = self.inner_box.right - 13, self.inner_box.top + 1
                    centerx, centery = self.inner_box.centerx - int(13/2), self.inner_box.centery
                elif self.side == "R":
                    basex, basey = self.inner_box.left, self.inner_box.top + 1
                    centerx, centery = self.inner_box.centerx + int(13/2), self.inner_box.centery
                if self.info["houses"] == 5:
                    window.blit(Assets.HOTEL_HORIZONTAL, (basex, basey))
                else:
                    for i in range(4):
                        if i < self.info["houses"]:
                            window.blit(Assets.HOUSE_FILLED, (basex, basey + i * 13))
                        else:
                            window.blit(Assets.HOUSE_EMPTY, (basex, basey + i * 13))
                if self.info["mortaged"]:
                    window.blit(Assets.MORTAGED, (centerx - 16, centery - 16))
                self.draw_players(window, centerx, centery, self.info["players"])

class CornerTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.box = pg.rect.Rect((x, y), (SIDE_LARGE, SIDE_LARGE))
        self.inner_box = pg.rect.Rect((x + BORDER_SIZE, y + BORDER_SIZE), (SIDE_LARGE - 2*BORDER_SIZE, SIDE_LARGE - 2*BORDER_SIZE))
    def draw(self, window, selected=False):
        if selected:
            pg.draw.rect(window, Colors.SELECTED, self.box)
        else:
            pg.draw.rect(window, Colors.BLACK, self.box)
        if self.info is not None and self.info["type"] == "corner":
            pg.draw.rect(window, self.info["color"], self.inner_box)
            window.blit(self.info["image"], self.inner_box)
            if self.info["jail"]:
                self.draw_players(window, self.inner_box.right - 40, self.inner_box.top + 40, self.info["jailed"])
                position_vector = VISIT_OFFSETS[len(self.info["players"])]
                for i, icon in enumerate(self.info["players"]):
                    posx, posy = position_vector[i]
                    centerx, centery = self.inner_box.left + 16, self.inner_box.top + 80
                    window.blit(Assets.ICONS["SMALL"][icon], (centerx + posx, centery + posy))
            else:
                self.draw_players(window, self.box.centerx, self.box.centery, self.info["players"])