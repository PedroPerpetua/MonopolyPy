import pygame as pg
from game.game import Game
from libs.UI.board_items.property import BoardProperty
from libs.UI.board_items.railroad import BoardRailroad
from libs.UI.board_items.utility import BoardUtility
from libs.UI.board_items.wildcard import BoardWildCard
from libs.UI.board_items.tax import BoardTax
from libs.UI.board_items.corner import BoardCorner

# NOTE: SIZES ARE SCALLED TO 1920:1080 SCREENS

SIZE = 1000
TILE_COLOR = WHITE = (255,255,255)
BORDER_COLOR = BLACK = (0,0,0)
SIDE = 131
TOP = 82


POSITIONS = [
			(869,869), (787,869), (705, 869), (623, 869), (541, 869), (459, 869), (377, 869), (295, 869), (213, 869), (131, 869),
			(0, 869), (0, 787), (0, 705), (0, 623), (0, 541), (0, 459), (0, 377), (0, 295), (0, 213), (0, 131), (0, 0),
			(131, 0), (213, 0), (295, 0), (377, 0), (459, 0), (541, 0), (623, 0), (705, 0), (787, 0), (869, 0),
			(869, 131), (869, 213), (869, 295), (869, 377), (869, 459), (869, 541), (869, 623), (869, 705), (869, 787)
			]


class Board:
	def __init__(self, x, y, game, alignment = "L"):
		self.game = game
		if alignment == "L":
			self.x = x
			self.y = y
		elif alignment == "C":
			self.x = x - int(SIZE/2)
			self.y = y - int(SIZE/2)

		self.tiles = self.setup_tiles()
		self.players_position = []

	def setup_tiles(self):
		fields = []
		for i in range(40):
			field_type = self.game.get_type(i)
			if 0 < i < 10:
				orientation = "B"
			elif 10 < i < 20:
				orientation = "L"
			elif 20 < i < 30:
				orientation = "T"
			else:
				orientation = "R"

			if field_type == "Property":
				fields.append(BoardProperty(orientation))
			elif field_type == "Railroad":
				fields.append(BoardRailroad(orientation))
			elif field_type  in ["Water Company", "Electric Company"]:
				fields.append(BoardUtility(orientation, field_type))
			elif field_type in ["Luck", "Community Chest"]:
				fields.append(BoardWildCard(orientation, field_type))
			elif field_type in ["Income Tax", "Luxury Tax"]:
				fields.append(BoardTax(orientation, field_type))
			elif field_type in ["Start", "Jail", "Free Parking", "Go to jail!"]:
				fields.append(BoardCorner(orientation, field_type))
		return fields

	def draw_border(self, window):
		pg.draw.rect(window, BORDER_COLOR, ((self.x, self.y), (SIZE, SIDE)))
		pg.draw.rect(window, BORDER_COLOR, ((self.x, self.y), (SIDE, SIZE)))
		pg.draw.rect(window, BORDER_COLOR, ((self.x, self.y + SIZE - SIDE), (SIZE, SIDE)))
		pg.draw.rect(window, BORDER_COLOR, ((self.x + SIZE - SIDE, self.y), (SIDE, SIZE)))

	def draw_tile(self, window, pos):
		x, y = POSITIONS[pos]
		x = x + self.x + 1
		y = y + self.y + 1
		# First we draw the tile
		tile = self.tiles[pos]
		info, players = self.game.get_info(pos)
		tile.update(info)
		window.blit(tile.get_surface(players), (x, y))

	def draw(self, window):
		self.draw_border(window)
		for i in range(40):
			self.draw_tile(window, i)

	def update(self, events):
		pass