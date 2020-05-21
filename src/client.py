import socket
import select
import threading
import json
from src.game.game import Game

MESSAGE_SIZE = 8192

class Client:
	def __init__(self, server, port, password):
		self.client = None
		self.addr = (server, port)
		self.password = password
		self.active = False
		self.game = None
		self.available_icons = {"available_icons": ["Dummy"] + [False for i in range(8)]}

	def start(self):
		self.active = True
		client_thread = threading.Thread(target=self.processing_thread)
		client_thread.start()
	
	def connect(self):
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client.connect(self.addr)
			self.send_data(self.password)
			response = self.receive_data()
			if response == -1:
				raise ConnectionAbortedError
		except socket.gaierror:
			raise ConnectionRefusedError

	def disconnect(self):
		self.active = False
		self.client.close()

	def send_data(self, data):
		try:
			data = json.dumps(data).encode()
			self.client.sendall(data)
		except socket.error:
			self.disconnect()
	
	def send_profile(self, name, icon):
		self.send_data(name)
		self.send_data(icon)

	def receive_data(self):
		try:
			data = self.client.recv(MESSAGE_SIZE).decode()
			if data != "":
				data = json.loads(data)
				return data
			else:
				return -1
		except socket.error:
			self.disconnect()
	
	def receive_icons(self):
		data = self.receive_data()
		if data != -1:
			self.available_icons = data

	def receive_game(self):
		data = self.receive_data()
		if data != -1:
			self.game = Game.deserialize(data)
		
	def processing_thread(self):
		while self.active:
			status = select.select([self.client], [], [], 1)
			if self.client in status[0]:
				try:
					received = self.receive_data()
					if received == -1:
						self.disconnect()
					if received == "icon_update":
						self.receive_icons()
					if received == "game_update":
						self.receive_game()
				except socket.error:
					self.disconnect()