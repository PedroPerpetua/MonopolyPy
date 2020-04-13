class Screen:
	def __init__(self, window, bg_color, items):
		self.win = window
		self.bg_color = bg_color
		self.items = items
		

	def draw(self):
		self.win.fill(self.bg_color)
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(self.win)

	def update(self, events):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].update(events)

	def get_texts(self):
		values = []
		for item in self.items["input_box"]:
			values += [self.items["input_box"][item].get_text()]
		return values