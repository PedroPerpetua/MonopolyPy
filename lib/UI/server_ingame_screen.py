from libs.UI.items.image_asset import ImageAsset
from libs.UI.items.text_label import TextLabel
from libs.UI.items.text_button import TextButton

BG_COLOR = (143, 188, 114)
RALEWAY = "libs/Raleway.ttf"

class Server_IngameScreen:
	def __init__(self, window):
		self.win = window
		self.bg_color = BG_COLOR
		self.items = self.setup_items()

	def setup_items(self):
		items = {}
		items["image_asset"] = {}
		items["image_asset"]["logo"] = ImageAsset(150, 50, "server_logo", "C")
		items["text_label"] = {}
		items["text_label"]["ingame_label_1"] = TextLabel(150, 126, "The server is", 32, RALEWAY, "C")
		items["text_label"]["ingame_label_2"] = TextLabel(150, 158, "running...", 32, RALEWAY, "C")
		items["text_button"] = {}
		# items["text_button"]["show_game"] = TextButton(150, 204, 250, 40, RALEWAY, "Spectate Game", True, "C")
		items["text_button"]["close_server"] = TextButton(150, 224, 250, 40, RALEWAY, "Close Server", True, "C")
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

	def check_quit(self):
		return self.items["text_button"]["close_server"].get_clicked()