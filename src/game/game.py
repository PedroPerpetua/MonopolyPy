from src.game.player import Player
from src.game.field import Field, BuyableField, PropertyField, RailroadField, UtilityField, import_fields

FIELDS_FILE = "src/fields.txt"

class Game:
	def __init__(self, id_list=[]):
		self.fields = import_fields(FIELDS_FILE)
		self.players = []
		for pair in id_list:
			self.players.append(Player(pair[0], pair[1]))
		self.current_player = 0

	# Functions for board drawing
	def get_fieldInfo(self, field_pos):
		field = self.fields[field_pos]
		info = field.get_fieldInfo()
		info["players"] = []
		info["jailed"] = []
		for player in self.players:
			if player.is_jailed():
				info["jailed"].append(player.icon)
			elif player.position == field_pos:
				info["players"].append(player.icon)
		return info
	def get_tooltipInfo(self, field_pos):
		field = self.fields[field_pos]
		info = field.get_tooltipInfo()
		if isinstance(field, BuyableField):
			if field.owner_id is None:
				info["owner"] = "Unowned"
				info["value"] = "Price: " + str(field.price)
			else:
				info["owner"] = self.players[field.owner_id].name
				if isinstance(field, PropertyField):
					info["value"] = "Tax: " + str(field.house_taxes[field.houses]) + "€"
					info["houses"] = "Houses: " + str(field.houses)
					info["house_price"] = "House price:" + str(field.house_price) + "€"
				elif isinstance(field, RailroadField):
					info["value"] = "Tax: " + str(self.players[field.owner_id].get_rail()) + "€"
				elif isinstance(field, UtilityField):
					info["value"] = "Tax: " + str(self.players[field.owner_id].get_util()) + " times the dice roll."
		return info

	# Serialization
	def serialize(self):
		info = {}
		info["current_player"] = self.current_player
		info["players"] = []
		for player in self.players:
			info["players"].append(player.serialize())
		info["fields"] = []
		for field in self.fields:
			info["fields"].append(field.serialize())
		return info
	@staticmethod
	def deserialize(info):
		game = Game()
		for player_info in info["players"]:
			game.players.append(Player.deserialize(player_info))
		game.fields.clear()
		for field_info in info["fields"]:
			game.fields.append(Field.deserializeField(field_info))
		return game

	def __str__(self):
		text = "Monopoly Game!\n"
		text += f"Num of fields: {str(len(self.fields))}\n"
		text += "Players:\n"
		for player in self.players:
			text += f"\t{player.name} @ postition {str(player.position)}\n"
		text += f"Current player: {str(self.players[self.current_player].name)}"
		return text
