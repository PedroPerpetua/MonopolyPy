import json
from src.game.player import Player
from src.game.fields import *

FIELDS_FILE = "src/fields.txt"

class Game:
	def __init__(self, id_list=[], server=None):
		self.players = self.create_players(id_list)
		self.fields = self.import_fields(FIELDS_FILE)
		self.MAX_PLAYERS = len(id_list)
		self.server = server
		self.current_player = 0

	def create_players(self, id_list):
		player_list = []
		for pair in id_list:
			player_list.append(Player(pair[0], pair[1]))
		return player_list

	def import_fields(self, file):
		field_list = []
		with open(file, "r") as in_file:
			for line in in_file:
				if line[0] == "#":
					pass
				else:
					args = line[:-1].split("|")
					if args[0] == "P":
						taxes = []
						for number in args[5].split(","):
							taxes.append(int(number))
						field_list.append(Property(args[1],int(args[2]),args[3],int(args[4]),taxes))
					elif args[0] == "R":
						field_list.append(Railroad(args[1]))
					elif args[0] == "U":
						field_list.append(Utility(args[1]))
					elif args[0] == "T":
						field_list.append(Tax(args[1], int(args[2])))
					elif args[0] == "W":
						field_list.append(WildcardField(args[1]))
					elif args[0] == "S":
						field_list.append(SpecialField(args[1]))
		return field_list

	# Functions for board drawing
	def get_type(self, filed_pos):
		return self.fields[filed_pos].get_type()
	def get_color(self, field_pos):
		return self.fields[field_pos].color
	def get_info(self, field_pos):
		field = self.fields[field_pos]
		info = field.get_info()
		info["icons"] = []
		info["jailed"] = []
		for player in self.players:
			if player.is_jailed():
				info["jailed"].append(player.get_icon())
			elif player.pos == field_pos:
				info["icons"].append(player.get_icon())
		return info
	def get_tooltip(self, field_pos):
		info = self.fields[field_pos].get_tooltip()
		if "owner_id" in info and info["owner_id"] != None:
			info["owner"] = self.players[info["owner_id"]].get_name()
			info["util"] = self.players[info["owner_id"]].get_util()
			info["rail"] = self.players[info["owner_id"]].get_rail()
		else:
			info["owner"] = "Unowned"
		return info


	def serialize(self):
		info = {}
		info["MAX_PLAYERS"] = self.MAX_PLAYERS
		info["current_player"] = self.current_player
		info["players"] = {}
		for i in range(self.MAX_PLAYERS):
			info["players"][i] = self.players[i].serialize()
		info["fields"] = {}
		for i in range(len(self.fields)):
			info["fields"][i] = self.fields[i].serialize()
		return info

	def deserialize(info):
		result = Game()
		for key in info:
			setattr(result, key, info[key])
		result.players = []
		for player in info["players"]:
			result.players.append(Player.deserialize(info["players"][player]))
		result.fields = []
		for field in info["fields"]:
			result.fields.append(Field.field_deserialize(info["fields"][field]))
		return result


	def receive_request(self, player_id, request):
		player = self.players[player_id]
		return f"player {player}: {request}"

	def send_request(self, player_id, request):
		response = self.server.receive_request(player_id, request)
		return response





	def pass_turn(self):
		self.current_player = (self.current_player + 1) % self.MAX_PLAYERS


	def __str__(self):
		text = "Monopoly Game!\n"
		text += f"Num of fields: {str(len(self.fields))}\n"
		text += "Players:\n"
		for player in self.players:
			text += f"\t{player.name} @ postition {str(player.pos)}\n"
		text += f"Current player: {str(self.players[self.current_player].name)}"
		return text
