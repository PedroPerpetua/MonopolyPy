import pygame
from libs.server import Server
from libs.UI.image_asset import ImageAsset
from libs.UI.input_box import InputBox
from libs.UI.text_button import TextButton
from libs.UI.text_label import TextLabel
from libs.UI.number_picker import NumberPicker
from libs.UI.screen import Screen

BG_COLOR = (143, 188, 114)
RALEWAY = "libs/Raleway.ttf"
WIN_W = 300
WIN_H = 294



def init_screen_items(window):
	items = {}
	items["image_asset"] = {}
	items["image_asset"]["logo"] = ImageAsset(150, 50, "server_logo", "C")
	items["text_label"] = {}
	items["text_label"]["host_label"] = TextLabel(20, 105, "Host IP", 20, RALEWAY, "L")
	items["text_label"]["port_label"] = TextLabel(20, 151, "Port", 20, RALEWAY, "L")
	items["text_label"]["players_label"] = TextLabel(160, 151, "Players", 20, RALEWAY, "L")
	items["text_label"]["password_label"] = TextLabel(20, 197, "Password", 20, RALEWAY, "L")
	items["input_box"] = {}
	items["input_box"]["host"] = InputBox(150, 136, 260, 20, "arial", "C")
	items["input_box"]["port"] = InputBox(20, 172, 120, 20, "arial", "L")
	items["input_box"]["password"] = InputBox(150, 228, 260, 20, "arial", "C")
	items["text_button"] = {}
	items["text_button"]["start"] = TextButton(150, 266, 100, 36, RALEWAY, "START", False, "C")
	items["number_drop"] = {}
	items["number_drop"]["players"] = NumberPicker(160, 172, 120, 20, "arial", 4, 2, 8, "L")
	return items

def validate_params(parameters):
	if parameters[0] == "":
		return False
	try:
		int(parameters[1])
	except ValueError:
		return False
	if parameters[2] == "":
		return False
	return True

def main():
	pygame.init()
	win = pygame.display.set_mode((WIN_W, WIN_H))
	pygame.display.set_caption("Monopoly server")
	screen = Screen(win, BG_COLOR, init_screen_items(win))
	
	run = True
	while run:
		pygame.time.delay(100)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				exit(0)
		screen.update(events)
		if validate_params(screen.get_texts()):
			screen.items["text_button"]["start"].switch(True)
		else:
			screen.items["text_button"]["start"].switch(False)
		if screen.items["text_button"]["start"].get_clicked():
			run = False

		screen.draw()
		pygame.display.update()
	pygame.quit()
	
	host, port, password = screen.get_texts()
	port = int(port)
	num_players = screen.items["number_drop"]["players"].get_number()
	server = Server(host, port, password, num_players)

	try:
		server.look_for_players()
		server.start_game()
	except KeyboardInterrupt:
		server.close_server()
	pygame.quit()

if __name__ == "__main__":
	main()