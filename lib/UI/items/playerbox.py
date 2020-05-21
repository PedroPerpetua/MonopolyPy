import pygame as pg
from lib.assets import Assets

TEXT_COLOR = BLACK = (0, 0, 0)
BG_COLOR = LIGHT_GRAY = (153, 153, 153)
X_POSITIONS = ["Dummy!", 20, 20, 20, 20, 160, 160, 160, 160]
Y_POSITIONS = ["Dummy!", 106, 153, 200, 247, 106, 153, 200, 247]


class PlayerBox:
	def __init__(self, pos, locked=False):
		# Drawing related vars:
		self.box = pg.Rect((X_POSITIONS[pos], Y_POSITIONS[pos]), (120, 32))
		if locked:
			self.locked = Assets.LOCKED_SLOT
		else:
			self.locked = False
			self.font = pg.font.Font(Assets.ARIAL, 20)
			self.cycle = 0
			self.blink = 0
			self.cycle_clock = pg.time.Clock()

			# Control related vars:
			self.player_id = None


	def draw(self, window):
		if self.locked:
			window.blit(self.locked, self.box)
		else:
			pg.draw.rect(window, BG_COLOR, self.box)
			if self.player_id is None:
				text = self.font.render("Waiting" + self.update_dots(), True, TEXT_COLOR)
				window.blit(text, (self.box.left + 6, self.box.top + 6))
			else:
				if self.player_id == []:
					text = self.font.render("Not ready" + self.update_dots(), True, TEXT_COLOR)
					window.blit(text, (self.box.left + 6, self.box.top + 6))
				else:
					window.blit(Assets.ICONS["MEDIUM"][self.player_id[1]], (self.box.left, self.box.top))
					text = self.font.render(self.player_id[0], True, TEXT_COLOR)
					window.blit(text, (self.box.left + 32 + 6, self.box.top + 6))

	def update(self, _):
		if not self.locked:
			self.cycle_clock.tick()

	def update_dots(self):
		if not self.locked:
			self.blink += self.cycle_clock.get_time()
			if self.blink >= 350:
				self.blink %= 350
				self.cycle = (self.cycle + 1)%4
			dots = ""
			for _ in range(self.cycle):
				dots += "."
			return dots

	def update_player(self, player_id):
		if not self.locked:
			self.player_id = player_id