import pygame
from libs.server import Server
from libs.UI.server_main_screen import Server_MainScreen

WIN_W = 300
WIN_H = 294

def setup_window():
	win = pygame.display.set_mode((WIN_W, WIN_H))
	pygame.display.set_caption("Monopoly server")
	icon = pygame.image.load("libs/assets/server_app_icon.png")
	icon.set_colorkey((255,0,255))
	pygame.display.set_icon(icon)
	return win

def main():
	pygame.init()
	win = setup_window()
	screen = Server_MainScreen(win)

	run = True
	while run:
		pygame.time.delay(100)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				exit(0)
		screen.update(events)
		screen.draw()
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	main()