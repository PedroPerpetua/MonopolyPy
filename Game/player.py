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

	def serialize(self):
		return vars(self)

	def deserialize(info):
		result = Player()
		for key in info:
			setattr(result, key, info[key])
		return result