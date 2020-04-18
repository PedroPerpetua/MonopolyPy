import pygame
from lib.assets import Assets, import_assets
from lib.UI.items.imagebutton import ImageButton

BG_COLOR = (143,188,114)

def setup_window():
	win = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	import_assets("Server")
	pygame.display.set_icon(Assets.SERVER_ICON)
	return win


def main():
	pygame.init()
	print(pygame.display.Info())
	win = setup_window()
	win.fill((143,188,114))

	button = ImageButton(10, 10, Assets.START_SELECTED, Assets.START_UNSELECTED, False)
	
	run = True
	while run:
		pygame.time.delay(100)
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					exit(0)

		button.update(events)
		win.fill(BG_COLOR)
		button.draw(win)

		if button.get_clicked():
			print("CLICK!")
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	main()