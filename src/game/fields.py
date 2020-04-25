class Field:
	def field_deserialize(info):
		tag = info["tag"]
		if tag == "P":
			return Property.deserialize(info)
		elif tag == "R":
			return Railroad.deserialize(info)
		elif tag == "U":
			return Utility.deserialize(info)
		elif tag == "T":
			return Tax.deserialize(info)
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
		info = {}
		info["houses"] = self.houses
		info["mortaged"]= self.mortaged
		return info
	def get_tooltip(self):
		info = {}
		info["name"] = self.name
		info["owner_id"] = self.owner_id
		info["type"] = self.get_type()
		info["color"] = self.color
		info["houses"] = str(self.houses)
		info["house_price"] = str(self.house_price)
		if self.owner_id != None:
			info["value"] = str(self.taxes[self.houses])
		else:
			info["value"] = str(self.price)
		return info

	def serialize(self):
		info = vars(self)
		info["tag"] = "P"
		return vars(self)
	def deserialize(info):
		result = Property()
		for key in info:
			if key != "tag":
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
	def get_tooltip(self):
		info = {}
		info["name"] = self.name
		info["type"] = self.get_type()
		info["owner_id"] = self.owner_id
		if not self.owner_id:
			info["rail"] = str(self.price)
		return info

	def serialize(self):
		info = vars(self)
		info["tag"] = "R"
		return vars(self)
	def deserialize(info):
		result = Railroad()
		for key in info:
			if key != "tag":
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
	def get_tooltip(self):
		return {"type": "Utility", "name": self.name, "util": str(self.price)}

	def serialize(self):
		info = vars(self)
		info["tag"] = "U"
		return vars(self)

	def deserialize(info):
		result = Utility()
		for key in info:
			if key != "tag":
				setattr(result, key, info[key])
		return result

class Tax:
	def __init__(self, name="", tax_value=""):
		self.name = name
		self.tax_value = tax_value

	def get_type(self):
		return self.name

	def get_info(self):
		return {}
	def get_tooltip(self):
		return {"name": self.name, "tax": self.tax_value, "type": "Tax"}

	def serialize(self):
		info = vars(self)
		info["tag"] = "T"
		return vars(self)

	def deserialize(info):
		result = Tax()
		for key in info:
			if key != "tag":
				setattr(result, key, info[key])
		return result


class WildcardField:
	def __init__(self, card_type=""):
		self.card_type = card_type

	def get_type(self):
		return self.card_type
	def get_info(self):
		return {}
	def get_tooltip(self):
		return {"name": self.card_type, "type": "WildCard"}

	def serialize(self):
		info = vars(self)
		info["tag"] = "W"
		return vars(self)
	def deserialize(info):
		result = WildcardField()
		for key in info:
			if key != "tag":
				setattr(result, key, info[key])
		return result


class SpecialField:
	def __init__(self, field_type=""):
		self.field_type = field_type

	def get_type(self):
		return self.field_type
	def get_info(self):
		return {}
	def get_tooltip(self):
		return {"name": self.field_type, "type": "Special"}

	def serialize(self):
		info = vars(self)
		info["tag"] = "S"
		return vars(self)
	def deserialize(info):
		result = SpecialField()
		for key in info:
			if key != "tag":
				setattr(result, key, info[key])
		return result