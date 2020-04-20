import pygame as pg
from lib.assets import Assets

TOP = 54
SIZE = 96

PLAYER_POSITIONS_OFFSET = [ "Dummy!",
							[(-8,-8)], [(-16, -8), (0, -8)], [(-16, -16), (0, -16), (-8, 0)], [(-16, -16), (0, -16), (-16, 0), (0, 0)],
							[(-16, -16), (0, -16), (-16, 0), (0, 0), (-8,-8)], [(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -8), (0, -8)],
							[(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -16), (0, -16), (-8, 0)],
							[(-16, -16), (0, -16), (-16, 0), (0, 0), (-16, -16), (0, -16), (-16, 0), (0, 0)]
							]

MORTAGED_OFFSET = (-16, -16)

class PropertyTile:
	def __init__(self, x, y, orientation, color):
		self.color = self.str_color(color)
		self.orientation = orientation
		# Calculate the positions based on landscape or portrait
		self.box, self.tooltip, self.offsets = self.map_positions((x, y), orientation)
		self.info = None
		self.show_tooltip = False

	def map_positions(self, position, orientation):
		pos = {}
		pos["houses"] = {}
		if orientation == "L":
			pos["houses"][1] = (83, 1)
			pos["houses"][2] = (83, 14)
			pos["houses"][3] = (83, 27)
			pos["houses"][4] = (83, 40)
			pos["houses"][5] = (83, 0)
			pos["hotel"] = Assets.HOTEL_PORTRAIT
			pos["center"] =  (42, 27)
			box = pg.Rect(position, (SIZE, TOP))
			pos["tooltip"] = (0, -40)
			tooltip = pg.Surface((SIZE, TOP))
		if orientation == "R":
			pos["houses"][1] = (0, 1)
			pos["houses"][2] = (0, 14)
			pos["houses"][3] = (0, 27)
			pos["houses"][4] = (0, 40)
			pos["houses"][5] = (0, 0)
			pos["hotel"] = Assets.HOTEL_PORTRAIT
			pos["center"] =  (55, 27)
			box = pg.Rect(position, (SIZE, TOP))
			pos["tooltip"] = (-129, -40)
			tooltip = pg.Surface((SIZE, TOP))
		if orientation == "T":
			pos["houses"][1] = (1, 83)
			pos["houses"][2] = (14, 83)
			pos["houses"][3] = (27, 83)
			pos["houses"][4] = (40, 83)
			pos["houses"][5] = (0, 83)
			pos["hotel"] = Assets.HOTEL_LANDSCAPE
			pos["center"] =  (27, 42)
			box = pg.Rect(position, (TOP, SIZE))
			pos["tooltip"] = (-40, 0)
			tooltip = pg.Surface((TOP, SIZE))
		if orientation == "B":
			pos["houses"][1] = (1, 0)
			pos["houses"][2] = (14, 0)
			pos["houses"][3] = (27, 0)
			pos["houses"][4] = (40, 0)
			pos["houses"][5] = (0, 0)
			pos["hotel"] = Assets.HOTEL_LANDSCAPE
			pos["center"] =  (27, 55)
			box = pg.Rect(position, (TOP, SIZE))
			pos["tooltip"] = (-40, -129)
			tooltip = pg.Surface((TOP, SIZE))
		return (box, tooltip, pos)

	def str_color(self, string):
		if string == "brown":
			return (51,25,0)
		elif string == "light-blue":
			return (102,178,255)
		elif string == "magenta":
			return (204, 0, 204)
		elif string == "orange":
			return (204, 102, 0)
		elif string == "red":
			return (255, 0, 0)
		elif string == "yellow":
			return (204, 204, 0)
		elif string == "green":
			return (0, 128, 0)
		elif string == "blue":
			return (48, 79, 254)
		return (0,0,0)


	def update_info(self, info):
		self.info = info

	def update(self, events):
		self.show_tooltip = False
		x, y = pg.mouse.get_pos()
		if self.box.collidepoint(x, y):
			self.show_tooltip = True

	def draw(self, window, player_list):
		pg.draw.rect(window, self.color, self.box)
		houses, mortaged = self.info
		if houses == 5:
			offset_x, offset_y = self.offsets["houses"][5]
			window.blit(self.offsets["hotel"], (self.box.left + offset_x, self.box.top + offset_y))
		else:
			for i in range(1, 5):
				offset_x, offset_y = self.offsets["houses"][i]
				if i <= houses:
					window.blit(Assets.HOUSE_FILLED, (self.box.left + offset_x, self.box.top + offset_y))
				else:
					window.blit(Assets.HOUSE_EMPTY, (self.box.left + offset_x, self.box.top + offset_y))
		if mortaged:
			x, y = self.offsets["center"]
			offset_x, offset_y = MORTAGED_OFFSET
			window.blit(Assets.MORTAGED, (self.box.left + x + offset_x, self.box.top + y + offset_y))

		positions = PLAYER_POSITIONS_OFFSET[len(player_list)]
		x, y = self.offsets["center"]
		for i in range(len(player_list)):
			offset_x, offset_y = positions[i]
			window.blit(Assets.ICONS[player_list[i]], (self.box.left + x + offset_x, self.box.top + y + offset_y))

	def draw_tooltip(self, window):
		if self.show_tooltip == True:
			x, y = pg.mouse.get_pos()
			offset_x, offset_y = self.offsets["tooltip"]
			window.blit(self.tooltip, (x + offset_x, y + offset_y))