import os.path
import pygame as pg


BUTTON_COLOR = BG_COLOR = WHITE = (255,255,255)
TEXT_COLOR = BLACK = (0,0,0)
BOX_COLOR = DARK_RED = (102,0,0)
HIGHLIGHT_COLOR = RED = (199,0,0)

class NumberPicker:
	def __init__(self, x, y, widht, height, font, default, min_num, max_num, alignment = "L"):
		# Text related vars:
		if not os.path.isfile(font):
			font = pg.font.match_font(font)
		self.font = pg.font.Font(font, height)
		self.surface = self.font.render(str(default), True, TEXT_COLOR)
		self.minus = pg.font.Font(pg.font.match_font("arial", True), height).render("-", True, BUTTON_COLOR)
		self.minus_highlight = False
		self.plus = pg.font.Font(pg.font.match_font("arial", True), height).render("+", True, BUTTON_COLOR)
		self.plus_highligt = False

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
		base = pg.draw.rect(window, BG_COLOR, pg.Rect((self.x, self.y), (self.w, self.h)))
		text_rect = self.surface.get_rect()
		window.blit(self.surface, (base.centerx - text_rect.centerx, base.centery - text_rect.centery))

		# The small constants added below (-1, +1) are there to center the character a bit more
		if self.minus_highlight:
			minus_box_color = HIGHLIGHT_COLOR
		else:
			minus_box_color = BOX_COLOR
		minus_box = pg.draw.rect(window, minus_box_color, pg.Rect((base.topleft), (self.h, self.h)))
		minus_rect = self.minus.get_rect()
		window.blit(self.minus, (minus_box.centerx - minus_rect.centerx - 1, minus_box.centery - minus_rect.centery - 1))

		if self.plus_highligt:
			plus_box_color = HIGHLIGHT_COLOR
		else:
			plus_box_color = BOX_COLOR
		plus_box = pg.draw.rect(window, plus_box_color, pg.Rect((base.right - self.h, base.top), (self.h, self.h)))
		plus_rect = self.plus.get_rect()
		window.blit(self.plus, (plus_box.centerx - plus_rect.centerx + 1, plus_box.centery - plus_rect.centery))

	def update(self, events):
		self.minus_highlight = False
		self.plus_highligt = False

		x,y = pg.mouse.get_pos()
		if self.y < y < self.y + self.h:
			if (self.x < x < self.x + self.h):
				self.minus_highlight = True
			elif (self.x + self.w - self.h < x < self.x + self.w):
				self.plus_highligt = True

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