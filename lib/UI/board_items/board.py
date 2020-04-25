import pygame as pg
from src.game.game import Game

from lib.UI.board_items.icon_tile import IconTile
from lib.UI.board_items.property_tile import PropertyTile
from lib.UI.board_items.corner_tile import CornerTile
from lib.UI.board_items.tooltip import Tooltip
from lib.assets import Assets
import lib.UI.board_items.constants as c

# Readability
XVAR = 0
YVAR = 1

# Colors
BORDER_COLOR = BLACK = (0,0,0)
LIGHT_GRAY = (128, 128, 128)
LIGHT_CYAN = (153, 255, 255)
WHITE = (255,255,255)
BG_GREEN = (143,188,114)

class Board:
	#Pairs of (x(i, j), y(i, j) corresponding to the offset of LARGE*i + SMALL*j, counting form the top right corner (x,y).
	POS_VECTORS	= [
				((1, 9), (1, 9)), ((1, 8), (1, 9)), ((1, 7), (1, 9)), ((1, 6), (1, 9)), ((1, 5), (1, 9)), ((1, 4), (1, 9)), ((1, 3), (1, 9)),
				((1, 2), (1, 9)), ((1, 1), (1, 9)), ((1, 0), (1, 9)), ((0, 0), (1, 9)), ((0, 0), (1, 8)), ((0, 0), (1, 7)), ((0, 0), (1, 6)),
				((0, 0), (1, 5)), ((0, 0), (1, 4)), ((0, 0), (1, 3)), ((0, 0), (1, 2)), ((0, 0), (1, 1)), ((0, 0), (1, 0)), ((0, 0), (0, 0)),
				((1, 0), (0, 0)), ((1, 1), (0, 0)), ((1, 2), (0, 0)), ((1, 3), (0, 0)), ((1, 4), (0, 0)), ((1, 5), (0, 0)), ((1, 6), (0, 0)),
				((1, 7), (0, 0)), ((1, 8), (0, 0)), ((1, 9), (0, 0)), ((1, 9), (1, 0)), ((1, 9), (1, 1)), ((1, 9), (1, 2)), ((1, 9), (1, 3)),
				((1, 9), (1, 4)), ((1, 9), (1, 5)), ((1, 9), (1, 6)), ((1, 9), (1, 7)), ((1, 9), (1, 8))
				]	

	def __init__(self, x, y, game):
		self.game = game
		self.x = x
		self.y = y

		self.tiles = self.setup_tiles((x, y))
		self.players_position = []

		self.tooltip = Tooltip(x, y)

	def setup_tiles(self, coords):
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
			
			vector = Board.POS_VECTORS[i]
			x = vector[XVAR][0] * c.SIDE_LARGE + vector[XVAR][1] * c.SIDE_SMALL + c.BORDER_SIZE + coords[XVAR]
			y = vector[YVAR][0] * c.SIDE_LARGE + vector[YVAR][1] * c.SIDE_SMALL + c.BORDER_SIZE + coords[YVAR]

			# Why does python not have switch statements. This is so ugly.
			if field_type == "Property":
				fields.append(PropertyTile(x, y, orientation, self.game.get_color(i)))
			elif field_type == "Railroad":
				fields.append(IconTile(x, y, orientation, Assets.TRAIN, LIGHT_GRAY))
			elif field_type == "Water Company":
				fields.append(IconTile(x, y, orientation, Assets.COMPANY_WATER, LIGHT_CYAN))
			elif field_type == "Electric Company":
				fields.append(IconTile(x, y, orientation, Assets.COMPANY_ELECTRICITY, LIGHT_CYAN))
			elif field_type == "Luck":
				fields.append(IconTile(x, y, orientation, Assets.LUCK, WHITE))
			elif field_type == "Community Chest":
				fields.append(IconTile(x, y, orientation, Assets.COMMUNITY_CHEST, WHITE))
			elif field_type == "Income Tax":
				fields.append(IconTile(x, y, orientation, Assets.TAX_INCOME, WHITE))
			elif field_type == "Luxury Tax":
				fields.append(IconTile(x, y, orientation, Assets.TAX_LUXURY, WHITE))
			elif field_type == "Start":
				fields.append(CornerTile(x, y, Assets.CORNER_START))
			elif field_type == "Jail":
				fields.append(CornerTile(x, y, Assets.CORNER_JAIL, True))
			elif field_type == "Free Parking":
				fields.append(CornerTile(x, y, Assets.CORNER_FREEPARKING))
			elif field_type == "Go to jail!":
				fields.append(CornerTile(x, y, Assets.CORNER_GOTOJAIL))
			else:
				fields.append(None)
		return fields

	# Drawing functions
	def update(self, events):
		tile_hovered = None
		for i in range(40):
			tile = self.tiles[i]
			tile.update(self.game.get_info(i))
			if tile.get_hovered():
				tile_hovered = i
		if tile_hovered != None:
			self.tooltip.update(self.game.get_tooltip(tile_hovered))
		else:
			self.tooltip.update(None)


	def draw(self, window):
		# First we draw the border
		pg.draw.rect(window, BORDER_COLOR, ((self.x, self.y), (c.SIZE, c.SIZE)))
		side_interior = c.SIZE - 2 * c.SIDE_LARGE
		pg.draw.rect(window, BG_GREEN, ((self.x + c.SIDE_LARGE, self.y + c.SIDE_LARGE), (side_interior, side_interior)))
		x, y, w, h = self.tooltip.get_dimensions()
		pg.draw.rect(window, BORDER_COLOR, ((x - c.BORDER_SIZE, y - c.BORDER_SIZE), (w + 2 * c.BORDER_SIZE,h + 2 * c.BORDER_SIZE)))

		# Then we draw the tiles
		for i in range(40):
			self.tiles[i].draw(window)

		# And finally we draw the tooltip
		self.tooltip.draw(window)

	