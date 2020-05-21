import pygame as pg
import lib.UI.board_items.constants as c
from lib.assets import Assets

WHITE = (255, 255, 255)

class CornerTile:
	# These have to be hard coded because of how position changes in the jail tile
	VISITING_POSITIONS_OFFSET = ["Dummy!",
							[(-16, 0)], [(-16, -48), (+32, 0)], [(-16, -80), (-16, -16), (+32, 0)], [(-16, -80), (-16, -16), (0, 0), (+44, 0)],
							[(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, 0)], [(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, -48), (+32, 0)],
							[(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, -80), (-16, -16), (+32, 0)],
							[(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, -80), (-16, -16), (0, 0), (+44, 0)]
							]

	JAIL_CENTER = (56, 40)
	VISITING_CENTER = (16, 80)
	SIDE = c.SIDE_LARGE - c.BORDER_SIZE * 2

	def __init__(self, x, y):
		self.box = pg.Rect((x, y), (CornerTile.SIDE, CornerTile.SIDE))
		self.hovered = False
		self.info = None

	def get_border(self):
		return ((self.box.left - c.BORDER_SIZE * 2, self.box.top - c.BORDER_SIZE * 2),
			(self.box.width + c.BORDER_SIZE * 4, self.box.height + c.BORDER_SIZE * 4))


	# Drawing Functions
	def update(self, game_info):
		self.hovered = False
		if self.box.collidepoint(pg.mouse.get_pos()):
			self.hovered = True
		self.info = game_info

	def draw(self, window):
		pg.draw.rect(window, self.info["color"], self.box)
		window.blit(self.info["image"], self.box)

		if self.info["jail"]:
			# Drawing the jailed players
			positions = c.PLAYER_POSITIONS_OFFSET[len(self.info["jailed"])]
			x, y = CornerTile.JAIL_CENTER
			for i in range(len(self.info["jailed"])):
				offset_x, offset_y = positions[i]
				window.blit(Assets.ICONS[self.info["jailed"][i]], (self.box.left + x + offset_x, self.box.top + y + offset_y))

			positions = CornerTile.VISITING_POSITIONS_OFFSET[len(self.info["players"])]
			x, y = CornerTile.VISITING_CENTER
			for i in range(len(self.info["players"])):
				offset_x, offset_y = positions[i]
				window.blit(Assets.ICONS[self.info["players"][i]], (self.box.left + x + offset_x, self.box.top + y + offset_y))
		else:
			positions = c.PLAYER_POSITIONS_OFFSET[len(self.info["players"])]
			for i in range(len(self.info["players"])):
				offset_x, offset_y = positions[i]
				window.blit(Assets.ICONS[self.info["players"][i]], (self.box.centerx + offset_x, self.box.centery + offset_y))