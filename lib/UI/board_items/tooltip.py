import pygame as pg
import lib.UI.board_items.constants as c
from lib.assets import Assets

TEXT_COLOR = BLACK = (0, 0, 0)
BG_COLOR = (143,188,114)
WHITE = (255, 255, 255)

class Tooltip:
	def __init__(self, board_x, board_y):
		x, y = c.TOOLTIP_POS
		self.box = pg.Rect((x + board_x, y+ board_y), c.TOOLTIP_SIZE)
		self.name_font = pg.font.Font(Assets.PIXEL, 32)
		self.line_font = pg.font.Font(Assets.ARIAL, 24)
		self.info = None

	def get_dimensions(self):
		return [self.box.left, self.box.top, self.box.width, self.box.height]

	# Drawing functions
	def update(self, info):
		self.info = info

	def draw(self, window):

		def draw_name(name_str):
			name = self.name_font.render(name_str, True, TEXT_COLOR)
			name_rect = name.get_rect()
			window.blit(name, (self.box.centerx - name_rect.centerx, self.box.top + 5))

		if self.info:
			mode = self.info["type"]
			if mode == "property":
				# Drawing the box
				pg.draw.rect(window, self.info["color"], self.box)
				# Drawing the name
				name = self.name_font.render(self.info["name"], True, TEXT_COLOR)
				name_rect = name.get_rect()
				window.blit(name, (self.box.centerx - name_rect.centerx, self.box.top + 5))
				# Drawing the owner
				owner = self.line_font.render(self.info["owner"], True, TEXT_COLOR)
				window.blit(owner, (self.box.left + 123 - owner.get_rect().centerx, self.box.top + 32))
				# Drawing the value
				value = self.line_font.render(self.info["value"], True, TEXT_COLOR)
				window.blit(value, (self.box.left + 123 - value.get_rect().centerx, self.box.bottom - 35))
				# Drawing the number of houses
				houses = self.line_font.render(self.info["houses"], True, TEXT_COLOR)
				window.blit(houses, (self.box.right - 123 - houses.get_rect().centerx, self.box.top + 32))
				# Drawing the price of each house
				house_price = self.line_font.render(self.info["house_price"], True, TEXT_COLOR)
				window.blit(house_price, (self.box.right - 123 - house_price.get_rect().centerx, self.box.bottom - 35))
			elif mode == "single":
				# Drawing the box
				pg.draw.rect(window, self.info["color"], self.box)
				# Drawing the name
				name = self.name_font.render(self.info["name"], True, TEXT_COLOR)
				name_rect = name.get_rect()
				window.blit(name, (self.box.centerx - name_rect.centerx, self.box.top + 5))
				# Drawing the owner
				owner = self.line_font.render(self.info["owner"], True, TEXT_COLOR)
				window.blit(owner, (self.box.centerx - owner.get_rect().centerx, self.box.top + 32))
				# Drawing the label
				label = self.line_font.render(self.info["label"], True, TEXT_COLOR)
				window.blit(label, (self.box.centerx - label.get_rect().centerx, self.box.bottom - 35))
			elif mode == "single_label":
				# Drawing the box
				pg.draw.rect(window, self.info["color"], self.box)
				# Drawing the name
				name = self.name_font.render(self.info["name"], True, TEXT_COLOR)
				name_rect = name.get_rect()
				window.blit(name, (self.box.centerx - name_rect.centerx, self.box.centery - name_rect.centery - 10))
				# Drawing the label
				label = self.line_font.render(self.info["label"], True, TEXT_COLOR)
				label_rect = label.get_rect()
				window.blit(label, (self.box.centerx - label_rect.centerx, self.box.centery - label_rect.centery + 15))
			elif mode == "wildcard":
				# Drawing the box
				pg.draw.rect(window, self.info["color"], self.box)
				# Drawing the name
				name = self.name_font.render(self.info["name"], True, TEXT_COLOR)
				name_rect = name.get_rect()
				window.blit(name, (self.box.centerx - name_rect.centerx, self.box.centery - name_rect.centery + 5))
				# Drawing the icons
				window.blit(self.info["image"], (self.box.left + 30, self.box.centery - 16))
				window.blit(self.info["image"], (self.box.right - 30 - 32, self.box.centery - 16))
		else:
			pg.draw.rect(window, BG_COLOR, self.box)