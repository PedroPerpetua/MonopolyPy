from datetime import datetime
from os import getcwd

SEPARATOR = "##################################################\n"
class Logger:
	def __init__(self):
		self.time = datetime.now().strftime("%d-%m-%Y %Hh%Mm%Ss")
		self.filename = "ServerLog " + self.time + ".txt"
		self.lines = []

	def log(self, entity, message):
		self.lines.append([entity, message])

	def write(self):
		log_file = open(getcwd() + "\\logs\\" + self.filename, "w+")
		log_file.write(SEPARATOR)
		log_file.write("MonopolyPy server log at " + self.time + "\n")
		log_file.write(SEPARATOR)
		log_file.write("SERVER MESSAGES:\n")
		for entry in self.lines:
			if entry[0] != "Game":
				segment1 = "[" + entry[0] + "]"
				while len(segment1) != 15:
					segment1 += " "
				log_file.write(f"{segment1} {entry[1]}\n")
		log_file.write(SEPARATOR)
		log_file.write("GAME HISTORY:\n")
		for entry in self.lines:
			if entry[0] == "Game":
				segment1 = "[" + entry[1][0] + "]"
				while len(segment1) != 15:
					segment1 += " "
				log_file.write(f"{segment1} {entry[1][1]}\n")
		log_file.write(SEPARATOR[:-1])