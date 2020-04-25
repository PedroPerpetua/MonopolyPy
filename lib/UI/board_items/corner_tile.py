import pygame as pg
import lib.UI.board_items.constants as c
from lib.assets import Assets

WHITE = (255, 255, 255)

class CornerTile:
	# These have to be hard coded because of how position changes in the jail tile
	VISITING_POSITIONS_OFFSET = [ "Dummy!",
							[(-16, 0)], [(-16, -48), (+32, 0)], [(-16, -80), (-16, -16), (+32, 0)], [(-16, -80), (-16, -16), (0, 0), (+44, 0)],
							[(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, 0)], [(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, -48), (+32, 0)],
							[(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, -80), (-16, -16), (+32, 0)],
							[(-16, -80), (-16, -16), (0, 0), (+44, 0), (-16, -80), (-16, -16), (0, 0), (+44, 0)]
							]

	JAIL_CENTER = (56, 40)
	VISITING_CENTER = (16, 80)
	SIDE = c.SIDE_LARGE - c.BORDER_SIZE * 2

	def __init__(self, x, y, image, jail=False):
		self.box = pg.Rect((x,y), (CornerTile.SIDE, CornerTile.SIDE))
		self.image = image
		self.jail = jail
		self.hovered = False

		self.info = None
		# Info should contain: icons (players standing here), jailed (players jailed)


	def get_hovered(self):
		return self.hovered


	# Drawing Functions
	def update(self, game_info):
		self.hovered = False
		if self.box.collidepoint(pg.mouse.get_pos()):
			self.hovered = True

		self.info = game_info

	def draw(self, window):
		pg.draw.rect(window, WHITE, self.box)
		window.blit(self.image, self.box)

		if self.jail:
			# Drawing the jailed players
			positions = c.PLAYER_POSITIONS_OFFSET[len(self.info["jailed"])]
			x, y = CornerTile.JAIL_CENTER
			for i in range(len(self.info["jailed"])):
				offset_x, offset_y = positions[i]
				window.blit(Assets.ICONS[self.info["jailed"][i]], (self.box.left + x + offset_x, self.box.top + y + offset_y))

			positions = CornerTile.VISITING_POSITIONS_OFFSET[len(self.info["icons"])]
			x, y = CornerTile.VISITING_CENTER
			for i in range(len(self.info["icons"])):
				offset_x, offset_y = positions[i]
				window.blit(Assets.ICONS[self.info["icons"][i]], (self.box.left + x + offset_x, self.box.top + y + offset_y))
		else:
			positions = c.PLAYER_POSITIONS_OFFSET[len(self.info["icons"])]
			for i in range(len(self.info["icons"])):
				offset_x, offset_y = positions[i]
				window.blit(Assets.ICONS[self.info["icons"][i]], (self.box.centerx + offset_x, self.box.centery + offset_y))