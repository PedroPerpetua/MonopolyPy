STARTING_MONEY = 1500
class Player:
	def __init__(self, name="", icon=None):
		self.name = name
		self.icon = icon
		self.position = 0
		self.money = STARTING_MONEY
		self.fields = []
		self.jail_counter = 0
		self.has_FreeJail = False
	def get_rail(self):
		return 0
	def get_util(self):
		return 0
	def is_jailed(self):
		return self.jail_counter != 0


	def serialize(self):
		info = {}
		info["name"] = self.name
		info["icon"] = self.icon
		info["position"] = self.position
		info["money"] = self.money
		info["fields"] = self.fields
		info["jail_counter"] = self.jail_counter
		info["has_FreeJail"] = self.has_FreeJail
		return info

	@staticmethod
	def deserialize(info):
		player = Player(info["name"], info["icon"])
		player.position = info["position"]
		player.money = info["money"]
		player.fields = info["fields"]
		player.jail_counter = info["jail_counter"]
		player.has_FreeJail = info["has_FreeJail"]
		return player