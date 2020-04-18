"""
Game_Board class.
"""
from field import *

class Game_Board(object):
	def __init__(self, player_list):
		self.fields = []
		self.players = player_list
		self.current_player_id = 0
		self.luck = []
		self.community = []

	def add_player(self, player):
		if player not in self.players:
			self.players.append(player)

	def get_current_player(self):
		return self.players[self.current_player_id]

	def import_fields(self, file):
		with open(file, "r") as in_file:
			for line in in_file:
				if line[0] == "#":
					pass
				else:
					args = line.split("|")
					if args[0] == "P":
						taxes = []
						for number in args[5].split(","):
							taxes.append(int(number))
						self.fields.append(Property(args[1],args[2],args[3],args[4],taxes))
					elif args[0] == "R":
						self.fields.append(Railroad(args[1]))
					elif args[0] == "U":
						self.fields.append(Utility(args[1]))
					elif args[0] == "S":
						self.fields.append(Special_Field(args[1]))

	def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


	# TODO: Methods