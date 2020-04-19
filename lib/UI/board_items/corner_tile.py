import pygame as pg
from lib.assets import Assets

SIZE = 129
WHITE = (255, 255, 255)

PLAYER_POSITIONS_OFFSET = [	"Dummy!",
							[(-16,-16)], [(-32, -16), (0, -16)], [(-32, -32), (0, -32), (-16, 0)], [(-32, -32), (0, -32), (-32, 0), (0, 0)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-16,-16)], [(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -16), (0, -16)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -32), (0, -32), (-16, 0)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -32), (0, -32), (-32, 0), (0, 0)]
							]

VISITING_POSITIONS_OFFSET = [ "Dummy!",
							[(-32, 0)], [(-32, -64), (+32, 0)], [(-32, -97), (-32, -32), (+32, 0)], [(-32, -97), (-32, -32), (0, 0), (+65, 0)],
							[(-32, -97), (-32, -32), (0, 0), (+65, 0), (-32, 0)], [(-32, -97), (-32, -32), (0, 0), (+65, 0), (-32, -64), (+32, 0)],
							[(-32, -97), (-32, -32), (0, 0), (+65, 0), (-32, -97), (-32, -32), (+32, 0)],
							[(-32, -97), (-32, -32), (0, 0), (+65, 0), (-32, -97), (-32, -32), (0, 0), (+65, 0)]
							]


class CornerTile:
	def __init__(self, x, y, image, jail=False):
		self.box = pg.Rect((x,y), (SIZE, SIZE))
		self.image = image
		self.jail = jail

	def update(self, _):
		pass

	def update_info(self, _):
		pass


	def draw(self, window, player_list, jailed_list=[]):
		pg.draw.rect(window, WHITE, self.box)
		window.blit(self.image, self.box)

		if self.jail:
			positions = PLAYER_POSITIONS_OFFSET[len(jailed_list)]
			offset_x, offset_y = 81, 49
			for i in range(len(jailed_list)):
				p_offset_x, p_offset_y = positions[i]
				window.blit(Assets.ICONS[jailed_list[i]], (self.box.left + offset_x + p_offset_x, self.box.top + offset_y + p_offset_y))

			positions = VISITING_POSITIONS_OFFSET[len(player_list)]
			offset_x, offset_y = 32, 97
			for i in range(len(player_list)):
				p_offset_x, p_offset_y = positions[i]
				window.blit(Assets.ICONS[player_list[i]], (self.box.left + offset_x + p_offset_x, self.box.top + offset_y + p_offset_y))
		else:
			positions = PLAYER_POSITIONS_OFFSET[len(player_list)]
			offset_x, offset_y = 65, 65
			for i in range(len(player_list)):
				p_offset_x, p_offset_y = positions[i]
				window.blit(Assets.ICONS[player_list[i]], (self.box.left + offset_x + p_offset_x, self.box.top + offset_y + p_offset_y))