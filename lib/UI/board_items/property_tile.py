import pygame as pg
from lib.assets import Assets

TOP = 80
SIZE = 129

PLAYER_POSITIONS_OFFSET = [	"Dummy!",
							[(-16,-16)], [(-32, -16), (0, -16)], [(-32, -32), (0, -32), (-16, 0)], [(-32, -32), (0, -32), (-32, 0), (0, 0)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-16,-16)], [(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -16), (0, -16)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -32), (0, -32), (-16, 0)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -32), (0, -32), (-32, 0), (0, 0)]
							]

class PropertyTile:
	def __init__(self, x, y, orientation, color):
		self.color = self.str_color(color)
		self.orientation = orientation
		# Calculate the positions based on landscape or portrait
		self.box, self.offsets = self.map_positions((x, y), orientation)
		self.info = None

	def map_positions(self, position, orientation):
		pos = {}
		pos["houses"] = {}
		if orientation == "L":
			pos["houses"][1] = (109, 0)
			pos["houses"][2] = (109, 20)
			pos["houses"][3] = (109, 40)
			pos["houses"][4] = (109, 60)
			pos["houses"][5] = (109, 0)
			pos["hotel"] = Assets.HOTEL_PORTRAIT
			pos["players"] =  (55, 40)
			pos["mortaged"] = (23, 8)
			box = pg.Rect(position, (SIZE, TOP))
		if orientation == "R":
			pos["houses"][1] = (0, 0)
			pos["houses"][2] = (0, 20)
			pos["houses"][3] = (0, 40)
			pos["houses"][4] = (0, 60)
			pos["houses"][5] = (0, 0)
			pos["hotel"] = Assets.HOTEL_PORTRAIT
			pos["players"] =  (75, 40)
			pos["mortaged"] = (43, 8)
			box = pg.Rect(position, (SIZE, TOP))
		if orientation == "T":
			pos["houses"][1] = (0, 109)
			pos["houses"][2] = (20, 109)
			pos["houses"][3] = (40, 109)
			pos["houses"][4] = (60, 109)
			pos["houses"][5] = (0, 109)
			pos["hotel"] = Assets.HOTEL_LANDSCAPE
			pos["players"] =  (40, 55)
			pos["mortaged"] = (8, 23)
			box = pg.Rect(position, (TOP, SIZE))
		if orientation == "B":
			pos["houses"][1] = (0, 0)
			pos["houses"][2] = (20, 0)
			pos["houses"][3] = (40, 0)
			pos["houses"][4] = (60, 0)
			pos["houses"][5] = (0, 0)
			pos["hotel"] = Assets.HOTEL_LANDSCAPE
			pos["players"] =  (40, 75)
			pos["mortaged"] = (8, 43)
			box = pg.Rect(position, (TOP, SIZE))
		return (box, pos)

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

	def update(self, _):
		pass

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
			offset_x, offset_y = self.offsets["mortaged"]
			window.blit(Assets.MORTAGED, (self.box.left + offset_x, self.box.top + offset_y))

		positions = PLAYER_POSITIONS_OFFSET[len(player_list)]
		offset_x, offset_y = self.offsets["players"]
		for i in range(len(player_list)):
			p_offset_x, p_offset_y = positions[i]
			window.blit(Assets.ICONS[player_list[i]], (self.box.left + offset_x + p_offset_x, self.box.top + offset_y + p_offset_y))