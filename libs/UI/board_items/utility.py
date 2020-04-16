import pygame as pg

COLORKEY = (255, 0, 255)
BG_COLOR = LIGHT_PURPLE = (255, 178, 102)
TOP = 80
SIZE = 129

class BoardUtility:
	def __init__(self, orientation, u_type):
		if u_type == "Water Company":
			icon = pg.image.load("libs/assets/company_water.png").convert()
		elif u_type == "Electric Company":
			icon = pg.image.load("libs/assets/company_electricity.png").convert()
		icon.set_colorkey(COLORKEY)

		if orientation in ["L", "R"]:
			self.surface = pg.Surface((SIZE, TOP))
			icon_x = 32
			icon_y = 8
		elif orientation in ["T", "B"]:
			self.surface = pg.Surface((TOP, SIZE))
			icon_x = 8
			icon_y = 32

		self.surface.fill(BG_COLOR)
		self.surface.blit(icon, (icon_x, icon_y))

	def update(self, _):
		pass

	def get_surface(self):
		return self.surface