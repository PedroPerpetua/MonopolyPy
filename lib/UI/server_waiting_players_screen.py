from libs.UI.items.image_asset import ImageAsset
from libs.UI.items.player_box import PlayerBox

BG_COLOR = (143, 188, 114)

class Server_WaitingPlayersScreen:
	def __init__(self, window, num_players):
		self.win = window
		self.bg_color = BG_COLOR
		self.slots = num_players
		self.items = self.setup_items()

	def setup_items(self):
		items = {}
		items["image_asset"] = {}
		items["image_asset"]["logo"] = ImageAsset(150, 50, "server_logo", "C")
		items["player_box"] = {}
		for i in range(1, 9): # So it loops over 8 items - array starts at 1
			if i <= self.slots:
				items["player_box"]["player" + str(i)] = PlayerBox(i, False)
			else:
				items["player_box"]["player" + str(i)] = PlayerBox(i, True)
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

	def update_players(self, player_id_list):
		for player_box_id in range(1, len(player_id_list) + 1):
			self.items["player_box"]["player" + str(player_box_id)].update_player(player_id_list[player_box_id - 1])