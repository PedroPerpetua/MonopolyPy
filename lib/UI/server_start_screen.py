from libs.UI.items.image_asset import ImageAsset
from libs.UI.items.input_box import InputBox
from libs.UI.items.text_button import TextButton
from libs.UI.items.text_label import TextLabel
from libs.UI.items.number_picker import NumberPicker

BG_COLOR = (143, 188, 114)
RALEWAY = "libs/Raleway.ttf"

class Server_StartScreen:
	def __init__(self, window):
		self.win = window
		self.bg_color = BG_COLOR
		self.items = self.setup_items()
		
	def setup_items(self):
		items = {}
		items["image_asset"] = {}
		items["image_asset"]["logo"] = ImageAsset(150, 50, "server_logo", "C")
		items["text_label"] = {}
		items["text_label"]["host_label"] = TextLabel(20, 105, "Host IP", 20, RALEWAY, "L")
		items["text_label"]["port_label"] = TextLabel(20, 151, "Port", 20, RALEWAY, "L")
		items["text_label"]["players_label"] = TextLabel(160, 151, "Players", 20, RALEWAY, "L")
		items["text_label"]["password_label"] = TextLabel(20, 197, "Password", 20, RALEWAY, "L")
		items["input_box"] = {}
		items["input_box"]["host"] = InputBox(150, 136, 260, 20, "arial", "C")
		items["input_box"]["port"] = InputBox(20, 172, 120, 20, "arial", "L")
		items["input_box"]["password"] = InputBox(150, 228, 260, 20, "arial", "C")
		items["text_button"] = {}
		items["text_button"]["start"] = TextButton(150, 266, 100, 36, RALEWAY, "START", False, "C")
		items["number_drop"] = {}
		items["number_drop"]["players"] = NumberPicker(160, 172, 120, 20, "arial", 4, 2, 8, "L")
		return items

	def draw(self):
		self.win.fill(self.bg_color)
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].draw(self.win)

	def update(self, events):
		for item_type in self.items:
			for item in self.items[item_type]:
				self.items[item_type][item].update(events)

		if self.validate_input():
			self.items["text_button"]["start"].switch(True)
		else:
			self.items["text_button"]["start"].switch(False)


	def validate_input(self):
		values = []
		for item in self.items["input_box"]:
			values += [self.items["input_box"][item].get_text()]

		# Check if host is not an empty string
		if values[0] == "":
			return False
		# Check if port is a number
		try:
			int(values[1])
		except ValueError:
			return False
		#Check if password is not an empty string
		if values[2] == "":
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
		for item in self.items["input_box"]:
			values += [self.items["input_box"][item].get_text()]
		values[1] = int(values[1])
		values += [self.items["number_drop"]["players"].get_number()]
		return values

	def check_end(self):
		return self.items["text_button"]["start"].get_clicked()