import pygame as pg
from src.game.game import Game

from lib.UI.board_items.icon_tile import IconTile
from lib.UI.board_items.property_tile import PropertyTile
from lib.UI.board_items.corner_tile import CornerTile
from lib.assets import Assets


# NOTE: SIZES ARE SCALLED TO 1920:1080 SCREENS
SIZE = 700
SIDE = 98
TOP = 56

BORDER_COLOR = BLACK = (0,0,0)
LIGHT_GRAY = (128, 128, 128)
LIGHT_CYAN = (153, 255, 255)
WHITE = (255,255,255)

POSITIONS = [
			(602,602), (546,602), (490, 602), (434, 602), (378, 602), (322, 602), (266, 602), (210, 602), (154, 602), (98, 602),
			(0, 602), (0, 546), (0, 490), (0, 434), (0, 378), (0, 322), (0, 266), (0, 210), (0, 154), (0, 98), (0, 0),
			(98, 0), (154, 0), (210, 0), (266, 0), (322, 0), (378, 0), (434, 0), (490, 0), (546, 0), (602, 0),
			(602, 98), (602, 154), (602, 210), (602, 266), (602, 322), (602, 378), (602, 434), (602, 490), (602, 546)
			]


class Board:
	def __init__(self, x, y, game):
		self.game = game
		self.x = x
		self.y = y

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
			
			x, y = POSITIONS[i]
			x += self.x + 1
			y += self.y + 1

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

	def draw_border(self, window):
		pg.draw.rect(window, BORDER_COLOR, ((self.x, self.y), (SIZE, SIDE)))
		pg.draw.rect(window, BORDER_COLOR, ((self.x, self.y), (SIDE, SIZE)))
		pg.draw.rect(window, BORDER_COLOR, ((self.x, self.y + SIZE - SIDE), (SIZE, SIDE)))
		pg.draw.rect(window, BORDER_COLOR, ((self.x + SIZE - SIDE, self.y), (SIDE, SIZE)))

	def draw_tile(self, window, pos):
		if pos == 10: # Jail
			info, players, jailed = self.game.get_info(pos)
			self.tiles[pos].draw(window, players, jailed)
		else:
			info, players = self.game.get_info(pos)
			self.tiles[pos].update_info(info)
			self.tiles[pos].draw(window, players)

	def draw_tooltip(self, window, pos):
		self.tiles[pos].draw_tooltip(window)

	def draw(self, window):
		self.draw_border(window)
		for i in range(40):
			self.draw_tile(window, i)
		# We can only check for tooltips after we've drawn all of them, so it's always on top
		for i in range(40):
			self.draw_tooltip(window, i)

	def update(self, events):
		for i in range(40):
			self.tiles[i].update(events)

