import pygame as pg
from lib.assets import Assets

SIZE = 96
WHITE = (255, 255, 255)

PLAYER_POSITIONS_OFFSET = [ "Dummy!",
							[(-8,-8)], [(-16, -8), (0, -8)], [(-16, -16), (0, -16), (-8, 0)], [(-16, -16), (0, -16), (-16, 0), (0, 0)],
							[(-16, -16), (0, -16), (-16, 0), (0, 0), (-8,-8)], [(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -8), (0, -8)],
							[(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -16), (0, -16), (-8, 0)],
							[(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -16), (0, -16), (-16, 0), (0, 0)]
							]

VISITING_POSITIONS_OFFSET = [ "Dummy!",
							[(-16, 0)], [(-16, -48), (+32, 0)], [(-16, -80), (-16, -16), (+32, 0)], [(-16, -80), (-16, -16), (0, 0), (+44, 0)],
							[(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, 0)], [(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, -48), (+32, 0)],
							[(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, -80), (-16, -16), (+32, 0)],
							[(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, -80), (-16, -16), (0, 0), (+44, 0)]
							]

JAIL_CENTER = (56, 40)
VISITING_CENTER = (16, 80)

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
			x, y = JAIL_CENTER
			for i in range(len(jailed_list)):
				offset_x, offset_y = positions[i]
				window.blit(Assets.ICONS[jailed_list[i]], (self.box.left + x + offset_x, self.box.top + y + offset_y))

			positions = VISITING_POSITIONS_OFFSET[len(player_list)]
			x, y = VISITING_CENTER
			for i in range(len(player_list)):
				offset_x, offset_y = positions[i]
				window.blit(Assets.ICONS[player_list[i]], (self.box.left + x + offset_x, self.box.top + y + offset_y))
		else:
			positions = PLAYER_POSITIONS_OFFSET[len(player_list)]
			for i in range(len(player_list)):
				offset_x, offset_y = positions[i]
				window.blit(Assets.ICONS[player_list[i]], (self.box.centerx + offset_x, self.box.centery + offset_y))

				
	def draw_tooltip(self, window):
		pass