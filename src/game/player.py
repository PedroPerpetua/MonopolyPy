STARTING_MONEY = 1500

class Player:
	def __init__(self, icon=None, name=""):
		self.name = name
		self.icon = icon
		self.pos = 0
		self.contracts = {
						"railroad": [], "utility": [],
						"brown": [], "light-blue": [], "magenta": [], "orange": [],
						"red": [], "yellow": [], "green": [], "blue": []
						}
		self.money = STARTING_MONEY
		self.jail_counter = 0
		self.jail_card = 0

	def is_jailed(self):
		return self.jail_counter != 0
	def get_icon(self):
		return self.icon

	def get_rail(self):
		return 50 * len(self.contracts["railroad"])
	def get_util(self):
		if len(self.contracts["utility"]) == 2:
			return 10
		elif len(self.contracts["utility"]) == 1:
			return 4
		else:
			return 0
	
	def add_contract(self, field):
		self.contracts[field.get_contract()].append(field)
		field.owner = self
	def remove_contract(self, field):
		self.contracts[field.get_contract()].remove(field)
		field.owner = None

	def has_monopoly(self, color):
		if color in ["railroad, utility"]:
			return False
		elif color in ["brown", "blue"]:
			return len(self.contracts[color] == 2)
		else:
			return len(self.contracts[color] == 3)

	def can_place_house(self, field):
		if field.owner != self:
			return False
		if not self.has_monopoly(field.color):
			return False
		if field.houses == 5:
			return False

	def serialize(self):
		return vars(self)

	@staticmethod
	def deserialize(info):
		result = Player()
		for key in info:
			setattr(result, key, info[key])
		return result