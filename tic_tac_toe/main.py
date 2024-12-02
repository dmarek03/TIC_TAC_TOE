import pygame
from typing import Final
from gui.Gui import GuiBoard
from board.Board import Board
from entity.RealPlayer import RealPlayer
from entity.AiPlayer import AiPlayer
from game.Game import Game


def main() -> None:
    pygame.init()
    NUMBER_OF_ROWS:Final = 6
    NUMBER_OF_COLUMNS:Final = 7
    NUMBER_OF_SIGN_TO_WIN:Final = 4

    width = 1300
    height = 800

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Kółko krzyżyk z ciążeniem')
    window.fill((255,0,255))
    gui_board = GuiBoard(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS, 100, 100, window)


    board = Board(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS)
    player_one = AiPlayer(name="Player one" , sign='o', opponent_sign='x')
    player_two = RealPlayer(name = "Player two" ,sign='x', opponent_sign='o')

    game = Game(board, NUMBER_OF_SIGN_TO_WIN, gui = gui_board)
    game.register_player(player_one)
    game.register_player(player_two)
    game.play()



if __name__ == '__main__':
    main()
