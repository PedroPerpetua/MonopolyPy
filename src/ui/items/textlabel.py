import pygame as pg

TEXT_COLOR = BLACK = (0, 0, 0)

class TextLabel:
	def __init__(self, x, y, text, font_size, font):
		# Text related vars:
		font = pg.font.Font(font, font_size)
		self.surface = font.render(text, True, TEXT_COLOR)

		# Draw related vars:
		self.x = x
		self.y = y

	def draw(self, window):
		window.blit(self.surface, (self.x, self.y))

	def update(self, _):
		pass