import socket, select
import threading, os
from datetime import datetime
from libs import colors as cs
import json


path = os.getcwd()
HOST = "localhost"
PORT = 5555
MAX_PLAYERS = 4

class Server:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.addr = (host, port)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clients = []
		self.requests = []
		self.active = False

	def send_data(self, client, data):
		try:
			message = json.dumps(data)
			client.conn.sendall(message.encode())
			print(cs.red("[SERVER]") + f" sent <{data}> to {client}.")
		except socket.error as e:
			self.disconnect(client, e)

	def authenticate(self, client):
		pass_code = client.conn.recv(1024).decode()
		pass_code = json.loads(pass_code)
		return pass_code == "pedro:monopoly"

	def disconnect(self, client, message):
		print(client.log() + f" DISCONNECTED: {message}.")
		if client in self.clients:
			self.clients.remove(client)
		client.shutdown()

	def log_requests(self):
		print(cs.red("[SERVER]") + " Logging requests.")
		filename = "log_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".txt"
		log = open(path + "/logs/" + filename, "w+")
		if self.requests == []:
			log.write("Nothing happened!")
		else:
			for request in self.requests:
				log.write(str(request[0].addr) + ": " + request[1] + "\n")

	def start_server(self):
		self.active = True
		try:
			self.socket.bind(self.addr)
		except socket.error as se:
			print(cs.red("[SERVER]") + f" Socket error: {str(se)}")
		self.socket.settimeout(1)	
		self.socket.listen(1)
		print(cs.red("[SERVER]") + " Awaiting connections...")
		while self.active and len(self.clients) != MAX_PLAYERS:
			try:
				conn, addr = self.socket.accept()
				new_client = Client(conn, addr, self)
				print(red("[CONNECTION]") + f" New connection @ {new_client}.")
				if self.authenticate(new_client):
					print(red("[CONNECTION]") + f" It passed authentication! Welcome {new_client}.")
					self.clients.append(new_client)
					new_client.start()
				else:
					self.disconnect(new_client, "FAILED AUTHENTICATION")
			except socket.timeout:
				continue
			except socket.error as se:
				print(cs.red("[SERVER]") + f" Socket error: {str(se)}")

		if self.active:
			print(cs.red("[SERVER]") + " I HAVE 4 PLAYERS CONNECTED!")
			self.start_game()

	def start_game(self):
		print(cs.red("[GAME]") + " Game starting!")
		for client in self.clients:
			client.ingame = True
		while self.active:
			continue

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
		self.name = None
		self.server = server
		self.active = False
		self.ingame = False

	def start(self):
		if not self.active:
			self.active = True
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
		while self.active:
			status = select.select([self.conn], [], [], 1)
			if self.conn in status[0]:
				try:
					received = self.receive_data()
					if received == -1:
						self.server.disconnect(self, "DISCONNECTED")
					if self.ingame:
						self.server.requests.append([self, received])
				except socket.error as se:
					self.server.disconnect(self, se)
		print(self.log() + " Finished processing thread.")

	def log(self):
		return cs.red("[CLIENT ") + str(self) + cs.red("]")

	def __str__(self):
		if self.name:
			return cs.yellow(self.name)
		else:
			return cs.yellow(self.addr) 


def main():
	server = Server(HOST, PORT)
	try:
		server.start_server()
	except KeyboardInterrupt:
		server.close_server()

if __name__ == "__main__":
	main()