import pygame as pg
from lib.UI.board_items.tile import HorizontalTile, VerticalTile, CornerTile
from lib.UI.board_items.tooltip import Tooltip

COORDS = [
				(602, 602), (546, 602), (490, 602), (434, 602), (378, 602), (322, 602), (266, 602), (210, 602), (154, 602), (98, 602), (0, 602),
				(0, 546), (0, 490), (0, 434), (0, 378), (0, 322), (0, 266), (0, 210), (0, 154), (0, 98), (0, 0),
				(98, 0), (154, 0), (210, 0), (266, 0), (322, 0), (378, 0), (434, 0), (490, 0), (546, 0), (602, 0),
				(602, 98), (602, 154), (602, 210), (602, 266), (602, 322), (602, 378), (602, 434), (602, 490), (602, 546)
]
class Board:
	def __init__(self, x, y, control_area, game):
		self.game = game
		self.x = x
		self.y = y
		self.tiles = []
		for i in range(40):
			xcoord, ycoord = x + COORDS[i][0], y + COORDS[i][1]
			if i in [0, 10, 20, 30]:
				tile = CornerTile(xcoord, ycoord)
			if i in range(1, 10):
				tile = VerticalTile(xcoord, ycoord, 'B')
			if i in range(11, 20):
				tile = HorizontalTile(xcoord, ycoord, 'L')
			if i in range(21, 30):
				tile = VerticalTile(xcoord, ycoord, 'T')
			if i in range(31, 40):
				tile = HorizontalTile(xcoord, ycoord, 'R')
			tile.update(game.get_fieldInfo(i))
			self.tiles.append(tile)
		self.control_box = pg.rect.Rect((x, y), control_area)
		self.selected = None
		self.tooltip = Tooltip(x + 112, y + 492)	
	def update(self, events):
		tile_hovered = None
		for i in range(40):
			tile = self.tiles[i]
			tile.update(self.game.get_fieldInfo(i))
			if tile.hovered:
				tile_hovered = i
		if tile_hovered is not None:
			self.tooltip.update_info(self.game.get_tooltipInfo(tile_hovered))
		else:
			self.tooltip.update_info(None)
		for event in events:
			if event.type == pg.MOUSEBUTTONDOWN and self.control_box.collidepoint(event.pos):
				self.selected = tile_hovered
	def draw(self, window):
		for i in range(40):
			if i == self.selected:
				self.tiles[i].draw(window, True)
			else:
				self.tiles[i].draw(window)
		self.tooltip.draw(window)