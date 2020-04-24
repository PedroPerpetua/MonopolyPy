class Field:
	def field_deserialize(info):
		tag = info["tag"]
		if tag == "P":
			return Property.deserialize(info)
		elif tag == "R":
			return Railroad.deserialize(info)
		elif tag == "U":
			return Utility.deserialize(info)
		elif tag == "W":
			return WildcardField.deserialize(info)
		elif tag == "S":
			return SpecialField.deserialize(info)

class Property:
	def __init__(self, name="", price=0, color="", house_price=0, tax_values=[]):
		self.name = name
		self.price = price
		self.color = color
		self.house_price = house_price
		self.taxes = tax_values

		self.owner_id = None
		self.houses = 0
		self.mortaged = False

	def get_type(self):
		return "Property"

	def get_info(self):
		''' 
		Returns the info that should be drawn on the board:
			Number of houses;
			Whether or not mortaged.
		'''
		info = {}
		info["houses"] = self.houses
		info["mortaged"]= self.mortaged
		return info

	def get_tooltip_info(self):
		'''
		Returns the info that should show on the tooltip:
			Name;
			Price if not owned;
			Owner and current tax if owned.
		'''
		return [self.name, self.owner_id, self.price, self.taxes[self.houses]]


	def serialize(self):
		info = vars(self)
		info["tag"] = "P"
		return vars(self)

	def deserialize(info):
		result = Property()
		for key in info:
			if key == "tag":
				setattr(result, key, info[key])
		return result

class Railroad:
	def __init__(self, name=""):
		self.name = name
		self.price = 200
		self.taxes = [25, 50, 100, 200]

		self.owner_id = None

	def get_type(self):
		return "Railroad"

	def get_info(self):
		return {}

	def get_tooltip_info(self):
		'''
		Returns the info that should show on the tooltip:
			Name;
			Price if not owned;
			Owner and current tax if owned.
		'''
		return [self.name, self.owner_id, self.price, self.taxes]

	def serialize(self):
		info = vars(self)
		info["tag"] = "R"
		return vars(self)

	def deserialize(info):
		result = Railroad()
		for key in info:
			if key == "tag":
				setattr(result, key, info[key])
		return result

class Utility:
	def __init__(self, name=""):
		self.name = name
		self.price = 150
		self.owner_id = None


	def get_type(self):
		return self.name

	def get_info(self):
		return {}

	def get_tooltip_info(self):
		return None

	def serialize(self):
		info = vars(self)
		info["tag"] = "U"
		return vars(self)

	def deserialize(info):
		result = Utility()
		for key in info:
			if key == "tag":
				setattr(result, key, info[key])
		return result

class WildcardField:
	def __init__(self, card_type=""):
		self.card_type = card_type


	def get_type(self):
		return self.card_type

	def get_info(self):
		return {}

	def get_tooltip_info(self):
		return None

	def serialize(self):
		info = vars(self)
		info["tag"] = "W"
		return vars(self)

	def deserialize(info):
		result = WildcardField()
		for key in info:
			if key == "tag":
				setattr(result, key, info[key])
		return result

class SpecialField:
	def __init__(self, field_type=""):
		self.field_type = field_type

	def get_type(self):
		return self.field_type

	def get_info(self):
		return {}

	def get_tooltip_info(self):
		return None

	def serialize(self):
		info = vars(self)
		info["tag"] = "S"
		return vars(self)

	def deserialize(info):
		result = SpecialField()
		for key in info:
			if key == "tag":
				setattr(result, key, info[key])
		return result