import socket, select
import threading, os
from datetime import datetime
import time
from game.game import Game
from libs import colors as cs
import json


path = os.getcwd()
HOST = "localhost"
PORT = 5555
PASSWORD = "1234"
MAX_PLAYERS = 2

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
		self.players_ready = 0

		self.game = None
		self.ingame = False
		self.requests = []


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
				client.conn.sendall(game_data.encode())
			except socket.error as e:
				self.disconnect(client, e)
		print(cs.green(self.game))


	def authenticate(self, client):
		pass_code = client.conn.recv(1024).decode()
		pass_code = json.loads(pass_code)
		return pass_code == self.password


	def disconnect(self, client, message):
		print(client.log() + f" DISCONNECTED: {message}.")
		if client.active:
			self.players_ready += -1
		if client in self.clients:
			self.clients.remove(client)
		client.shutdown()


	def look_for_players(self):
		self.active = True
		def count_ready():
			ready = -1
			while self.players_ready != self.MAX_PLAYERS and self.active:
				if ready != self.players_ready:
					ready = self.players_ready
					print(cs.red("[SERVER]") + f" {ready}/{self.MAX_PLAYERS} ready...")
		print_counter = threading.Thread(target=count_ready)
		print_counter.start()

		try:
			self.socket.bind(self.addr)
		except socket.error as se:
			print(cs.red("[SERVER]") + f" Socket error: {str(se)}")
		self.socket.settimeout(1)	
		self.socket.listen(0)
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
					self.clients.append(new_client)
					new_client.start()
				else:
					self.disconnect(new_client, "FAILED AUTHENTICATION")
			except socket.timeout:
				continue
			except socket.error as se:
				print(cs.red("[SERVER]") + f" Socket error: {str(se)}")
		if self.active:
			print(cs.red("[SERVER]") + " I HAVE 4 PLAYERS CONNECTED AND READY!")
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

	def start_game(self):
		print(cs.red("[GAME]") + " Game starting!")
		clients_ids = []
		counter = 0
		for client in self.clients:
			client.id[0] = counter
			counter += 1
			clients_ids.append(client.id[1:])

		self.game = Game(clients_ids, self.MAX_PLAYERS)
		for client in self.clients:
			self.send_data(client, "GAME_START")
		self.send_game_state()
		if self.active:
			self.ingame = True
			thread = threading.Thread(target=self.processing_thread)
			thread.start()
		while self.active:
			continue

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
			data = self.conn.recv(1024).decode()
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

		print(self.log() + " Awaiting name and icon...")
		name = self.receive_data()
		icon = self.receive_data()
		if name == -1 or icon == -1:
			self.server.disconnect(self, "Invalid name or icon - DISCONNECTED")
		self.id = [None, name, icon]
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


def main():
	server = Server(HOST, PORT, PASSWORD, MAX_PLAYERS)
	try:
		server.look_for_players()
		server.start_game()
	except KeyboardInterrupt:
		server.close_server()

if __name__ == "__main__":
	main()