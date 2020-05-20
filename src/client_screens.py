from lib.assets import Assets
from lib.UI.items import image, inputbox, textlabel, imagebutton, iconselector
from lib.UI.board_items import board
import os

BG_COLOR = (143, 188, 114)

class StartScreen:
	def __init__(self):
		self.items = StartScreen.setup_items()
		self.help = HelpScreen()
		self.show_help = False

	@staticmethod
	def setup_items():
		items = {}
		items["image"] = {}
		items["textlabel"] = {}
		items["inputbox"] = {}
		items["numberpicker"] = {}
		items["button"] = {}
		items["image"]["logo"] = image.Image(128, 0, Assets.APP_LOGO)
		items["textlabel"]["host"] = textlabel.TextLabel(128, 290, "Host IP", 48, Assets.PIXEL)
		items["inputbox"]["host"] = inputbox.InputBox(128, 338, 856, 48, Assets.ARIAL)
		items["textlabel"]["port"] = textlabel.TextLabel(1024, 290, "Port", 48, Assets.PIXEL)
		items["inputbox"]["port"] = inputbox.InputBox(1024, 338, 128, 48, Assets.ARIAL, True)
		items["textlabel"]["password"] = textlabel.TextLabel(128, 426, "Password", 48, Assets.PIXEL)
		items["inputbox"]["password"] = inputbox.InputBox(128, 474, 1024, 48, Assets.ARIAL)
		items["button"]["connect"] = imagebutton.ImageButton(398, 572, [Assets.CONNECT_SELECTED, Assets.CONNECT_UNSELECTED], False)
		items["button"]["help"] = imagebutton.ImageButton(794, 572, [Assets.HELP_SELECTED, Assets.HELP_UNSELECTED], True)
		return items

	def draw(self, window):
		window.fill(BG_COLOR)
		if self.show_help:
			self.help.draw(window)
		else:
			for item_type in self.items:
				for item in self.items[item_type]:
					self.items[item_type][item].draw(window)

	def update(self, events):
		if self.show_help:
			self.help.update(events)
			if self.help.check_end():
				self.show_help = False
			if self.help.items["button"]["github"].get_clicked():
				os.startfile("https://github.com/PedroPerpetua/MonopolyPy")
		else:
			for item_type in self.items:
				for item in self.items[item_type]:
					self.items[item_type][item].update(events)
			
			if self.validate_input():
				self.items["button"]["connect"].switch(True)
			else:
				self.items["button"]["connect"].switch(False)
			if self.items["button"]["help"].get_clicked():
				self.show_help = True


	def validate_input(self):
		for box in self.items["inputbox"]:
			if self.items["inputbox"][box].get_text() == "":
				return False
		return True

	def get_values(self):
		values = []
		for box in self.items["inputbox"]:
			values += [self.items["inputbox"][box].get_text()]
		values[1] = int(values[1])
		return values

	def submited(self):
		return self.items["button"]["connect"].get_clicked()

class HelpScreen:
	def __init__(self):
		self.items = HelpScreen.setup_items()

	@staticmethod
	def setup_items():
		items = {}
		items["image"] = {}
		items["button"] = {}
		items["image"]["logo"] = image.Image(128, 0, Assets.APP_LOGO)
		items["image"]["about"] = image.Image(128, 290, Assets.ABOUT)
		items["button"]["github"] = imagebutton.ImageButton(260, 430, [Assets.GIT_SELECTED, Assets.GIT_UNSELECTED], True)
		items["button"]["return"] = imagebutton.ImageButton(476, 572, [Assets.RETURN_SELECTED, Assets.RETURN_UNSELECTED], True)
		return items

	def draw(self, window):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(window)

	def update(self, events):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].update(events)

	def check_end(self):
		return self.items["button"]["return"].get_clicked()

class ProfileScreen:
	def __init__(self, client):
		self.items = ProfileScreen.setup_items()
		self.client = client
		self.submited = False
		self.wait_text = textlabel.TextLabel(322, 602, "Waiting for game to start.", 36, Assets.PIXEL)
	
	@staticmethod
	def setup_items():
		items = {}
		items["image"] = {}
		items["textlabel"] = {}
		items["inputbox"] = {}
		items["iconselector"] = {}
		items["button"] = {}
		items["image"]["logo"] = image.Image(128, 0, Assets.APP_LOGO)
		items["textlabel"]["name"] = textlabel.TextLabel(568, 290, "name", 48, Assets.PIXEL)
		items["inputbox"]["name"] = inputbox.InputBox(540, 338, 200, 48, Assets.ARIAL)
		items["iconselector"]["selector"] = iconselector.IconSelector(492, 405, Assets.ICONS["LARGE"])
		items["button"]["submit"] = imagebutton.ImageButton(480, 572, [Assets.SUBMIT_SELECTED, Assets.SUBMIT_UNSELECTED], False)
		return items

	def draw(self, window):
		window.fill(BG_COLOR)
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(window)
		if self.submited:
			self.wait_text.draw(window)


	def update(self, events):
		if not self.submited:
			for item_type in self.items:
				for item in self.items[item_type]:
					self.items[item_type][item].update(events)
			if self.validate_input():
				self.items["button"]["submit"].switch(True)
			else:
				self.items["button"]["submit"].switch(False)
			if self.items["button"]["submit"].get_clicked():
				self.client.send_profile(self.items["inputbox"]["name"].get_text(), self.items["iconselector"]["selector"].get_selected())
				del self.items["button"]["submit"]
				self.submited = True
		self.items["iconselector"]["selector"].update_info(self.client.available_icons)

	def validate_input(self):
		return self.items["inputbox"]["name"].get_text() != "" and self.items["iconselector"]["selector"].get_selected() is not None

class GameScreen:
	def __init__(self, client):
		self.client = client
		self.items = GameScreen.setup_items()
		self.items["game_items"]["board"] = board.Board(10, 10, (720, 720), self.client.game)

	@staticmethod
	def setup_items():
		items = {}
		items["game_items"] = {}
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