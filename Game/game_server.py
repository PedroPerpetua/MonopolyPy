"""
Represents a game server. Used to start it.
"""

import socket, select
import signal, os, threading
from game_board import Game_Board
import time
from colorama import Fore
from colorama import Style

class Server(object):

	def __init__(self, server, port):
		"""
		Initializes a server object
		
		Args:
			server (address): Address where the server will be open.
			port (int): Port where the server will be open.
		"""
		self.server = server
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.settimeout(1)
		self.connections = []

		self.requests = [] #Every request received is stored here.
		self.request_counter = 0

		self.conn_thread = threading.Thread(target=self.connection_thread)
		self.process_thread = threading.Thread(target=self.processing_thread)
		self.active = True
		signal.signal(signal.SIGINT, self.close_server)

	def start(self):
		"""
		Starts the server threads.
		"""
		self.conn_thread.start()
		self.process_thread.start()

	def connection_thread(self):
		"""
		Handles all incoming connections, authenticating them and creating Client objects for each.
		"""
		print(f"{Fore.RED}[SERVER]{Style.RESET_ALL} Started connection thread.")
		try:
			self.socket.bind((self.server,self.port))
		except socket.error as e:
			print(f"{Fore.RED}[SERVER]{Style.RESET_ALL} Socket error: ", str(e))
		self.socket.listen(1)
		print(f"{Fore.RED}[SERVER]{Style.RESET_ALL} Awaiting connections.")
		while len(self.connections) < 4 and self.active:
			try:
				conn, addr = self.socket.accept()
				connection = Client(conn, addr, self)
				print(f"{Fore.RED}[CONNECTION]{Style.RESET_ALL} New connection: {Fore.YELLOW}{connection}{Style.RESET_ALL}.")
				if self.authenticate(connection):
					print(f"{Fore.RED}[CLIENT{Style.RESET_ALL} {Fore.YELLOW}{connection}{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL} Passed authentication.")
					self.connections.append(connection)
					connection.start()
				else:
					self.disconnect(connection, "FAILED AUTHENTICATION")
			except socket.timeout:
				continue

		print(f"{Fore.RED}[SERVER]{Style.RESET_ALL} Finished connection thread.")

	def processing_thread(self):
		"""
		Handles all the requests received from the clients, in order of first in first handled.
		"""
		print(f"{Fore.RED}[SERVER]{Style.RESET_ALL} Started processing thread.")
		while self.active:
			if self.request_counter < len(self.requests):
				request = self.requests[self.request_counter]
				print(f"{Fore.GREEN}[REQUEST]{Style.RESET_ALL} <{request[1]}> by {request[0]}.")
				self.request_counter +=1
		print(f"{Fore.RED}[SERVER]{Style.RESET_ALL} Finished processing thread.")


	def authenticate(self, connection):
		"""
		Function used to authenticate a connection. A connection is authenticated if the first
		message they send is the key "pedro:monopoly".
		
		Args:
			connection (Client): Client to be authenticated.
		
		Returns:
			Bool: True if it passes authentication
		"""
		pass_code = connection.receive_data()
		keys = pass_code.split(' ')
		if keys[0] == "pedro:monopoly":
			try:
				connection.name = keys[1]
			except IndexError as e:
				return False
			return True
		else:
			return False

	def add_request(self, request):
		"""
		Adds a request to the request queue.
		
		Args:
			request (List): A request is a list composed of a Client object that made
			the request, and an int representing the request code.
		"""
		self.requests.append(request)

	def send_data(self, connection, data):
		"""
		Sends that to the specified client.
		
		Args:
			connection (Client): Client to be sent data.
			data (Object): Data to be sent to said client.
		"""
		try:
			connection[0].sendall(data.encode())
			print(f"{Fore.RED}[SERVER]{Style.RESET_ALL} SENT: <{data}> to {Fore.YELLOW}{connection}{Style.RESET_ALL}.")
		except socket.error as e:
			self.disconnect(connection, e)

	def disconnect(self, connection, message):
		"""
		Disconnects a client and handles its leftover, deleting all its pending requests.
		
		Args:
			connection (Client): Client to be disconnected.
			message (String): String to be logged regarding why the client was disconnected.
		"""
		for request in list(self.requests):
			if request[0] == connection:
				self.requests.remove(request)
				self.request_counter += -1
		if connection in self.connections:
			self.connections.remove(connection)
		connection.shutdown()
		print(f"{Fore.RED}[CLIENT{Style.RESET_ALL} {Fore.YELLOW}{connection}{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL} DISCONNECTED: {message}.")

	def close_server(self, signum, frame):
		"""
		Closes the server, finishing all threads and disconnecting all clients. This is
		called by the signal SIGINT.
		
		Args:
			signum (Signal): SIGINT.
			frame (Frame): Used by signal handling.
		"""
		self.active = False
		print(f"{Fore.RED}[SERVER]{Style.RESET_ALL} Server closing.")
		for client in self.connections:
			self.disconnect(client, "SERVER CLOSING")
			if client.process_thread != None:
				client.process_thread.join()
		self.process_thread.join()
		self.conn_thread.join()


class Client(object):
	def __init__(self, conn, addr, server):
		self.conn = conn
		self.addr = addr
		self.name = None
		self.server = server
		self.active = True
		self.process_thread = None

	def start(self):
		self.process_thread = threading.Thread(target=self.processing_thread)
		self.process_thread.start()

	def shutdown(self):
		self.active = False
		self.conn.close()

	def receive_data(self):
		"""Receives data from this client.
		
		Returns:
			Data: the data retrieved; -1 in case of error.
		"""
		try: 
			data = self.conn.recv(1024).decode()
			if data == "":
				self.server.disconnect(self, "client disconnected")
				return -1
			print(f"{Fore.RED}[CLIENT {Fore.YELLOW}{self}{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL} RECEIVED: <{data}>")
		except socket.error as e:
			self.server.disconnect(self, e)
			return -1
		return data

	def processing_thread(self):
		print(f"{Fore.RED}[CLIENT{Style.RESET_ALL} {Fore.YELLOW}{self}{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL} Started processing thread.")
		while self.active:
			status = select.select([self.conn], [], [], 60)
			if self.conn in status[0]:
				try:
					received = self.receive_data()
					if received != -1:
						request = [self, received]
						self.server.add_request(request)
				except socket.error as e:
					self.server.disconnect(self, e)

					
		print(f"{Fore.RED}[CLIENT {Fore.YELLOW}{self}{Style.RESET_ALL}{Fore.RED}]{Style.RESET_ALL} Finished processing thread.")

	def __str__(self):
		if (self.name):
			return self.name
		else:
			return str(self.addr)

	def __repr__(self):
		return str(self)

if __name__ == "__main__":
	game_server = Server("localhost", 5555)
	game_server.start()