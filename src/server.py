import socket, select
import threading
import json
import time

from lib import colors as cs
from src.logger import write_log
from src.game.game import Game
from src.server_client import ServerClient

# Tag constants for readability:
CLIENT = 0
DATA = 1
ICON = 0
NAME = 1

class Server:
	def __init__(self, host, port, password, max_players):
		self.active = False
		self.addr = (host, port)
		self.password = password
		self.max_players = max_players
		# An id_tag is a list containing [client (object), [icon (int), name (string)]]
		self.id_tags = [[None, []] for _ in range(max_players)]

		self.game = None
		self.requests = []


	# Functions dealing with Tags
	def add_tag(self, client):
		tag = [client, []]
		for index in range(self.max_players):
			if self.id_tags[index][CLIENT] == None:
				self.id_tags[index] = tag
				break
		return tag

	def add_data(self, client, data_list):
		for index in range(self.max_players):
			if self.id_tags[index][CLIENT] == client:
				self.id_tags[index][DATA] = data_list
				return self.id_tags[index]

	def remove_tag(self, old_tag):
		for index in range(self.max_players):
			if self.id_tags[index] == old_tag:
				self.id_tags[index] = [None, []]

	def get_tags(self):
		tags = []
		for tag in self.id_tags:
			if tag[CLIENT] == None:
				tags.append(None)
			else:
				tags.append(tag[DATA])
		return tags

	def check_state(self, value, tag=None):
		''' value should be:
		CLIENT returns True if server is full (except tag)
		DATA return True if every player is ready
		'''
		if value == CLIENT:
			for tag in self.id_tags:
				if tag[CLIENT] == tag:
					return True
			return False
		else:
			for tag in self.id_tags:
				if tag[DATA] == []:
					return False
			return True


	# Functions dealing with clients
	def authenticate(self, tag):
		pass_code = tag[CLIENT].receive_data()
		return pass_code == self.password

	def disconnect(self, tag, message):
		self.remove_tag(tag)
		tag[CLIENT].shutdown()
		print(cs.green(f"[CLIENT {tag[CLIENT]}]") + f" DISCONNECTED: {message}")

	def send_data(self, tag, data):
		try:
			message = json.dumps(data)
			tag[CLIENT].conn.sendall(message.encode())
			print(cs.red("[SERVER]") + f" sent <{data}> to {tag[CLIENT]}.")
		except socket.error as se:
			self.disconnect(tag, se)

	def send_game(self):
		# Because this function is only used when the game is full, no check for None
		for tag in self.id_tags:
			self.send_data(tag[CLIENT], "game_update")
			# We sleep so the socket doesn't think it's the same message
			time.sleep(0.2)
			try:
				game_data = json.dumps(self.game.serialize())
				tag[CLIENT].conn.sendall(game_data.encode())
			except socket.error as se:
				self.disconnect(tag, se)

	
	# Server functions
	def search_players(self):
		self.active = True

		# Prepares the socket
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			server_socket.bind(self.addr)
		except socket.error as se:
			self.close_server(se)
		server_socket.settimeout(1)
		server_socket.listen(0)

		# Main loop looking for connections
		print(cs.red("[SERVER]") + "Awaiting connections...")
		while self.active and not self.check_state(DATA):
			try:
				conn, addr = server_socket.accept()
				new_tag = self.add_tag(ServerClient(conn,addr,self))
				print(cs.yellow("[CONNECTION]") + f" New connection @ {new_tag[CLIENT]}.")
				if self.check_state(CLIENT, new_tag):
					self.disconnect(new_tag, "SERVER FULL")
				elif self.authenticate(new_tag):
					print(cs.yellow("[CONNECTION]") + " Passed authentication!")
					new_tag[CLIENT].start()
				else:
					self.disconnect(new_tag, "FAIELD AUTHENTICATION")
			except socket.timeout:
				continue
			except socket.error as se:
				self.close_server(se)

		# If the loop finished because everyone is ready...
		if self.active:
			print(cs.red("[Server]") + " All players are ready!")
			server_socket.close()

	def start_game(self):
		self.game = Game()

	# Main thread handling communication and requests
	def processing_thread(self):
		pass

	def close_server(self, message):
		print(cs.red("[SERVER]") + " Server closing.")
		self.active = False
		for tag in self.id_tags:
			if tag[CLIENT]:
				self.disconnect(tag, message)
		write_log(self.requests)

	def run(self):
		self.search_players()
		self.start_game()