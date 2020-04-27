import socket, select
import json
from threading import Thread
import lib.colors as cs

MESSAGE_SIZE = 1024

# Tag constants for readability:
CLIENT = 0
DATA = 1
ICON = 0
NAME = 1

class ServerClient:
	def __init__(self, conn, addr, server):
		self.active = False
		self.conn = conn
		self.addr = addr
		self.tag = None
		self.server = server


	# Client functions
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
				self.server.disconnect(self.tag, "Empty string received.")
				return None
		except socket.error as se:
			self.server.disconnect(self.tag, se)

	def get_tag(self):
		name = self.receive_data()
		icon = self.receive_data()
		if name == -1 or icon == -1:
			self.server.disconnect(self.tag, "Invalid name or icon - DISCONNECTED")
		else:
			self.tag = self.server.add_data(self, [icon, name])

	def shutdown(self):
		self.active = False
		self.conn.close()


	# Main client thread
	def processing_thread(self):
		print(cs.green(f"[CLIENT {self}]") + " Started processing thread.")

		self.get_tag()
		while self.active:
			status = select.select([self.conn], [], [], 1)
			if self.conn in status[0]:
				received = self.receive_data()
				if received and self.server.game:
					self.server.requests.append([self.tag, received])
		print(cs.green(f"[CLIENT {self}]") + " Finished processing thread.")


	# Python functions
	def __str__(self):
		if self.tag:
			return self.tag[DATA][NAME]
		else:
			return str(self.addr)