import pygame
from board.Board import Board
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Player(ABC):
    name:str
    sign:str
    opponent_sign: str
    board: Board = None
    updated_position: tuple[int, str] = (None, None)

    @abstractmethod
    def move(self) -> None:
        pass


    def update(self, row:int, col:int) -> None:
        self.updated_position = (row*self.board.number_of_columns +col, self.sign)
        self.board.game_board[row][col] = self.sign
        pygame.display.update()

    def is_occupied(self, row:int, col:int) -> bool:
        return self.board.game_board[row][col] != '_'