from lib.assets import Assets
from lib.UI.items import image, inputbox, textlabel, numberpicker, imagebutton, playerbox

# SCREEN_SIZE = (300, 300)
BG_COLOR = (143,188,114)

class StartScreen:
	def __init__(self):
		self.items = self.setup_items()

	def setup_items(self):
		items = {}
		items["image"] = {}
		items["textlabel"]= {}
		items["inputbox"] = {}
		items["numberpicker"] = {}
		items["button"] = {}
		items["image"]["logo"] = image.Image(22, 0, Assets.APP_LOGO)
		items["textlabel"]["host"] = textlabel.TextLabel(20, 113, "Host IP", 20, Assets.PIXEL)
		items["inputbox"]["host"] = inputbox.InputBox(20, 128, 260, 20, Assets.ARIAL)
		items["textlabel"]["port"] = textlabel.TextLabel(20, 156, "Port", 20, Assets.PIXEL)
		items["textlabel"]["players"] = textlabel.TextLabel(160, 156, "Players", 20, Assets.PIXEL)
		items["inputbox"]["port"] = inputbox.InputBox(20, 171, 120, 20, Assets.ARIAL, True)
		items["numberpicker"]["players"] = numberpicker.NumberPicker(160, 171, 120, 
			[Assets.MINUS_SELECTED, Assets.MINUS_UNSELECTED], [Assets.PLUS_SELECTED, Assets.PLUS_UNSELECTED], 4, 2, 8)
		items["textlabel"]["password"] = textlabel.TextLabel(20, 204, "Password", 20, Assets.PIXEL)
		items["inputbox"]["password"] = inputbox.InputBox(20, 219, 260, 20, Assets.ARIAL)
		items["button"]["start"] = imagebutton.ImageButton(80, 245, [Assets.START_SELECTED, Assets.START_UNSELECTED], False)
		return items

	def draw(self, window):
		window.fill(BG_COLOR)
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(window)

	def update(self, events):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].update(events)

		if self.validate_input():
			self.items["button"]["start"].switch(True)
		else:
			self.items["button"]["start"].switch(False)

	def validate_input(self):
		for box in self.items["inputbox"]:
			if self.items["inputbox"][box].get_text() == "":
				return False
		return True

	def get_values(self):
		''' Returns a list with the following indexes - keys:
			0 -> host (string)
			1 -> port (int)
			2 -> password (string)
			3 -> number of players (int)
		'''
		values = []
		for item in self.items["inputbox"]:
			values += [self.items["inputbox"][item].get_text()]
		values[1] = int(values[1])
		values += [self.items["numberpicker"]["players"].get_number()]
		return values

	def check_end(self):
		return self.items["button"]["start"].get_clicked()

class QueueScreen:
	def __init__(self, num_players):
		self.slots = num_players
		self.items = self.setup_items()

	def setup_items(self):
		items = {}
		items["image"] = {}
		items["playerbox"] = {}
		items["image"]["logo"] = image.Image(22, 0, Assets.APP_LOGO)
		for i in range(1, 9): # So it loops 8 times starting at 1.
			if i <= self.slots:
				items["playerbox"][i] = playerbox.PlayerBox(i)
			else:
				items["playerbox"][i] = playerbox.PlayerBox(i, True)
		return items

	def draw(self, window):
		window.fill(BG_COLOR)
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(window)

	def update(self, events):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].update(events)

	def update_players(self, id_list):
		for slot in range(1, len(id_list) + 1):
			self.items["playerbox"][slot].update_player(id_list[slot - 1])

class InGameScreen:
	def __init__(self):
		self.items = self.setup_items()

	def setup_items(self):
		items = {}
		items["image"] = {}
		items["button"] = {}
		items["image"]["logo"] = image.Image(22, 0, Assets.APP_LOGO)
		items["image"]["message"] = image.Image(18, 140, Assets.GAME_STARTED)
		items["button"]["quit"] = imagebutton.ImageButton(92, 245,[Assets.QUIT_SELECTED, Assets.QUIT_UNSELECTED], True)
		return items

	def draw(self, window):
		window.fill(BG_COLOR)
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(window)

	def update(self, events):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].update(events)

	def check_end(self):
		return self.items["button"]["quit"].get_clicked()