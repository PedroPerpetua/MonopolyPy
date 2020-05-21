from threading import Thread
import pygame as pg
from lib.assets import Assets, import_assets
from src.server_screens import StartScreen, QueueScreen, InGameScreen
from src.server import Server

WIN_W = 300
WIN_H = 300


def server_thread(server):
	server.run()

# MAIN APPLICATION LOOP
def main():
	# INITIALIZE PYGAME WINDOW
	pg.init()
	win = pg.display.set_mode((WIN_W, WIN_H))
	import_assets("Server")
	pg.display.set_caption("MonopolyPy server")
	icon = Assets.APP_ICON
	pg.display.set_icon(icon)

	# This will store all choices the user makes along the problem (number of players, ip, port, the actual server...)
	options = {}
	
	StartScreen.screen_loop(win, options)
	options["server"] = Server(options["host"], options["port"], options["password"], options["num_players"])
	thread = Thread(target=server_thread, args=[options["server"]])
	thread.start()
	QueueScreen.screen_loop(win, options)
	InGameScreen.screen_loop(win, options)

if __name__ == "__main__":
	main()