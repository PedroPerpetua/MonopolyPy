from lib.assets import Assets
from lib.UI.items import image, inputbox, textlabel, imagebutton, iconselector
from lib.UI.board_items import board
from os import startfile as open_link
from src.client import Client
import pygame as pg

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
		self.items["image"]["logo"] = image.Image(128, 0, Assets.APP_LOGO)
		self.items["textlabel"]["host"] = textlabel.TextLabel(128, 290, "Host IP", 48, Assets.PIXEL)
		self.items["inputbox"]["host"] = inputbox.InputBox(128, 338, 856, 48, Assets.ARIAL)
		self.items["textlabel"]["port"] = textlabel.TextLabel(1024, 290, "Port", 48, Assets.PIXEL)
		self.items["inputbox"]["port"] = inputbox.InputBox(1024, 338, 128, 48, Assets.ARIAL, True)
		self.items["textlabel"]["password"] = textlabel.TextLabel(128, 426, "Password", 48, Assets.PIXEL)
		self.items["inputbox"]["password"] = inputbox.InputBox(128, 474, 1024, 48, Assets.ARIAL)
		self.items["button"]["connect"] = imagebutton.ImageButton(398, 572, [Assets.CONNECT_SELECTED, Assets.CONNECT_UNSELECTED], False)
		self.items["button"]["help"] = imagebutton.ImageButton(794, 572, [Assets.HELP_SELECTED, Assets.HELP_UNSELECTED], True)

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
			self.items["button"]["connect"].switch(True)
		else:
			self.items["button"]["connect"].switch(False)

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
			if screen.items["button"]["connect"].clicked:
				try:
					client = Client(screen.items["inputbox"]["host"].text, int(screen.items["inputbox"]["port"].text), screen.items["inputbox"]["password"].text)
					client.connect()
					info["client"] = client
					break
				except ConnectionAbortedError:
					ErrorBox.screen_loop(window, "Wrong Password")
				except ConnectionRefusedError:
					ErrorBox.screen_loop(window, "Server Offline")
			screen.update(events)
			screen.draw(window)
			pg.display.update()

class HelpScreen:
	def __init__(self):
		self.items = {}
		self.items["image"] = {}
		self.items["button"] = {}
		self.items["image"]["logo"] = image.Image(128, 0, Assets.APP_LOGO)
		self.items["image"]["about"] = image.Image(128, 290, Assets.ABOUT)
		self.items["button"]["github"] = imagebutton.ImageButton(260, 430, [Assets.GIT_SELECTED, Assets.GIT_UNSELECTED], True)
		self.items["button"]["return"] = imagebutton.ImageButton(476, 572, [Assets.RETURN_SELECTED, Assets.RETURN_UNSELECTED], True)

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
			if screen.items["button"]["return"].clicked:
				break
			screen.update(events)
			screen.draw(window)
			pg.display.update()

class ProfileScreen:
	def __init__(self, client):
		self.items = {}
		self.items["image"] = {}
		self.items["textlabel"] = {}
		self.items["inputbox"] = {}
		self.items["iconselector"] = {}
		self.items["button"] = {}
		self.items["image"]["logo"] = image.Image(128, 0, Assets.APP_LOGO)
		self.items["textlabel"]["name"] = textlabel.TextLabel(568, 290, "name", 48, Assets.PIXEL)
		self.items["inputbox"]["name"] = inputbox.InputBox(540, 338, 200, 48, Assets.ARIAL)
		self.items["iconselector"]["selector"] = iconselector.IconSelector(492, 405, Assets.ICONS["LARGE"])
		self.items["button"]["submit"] = imagebutton.ImageButton(480, 572, [Assets.SUBMIT_SELECTED, Assets.SUBMIT_UNSELECTED], False)
		
		self.client = client
		self.submited = False
		self.wait_text = textlabel.TextLabel(322, 602, "Waiting for game to start.", 36, Assets.PIXEL)

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
			if self.items["button"]["submit"].clicked:
				self.client.send_profile(self.items["inputbox"]["name"].text, self.items["iconselector"]["selector"].selected)
				del self.items["button"]["submit"]
				self.submited = True
		self.items["iconselector"]["selector"].update_info(self.client.available_icons)

	def validate_input(self):
		return self.items["inputbox"]["name"].text != "" and self.items["iconselector"]["selector"].selected is not None

	@staticmethod
	def screen_loop(window, info):
		screen = ProfileScreen(info["client"])
		while True:
			pg.time.delay(100)
			events = pg.event.get()
			for event in events:
				if event.type == pg.QUIT:
					pg.quit()
					screen.client.disconnect()
					exit(0)
			if screen.client.game:
				break
			screen.update(events)
			screen.draw(window)
			pg.display.update()

class GameScreen:
	def __init__(self, client):
		self.client = client
		self.items = {}
		self.items["game_items"] = {}
		self.items["game_items"]["board"] = board.Board(10, 10, (720, 720), self.client.game)

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
		screen = GameScreen(info["client"])
		while True:
			pg.time.delay(100)
			events = pg.event.get()
			for event in events:
				if event.type == pg.QUIT:
					pg.quit()
					screen.client.disconnect()
					exit(0)
			screen.update(events)
			screen.draw(window)
			pg.display.update()

class ErrorBox:
	def __init__(self, message):
		self.items = {}
		self.items["textlabel"] = {}
		self.items["button"] = {}
		self.items["textlabel"]["message"] = textlabel.TextLabel(345, 325, message, 60, Assets.ARIAL)
		self.items["button"]["return"] = imagebutton.ImageButton(846, 316, [Assets.X_SELECTED, Assets.X_UNSELECTED], True)
		self.box = pg.rect.Rect((340, 310), (600, 100))
	
	def draw(self, window):
		pg.draw.rect(window, BLACK, ((self.box.left - 10, self.box.top - 10), (self.box.width + 20, self.box.height + 20)))
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