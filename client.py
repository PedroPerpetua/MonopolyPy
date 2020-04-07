import socket, select
import threading
from libs import colors as cs
import json

SERVER = None

class Network:
	def __init__(self, server, port):
		self.client = None
		self.addr = (server, port)
		self.active = False


	def start(self):
		if not self.active:
			self.active = True
			thread = threading.Thread(target=self.processing_thread)
			thread.start()

	def connect(self):
		global SERVER
		if SERVER == None:
			try:
				self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.client.connect(self.addr)
				print(cs.red("[CONNECT]") + f" Connected to {self.addr}.")
				SERVER = self.addr
				self.start()
			except OSError as ose:
				print(cs.red("[ERROR]") + " Server is closed! " + str(ose))
		else:
			print(cs.red("[ERROR]") + " connect -> Already connected!")

	def disconnect(self, message):
		global SERVER
		if SERVER != None:
			SERVER = None
			print(cs.red("[DISCONNECT]") + f" Disconnected: {message}.")
			self.active = False
			self.client.close()
		else:
			print(cs.red("[ERROR]") + " disconnect -> Not connected!")

	def send_data(self, data):
		global SERVER
		if SERVER != None:
			try:
				data = json.dumps(data)
				self.client.sendall(data.encode())
				print(cs.red("[DATA]") + f" Sent <{data}>.")
			except socket.error as e:
				self.disconnect("send_data -> " + str(e))
		else:
			print(cs.red("[ERROR]") + " send_data -> Not connected!")

	def receive_data(self):
		global SERVER
		if SERVER != None:
			try:
				data = self.client.recv(1024).decode()
				if data != "":
					data = json.loads(data)
					print(cs.red("[DATA]") + f" Received <{data}>.")
					return data
				else:
					return -1
			except socket.error as e:
				self.disconnect("receive_data -> " + str(e))
		else:
			print(cs.red("[ERROR]") + " receive_data -> Not connected!")

	def processing_thread(self):
		global SERVER
		while self.active:
			status = select.select([self.client], [], [], 1)
			if self.client in status[0]:
				try:
					if SERVER != None:
						received = self.receive_data()
						if received == -1:
							self.disconnect("Server closed")
				except socket.error as se:
					self.disconnect("processing_thread -> " + str(se))

def main():
	global SERVER
	server = input("Please input the server -> ")
	port = int(input("Please input the port -> "))
	network = Network(server, port)

	print("Please input a command:")
	while True:
		command = input()
		if command[0] == 'c':
			network.connect()
		elif command[0] == 'a':
			network.send_data("pedro:monopoly")
		elif command[0] == 's':
			network.send_data(command[2:])
		elif command[0] == 'd':
			network.disconnect("main -> Requested disconnect")
		elif command[0] == 'x':
			if SERVER != None:
				network.disconnect("main -> Closing")
			break
		else:
			print("COMMANDS:")
			print("c      - connect to the server with a name.")
			print("a      - send the authentication key.")
			print("s DATA - send said data to the connected server, if any.")
			print("d      - disconnect from the connected server, if any.")
			print("x      - close the client.")

if __name__ == "__main__":
	main()