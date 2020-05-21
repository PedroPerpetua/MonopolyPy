import socket
import select
from threading import Thread
import json
import time

from lib import colors as cs
from src.logger import write_log
from src.game.game import Game

MESSAGE_SIZE = 8192

class Server:
	def __init__(self, host, port, password, max_players):
		self.active = False
		self.addr = (host, port)
		self.password = password
		self.max_players = max_players
		self.clients = [None for _ in range(max_players)]
		self.available_icons = ["Dummy", True, True, True, True, True, True, True, True]

		self.in_game = False
		self.game = None
		self.requests = []


	def add_client(self, client):
		for i in range(self.max_players):
			if self.clients[i] is None:
				self.clients[i] = client
				break

	def remove_client(self, client):
		for i in range(self.max_players):
			if self.clients[i] == client:
				if client.tag is not None:
					self.available_icons[client.tag[1]] = True
				self.clients[i] = None

	def check_full(self):
		for client in self.clients:
			if client is None:
				return False
		return True

	def check_ready(self):
		for client in self.clients:
			if client is None:
				return False
			if not client.ready:
				return False
		return True


	# Functions dealing with clients
	def authenticate(self, client):
		pass_code = client.receive_data()
		return pass_code == self.password

	def disconnect(self, client, message):
		if isinstance(client, Client):
			self.remove_client(client)
			client.shutdown()
			print(cs.green(f"[CLIENT {client}]") + f" DISCONNECTED: {message}")

	def send_data(self, client, data):
		try:
			message = json.dumps(data)
			client.conn.sendall(message.encode())
			print(cs.red("[SERVER]") + f" sent <{data}> to {client}.")
		except socket.error as se:
			self.disconnect(client, se)

	def send_all(self, message, data):
		for client in self.clients:
			if client is not None:
				self.send_data(client, message)
				time.sleep(0.2)
				self.send_data(client, data)
	
	def send_icons(self):
		self.send_all("icon_update", {"available_icons": self.available_icons})
	def send_game(self):
		self.send_all("game_update", self.game.serialize())

	# Server functions
	def search_players(self):
		# Prepares the socket
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			server_socket.bind(self.addr)
			server_socket.settimeout(1)
			server_socket.listen(0)
		except socket.error as se:
			self.close_server(se)
	
		# Main loop looking for connections
		print(cs.red("[SERVER]") + "Awaiting connections...")
		while self.active and not self.check_ready():
			try:
				conn, addr = server_socket.accept()
				client = Client(conn, addr, self)
				print(cs.yellow("[CONNECTION]") + f" New connection @ {client}.")
				if self.check_full():
					self.disconnect(client, "SERVER FULL")
				elif self.authenticate(client):
					print(cs.yellow("[CONNECTION]") + " Passed authentication!")
					self.add_client(client)
					self.send_data(client, 0)
					client.start()
				else:
					self.send_data(client, -1)
					self.disconnect(client, "FAIELD AUTHENTICATION")
			except socket.timeout:
				continue
			except socket.error as se:
				self.close_server(se)

		# If the loop finished because everyone is ready...
		if self.active:
			print(cs.red("[Server]") + " All players are ready!")
			server_socket.close()

	# Main thread handling communication and requests
	def processing_thread(self):
		pass

	def close_server(self, message):
		print(cs.red("[SERVER]") + " Server closing: " + str(message))
		self.active = False
		for client in self.clients:
			if client is not None:
				self.disconnect(client, str(message))
		write_log(self.requests)

	def start_game(self):
		self.in_game = True
		self.game = Game()
		player_tags = []
		for player in self.clients:
			player_tags += [player.tag]
		self.game.create_players(player_tags)
		self.send_game()


	def run(self):
		self.active = True
		if self.active:
			self.search_players()
		if self.active:
			self.start_game()

	def get_info(self):
		info = {}
		info["tags"] = ["Dummy"]
		for client in self.clients:
			if client is None:
				info["tags"] += [None]
			elif not client.ready:
				info["tags"] += [[]]
			else:
				info["tags"] += [client.tag]
		return info

class Client:
	def __init__(self, conn, addr, server):
		self.active = False
		self.conn = conn
		self.addr = addr
		self.server = server

		self.ready = False
		self.tag = None

	def start(self):
		self.active = True
		thread = Thread(target=self.processing_thread)
		thread.start()

	def receive_data(self):
		try:
			data = self.conn.recv(MESSAGE_SIZE).decode()
			if data != "":
				data = json.loads(data)
				print(cs.green(f"[CLIENT {self}]") + f" received <{data}>.")
				return data
			else:
				self.server.disconnect(self, "Empty string received.")
				return None
		except socket.error as se:
			self.server.disconnect(self.tag, se)

	def get_tag(self):
		self.server.send_icons()
		name = self.receive_data()
		icon = self.receive_data()
		if not name or not icon:
			self.server.disconnect(self, "Invalid name or icon - DISCONNECTED")
		else:
			self.tag = [name, icon]
			self.server.available_icons[icon] = False
			self.server.send_icons()
			self.ready = True

	def shutdown(self):
		self.active = False
		self.conn.close()


	# Main client thread
	def processing_thread(self):
		print(cs.green(f"[CLIENT {self}]") + " Started processing thread.")
		self.get_tag()
		while self.active:
			if self.conn:
				status = select.select([self.conn], [], [], 1)
				if self.conn in status[0]:
					received = self.receive_data()
					if received and self.server.game:
						self.server.requests.append([self.tag, received])
		print(cs.green(f"[CLIENT {self}]") + " Finished processing thread.")


	# Python functions
	def __str__(self):
		if self.tag:
			return self.tag[0]
		else:
			return str(self.addr)