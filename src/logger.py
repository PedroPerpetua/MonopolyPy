from datetime import datetime
from os import getcwd


def write_log(requests):
	filename = "GameLog_" + datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".txt"
	log_file = open(getcwd() + "/logs/" + filename, "w+")
	if len(requests) == 0:
		log_file.write("Nothing happened!")
	else:
		for request in self.reuqests:
			log_file.write(str(request) + "\n")