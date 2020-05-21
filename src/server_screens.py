from lib.assets import Assets
from socket import getaddrinfo, gaierror
from lib.UI.items import image, inputbox, textlabel, numberpicker, imagebutton, playerbox
import pygame as pg
from os import startfile as open_link

BG_COLOR = (143, 188, 114)
BLACK = (0, 0, 0)

class StartScreen:
	def __init__(self):
		self.items = {}
		self.items["image"] = {}
		self.items["textlabel"] = {}
		self.items["inputbox"] = {}
		self.items["numberpicker"] = {}
		self.items["button"] = {}
		self.items["image"]["logo"] = image.Image(22, 0, Assets.APP_LOGO)
		self.items["textlabel"]["host"] = textlabel.TextLabel(20, 113, "Host IP", 20, Assets.PIXEL)
		self.items["inputbox"]["host"] = inputbox.InputBox(20, 128, 260, 20, Assets.ARIAL)
		self.items["textlabel"]["port"] = textlabel.TextLabel(20, 156, "Port", 20, Assets.PIXEL)
		self.items["textlabel"]["players"] = textlabel.TextLabel(160, 156, "Players", 20, Assets.PIXEL)
		self.items["inputbox"]["port"] = inputbox.InputBox(20, 171, 120, 20, Assets.ARIAL, True)
		self.items["numberpicker"]["players"] = numberpicker.NumberPicker(160, 171, 120,
			[Assets.MINUS_SELECTED, Assets.MINUS_UNSELECTED], [Assets.PLUS_SELECTED, Assets.PLUS_UNSELECTED], 4, 2, 8)
		self.items["textlabel"]["password"] = textlabel.TextLabel(20, 204, "Password", 20, Assets.PIXEL)
		self.items["inputbox"]["password"] = inputbox.InputBox(20, 219, 260, 20, Assets.ARIAL)
		self.items["button"]["start"] = imagebutton.ImageButton(53, 245, [Assets.START_SELECTED, Assets.START_UNSELECTED], False)
		self.items["button"]["help"] = imagebutton.ImageButton(203, 245, [Assets.HELP_SELECTED, Assets.HELP_UNSELECTED], True)

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
			if self.items["inputbox"][box].text == "":
				return False
		return True
	
	@staticmethod
	def screen_loop(window, info):
		screen = StartScreen()
		while True:
			pg.time.delay(100)
			events = pg.event.get()
			for event in events:
				if event.type == pg.QUIT:
					pg.quit()
					exit(0)
			if screen.items["button"]["help"].clicked:
				HelpScreen.screen_loop(window, info)
			if screen.items["button"]["start"].clicked:
				try:
					# Checks if the address is valid
					getaddrinfo(screen.items["inputbox"]["host"].text, int(screen.items["inputbox"]["port"].text))
					break
				except gaierror:
					ErrorBox.screen_loop(window, "Invalid Server")
			screen.update(events)
			screen.draw(window)
			pg.display.update()
		info["host"] = screen.items["inputbox"]["host"].text
		info["port"] = int(screen.items["inputbox"]["port"].text)
		info["password"] = screen.items["inputbox"]["password"].text
		info["num_players"] = screen.items["numberpicker"]["players"].value


class HelpScreen:
	def __init__(self):
		self.items = {}
		self.items["image"] = {}
		self.items["button"] = {}
		self.items["image"]["about"] = image.Image(25, 25, Assets.ABOUT)
		self.items["button"]["whatsmyip"] = imagebutton.ImageButton(125, 80, [Assets.INTERNET_SELECTED, Assets.INTERNET_UNSELECTED], True)
		self.items["button"]["github"] = imagebutton.ImageButton(60, 185, [Assets.GIT_SELECTED, Assets.GIT_UNSELECTED], True)
		self.items["button"]["return"] = imagebutton.ImageButton(68, 245, [Assets.RETURN_SELECTED, Assets.RETURN_UNSELECTED], True)

	def draw(self, window):
		window.fill(BG_COLOR)
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(window)

	def update(self, events):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].update(events)

	@staticmethod
	def screen_loop(window, _):
		screen = HelpScreen()
		while True:
			pg.time.delay(100)
			events = pg.event.get()
			for event in events:
				if event.type == pg.QUIT:
					pg.quit()
					exit(0)
			if screen.items["button"]["github"].clicked:
				open_link("https://github.com/PedroPerpetua/MonopolyPy")
			if screen.items["button"]["whatsmyip"].clicked:
				open_link("https://www.whatsmyip.org/")
			if screen.items["button"]["return"].clicked:
				break
			screen.update(events)
			screen.draw(window)
			pg.display.update()

class QueueScreen:
	def __init__(self, num_players):
		self.items = {}
		self.items["image"] = {}
		self.items["playerbox"] = {}
		self.items["image"]["logo"] = image.Image(22, 0, Assets.APP_LOGO)
		for i in range(1, 9): # So it loops 8 times starting at 1.
			if i <= num_players:
				self.items["playerbox"][i] = playerbox.PlayerBox(i)
			else:
				self.items["playerbox"][i] = playerbox.PlayerBox(i, True)

	def draw(self, window):
		window.fill(BG_COLOR)
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(window)

	def update(self, events):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].update(events)

	def update_players(self, info):
		for slot in range(1, len(info["tags"])):
			self.items["playerbox"][slot].update_player(info["tags"][slot])
	
	@staticmethod
	def screen_loop(window, info):
		screen = QueueScreen(info["num_players"])
		while True:
			pg.time.delay(100)
			events = pg.event.get()
			for event in events:
				if event.type == pg.QUIT:
					info["server"].close_server("PG QUIT")
					pg.quit()
					exit(0)
			if info["server"].game:
				break
			screen.update_players(info["server"].get_info())
			screen.update(events)
			screen.draw(window)
			pg.display.update()

class InGameScreen:
	def __init__(self):
		self.items = {}
		self.items["image"] = {}
		self.items["button"] = {}
		self.items["image"]["logo"] = image.Image(22, 0, Assets.APP_LOGO)
		self.items["image"]["message"] = image.Image(18, 140, Assets.GAME_STARTED)
		self.items["button"]["quit"] = imagebutton.ImageButton(92, 245, [Assets.QUIT_SELECTED, Assets.QUIT_UNSELECTED], True)

	def draw(self, window):
		window.fill(BG_COLOR)
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(window)

	def update(self, events):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].update(events)

	@staticmethod
	def screen_loop(window, info):
		screen = InGameScreen()
		while True:
			pg.time.delay(100)
			events = pg.event.get()
			for event in events:
				if event.type == pg.QUIT:
					info["server"].close_server("PG QUIT")
					pg.quit()
					exit(0)
			if screen.items["button"]["quit"].clicked:
				info["server"].close_server("PG QUIT")
				pg.quit()
				exit(0)
			screen.update(events)
			screen.draw(window)
			pg.display.update()

class ErrorBox:
	def __init__(self, message):
		self.items = {}
		self.items["textlabel"] = {}
		self.items["button"] = {}
		self.items["textlabel"]["message"] = textlabel.TextLabel(55, 134, message, 24, Assets.ARIAL)
		self.items["button"]["return"] = imagebutton.ImageButton(213, 134, [Assets.X_SELECTED, Assets.X_UNSELECTED], True)
		self.box = pg.rect.Rect((50, 130), (200, 40))
	
	def draw(self, window):
		pg.draw.rect(window, BLACK, ((self.box.left - 3, self.box.top - 3), (self.box.width + 6, self.box.height + 6)))
		pg.draw.rect(window, BG_COLOR, self.box)
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(window)

	
	def update(self, events):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].update(events)
	
	@staticmethod
	def screen_loop(window, info):
		screen = ErrorBox(info)
		while True:
			pg.time.delay(100)
			events = pg.event.get()
			for event in events:
				if event.type == pg.QUIT:
					pg.quit()
					exit(0)
			if screen.items["button"]["return"].clicked:
				break
			screen.update(events)
			screen.draw(window)
			pg.display.update()