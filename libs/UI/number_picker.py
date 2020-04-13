import os.path
import pygame as pg

BORDER_SIZE = 2
TEXT_COLOR = WHITE = (255,255,255)
BORDER_COLOR = BOX_COLOR = DARK_RED = (102,0,0)
BG_COLOR = RED = (199,0,0)

class NumberPicker:
	def __init__(self, x, y, widht, height, font, default, min_num, max_num, alignment = "L"):
		# Text related vars:
		if not os.path.isfile(font):
			font = pg.font.match_font(font)
		self.font = pg.font.Font(font, height - BORDER_SIZE * 2)
		self.surface = self.font.render(str(default), True, TEXT_COLOR)
		self.minus = pg.font.Font(pg.font.match_font("arial", True), height).render("-", True, TEXT_COLOR)
		self.plus = pg.font.Font(pg.font.match_font("arial", True), height).render("+", True, TEXT_COLOR)

		# Drawing related vars:
		self.h = height
		self.w = widht
		if alignment == "L":
			self.x = x
			self.y = y
		elif alignment == "C":
			self.x = x - int(widht/2)
			self.y = y - int(height/2)		

		# Data related vars:
		self.value = default
		self.low = min_num
		self.high = max_num


	def draw(self, window):
		border = pg.draw.rect(window, BORDER_COLOR, pg.Rect((self.x, self.y), (self.w, self.h)))
		base = pg.draw.rect(window, BG_COLOR, pg.Rect((self.x + BORDER_SIZE, self.y + BORDER_SIZE), (self.w - BORDER_SIZE * 2, self.h - BORDER_SIZE * 2)))
		text_rect = self.surface.get_rect()
		window.blit(self.surface, (base.centerx - text_rect.centerx, base.centery - text_rect.centery))

		box_size = self.h - BORDER_SIZE * 2
		# The small constants added below (-1, +1) are there to center the character a bit more
		minus_box = pg.draw.rect(window, BOX_COLOR, pg.Rect((base.topleft), (box_size, box_size)))
		minus_rect = self.minus.get_rect()
		window.blit(self.minus, (minus_box.centerx - minus_rect.centerx - 1, minus_box.centery - minus_rect.centery - 1))

		plus_box = pg.draw.rect(window, BOX_COLOR, pg.Rect((base.right - box_size, base.top), (box_size, box_size)))
		plus_rect = self.plus.get_rect()
		window.blit(self.plus, (plus_box.centerx - plus_rect.centerx + 1, plus_box.centery - plus_rect.centery))

	def update(self, events):
		for event in events:
			if event.type == pg.MOUSEBUTTONDOWN:
				x, y = event.pos
				if self.y < y < self.y + self.h:
					if (self.x < x < self.x + self.h) and self.value > self.low:
						self.value += -1
					elif (self.x + self.w - self.h < x < self.x + self.w) and self.value < self.high:
						self.value += 1
		self.surface = self.font.render(str(self.value), True, TEXT_COLOR)

	def get_number(self):
		return self.value