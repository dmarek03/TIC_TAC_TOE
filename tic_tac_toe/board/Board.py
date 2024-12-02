from dataclasses import dataclass, field


@dataclass
class Board:
    number_of_rows:int
    number_of_columns:int
    game_board:list[list[str]] = field(default_factory=list)


    def in_range(self,col:int) -> bool:
        return 0 <= col <= self.number_of_columns

    def initialize_game_board(self) -> None:
        self.game_board = [["_"]*self.number_of_columns for _ in range(self.number_of_rows)]

    def draw(self) -> None:
        for i in range(1, self.number_of_columns + 1):
            print(i, end=' ')

        print(' ' * 14)
        for row in range(self.number_of_rows):
            for col in range(self.number_of_columns):
                if self.game_board[row][col] == ' ':
                    print('.', end=' ')

                else:
                    print(self.game_board[row][col], end=' ')
            print()

