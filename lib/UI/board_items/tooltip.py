import pygame as pg
from lib.assets import Assets, Colors

BORDER_SIZE = 1

class Tooltip:
	def __init__(self, x, y):
		self.box = pg.Rect((x, y), (476, 100))
		self.inner_box = pg.Rect((x + BORDER_SIZE, y + BORDER_SIZE), (476 - 2 * BORDER_SIZE, 100 - 2 * BORDER_SIZE))
		self.name_font = pg.font.Font(Assets.PIXEL, 32)
		self.text_font = pg.font.Font(Assets.ARIAL, 24)
		self.info = None
	def update_info(self, info):
		self.info = info
	def draw(self, window):
		def write_name(name, offsetx, offsety):
			name = self.name_font.render(name, True, Colors.BLACK)
			name_box = name.get_rect()
			window.blit(name, (self.box.centerx - name_box.centerx + offsetx, self.box.centery - name_box.centery + offsety))
		def write_text(text, offsetx, offsety):
			text = self.text_font.render(text, True, Colors.BLACK)
			text_box = text.get_rect()
			window.blit(text, (self.box.centerx - text_box.centerx + offsetx, self.box.centery - text_box.centery + offsety))
		def put_image(image, offsetx, offsety):
			image_box = image.get_rect()
			window.blit(image, (self.box.centerx - image_box.centerx + offsetx, self.box.centery - image_box.centery + offsety))
		pg.draw.rect(window, Colors.BLACK, self.box)
		if self.info is None:
			pg.draw.rect(window, Colors.BG_COLOR, self.inner_box)
		else:
			pg.draw.rect(window, self.info["color"], self.inner_box)
			if self.info["type"] == "label":
				write_name(self.info["name"], 0, -10)
				write_text(self.info["label"], 0, 15)
			elif self.info["type"] == "simple":
				write_name(self.info["name"], 0, -20)
				write_text(self.info["owner"], 0, 0)
				write_text(self.info["value"], 0, +24)
			elif self.info["type"] == "property":
				write_name(self.info["name"], 0, -20)
				write_text(self.info["owner"], -100, 0)
				write_text(self.info["value"], -100, +24)
				write_text(self.info["houses"], +100, 0)
				write_text(self.info["house_price"], +100, +24)
			elif self.info["type"] == "wildcard":
				write_name(self.info["name"], 0, +4)
				put_image(self.info["image"], -200, 0)
				put_image(self.info["image"], +200, 0)