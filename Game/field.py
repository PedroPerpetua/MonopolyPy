"""
Field class and its subclasses:
	+Contract_Field
		+Property
		+Railroad
		+Utility
	+Special
"""

class Field(object):
	def __init__(self, name):
		self.name = name

	def do_action(self, player):
		pass

class Contract_Field(Field):
	def __init__(self, name, price):
		super().__init__(name)
		self.price = price
		self.owner = None
		self.state = True

	def mortgage(self):
		"""
		Mortgages the contract, paying the owner the amount and changing the contract's state to False.
		
		Returns:
		    Bool: True on success.
		"""
		if self.state:
			self.state = False;
			self.owner.add_money(self.price/2)
			return True
		else:
			return False

	def do_action(self, player):
		pass

class Property(Contract_Field):
	def __init__(self, name, price, color, house_price, tax_values):
		"""
		Initializes a Property
		
		Args:
		    name (string): Property's name.
		    price (int): Property's price.
		    color (string): Property's color.
		    house_price (int): Price of a house in the property.
		    tax_values (int[]): tax value according to the number of houses.
		"""
		super().__init__(name, price)
		self.color = color 
		self.houses = 0 # 1,2,3 and 4 equal number of houses, 5 equal a hotel
		self.house_price = house_price
		self.tax_values = tax_values

	def do_action(self, player):
		if self.owner == None:
			super().do_action(player)
		elif self.owner == player:
			pass
		elif self.state:
			print("PAY")
		# if self.owner = None:
		# 	super().do_action(player)
		# elif self.owner = player:
		# 	pass
		# elif self.state:
		# 	if self.owner.has_monopoly(self.color) && self.houses = 0:
		# 		player.pay_player(self.owner, self.tax_values[0] * 2)
		# 	else:
		# 		player.pay_player(self.owner, self.tax_values[self.houses])

	def buy_house(self):
		"""
		Buys a house on the property.
		
		Returns:
		    Bool: True if successful
		"""
		if self.owner.has_monopoly(self.color) == False or self.houses >= 5:
			return False
		self.owner.pay_player(None, self.house_price)
		houses += 1
		return True

	def sell_house(self):
		"""
		Sells off a house on the property
		
		Returns:
		    Bool: True if successfull
		"""
		if self.houses == 0:
			return False
		self.owner.add_money(self.house_price/2)
		self.houses += -1
		return True



class Railroad(Contract_Field):
	def __init__(self, name):
		super().__init__(name, 200)
		self.tax_values = [25, 50, 100, 200]

	def do_action(self, player):
		# TODO: Implement
		pass

class Utility(Contract_Field):
	def __init__(self, name):
		super().__init__(name, 150)

	def do_action(self, player):
		#TODO: Implement
		pass

class Special_Field(Field):
	def __init__(self, name):
		super().__init__(name)

	def do_action(self, player):
		#TODO: Implement
		pass