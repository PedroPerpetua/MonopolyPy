import pygame as pg

COLORKEY = (255, 0, 255)
WHITE = (255, 255, 255)
TOP = 80
SIZE = 129

class BoardCorner:
	def __init__(self, orientation, c_type):
		self.surface = pg.Surface((SIZE, SIZE))
		self.surface.fill(WHITE)
		if c_type == "Start":
			print("Started")
			icon = pg.image.load("libs/assets/corner_start.png").convert()
			icon.set_colorkey(COLORKEY)
			self.surface.blit(icon, (0,0))

	def update(self, _):
		pass

	def get_surface(self):
		return self.surface