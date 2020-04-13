import socket, select
import threading, os
from datetime import datetime
import time
from game.game import Game
from libs import colors as cs
import json
import pygame


path = os.getcwd()
MESSAGE_SIZE = 8192

class Server:
	def __init__(self, host, port, password, max_players):
		self.active = False
		self.host = host
		self.port = port
		self.password = password
		self.MAX_PLAYERS = max_players
		self.addr = (host, port)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clients = []

		self.ids = [None for _ in range(max_players)]
		self.players_ready = 0

		self.game = None
		self.ingame = False
		self.requests = []

	def get_empty_slot(self):
		for i in range(self.MAX_PLAYERS):
			if self.ids[i] == None:
				return i
		return -1

	def get_client_slot(self, client):
		for i in range(self.MAX_PLAYERS):
			if self.ids[i]:
				if self.ids[i][0] == client:
					return i
		return -1

	def send_data(self, client, data):
		try:
			message = json.dumps(data)
			client.conn.sendall(message.encode())
			print(cs.red("[SERVER]") + f" sent <{data}> to {client}.")
		except socket.error as e:
			self.disconnect(client, e)

	def send_game_state(self):
		print(cs.red("[SERVER]") + " Sending game state.")
		for client in self.clients:
			self.send_data(client, "game_update")
			time.sleep(0.2)
			try:
				game_data = json.dumps(self.game.serialize())
				print(cs.red("SIZE:") + str(len(game_data)))
				client.conn.sendall(game_data.encode())
			except socket.error as e:
				self.disconnect(client, e)
		print(cs.green(self.game))


	def authenticate(self, client):
		pass_code = client.conn.recv(MESSAGE_SIZE).decode()
		pass_code = json.loads(pass_code)
		return pass_code == self.password


	def disconnect(self, client, message):
		print(client.log() + f" DISCONNECTED: {message}.")
		if client.active:
			self.players_ready += -1
		if client in self.clients:
			self.clients.remove(client)
		slot = self.get_client_slot(client)
		if slot != -1:
			self.ids[slot] = None
		client.shutdown()


	def look_for_players(self):
		self.active = True

		# Prepares the socket
		try:
			self.socket.bind(self.addr)
		except socket.error as se:
			print(cs.red("[SERVER]") + f" Socket error: {str(se)}")
		self.socket.settimeout(1)
		self.socket.listen(0)

		# Main loop looking for connections
		print(cs.red("[SERVER]") + " Awaiting connections...")
		while self.active and self.players_ready != self.MAX_PLAYERS:
			try:
				conn, addr = self.socket.accept()
				new_client = Client(conn, addr, self)
				print(cs.red("[CONNECTION]") + f" New connection @ {new_client}.")
				if len(self.clients) == self.MAX_PLAYERS:
					self.disconnect(new_client, "SERVER FULL")
				elif self.authenticate(new_client):
					print(cs.red("[CONNECTION]") + f" It passed authentication! Welcome {new_client}.")
					slot = self.get_empty_slot()
					self.ids[slot] = [new_client, []]
					self.clients.append(new_client)
					new_client.start()
				else:
					self.disconnect(new_client, "FAILED AUTHENTICATION")
			except socket.timeout:
				continue
			except socket.error as se:
				print(cs.red("[SERVER]") + f" Socket error: {str(se)}")
		if self.active:
			print(cs.red("[SERVER]") + f" I HAVE {self.MAX_PLAYERS} PLAYERS CONNECTED AND READY!")
			self.socket.close()


	def processing_thread(self):
		print(cs.red("[SERVER]") + " Started processing thread.")
		current_request = 0
		while self.active and self.ingame:
			if current_request <= len(self.requests) -1:
				to_process = self.requests[current_request]
				result = self.game.receive_request(to_process[0][0],to_process[1])
				print(cs.green("[REQ]") + " " + str(result))
				current_request += 1
				self.send_game_state()
		print(cs.red("[SERVER]") + " Finished processing thread.")

	def receive_request(self, player_id, request):
		client = self.clients[player_id]
		self.send_data(client, request)
		response = client.receive_data()
		return response

	def get_players(self):
		players = []
		for i in range(self.MAX_PLAYERS):
			if self.ids[i] == None:
				players += [None]
			else:
				players += [self.ids[i][1]]
		return players

	def log_requests(self):
		print(cs.red("[SERVER]") + " Logging requests.")
		filename = "log_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".txt"
		log = open(path + "/logs/" + filename, "w+")
		if len(self.requests) == 0:
			log.write("Nothing happened!")
		else:
			for request in self.requests:
				if request[1] == -1:
					log.write(str(request[0][1]) + ": disconnected\n")
				else:
					log.write(str(request[0][1]) + ": " + request[1] + "\n")


	def close_server(self):
		print(cs.red("[SERVER]") + " Server closing.")
		self.active = False
		last_clients = self.clients.copy()
		for client in last_clients:
			self.disconnect(client, "SERVER CLOSED")
		self.log_requests()



class Client:
	def __init__(self, conn, addr, server):
		self.conn = conn
		self.addr = addr
		self.id = None # [ID, name, icon]
		self.server = server
		self.active = False


	def start(self):
		if not self.active:
			process = threading.Thread(target=self.processing_thread)
			process.start()


	def receive_data(self):
		try:
			data = self.conn.recv(MESSAGE_SIZE).decode()
			if data != "":
				data = json.loads(data)
				print(cs.red("[SERVER]") + f" received <{data}> from {self}.")
				return data
			return -1
		except socket.error as se:
			self.server.disconnect(self, se)


	def shutdown(self):
		self.active = False
		self.conn.close()


	def processing_thread(self):
		print(self.log() + " Started processing thread.")

		# Receive name and icon
		print(self.log() + " Awaiting name and icon...")
		name = self.receive_data()
		icon = self.receive_data()
		if name == -1 or icon == -1:
			self.server.disconnect(self, "Invalid name or icon - DISCONNECTED")
		self.id = [None, name, icon]
		slot = self.server.get_client_slot(self)
		self.server.ids[slot] = [self, [icon, name]]
		self.server.players_ready += 1

		self.active = True
		print(self.log() + f" Received name and icon! {self.log()} is ready.")
		while self.active:
			status = select.select([self.conn], [], [], 1)
			if self.conn in status[0]:
				try:
					received = self.receive_data()
					if received == -1:
						self.server.disconnect(self, "DISCONNECTED")
					if self.server.ingame and received != None:
						self.server.requests.append([self.id, received])
				except socket.error as se:
					self.server.disconnect(self, se)
		print(self.log() + " Finished processing thread.")


	def log(self):
		return cs.red("[CLIENT ") + str(self) + cs.red("]")


	def __str__(self):
		if self.id:
			return cs.yellow(self.id[1])
		else:
			return cs.yellow(self.addr) 