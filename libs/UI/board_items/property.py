import pygame as pg

TOP = 80
SIZE = 129
COLORKEY = (255, 0, 255)

PLAYER_POSITIONS_OFFSET = [
							[(-16,-16)], [(-32, -16), (0, -16)], [(-32, -32), (0, -32), (-16, 0)], [(-32, -32), (0, -32), (-32, 0), (0, 0)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-16,-16)], [(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -16), (0, -16)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -32), (0, -32), (-16, 0)],
							[(-32, -32), (0, -32), (-32, 0), (0, 0), (-32, -32), (0, -32), (-32, 0), (0, 0)]
						]

class BoardProperty:
	def __init__(self, orientation):
		if orientation in ["L", "R"]:
			self.surface = pg.Surface((SIZE, TOP))
			self.hotel = pg.image.load("libs/assets/hotel_portrait.png").convert()
			self.house_y = [0, 20, 40, 60]
			self.player_center_y = 40
			self.mortaged_y = 8
			if orientation == "L":
				self.house_x = [109, 109, 109, 109]
				self.player_center_x = 55
				self.mortaged_x = 23
			if orientation ==  "R":
				self.house_x = [0, 0, 0, 0]
				self.player_center_x = 75
				self.mortaged_x = 43
		elif orientation in ["T", "B"]:
			self.surface = pg.Surface((TOP, SIZE))
			self.hotel = pg.image.load("libs/assets/hotel_landscape.png").convert()
			self.hotel.set_colorkey(COLORKEY)
			self.house_x = [0, 20, 40, 60]
			self.player_center_x = 40
			self.mortaged_x = 8
			if orientation == "T":
				self.house_y = [109, 109, 109, 109]
				self.player_center_y = 55
				self.mortaged_y = 23
			if orientation ==  "B":
				self.house_y = [0, 0, 0, 0]
				self.player_center_y = 75
				self.mortaged_y = 43

		self.mortaged = pg.image.load("libs/assets/mortaged.png").convert()
		self.mortaged.set_colorkey(COLORKEY)
		self.hotel.set_colorkey(COLORKEY)
		self.house_empty = pg.image.load("libs/assets/house_empty.png").convert()
		self.house_empty.set_colorkey(COLORKEY)
		self.house_selected = pg.image.load("libs/assets/house_selected.png").convert()
		self.house_selected.set_colorkey(COLORKEY)


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


	def update(self, attributes):
		color, houses, mortaged = attributes
		color = self.str_color(color)
		self.surface.fill(color)
		if houses == 5:
			self.surface.blit(self.hotel, (self.house_x[0], self.house_y[0]))
		else:
			for i in range(4):
				if i + 1 <= houses:
					self.surface.blit(self.house_selected, (self.house_x[i], self.house_y[i]))
				else:
					self.surface.blit(self.house_empty, (self.house_x[i], self.house_y[i]))
		

	def get_surface(self, player_list):

		# Draw the players
		positions = PLAYER_POSITIONS_OFFSET[len(player_list) - 1]
		for i in range(len(player_list)):
			icon = pg.image.load("libs/assets/icon_" + str(player_list[i]) + ".png").convert()
			icon.set_colorkey(COLORKEY)
			offset_x, offset_y = positions[i]
			self.surface.blit(icon, (self.player_center_x + offset_x, self.player_center_y + offset_y))

		return self.surface
