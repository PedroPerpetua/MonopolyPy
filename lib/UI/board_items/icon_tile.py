import pygame as pg
import lib.UI.board_items.constants as c
from lib.assets import Assets



class IconTile:
	SIDE_LARGE = c.SIDE_LARGE - c.BORDER_SIZE * 2
	SIDE_SMALL = c.SIDE_SMALL - c.BORDER_SIZE * 2

	def __init__(self, x, y, orientation):
		if orientation in ["L", "R"]:
			self.box = pg.Rect((x, y), (IconTile.SIDE_LARGE, IconTile.SIDE_SMALL))
		elif orientation in ["T", "B"]:
			self.box = pg.Rect((x, y), (IconTile.SIDE_SMALL, IconTile.SIDE_LARGE))
		self.hovered = False

		self.info = None
		# Info should contain: icons (players standing here)


	def get_hovered(self):
		return self.hovered
	def get_border(self):
		return ((self.box.left - c.BORDER_SIZE * 2, self.box.top - c.BORDER_SIZE * 2),
			(self.box.width + c.BORDER_SIZE * 4, self.box.height + c.BORDER_SIZE * 4))


	# Drawing functions
	def update(self, game_info):
		self.hovered = False
		if self.box.collidepoint(pg.mouse.get_pos()):
			self.hovered = True
		self.info = game_info

	def draw(self, window):
		pg.draw.rect(window, self.info["color"], self.box)
		offset_x, offset_y = c.IMAGE_OFFSET
		window.blit(self.info["image"], (self.box.centerx + offset_x, self.box.centery + offset_y))

		positions = c.PLAYER_POSITIONS_OFFSET[len(self.info["players"])]
		for i in range(len(self.info["players"])):
			offset_x, offset_y = positions[i]
			window.blit(Assets.ICONS[self.info["players"][i]], (self.box.centerx + offset_x, self.box.centery + offset_y))

	