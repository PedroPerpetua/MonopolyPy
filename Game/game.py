from game.player import Player
import json
#from game.field import *

FIELDS_FILE = "game/fields.txt"

class Game:
	def __init__(self, id_list=[], num_players=0):
		self.players = self.create_players(id_list)
		self.MAX_PLAYERS = num_players
		#self.fields = self.import_fields(FIELDS_FILE)
		self.current_player = 0

	def create_players(self, id_list):
		player_list = []
		for pair in id_list:
			player_list.append(Player(pair[0], pair[1]))
		return player_list

	# def import_fields(self, file):
	# 	field_list = []
	# 	with open(file, "r") as in_file:
	# 		for line in in_file:
	# 			if line[0] == "#":
	# 				pass
	# 			else:
	# 				args = line.split("|")
	# 				if args[0] == "P":
	# 					taxes = []
	# 					for number in args[5].split(","):
	# 						taxes.append(int(number))
	# 					field_list.append(Property(args[1],args[2],args[3],args[4],taxes))
	# 				elif args[0] == "R":
	# 					field_list.append(Railroad(args[1]))
	# 				elif args[0] == "U":
	# 					field_list.append(Utility(args[1]))
	# 				elif args[0] == "S":
	# 					field_list.append(Special_Field(args[1]))
	# 	return field_list


	def serialize(self):
		info = {}
		info["MAX_PLAYERS"] = self.MAX_PLAYERS
		info["current_player"] = self.current_player
		info["players"] = {}
		for i in range(self.MAX_PLAYERS):
			info["players"][i] = self.players[i].serialize()
		return info

	def deserialize(info):
		result = Game()
		for key in info:
			setattr(result, key, info[key])
		result.players = []
		for player in info["players"]:
			result.players.append(Player.deserialize(info["players"][player]))
		return result


	def receive_request(self, player_id, request):
		player = self.players[player_id]
		return f"player {player}: {request}"

	def pass_turn(self):
		self.current_player = (self.current_player + 1) % self.MAX_PLAYERS


	def __str__(self):
		text = "Monopoly Game!\n"
		text += "Players:\n"
		for player in self.players:
			text += f"\t{player.name} @ postition {str(player.pos)}\n"
		text += f"Current player: {str(self.players[self.current_player].name)}"
		return text
