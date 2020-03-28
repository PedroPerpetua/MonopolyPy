import socket
import time

class Network:
	def __init__(self, name, server, port):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.addr = (server, port)
		self.name = name

	def connect(self):
		try:
			self.client.connect(self.addr)
			print(f"[CONNECT] Connected to {self.addr}.")
			self.send_data("pedro:monopoly" + " " + self.name)
		except Exception as e:
			self.disconnect(e)

	def disconnect(self, message):
		print(f"[DISCONNECT] Disconnected. Error:", message)
		self.client.shutdown(socket.SHUT_RDWR)
		self.client.close()

	def send_data(self, data):
		try:
			self.client.sendall(data.encode())
			time.sleep(0.1)
			print(f"[DATA] Sent <{data}>.")
		except socket.error as e:
			self.disconnect(e)

	def receive_data(self):
		try:
			data = self.client.recv(1024).decode()
			print(f"[DATA] Received <{data}>.")
		except socket.error as e:
			self.disconnect(e)
			return -1
		return data

if __name__ == "__main__":

	network = None
	while True:
		command = input("Insert a command:\n")
		if command[0] == 'c':
			name, server, port = command[2:].split(' ')
			network = Network(name, server, int(port))
			network.connect()
		elif command[0] == 's':
			if network == None:
				print("Not connected.")
			else:
				try:
					network.send_data(command[2:])
				except ValueError as e:
					print("Please try to send a number!")
		elif command[0] == "d":
			if network == None:
				print("Not connected.")
			else:
				network.disconnect("End")
				network = None
		elif command[0] == 'x':
			if network != None:
				network.disconnect("Closing.")
			break;
		else:
			print("COMMANDS:")
			print("c NAME SERVER PORT - connect to the server with a name.")
			print("s DATA             - send said data to the connected server, if any.")
			print("d                  - disconnect from the connected server, if any.")
			print("x                  - close the client.")