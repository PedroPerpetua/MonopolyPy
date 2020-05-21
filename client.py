import pygame as pg
from lib.assets import Assets, import_assets
from src.client_screens import StartScreen, ProfileScreen, GameScreen

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

   	# This will store all choices the user makes along the problem (client...)
	options = {}

	StartScreen.screen_loop(win, options)
	options["client"].start()
	ProfileScreen.screen_loop(win, options)
	GameScreen.screen_loop(win, options)

if __name__ == "__main__":
    main()