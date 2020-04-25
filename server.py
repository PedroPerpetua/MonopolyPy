import pygame
pygame.init()
win = pygame.display.set_mode((300, 294))

from threading import Thread
from lib.assets import Assets, import_assets
from src.server_screens import StartScreen, QueueScreen, InGameScreen
from src.server import Server

WIN_W = 300
WIN_H = 300

def server_thread(server):
	server.run()

def setup_window():
	win = pygame.display.set_mode((WIN_W, WIN_H))
	import_assets("Server")
	pygame.display.set_caption("MonopolyPy server")
	icon = Assets.APP_ICON
	pygame.display.set_icon(icon)
	return win

# MAIN APPLICATION LOOP
def main():
	pygame.init()
	win = setup_window()
	
	# START SCREEN
	screen = StartScreen()
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
		screen.draw(win)
		pygame.display.update()

	# PROCESSES DATA AND CREATES THE SERVER
	values = screen.get_values()
	server = Server(values[0], values[1], values[2], values[3])
	thread = Thread(target=server_thread, args=[server])
	thread.start()

	# WAITING FOR PLAYERS SCREEN
	screen = QueueScreen(values[3])
	waiting_players_screen = True
	while waiting_players_screen:
		pygame.time.delay(100)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				server.close_server("PG QUIT")
				exit(0)
		screen.update(events)
		
		# EVENTS INSIDE THIS SCREEN
		screen.update_players(server.get_tags())
		if server.game:
			waiting_players_screen = False

		screen.draw(win)
		pygame.display.update()

	# IN GAME SCREEN
	screen = InGameScreen()
	ingame_screen = True
	while ingame_screen:
		pygame.time.delay(100)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				server.close_server("PG QUIT")
				exit(0)
		screen.update(events)

		# EVENTS INSIDE THIS SCREEN
		if screen.check_end():
			pygame.quit()
			server.close_server("PG QUIT")
			exit(0)

		screen.draw(win)
		pygame.display.update()

	# END
	pygame.quit()
	server.close_server("END OF PROGRAM")

if __name__ == "__main__":
	main()