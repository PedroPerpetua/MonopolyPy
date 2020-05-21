import pygame as pg

BORDER_COLOR = (0, 128, 0)
BG_COLOR = (0, 100, 0)
SELECTED_COLOR = (255, 128, 0)
ICONS_OFFSET = ["Dummy!", (5, 5), (79, 5), (153, 5), (227, 5), (5, 79), (79, 79), (153, 79), (227, 79)]

class IconSelector:
	def __init__(self, x, y, icon_images: "List of the 8 icon images"):
		self.box = pg.rect.Rect((x, y), (296, 148))
		self.icons = icon_images
		self.icon_boxes = self.setup_boxes()
		self.info = {"available_icons": ["Dummy"] + [False for _ in range(8)]}
		self.hovered = None
		self.selected = None

	def setup_boxes(self):
		boxes = ["Dummy!"]
		for i in range(1, 9):
			x, y = ICONS_OFFSET[i]
			boxes += [pg.rect.Rect((self.box.left + x, self.box.top + y), (64, 64))]
		return boxes
		
	def draw(self, window):
		pg.draw.rect(window, BORDER_COLOR, self.box)
		for i in range(1, 9):
			pg.draw.rect(window, BG_COLOR, self.icon_boxes[i])
			if self.info["available_icons"][i]:
				self.icons[i].set_alpha(255)
				if self.selected == i:
					pg.draw.rect(window, SELECTED_COLOR, ((self.icon_boxes[i].left - 5, self.icon_boxes[i].top - 5), (74, 74)))
			else:
				self.icons[i].set_alpha(100)
			window.blit(self.icons[i], self.icon_boxes[i])

	def update(self, events):
		for event in events:
			if event.type == pg.MOUSEBUTTONDOWN:
				click_pos = event.pos
				for i in range(1, 9):
					if self.info["available_icons"][i] and self.icon_boxes[i].collidepoint(click_pos):
						self.selected = i		

	def update_info(self, info):
		self.info = info
		if self.selected is not None and not self.info["available_icons"][self.selected]:
			self.selected = None
		for i in range(1, 9):
			if self.icon_boxes[i].collidepoint(pg.mouse.get_pos()):
				self.hovered = i