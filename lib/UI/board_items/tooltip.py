import pygame as pg
import lib.UI.board_items.constants as c
from lib.assets import Assets

TEXT_COLOR = BLACK = (0, 0, 0)
BG_COLOR = (143,188,114)
WHITE = (255, 255, 255)
LIGHT_GRAY = (128, 128, 128)
LIGHT_CYAN = (153, 255, 255)

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

		def draw_owner_value(owner_str, value_str, centerx):
			owner = self.line_font.render(owner_str, True, TEXT_COLOR)
			window.blit(owner, (centerx - owner.get_rect().centerx, self.box.top + 32))
			if self.info["owner"] == "Unowned":
				value = self.line_font.render("Price: " + value_str + "€", True, TEXT_COLOR)
			else:
				value = self.line_font.render("Tax: " + value_str + "€", True, TEXT_COLOR)
			window.blit(value, (centerx - value.get_rect().centerx, self.box.bottom - 35))


		if self.info:
			mode = self.info["type"]
			if mode == "Property":
				pg.draw.rect(window, c.get_rgb(self.info["color"]), self.box)
				draw_name(self.info["name"])
				
				draw_owner_value(self.info["owner"], self.info["value"], self.box.left + 123)

				houses = self.line_font.render("Houses: " + self.info["houses"], True, TEXT_COLOR)
				window.blit(houses, (self.box.right - 123 - houses.get_rect().centerx, self.box.top + 32))
				house_price = self.line_font.render("House Price: " + self.info["house_price"] + "€", True, TEXT_COLOR)
				window.blit(house_price, (self.box.right - 123 - house_price.get_rect().centerx, self.box.bottom - 35))
			elif mode == "Railroad":
				pg.draw.rect(window, LIGHT_GRAY, self.box)
				draw_name(self.info["name"])
				draw_owner_value(self.info["owner"], self.info["rail"], self.box.centerx)
			elif mode == "Utility":
				pg.draw.rect(window, LIGHT_CYAN, self.box)
				draw_name(self.info["name"])
				draw_owner_value(self.info["owner"], self.info["util"], self.box.centerx)
			elif mode == "Tax":
				pg.draw.rect(window, WHITE, self.box)
				draw_name(self.info["name"])
				value = self.line_font.render("Pay " + str(self.info["tax"]) + "€", True, TEXT_COLOR)
				value_rect = value.get_rect()
				window.blit(value, (self.box.centerx - value_rect.centerx, self.box.centery - value_rect.height + 20))
			elif mode == "Special" or mode == "WildCard":
				pg.draw.rect(window, WHITE, self.box)
				text = self.name_font.render(self.info["name"], True, TEXT_COLOR)
				text_rect = text.get_rect()
				window.blit(text, (self.box.centerx - text_rect.centerx, self.box.centery - text_rect.centery))
		else:
			pg.draw.rect(window, BG_COLOR, self.box)