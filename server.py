import pygame
from threading import Thread
from libs.server import Server
from libs.UI.server_start_screen import Server_StartScreen
from libs.UI.server_waiting_players_screen import Server_WaitingPlayersScreen

WIN_W = 300
WIN_H = 294

def setup_window():
	win = pygame.display.set_mode((WIN_W, WIN_H))
	pygame.display.set_caption("Monopoly server")
	icon = pygame.image.load("libs/assets/server_app_icon.png")
	icon.set_colorkey((255,0,255))
	pygame.display.set_icon(icon)
	return win

def start_server(server):
	server.look_for_players()

# MAIN APPLICATION LOOP
def main():
	pygame.init()
	win = setup_window()

	# START SCREEN
	screen = Server_StartScreen(win)
	start_screen = True
	while start_screen:
		pygame.time.delay(100)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
		screen.update(events)

		# EVENTS INSIDE THIS SCREEN
		if screen.check_end():
			start_screen = False

		screen.draw()
		pygame.display.update()

	# PROCESSES DATA AND CREATES THE SERVER
	values = screen.get_values()
	server = Server(values[0], values[1], values[2], values[3])
	server_thread = Thread(target=start_server, args=[server])
	server_thread.start()

	# WAITING FOR PLAYERS SCREEN
	screen = Server_WaitingPlayersScreen(win, values[3])
	waiting_players_screen = True
	
	while waiting_players_screen:
		pygame.time.delay(100)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				server.close_server()
				exit(0)
		screen.update(events)
		
		# EVENTS INSIDE THIS SCREEN
		screen.update_players(server.get_players())

		screen.draw()
		pygame.display.update()

	# END
	pygame.quit()

if __name__ == "__main__":
	main()