import pygame as pg
import lib.UI.board_items.constants as c
from lib.assets import Assets


class PropertyTile:
	SIDE_LARGE = c.SIDE_LARGE - c.BORDER_SIZE * 2
	SIDE_SMALL = c.SIDE_SMALL - c.BORDER_SIZE * 2

	def __init__(self, x, y, orientation, color):
		self.color = c.get_rgb(color)
		# Calculate the positions based on landscape or portrait
		self.box, self.offsets = self.map_positions((x, y), orientation)
		self.hovered = False

		self.info = {}
		# Info should contain: color, icons (players standing here), houses, mortaged


	def map_positions(self, position, orientation):
		pos = {}
		pos["houses"] = c.HOUSE_OFFSETS[orientation]
		pos["center"] = c.CENTER_OFFSETS[orientation]
		if orientation in ["L", "R"]:
			pos["hotel"] = Assets.HOTEL_PORTRAIT
			box = pg.Rect(position, (PropertyTile.SIDE_LARGE, PropertyTile.SIDE_SMALL))
		if orientation in ["T", "B"]:
			pos["hotel"] = Assets.HOTEL_LANDSCAPE
			box = pg.Rect(position, (PropertyTile.SIDE_SMALL, PropertyTile.SIDE_LARGE))
		return (box, pos)

	def get_hovered(self):
		return self.hovered


	# Drawing functions
	def update(self, info):
		self.hovered = False
		if self.box.collidepoint(pg.mouse.get_pos()):
			self.hovered = True

		self.info = info

	def draw(self, window):
		pg.draw.rect(window, self.color, self.box)
		num_houses = self.info["houses"]
		if num_houses == 5:
			offset_x = self.offsets["houses"]["x"][5]
			offset_y = self.offsets["houses"]["y"][5]
			window.blit(self.offsets["hotel"], (self.box.left + offset_x, self.box.top + offset_y))
		else:
			for i in range(1, 5):
				offset_x = self.offsets["houses"]["x"][i]
				offset_y = self.offsets["houses"]["y"][i]
				if i <= num_houses:
					window.blit(Assets.HOUSE_FILLED, (self.box.left + offset_x, self.box.top + offset_y))
				else:
					window.blit(Assets.HOUSE_EMPTY, (self.box.left + offset_x, self.box.top + offset_y))
		if self.info["mortaged"]:
			x, y = self.offsets["center"]
			offset_x, offset_y = c.IMAGE_OFFSET
			window.blit(Assets.MORTAGED, (self.box.left + x + offset_x, self.box.top + y + offset_y))

		positions = c.PLAYER_POSITIONS_OFFSET[len(self.info["icons"])]
		x, y = self.offsets["center"]
		for i in range(len(self.info["icons"])):
			offset_x, offset_y = positions[i]
			window.blit(Assets.ICONS[self.info["icons"][i]], (self.box.left + x + offset_x, self.box.top + y + offset_y))