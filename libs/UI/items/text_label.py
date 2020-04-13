import pygame as pg
import os.path

TEXT_COLOR = BLACK = (0,0,0)

class TextLabel:
	def __init__(self, x, y, text, font_size, font, alignment="C"):
		# Text related vars:
		if not os.path.isfile(font):
			font = pg.font.match_font(font)
		font = pg.font.Font(font, font_size)
		self.surface = font.render(text, True, TEXT_COLOR)

		# Draw related vars:
		if alignment == "L":
			self.x = x
			self.y = y
		elif alignment == "C":
			text_rect = self.surface.get_rect()
			self.x = x - text_rect.centerx
			self.y = y - text_rect.centery

	def draw(self, window):
		window.blit(self.surface, (self.x, self.y))

	def update(self, events):
		pass