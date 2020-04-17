import pygame as pg

TEXT_COLOR = BLACK = (0,0,0)
BG_COLOR = LIGHT_GRAY = (211,211,211)
LOCKED_COLOR = DARK_GRAY = (92,92,92)
COLOR_KEY = (255,0,255)
WIDHT = 120
HEIGHT = 32
TEXT_SIZE = 20
X_POSITIONS = [20, 20, 20, 20, 160, 160, 160, 160]
Y_POSITIONS = [106, 153, 200, 247, 106, 153, 200, 247]
FONT = "arial"

class PlayerBox:
	def __init__(self, pos, locked=False, player_id=None):
		# Drawing related vars:
		self.x = X_POSITIONS[pos - 1]
		self.y = Y_POSITIONS[pos - 1]
		self.font = pg.font.Font(pg.font.match_font(FONT), TEXT_SIZE)
		self.cycle = 0
		self.blink = 0
		self.cycle_clock = pg.time.Clock()

		# Control related vars:
		self.player_id = None
		self.icon = None
		self.name = None
		if locked:
			self.locked = pg.image.load("libs/assets/lock.png").convert()
			self.locked.set_colorkey(COLOR_KEY)
		else:
			self.locked = None

	def draw(self, window):
		if self.locked:
			box = pg.draw.rect(window, LOCKED_COLOR, ((self.x, self.y), (WIDHT, HEIGHT)))
			window.blit(self.locked, (box.centerx - 16, box.centery - 16))
		else:
			box = pg.draw.rect(window, BG_COLOR, ((self.x, self.y), (WIDHT, HEIGHT)))
			dots = self.update_dots()
			if self.player_id == None:
				text = self.font.render("Waiting" + dots, True, TEXT_COLOR)
				window.blit(text, (box.left + 6, box.top + 6))
			else:
				if self.player_id == []:
					text = self.font.render("Not ready" + dots, True, TEXT_COLOR)
					window.blit(text, (box.left + 6, box.top + 6))
				else:
					window.blit(self.icon, (box.left, box.top))
					window.blit(self.name, (box.left + 33 + 6, box.top + 6))

	def update(self, _):
		self.cycle_clock.tick()

	def update_dots(self):
		self.blink += self.cycle_clock.get_time()
		if self.blink >= 350:
			self.blink %= 350
			self.cycle = (self.cycle + 1)%4
		dots = ""
		for i in range(self.cycle):
			dots += "."
		return dots

	def update_player(self, player_id):
		if player_id == None:
			self.player_id = None
			self.icon = None
			self.name = None
		elif player_id == []:
			self.player_id = []
		elif player_id != self.player_id:
			self.player_id = player_id
			self.icon = pg.image.load(f"libs/assets/icon_{str(player_id[0])}.png").convert()
			self.icon.set_colorkey(COLOR_KEY)
			self.name = self.font.render(player_id[1], True, TEXT_COLOR)