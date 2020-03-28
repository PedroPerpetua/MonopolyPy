from action import *
from field import *
from game_board import Game_Board
from player import Player

def main():
	p = Player("Pedro", "P")
	b = Game_Board()
	b.import_fields("fields.txt")
	p.join_game_board(b)
	print(p)
	p.move(p.roll_DEBUG(1,0))
	print(p)


if __name__ == "__main__":
	main()