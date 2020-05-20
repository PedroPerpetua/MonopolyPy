import pygame as pg
from lib.assets import Assets, import_assets
from src.client_screens import StartScreen, ProfileScreen, GameScreen
from src.client import Client

WIN_W = 1280
WIN_H = 720

# MAIN APPLICATION LOOP
def main():
	# INITIALIZE PYGAME WINDOW
	pg.init()
	 # TODO: FULLSCREEN
	win = pg.display.set_mode((WIN_W, WIN_H))
	import_assets("Client")
	pg.display.set_caption("MonopolyPy")
	icon = Assets.APP_ICON
	pg.display.set_icon(icon)

    # START SCREEN
	screen = StartScreen()
	connected = False
	while not connected:
		pg.time.delay(100)
		events = pg.event.get()
		for event in events:
			if event.type == pg.QUIT:
				pg.quit()
				exit(0)
		screen.update(events)

		# EVENTS INSIDE THIS SCREEN
		if screen.submited():
			server, port, password = screen.get_values()
			client = Client(server, port, password)
			try:
				client.connect()
				connected = True
			except ConnectionAbortedError:
				print("Wrong password")
			except ConnectionRefusedError:
				print("Server offline")
		
		screen.draw(win)
		pg.display.update()

	client.start()

	screen = ProfileScreen(client)
	game_started = False
	while not game_started:
		pg.time.delay(100)
		events = pg.event.get()
		for event in events:
			if event.type == pg.QUIT:
				pg.quit()
				screen.client.disconnect()
				exit(0)
		screen.update(events)

		if screen.client.game:
			game_started = True
		# EVENTS INSIDE THIS SCREEN
		screen.draw(win)
		pg.display.update()
	
	screen = GameScreen(client)
	game_running = True
	while game_running:
		pg.time.delay(100)
		events = pg.event.get()
		for event in events:
			if event.type == pg.QUIT:
				pg.quit()
				screen.client.disconnect()
				exit(0)
		screen.update(events)

		# EVENTS INSIDE THIS SCREEN
		screen.draw(win)
		pg.display.update()


if __name__ == "__main__":
    main()