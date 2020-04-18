import os.path
import pygame as pg
from lib.assets import Assets


BG_COLOR = WHITE = (255,255,255)
TEXT_COLOR = BLACK = (0,0,0)

class NumberPicker:
	def __init__(self, x, y, widht, minus_images, plus_images, default, min_num, max_num):
		# Text related vars:
		self.font = pg.font.Font(Assets.ARIAL, 20)
		self.minus_selected, self.minus_unselected = minus_images
		self.minus_highlight = False
		self.plus_selected, self.plus_unselected = plus_images
		self.plus_highligt = False

		# Drawing related vars:
		self.x = x
		self.y = y
		self.box = pg.Rect((x, y), (widht, 20))
		self.minus_box = pg.Rect((x, y), (20, 20))
		self.plus_box = pg.Rect((x + widht - 20, y), (20, 20))
		
		# Data related vars:
		self.value = default
		self.low = min_num
		self.high = max_num

	def draw(self, window):
		pg.draw.rect(window, BG_COLOR, self.box)
		if self.minus_highlight:
			window.blit(self.minus_selected, self.minus_box)
		else:
			window.blit(self.minus_unselected, self.minus_box)
		if self.plus_highligt:
			window.blit(self.plus_selected, self.plus_box)
		else:
			window.blit(self.plus_unselected, self.plus_box)

		text = self.font.render(str(self.value), True, TEXT_COLOR)
		text_rect = text.get_rect()
		window.blit(text, (self.box.centerx - text_rect.centerx, self.box.centery - text_rect.centery))

	def update(self, events):
		self.minus_highlight = False
		self.plus_highligt = False

		x,y = pg.mouse.get_pos()
		if self.minus_box.collidepoint(x, y):
			self.minus_highlight = True
		elif self.plus_box.collidepoint(x, y):
			self.plus_highligt = True

		for event in events:
			if event.type == pg.MOUSEBUTTONDOWN:
				x, y = event.pos
				if self.minus_box.collidepoint(x, y) and self.value > self.low:
					self.value += -1
				elif self.plus_box.collidepoint(x, y) and self.value < self.high:
					self.value += 1
		self.surface = self.font.render(str(self.value), True, TEXT_COLOR)

	def get_number(self):
		return self.value