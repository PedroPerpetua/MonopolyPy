import pygame as pg

class ImageButton:
	def __init__(self, x, y, button_images, clickable):
		# Drawing related vars
		self.selected, self.unselected = button_images
		self.current = self.selected
		self.box = self.current.get_rect().move(x, y) #Because both images should be the same size, we can just take one box

		# Control related vars:
		self.clickable = clickable
		self.clicked = False
		self.highlited = False

	def draw(self, window):
		if self.clickable:
			if self.highlited:
				self.current = self.selected
			else:
				self.current = self.unselected
			self.current.set_alpha(255)
		else:
			self.current.set_alpha(50)

		window.blit(self.current, self.box)

	def update(self, events):
		self.clicked = False
		self.highlited = False

		x,y = pg.mouse.get_pos()
		if self.box.collidepoint(x, y):
			self.highlited = True

		for event in events:
			if event.type == pg.MOUSEBUTTONDOWN and self.clickable:
				x, y = event.pos
				if self.box.collidepoint(x, y):
					self.clicked = True
					self.highlited = False

	def switch(self, state):
		self.clickable = state

	def get_clicked(self):
		return self.clicked