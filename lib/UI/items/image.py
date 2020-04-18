import pygame as pg

class Image:
	def __init__(self, x, y, image):
		self.image = image
		self.x = x
		self.y = y

	def draw(self, window):
		window.blit(self.image, (self.x, self.y))

	def update(self, _):
		pass