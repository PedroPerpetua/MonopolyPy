import pygame as pg
from lib.assets import Assets

TOP = 80
SIZE = 129

PLAYER_POSITIONS_OFFSET = [ "Dummy!",
							[(-16,-16)], [(-32, -16), (0, -16)], [(-32, -32), (0, -32), (-16, 0)], [(-32, -32), (0, -32), (-32, 0), (0, 0)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-16,-16)], [(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -16), (0, -16)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -32), (0, -32), (-16, 0)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -32), (0, -32), (-32, 0), (0, 0)]
							]
class IconTile:
	def __init__(self, x, y, orientation, image, bg_color):
		self.image = image
		self.bg_color = bg_color
		if orientation in ["L", "R"]:
			self.box = pg.Rect((x, y), (SIZE, TOP))
			self.image_offset = (32, 8)
			self.player_offset = (65, 40)
		elif orientation in ["T", "B"]:
			self.box = pg.Rect((x, y), (TOP, SIZE))
			self.image_offset = (8, 32)
			self.player_offset = (40, 65)

	def update_info(self, _):
		pass

	def update(self, _):
		pass

	def draw(self, window, player_list):
		pg.draw.rect(window, self.bg_color, self.box)
		offset_x, offset_y = self.image_offset
		window.blit(self.image, (self.box.left + offset_x, self.box.top + offset_y))

		positions = PLAYER_POSITIONS_OFFSET[len(player_list)]
		offset_x, offset_y = self.player_offset
		for i in range(len(player_list)):
			p_offset_x, p_offset_y = positions[i]
			window.blit(Assets.ICONS[player_list[i]], (self.box.left + offset_x + p_offset_x, self.box.top + offset_y + p_offset_y))