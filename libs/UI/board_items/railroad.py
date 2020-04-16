import pygame as pg

TOP = 80
SIZE = 129
BG_COLOR = LIGHT_GRAY = (128, 128, 128)
COLORKEY = (255, 0, 255)

class BoardRailroad:
	def __init__(self, orientation):
		train = pg.image.load("libs/assets/train.png").convert()
		train.set_colorkey(COLORKEY)
		if orientation in ["L", "R"]:
			self.surface = pg.Surface((SIZE, TOP))
			train_x = 32
			train_y = 8
		elif orientation in ["T", "B"]:
			self.surface = pg.Surface((TOP, SIZE))
			train_x = 8
			train_y = 32
		self.surface.fill(BG_COLOR)
		self.surface.blit(train, (train_x, train_y))

	def update(self, _):
		pass

	def get_surface(self):
		return self.surface