import pygame as pg
from lib.assets import Assets

TOP = 54
SIZE = 96

PLAYER_POSITIONS_OFFSET = [ "Dummy!",
							[(-8,-8)], [(-16, -8), (0, -8)], [(-16, -16), (0, -16), (-8, 0)], [(-16, -16), (0, -16), (-16, 0), (0, 0)],
							[(-16, -16), (0, -16), (-16, 0), (0, 0), (-8,-8)], [(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -8), (0, -8)],
							[(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -16), (0, -16), (-8, 0)],
							[(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -16), (0, -16), (-16, 0), (0, 0)]
							]
IMAGE_OFFSET = (-16, -16)

class IconTile:
	def __init__(self, x, y, orientation, image, bg_color):
		self.image = image
		self.bg_color = bg_color
		if orientation in ["L", "R"]:
			self.box = pg.Rect((x, y), (SIZE, TOP))
		elif orientation in ["T", "B"]:
			self.box = pg.Rect((x, y), (TOP, SIZE))

	def update_info(self, _):
		pass

	def update(self, _):
		pass

	def draw(self, window, player_list):
		pg.draw.rect(window, self.bg_color, self.box)
		offset_x, offset_y = IMAGE_OFFSET
		window.blit(self.image, (self.box.centerx + offset_x, self.box.centery + offset_y))

		positions = PLAYER_POSITIONS_OFFSET[len(player_list)]
		for i in range(len(player_list)):
			offset_x, offset_y = positions[i]
			window.blit(Assets.ICONS[player_list[i]], (self.box.centerx + offset_x, self.box.centery + offset_y))

	def draw_tooltip(self, window):
		pass