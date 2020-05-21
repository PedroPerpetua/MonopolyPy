from src.game.player import Player
from src.game.fields import field_deserialize, Property, Railroad, Utility, Tax, WildcardField, StartField, JailField, FreeParkingField, GoToJailField

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
						field_list.append(Property(args[1], int(args[2]), args[3], int(args[4]), taxes))
					elif args[0] == "R":
						field_list.append(Railroad(args[1]))
					elif args[0] == "U":
						field_list.append(Utility(args[1]))
					elif args[0] == "T":
						field_list.append(Tax(args[1], int(args[2])))
					elif args[0] == "W":
						field_list.append(WildcardField(args[1]))
					elif args[0] == "C0":
						field_list.append(StartField())
					elif args[0] == "C1":
						field_list.append(JailField())
					elif args[0] == "C2":
						field_list.append(FreeParkingField())
					elif args[0] == "C3":
						field_list.append(GoToJailField())
					else:
						raise ValueError
		return field_list

	# Functions for board drawing
	def get_type(self, filed_pos):
		return self.fields[filed_pos].get_type()
	def get_field(self, field_pos):
		field = self.fields[field_pos]
		info = field.get_field()
		info["players"] = []
		info["jailed"] = []
		for player in self.players:
			if player.is_jailed():
				info["jailed"].append(player.get_icon())
			elif player.pos == field_pos:
				info["players"].append(player.get_icon())
		return info
	def get_tooltip(self, field_pos):
		return self.fields[field_pos].get_tooltip()


	def serialize(self):
		info = {}
		info["MAX_PLAYERS"] = self.MAX_PLAYERS
		info["current_player"] = self.current_player
		info["players"] = []
		for i in range(self.MAX_PLAYERS):
			info["players"].append(self.players[i].serialize())
		info["fields"] = {}
		for i in range(len(self.fields)):
			info["fields"][i] = self.fields[i].serialize()
		return info

	@staticmethod
	def deserialize(info):
		result = Game()
		for key in info:
			setattr(result, key, info[key])
		result.players = []
		for player_info in info["players"]:
			player = Player.deserialize(player_info)
			player.game = result
			result.players.append(player)
		result.fields = []
		for field in info["fields"]:
			result.fields.append(field_deserialize(info["fields"][field]))
		return result


	def receive_request(self, player_id, request):
		player = self.players[player_id]
		return f"player {player}: {request}"

	def send_request(self, player_id, request):
		response = self.server.receive_request(player_id, request)
		return response


	def __str__(self):
		text = "Monopoly Game!\n"
		text += f"Num of fields: {str(len(self.fields))}\n"
		text += "Players:\n"
		for player in self.players:
			text += f"\t{player.name} @ postition {str(player.pos)}\n"
		text += f"Current player: {str(self.players[self.current_player].name)}"
		return text
