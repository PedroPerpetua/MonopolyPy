"""
Player class.
"""
import random

STARTING_MONEY = 1500

class Player(object):

	"""
	Representes a player.
	
	Attributes:
	    contracts (dict): dictionary containing all the contracts the player owns. Format: "color": contract.
	    game_board (Game_Board): game in wich the player is included.
	    icon (char): char that represents the player on the board.
	    jail_counter (int): if the counter is more than 0, it represents the number of rolls left till the player can leave jail.
	    money (int): amount of money that the player has.
	    name (string): player's name.
	    pos (int): player's position on the bame_board
	    STARTINT_MONEY (int): variable that represents the amount of money each player starts with.
	"""
	def __init__(self, name, icon):
		"""
		Initializes a Player
		
		Args:
		    name (string): name of the player.
		    icon (char): character that represents the player on the board
		    game_board (Game_Board): the game that the player is a part of
		"""
		self.name = name
		self.pos = 0
		self.icon = icon
		self.game_board = None
		self.money = STARTING_MONEY
		self.contracts = {"brown":[], "light-blue": [], "magenta": [], "orange": [], "red": [], "yellow": [], "green": [], "blue": [], "railroad": [], "utility": []}
		self.jail_counter = 0

	def join_game_board(self, board):
		self.game_board = board
		self.game_board.add_player(self)

	def add_money(self, ammount):
		"""
		Adds/subtracts the ammount of money from the player.

		Args:
		    ammount (int): ammount to add.
		"""
		self.money += ammount

	def add_contract(self, contract):
		"""
		Adds a contract to the player's contract list.
		
		Args:
		    contract (Contract_Field): contract to add.
		
		Raises:
		    Exception: Invalid type of contract to add.
		"""
		if isinstance(contract, Property):
			self.contracts[Property.color].append(contract)
		elif isinstance(contract, Railroad):
			self.contracts["railroad"].append(contract)
		elif isinstance(contract, Utility):
			self.contracts["utility"].append(contract)
		else:
			raise Exception("Invalid type of contract.")

	def remove_contract(self, contract):
		"""
		Removes a contract from the player's contracts.
		
		Args:
		    contract (Contract_Field): contract to be removed.
		
		Raises:
		    Exception: Player doesn't own that contract.
		"""
		try:
			if isinstance(contract, Property):
				self.contracts[Property.color].remove(contract)
			elif isinstance(contract, Railroad):
				self.contracts["railroad"].remove(contract)
			elif isinstance(contract, Utility):
				self.contracts["utility"].remove(contract)
			else:
				raise Exception("Invalid type of contract.")
		except ValueError as e:
			raise Exception("Player doesn't own that contract")

	def roll(self):
		"""
		Rolls two dice.
		
		Returns:
		    Tupple: both results.
		"""
		roll1 = random.randint(1,6)
		roll2 = random.randint(1,6)
		result = (roll1, roll2)
		print(f"[GAME]: player {self.name} rolled a {roll1} and a {roll2}.")
		return result

	def roll_DEBUG(self, roll1, roll2):
		print(f"[GAME]: player {self.name} rolled a {roll1} and a {roll2}. DEBUG.")
		return (roll1, roll2)

	def move(self, roll):
		"""
		Moves the player after a roll
		
		Args:
		    roll (Tupple): Tupple containing the rolls.
		"""
		new_pos = self.pos + roll[0] + roll[1]
		self.move_to(new_pos)


	def move_to(self, new_pos):
		"""
		Moves the player to a new position.
		
		Args:
		    new_pos (int): Position to be moved to.
		"""
		new_pos = new_pos%40 # in case it trys to move to a space out of the board
		orig_pos, self.pos = self.pos, new_pos
		if new_pos - orig_pos < 0:
			self.money += 200
			print(f"[GAME]: {self.name} passed the starting house and earned 200€")
		self.game_board.fields[self.pos].do_action(self)

	def has_monopoly(self, color):
		"""
		Checks if a player has monopoly on the specified color.
		
		Args:
		    color (string): color to check.
		
		Returns:
		    bool: True if the player has monopoly on the specified color.
		"""
		for color in self.contracts:
			if (color != "railroad" and color != "utility") or (len(self.contracts[color]) == 3) or	(len.self.contracts[color] == 2 and (color == "brown" or color == "blue")):
				return True
			else:
				return False

	def __repr__(self):
		return "Player:  " + self.name + " (" + self.icon + ")\nBalance: " + str(self.money) + "€\nPosition: " + self.game_board.fields[self.pos].name