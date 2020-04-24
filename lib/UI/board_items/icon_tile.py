import pygame as pg
import lib.UI.board_items.constants as c
from lib.assets import Assets



class IconTile:
	SIDE_LARGE = c.SIDE_LARGE - c.BORDER_SIZE * 2
	SIDE_SMALL = c.SIDE_SMALL - c.BORDER_SIZE * 2

	def __init__(self, x, y, orientation, image, bg_color):
		self.image = image
		self.bg_color = bg_color
		if orientation in ["L", "R"]:
			self.box = pg.Rect((x, y), (IconTile.SIDE_LARGE, IconTile.SIDE_SMALL))
		elif orientation in ["T", "B"]:
			self.box = pg.Rect((x, y), (IconTile.SIDE_SMALL, IconTile.SIDE_LARGE))
		self.hovered = False

		self.info = None
		# Info should contain: icons (players standing here)

	def get_hovered(self):
		return self.hovered


	# Drawing functions
	def update(self, game_info):
		self.hovered = False
		if self.box.collidepoint(pg.mouse.get_pos()):
			self.hovered = True
		self.info = game_info

	def draw(self, window):
		pg.draw.rect(window, self.bg_color, self.box)
		offset_x, offset_y = c.IMAGE_OFFSET
		window.blit(self.image, (self.box.centerx + offset_x, self.box.centery + offset_y))

		positions = c.PLAYER_POSITIONS_OFFSET[len(self.info["icons"])]
		for i in range(len(self.info["icons"])):
			offset_x, offset_y = positions[i]
			window.blit(Assets.ICONS[self.info["icons"][i]], (self.box.centerx + offset_x, self.box.centery + offset_y))

	