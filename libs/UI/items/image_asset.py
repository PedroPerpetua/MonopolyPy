import pygame as pg

COLOR_KEY = (255,0,255)
class ImageAsset:
	def __init__(self, x, y, image, alignment="L"):
		self.image = pg.image.load(f"libs/assets/{image}.png").convert()
		self.image.set_colorkey(COLOR_KEY)
		if alignment == "L":
			self.x = x
			self.y = y
		elif alignment == "C":
			image_rect = self.image.get_rect()
			self.x = x - image_rect.centerx
			self.y = y - image_rect.centery

	def draw(self, window):
		window.blit(self.image, (self.x, self.y))

	def update(self, events):
		pass