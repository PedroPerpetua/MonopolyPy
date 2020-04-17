import pygame as pg

COLORKEY = (255, 0, 255)
LIGHT_RED = (255, 102, 102)
WHITE = (255, 255, 255)
LIGHT_BLUE = (153, 204, 255)
TOP = 80
SIZE = 129

class BoardWildCard:
	def __init__(self, orientation, w_type):
		if orientation in ["L", "R"]:
			self.surface = pg.Surface((SIZE, TOP))
			icon_x = 32
			icon_y = 8
		elif orientation in ["T", "B"]:
			self.surface = pg.Surface((TOP, SIZE))
			icon_x = 8
			icon_y = 32

		if w_type == "Luck":
			icon = pg.image.load("libs/assets/luck.png").convert()
			self.surface.fill(WHITE)
		elif w_type == "Community Chest":
			icon = pg.image.load("libs/assets/community_chest.png").convert()
			self.surface.fill(WHITE)
		icon.set_colorkey(COLORKEY)
		
		self.surface.blit(icon, (icon_x, icon_y))

	def update(self, _):
		pass

	def draw_players(self, player_list):
		pass

	def get_surface(self, player_list):
		return self.surface