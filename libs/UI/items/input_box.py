import os.path
import pygame as pg
import pygame.locals as pl

TEXT_COLOR = BLACK = (0,0,0)
BG_COLOR = WHITE = (255,255,255)

FORBIDDEN_KEYS = [pl.K_RETURN, pl.K_ESCAPE, pl.K_TAB]
class InputBox:
	def __init__(self, x, y, widht, height, font, alignment="L"):
		# Text related vars:
		self.text = ""
		if not os.path.isfile(font):
			font = pg.font.match_font(font)
		self.font = pg.font.Font(font, height)
		self.max_space = widht - int(height/2)
		self.surface = self.font.render(self.text, True, TEXT_COLOR)
		self.surface.set_alpha(0)

		# Cursor related vars:
		self.cursor_surface = pg.Surface((1, height))
		self.cursor_surface.fill(TEXT_COLOR)
		self.cursor_pos = 0
		self.cursor_visible = False
		self.cursor_clock = pg.time.Clock()
		self.cursor_blink = 0

		# Drawing related vars:
		if alignment == "L":
			self.x = x
			self.y = y
		elif alignment == "C":
			self.x = x - int(widht/2)
			self.y = y - int(height/2)
		self.box = pg.Rect((self.x,self.y),(widht, height))
		self.active = False


	def draw(self, window):
		pg.draw.rect(window, BG_COLOR, self.box)
		window.blit(self.surface, self.box.topleft)
		if self.cursor_visible:
			cursor_y_pos = self.box.left + self.font.size(self.text[:self.cursor_pos])[0] - self.cursor_surface.get_width() + 1
			window.blit(self.cursor_surface, (cursor_y_pos, self.box.top))

	def update(self, events):
		for event in events:
			if event.type == pg.MOUSEBUTTONDOWN:
				if self.box.collidepoint(event.pos):
					self.active = True
				else:
					self.active = False
			elif event.type == pg.KEYDOWN and self.active:
				if event.key == pl.K_BACKSPACE:
					self.text = self.text[:max(self.cursor_pos - 1, 0)] + self.text[self.cursor_pos:]
					self.cursor_pos = max(self.cursor_pos -1, 0)
				elif event.key == pl.K_DELETE:
					self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
				elif event.key == pl.K_RIGHT:
					self.cursor_pos = min(self.cursor_pos +1, len(self.text))
				elif event.key == pl.K_LEFT:
					self.cursor_pos = max(self.cursor_pos -1, 0)
				elif self.surface.get_width() < self.max_space and event.key not in FORBIDDEN_KEYS:
					self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
					self.cursor_pos += len(event.unicode)
			self.surface = self.font.render(self.text, True, TEXT_COLOR)

		if self.active:
			self.cursor_blink += self.cursor_clock.get_time()
			if self.cursor_blink >= 500:
				self.cursor_blink %= 500
				self.cursor_visible = not self.cursor_visible
		else:
			self.cursor_visible = False
			self.cursor_blink = 0
		self.cursor_clock.tick()

	def get_text(self):
		return self.text