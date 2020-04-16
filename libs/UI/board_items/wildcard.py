import pygame as pg

COLORKEY = (255, 0, 255)
LIGHT_RED = (255, 102, 102)
LIGHT_BLUE = (153, 204, 255)
TOP = 80
SIZE = 129

class BoardWildCard:
	def __init__(self, orientation, w_type):
		if orientation in ["L", "R"]:
			self.surface = pg.Surface((SIZE, TOP))
			icon_x = 32
			icon_y = 8
		elif orientation in ["T", "B"]:
			self.surface = pg.Surface((TOP, SIZE))
			icon_x = 8
			icon_y = 32

		if w_type == "Luck":
			icon = pg.image.load("libs/assets/luck.png").convert()
			self.surface.fill(LIGHT_RED)
		elif w_type == "Community Chest":
			icon = pg.image.load("libs/assets/community_chest.png").convert()
			self.surface.fill(LIGHT_BLUE)
		icon.set_colorkey(COLORKEY)
		
		self.surface.blit(icon, (icon_x, icon_y))

	def update(self, _):
		pass

	def get_surface(self):
		return self.surface
