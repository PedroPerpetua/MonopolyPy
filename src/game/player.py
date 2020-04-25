STARTING_MONEY = 1500

class Player:
	def __init__(self, icon, name):
		self.name = name
		self.icon = icon
		self.pos = 0
		self.contracts = []
		self.money = STARTING_MONEY

		self.jail_counter = 0
		self.jail_card = 0


	def is_jailed(self):
		return self.jail_counter != 0
	def get_icon(self):
		return self.icon
	def get_name(self):
		return self.name
	def get_rail(self):
		return 0
	def get_util(self):
		return 0
		
	def serialize(self):
		return vars(self)

	def deserialize(info):
		result = Player()
		for key in info:
			setattr(result, key, info[key])
		return result