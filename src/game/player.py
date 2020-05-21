import random

STARTING_MONEY = 1500


class Player:
	def __init__(self, name="", icon=None):
		self.name = name
		self.icon = icon
		self.pos = 0
		self.contracts = {
						"railroad": [], "utility": [],
						"brown": [], "light-blue": [], "magenta": [], "orange": [],
						"red": [], "yellow": [], "green": [], "blue": []
						}
		self.game = None
		self.money = STARTING_MONEY
		self.jail_counter = 0
		self.jail_card = 0

		self.can_roll = False

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
		if color in ["brown", "blue"]:
			return len(self.contracts[color] == 2)
		return len(self.contracts[color] == 3)

	def can_place_house(self, field):
		if field.owner != self:
			return False
		if not self.has_monopoly(field.color):
			return False
		if field.houses == 5:
			return False
		return True

	def move(self, number):
		new_pos = self.pos + number
		if new_pos >= 40:
			new_pos += -40
			self.money += 200
		self.pos = new_pos

	def dice_roll(self):
		roll1 = random.randint(1, 6)
		roll2 = random.randint(1, 6)
		return (roll1, roll2)
	
	def turn_roll(self):
		roll = self.dice_roll()
		if self.jail_counter == 0:
			self.move(roll[0] + roll[1])
			self.game.fields[self.pos].do_action(self, roll)
			if roll[0] != roll[2]:
				self.can_roll = False
		else:
			if roll[0] == roll[1]:
				self.jail_counter = 0
				self.move(roll[0] + roll[1])
			self.can_roll = False

	def serialize(self):
		return vars(self)

	@staticmethod
	def deserialize(info):
		result = Player()
		for key in info:
			setattr(result, key, info[key])
		return result