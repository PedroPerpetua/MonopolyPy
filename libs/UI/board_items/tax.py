import pygame as pg

COLORKEY = (255, 0, 255)
BG_COLOR = LIGHT_GREEN = (153, 255, 153)
TOP = 80
SIZE = 129

class BoardTax:
	def __init__(self, orientation, t_type):
		if t_type == "Luxury Tax":
			icon = pg.image.load("libs/assets/tax_luxury.png").convert()
		elif t_type == "Income Tax":
			icon = pg.image.load("libs/assets/tax_income.png").convert()
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