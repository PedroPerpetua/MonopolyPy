import pygame as pg

COLORKEY = (255, 0, 255)
WHITE = (255, 255, 255)
TOP = 80
SIZE = 129

PLAYER_POSITIONS = [
					[(49, 49)], [(33, 49), (65, 49)], [(33, 33), (65, 33), (49, 65)], [(33, 33), (65, 33), (33, 65), (65, 65)],
					[(33, 33), (65, 33), (33, 65), (65, 65), (49, 49)], [(33, 33), (65, 33), (33, 65), (65, 65), (33, 49), (65, 49)],
					[(33, 33), (65, 33), (33, 65), (65, 65), (33, 33), (65, 33), (49, 65)],
					[(33, 33), (65, 33), (33, 65), (65, 65), (33, 33), (65, 33), (33, 65), (65, 65)]
					]

class BoardCorner:
	def __init__(self, orientation, c_type):
		self.surface = pg.Surface((SIZE, SIZE))
		self.surface.fill(WHITE)
		if c_type == "Start":
			self.icon = pg.image.load("libs/assets/corner_start.png").convert()
		elif c_type == "Jail":
			self.icon = pg.image.load("libs/assets/corner_jail.png").convert()
		elif c_type == "Free Parking":
			self.icon = pg.image.load("libs/assets/corner_freeparking.png").convert()
		elif c_type == "Go to jail!":
			self.icon = pg.image.load("libs/assets/corner_gotojail.png").convert()
		self.icon.set_colorkey(COLORKEY)


	def update(self, _):
		pass


	def get_surface(self, player_list):
		self.surface.fill(WHITE)
		self.surface.blit(self.icon, (0,0))

		# Draw the players
		positions = PLAYER_POSITIONS[len(player_list) - 1]
		for i in range(len(player_list)):
			icon = pg.image.load("libs/assets/icon_" + str(player_list[i]) + ".png").convert()
			icon.set_colorkey(COLORKEY)
			pos = positions[i]
			self.surface.blit(icon, pos)

		return self.surface