from lib.assets import Assets
from lib.UI.board_items.constants import get_rgb

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
	# The last few don't hold any data, so we can just create new ones
	elif tag == "C0":
		return StartField()
	elif tag == "C1":
		return JailField()
	elif tag == "C2":
		return FreeParkingField()
	elif tag == "C3":
		return GoToJailField()


class Property:
	def __init__(self, name="", price=0, color="", house_price=0, tax_values=[]):
		self.name = name
		self.price = price
		self.color = color
		self.house_price = house_price
		self.taxes = tax_values
		self.owner = None
		self.houses = 0
		self.mortaged = False

	def get_contract(self):
		return self.color

	def get_type(self):
		return "property"

	def get_field(self):
		info = {}
		info["color"] = self.color
		info["houses"] = self.houses
		info["mortaged"] = self.mortaged
		return info

	def get_tooltip(self):
		info = {}
		info["type"] = "property"
		info["name"] = self.name
		if self.owner is not None:
			info["owner"] = "Unowned"
			info["value"] = "Price: " + str(self.price) + "€"
		else:
			info["owner"] = self.owner.name
			if self.mortaged:
				info["value"] = "MORTAGED!"
			else:
				info["value"] = "Tax: " + str(self.taxes[self.houses]) + "€"
		info["color"] = get_rgb(self.color)
		info["houses"] = "Houses: " + str(self.houses)
		info["house_price"] = "House price: " + str(self.house_price) + "€"
		return info

	def do_action(self, player, roll):
		pass

	def serialize(self):
		info = vars(self)
		info["tag"] = "P"
		return vars(self)

	@staticmethod
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
		self.owner = None

	def get_contract(self):
		return "railroad"

	def get_type(self):
		return "icon"

	def get_field(self):
		info = {}
		info["image"] = Assets.TRAIN
		info["color"] = (128, 128, 128) # Light-Gray
		return info

	def get_tooltip(self):
		info = {}
		info["type"] = "single"
		info["name"] = self.name
		info["color"] = (128, 128, 128) # Light-Gray
		if self.owner is not None:
			info["owner"] = "Unowned"
			info["label"] = "Price: " + str(self.price) + "€"
		else:
			info["owner"] = self.owner.name
			info["label"] = "Tax: " + str(self.owner.get_rail()) + "€"
		return info

	def do_action(self, player, roll):
		pass

	def serialize(self):
		info = vars(self)
		info["tag"] = "R"
		return vars(self)

	@staticmethod
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
		self.owner = None

	def get_contract(self):
		return "utility"

	def get_type(self):
		return "icon"

	def get_field(self):
		info = {}
		if self.name == "Electric Company":
			image = Assets.COMPANY_ELECTRICITY
		else:
			image = Assets.COMPANY_WATER
		info["image"] = image
		info["color"] = (153, 255, 255) # Light-Cyan
		return info

	def get_tooltip(self):
		info = {}
		info["type"] = "single"
		info["name"] = self.name
		info["color"] = (153, 255, 255) # Light-Cyan
		if self.owner is not None:
			info["owner"] = "Unowned"
			info["label"] = "Price: " + str(self.price) + "€"
		else:
			info["owner"] = self.owner.name
			info["label"] = "Tax: " + str(self.owner.get_util()) + " times the dice roll"
		return info

	def serialize(self):
		info = vars(self)
		info["tag"] = "U"
		return vars(self)

	@staticmethod
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
		return "icon"

	def get_field(self):
		info = {}
		if self.name == "Income Tax":
			image = Assets.TAX_INCOME
		else:
			image = Assets.TAX_LUXURY
		info["image"] = image
		info["color"] = (255, 255, 255) # White
		return info

	def get_tooltip(self):
		info = {}
		info["type"] = "single_label"
		info["name"] = self.name
		info["color"] = (255, 255, 255) # White
		info["label"] = "Tax: " + str(self.tax_value) + "€"
		return info

	def serialize(self):
		info = vars(self)
		info["tag"] = "T"
		return vars(self)
	
	@staticmethod
	def deserialize(info):
		result = Tax()
		for key in info:
			if key != "tag":
				setattr(result, key, info[key])
		return result


class WildcardField:
	def __init__(self, name=""):
		self.name = name

	def get_type(self):
		return "icon"

	def get_field(self):
		info = {}
		if self.name == "Luck":
			image = Assets.LUCK
		else:
			image = Assets.COMMUNITY_CHEST
		info["image"] = image
		info["color"] = (255, 255, 255) # White
		return info

	def get_tooltip(self):
		info = self.get_field()
		info["type"] = "wildcard"
		info["name"] = self.name
		return info

	def serialize(self):
		info = vars(self)
		info["tag"] = "W"
		return vars(self)

	@staticmethod
	def deserialize(info):
		result = WildcardField()
		for key in info:
			if key != "tag":
				setattr(result, key, info[key])
		return result

class StartField:
	def get_type(self):
		return "corner"

	def get_field(self):
		info = {}
		info["image"] = Assets.CORNER_START
		info["color"] = (255, 255, 255) # White
		info["jail"] = False
		return info

	def get_tooltip(self):
		info = {}
		info["type"] = "single_label"
		info["name"] = "Start"
		info["color"] = (255, 255, 255) # White
		info["label"] = "You get 200€ whenever you pass here!"
		return info

	def serialize(self):
		return {"tag": "C0"}

class JailField:
	def get_type(self):
		return "corner"

	def get_field(self):
		info = {}
		info["image"] = Assets.CORNER_JAIL
		info["color"] = (255, 255, 255) # White
		info["jail"] = True
		return info

	def get_tooltip(self):
		info = {}
		info["type"] = "single_label"
		info["name"] = "Jail"
		info["color"] = (255, 255, 255) # White
		info["label"] = "The jailed and the ones just visiting!"
		return info

	def serialize(self):
		return {"tag": "C1"}

class FreeParkingField:
	def get_type(self):
		return "corner"

	def get_field(self):
		info = {}
		info["image"] = Assets.CORNER_FREEPARKING
		info["color"] = (255, 255, 255) # White
		info["jail"] = False
		return info

	def get_tooltip(self):
		info = {}
		info["type"] = "single_label"
		info["name"] = "Free Parking"
		info["color"] = (255, 255, 255) # White
		info["label"] = "Free money!"
		return info
	
	def serialize(self):
		return {"tag": "C2"}

class GoToJailField:
	def get_type(self):
		return "corner"

	def get_field(self):
		info = {}
		info["image"] = Assets.CORNER_GOTOJAIL
		info["color"] = (255, 255, 255) # White
		info["jail"] = False
		return info

	def get_tooltip(self):
		info = {}
		info["type"] = "single_label"
		info["name"] = "Go to Jail!"
		info["color"] = (255, 255, 255) # White
		info["label"] = "Stop right there criminal scum!"
		return info

	def serialize(self):
		return {"tag": "C3"}