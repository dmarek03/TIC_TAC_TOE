import re
from entity.Player import Player
from dataclasses import dataclass


@dataclass
class RealPlayer(Player):
    chosen_column:int  = None

    def get_column(self,message:str) -> int:
        while True:
            if re.match(r'\d', column := input(f'{message}:\n')):

                if self.board.in_range(int(column)-1):


                    if  not self.is_occupied(0, int(column)-1):


                        return int(column)-1
                    else:
                        print(f'Please choose not occupied column')
            else:
                print(f'Column must be an integer number')



    def move(self) -> None:

        for row in range(self.board.number_of_rows-1, -1, -1):
            if not self.is_occupied(row, self.chosen_column):
                self.update(row, self.chosen_column)
                break
