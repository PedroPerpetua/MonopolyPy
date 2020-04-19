import pygame
from lib.assets import Assets, import_assets
from lib.UI.board_items.board import Board
from src.game.game import Game

BG_COLOR = (143,188,114)

def setup_window():
	win = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	import_assets("Client")
	pygame.display.set_icon(Assets.APP_ICON)
	return win


def main():
	pygame.init()
	print(pygame.display.Info())
	win = setup_window()
	win.fill((143,188,114))

	game = Game([[5, "Pedro"], [6, "Hugo"], [7, "Joao"], [8, "Teste"]])
	game.players[0].jail_counter = 1
	board = Board(40, 40, game)

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
				# SHOW OFF:
				if event.key == pygame.K_LEFT:
					game.players[0].pos = (game.players[0].pos + 1)%40
				if event.key == pygame.K_RIGHT:
					game.players[0].pos = (game.players[0].pos - 1)%40
				if event.key == pygame.K_UP:
					game.players[1].pos = (game.players[1].pos + 1)%40
				if event.key == pygame.K_DOWN:
					game.players[1].pos = (game.players[1].pos - 1)%40
				if event.key == pygame.K_a:
					game.players[2].pos = (game.players[2].pos + 1)%40
				if event.key == pygame.K_d:
					game.players[2].pos = (game.players[2].pos - 1)%40
				if event.key == pygame.K_w:
					game.players[3].pos = (game.players[3].pos + 1)%40
				if event.key == pygame.K_s:
					game.players[3].pos = (game.players[3].pos - 1)%40

		board.update(events)
		win.fill(BG_COLOR)
		board.draw(win)

		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	main()