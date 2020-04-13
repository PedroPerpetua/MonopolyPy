import os.path
import pygame as pg

TEXT_COLOR = WHITE = (255,255,255)
HIGHLIGHT_COLOR = DARK_RED = (102,0,0)
RED = (255,51,51)
BORDER_SIZE = 8

class TextButton:
	def __init__(self, x, y, widht, height, font, text, clickable, alignment="L"):
		# Text related vars:
		if not os.path.isfile(font):
			font = pg.font.match_font(font)
		self.surface = pg.font.Font(font, height - BORDER_SIZE * 2).render(text, True, TEXT_COLOR)

		# Drawing related vars:
		if alignment == "L":
			self.x = x
			self.y = y
		elif alignment == "C":
			self.x = x - int(widht/2)
			self.y = y - int(height/2)
		self.w = widht
		self.h = height
		# Everything has to be a surface in order to reduce the alpha value and make it non-clickable aspect
		self.box = pg.Surface((widht - BORDER_SIZE * 2, height - BORDER_SIZE * 2))
		self.box.fill(RED)
		self.white_border = pg.Surface((widht - (BORDER_SIZE), height - (BORDER_SIZE)))
		self.white_border.fill(WHITE)
		self.red_border = pg.Surface((widht, height))
		self.red_border.fill(DARK_RED)

		# Control related vars:
		self.clickable = clickable
		self.clicked = False
		self.highlited = False


	def draw(self, window):
		if self.clickable:
			self.box.set_alpha(255)
			self.white_border.set_alpha(255)
			self.red_border.set_alpha(255)
			self.surface.set_alpha(255)
			if self.highlited:
				self.red_border.fill(RED)
			else:
				self.red_border.fill(DARK_RED)
		else:
			self.box.set_alpha(50)
			self.white_border.set_alpha(50)
			self.red_border.set_alpha(50)
			self.surface.set_alpha(50)
		window.blit(self.red_border, (self.x, self.y))
		window.blit(self.white_border, (self.x + BORDER_SIZE/2, self.y + BORDER_SIZE/2))
		window.blit(self.box, (self.x + BORDER_SIZE, self.y + BORDER_SIZE))
		text_rect = self.surface.get_rect()
		window.blit(self.surface, (self.x + int(self.w/2) - text_rect.centerx, self.y + int(self.h/2) - text_rect.centery))

	def update(self, events):
		self.clicked = False
		self.highlited = False

		x,y = pg.mouse.get_pos()
		if (self.x < x < self.x + self.w) and (self.y < y < self.y + self.h):
			self.highlited = True

		for event in events:
			if event.type == pg.MOUSEBUTTONDOWN and self.clickable:
				x, y = event.pos
				if (self.x < x < self.x + self.w) and (self.y < y < self.y + self.h):
					self.clicked = True
		pass

	def switch(self, state):
		self.clickable = state

	def get_clicked(self):
		return self.clicked