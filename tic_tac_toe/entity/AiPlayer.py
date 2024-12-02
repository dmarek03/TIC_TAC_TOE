import pygame
from entity.Player import Player
from dataclasses import dataclass, field


@dataclass
class AiPlayer(Player):
    founded_sign_positions:list[list[int | tuple[int, int]]] = field(default_factory=list)


    def is_occupied(self, row:int, col:int) -> bool:

        if row < 0 or row >= self.board.number_of_rows:
            return True
        if col < 0 or col >= self.board.number_of_columns:
            return True
        return self.board.game_board[row][col] != '_'
    def can_move_to(self, row:int , col:int) -> bool:
        return (0 <= row < self.board.number_of_rows) and (0 <= col < self.board.number_of_columns) and self.board.game_board[row][col] == '_'

    def update(self, row:int, col:int) -> None:

        if self.can_move_to(row, col):
            self.updated_position = (row * self.board.number_of_columns + col, self.sign)
            self.board.game_board[row][col] = self.sign
            pygame.display.update()


    def check_rows(self, sign: str, number_of_occurrence:int) -> None:
        self.founded_sign_positions = []
        for row in range(self.board.number_of_rows-1, -1, -1):
            s = "".join(self.board.game_board[row][col] for col in range(self.board.number_of_columns))
            x = s.find(sign)

            if x  >= 0:


                self.founded_sign_positions.append([row, x, x + number_of_occurrence - 1])

            if number_of_occurrence == 1:
                x1 = s.find('_'+sign)
                if x1 >=0:

                    self.founded_sign_positions.append([row, x1 + 1, x1 + 1])

                x2 = s.find(sign+'_')
                if x2 >=0:

                    self.founded_sign_positions.append([row, x2, x2])


    def check_columns(self, sign: str, number_of_occurrence:int) -> None:
        self.founded_sign_positions = []
        for col in range(self.board.number_of_columns):
            s = "".join(self.board.game_board[row][col] for row in range(self.board.number_of_rows))
            y = s.find(sign)
            if y >= 0:
                self.founded_sign_positions.append([col, y, y + number_of_occurrence - 1])


    def check_diagonals(self, sign: str, number_of_occurrence: int) -> None:
        self.founded_sign_positions = []
        n = self.board.number_of_rows
        m = self.board.number_of_columns

        # Checking even diagonals
        for start_row in range(n-number_of_occurrence+1):
            s = "".join(self.board.game_board[start_row + i][i] for i in range(min(m, n - start_row)))

            x = s.find(sign)
            if x >= 0:
                self.founded_sign_positions.append(
                    [0, (start_row + x, x), (start_row + x + number_of_occurrence - 1, x + number_of_occurrence - 1)]
                )

        for start_col in range(1, m-number_of_occurrence+1):
            s = "".join(self.board.game_board[i][start_col + i] for i in range(min(n, m - start_col)))

            x = s.find(sign)
            if x >= 0:
                self.founded_sign_positions.append(
                    [0, (x, start_col + x), (x + number_of_occurrence - 1, start_col + x + number_of_occurrence - 1)]
                )

        # Checking odd diagonals
        for start_row in range(number_of_occurrence-1, n):
            s = "".join(self.board.game_board[start_row - i][i] for i in range(min(m, start_row + 1)))

            x = s.find(sign)
            if x >= 0:
                self.founded_sign_positions.append(
                    [1, (start_row - x, x), (start_row - x - number_of_occurrence + 1, x + number_of_occurrence - 1)]
                )

        for start_col in range(1, m-number_of_occurrence+1):
            s = "".join(self.board.game_board[n - 1 - i][start_col + i] for i in range(min(n, m - start_col)))

            x = s.find(sign)
            if x >= 0:
                self.founded_sign_positions.append(
                    [1, (n - 1 - x, start_col + x), (n - 1 - x - number_of_occurrence + 1, start_col + x + number_of_occurrence - 1)]
                )


    def get_start_position(self) -> list[list[int]]:
        possible_start_moves = []
        for row in range(self.board.number_of_rows-1, -1, -1):
            for col in range(self.board.number_of_columns//2, self.board.number_of_columns):
                if self.can_move_to(row, col) and self.is_occupied(row+1, col):
                    possible_start_moves.append([row, col])

            for col in range(self.board.number_of_columns//2-1, -1, -1):
                if self.can_move_to(row,col) and self.is_occupied(row+1, col):
                    possible_start_moves.append([row, col])

        return possible_start_moves


    def can_opponent_win_in_the_next_move(self, position: tuple[int, int]) -> bool:
        if position:

            self.update(position[0], position[1])
            opponent_position_to_win_1  = self.find_standard_best_option(3 * self.opponent_sign, 3)
            opponent_position_to_win_2 = self.find_trap_positions(self.opponent_sign + '_' + 2 * self.opponent_sign, 4, 0)
            opponent_position_to_win_3 = self.find_trap_positions(2 * self.opponent_sign + '_' + self.opponent_sign, 4, 1)
            self.board.game_board[position[0]][position[1]] = '_'
            if opponent_position_to_win_1 or opponent_position_to_win_2 or opponent_position_to_win_3:

                return True
            return False


    def prepare_trap_position(self, sign:str, number_of_occurrence:int, trap_type:int) -> list[list[int]]:
        possible_trap_positions = []
        self.check_rows(sign, number_of_occurrence)
        for row, start, end in self.founded_sign_positions:
            if trap_type == 0:
                if self.is_occupied(row+1, start):
                    possible_trap_positions.append([row, start])


            if trap_type ==  1:
                if self.is_occupied(row+1, end):
                    possible_trap_positions.append([row, end])


            if trap_type == 2:
                if self.is_occupied(row +1,start) and self.is_occupied(row+1, start+1) and self.is_occupied(row+1, end):
                    possible_trap_positions.append([row, start+1])


            if trap_type == 3:
                if self.is_occupied(row+1, start) and self.is_occupied(row+1, end-1) and self.is_occupied(row+1, end):
                    possible_trap_positions.append([row, end-1])


        # We did not have to check columns as in this variant of game such as trap situation cannot appear in columns

        self.check_diagonals(sign, number_of_occurrence)

        for diagonal_type,start_pos, end_pos in self.founded_sign_positions:

            if trap_type == 0:
                if self.is_occupied(start_pos[0]+1, start_pos[1]):
                    possible_trap_positions.append([start_pos[0], start_pos[1]])


            if trap_type == 1:
                if self.is_occupied(end_pos[0]+1, end_pos[1]):
                    possible_trap_positions.append([end_pos[0], end_pos[1]])


            if diagonal_type == 0:

                if trap_type == 2:
                    if self.is_occupied(start_pos[0]+1, start_pos[1]) and self.is_occupied(start_pos[0]+2, start_pos[1]+1) and self.is_occupied(end_pos[0]+1, end_pos[1]):
                        possible_trap_positions.append([start_pos[0]+1, start_pos[1]+1])


                if trap_type == 3:
                    if self.is_occupied(start_pos[0]+1, start_pos[1]) and self.is_occupied(end_pos[0], end_pos[1]-1) and self.is_occupied(end_pos[0]+1, end_pos[1]):
                        possible_trap_positions.append([end_pos[0]-1, end_pos[1]-1])


            else:

                if trap_type == 2:
                    if self.is_occupied(start_pos[0]+1, start_pos[1]) and self.is_occupied(start_pos[0], start_pos[0]+1) and self.is_occupied(end_pos[0]+1, end_pos[1]):
                        possible_trap_positions.append([start_pos[0]-1, start_pos[1]+1])


                if trap_type == 3:
                    if self.is_occupied(start_pos[0]+1, start_pos[1]) and self.is_occupied(end_pos[0]+2, end_pos[1]-1) and self.is_occupied(end_pos[0]+1, end_pos[1]):
                        possible_trap_positions.append([end_pos[0]+1, end_pos[1]-1])

        return possible_trap_positions


    def find_trap_positions(self, sign:str,number_of_occurrence:int, trap_type:int) -> list[list[int]]:
        founded_trap_positions = []
        self.check_rows(sign, number_of_occurrence)
        for row, start, end in self.founded_sign_positions:
            if trap_type == 0:
                if self.is_occupied(row+1, start+1):
                    founded_trap_positions.append([row, start+1])

            if trap_type == 1:
                if self.is_occupied(row+1, start+2):
                    founded_trap_positions.append([row, start+2])


        # We did not have to check columns as in this variant of game such as trap situation cannot appear in columns


        self.check_diagonals(sign, number_of_occurrence)
        for diagonal_type, start_pos, end_pos in self.founded_sign_positions:
            if diagonal_type == 0:
                if trap_type == 0:
                    if self.is_occupied(start_pos[0]+2, start_pos[1]+1):
                        founded_trap_positions.append([start_pos[0]+1, start_pos[1]+1])


                if trap_type == 1:
                    if self.is_occupied(start_pos[0]+3, start_pos[1]+2):
                        founded_trap_positions.append([start_pos[0]+2, start_pos[1]+2])



            else:

                if trap_type == 0:
                    if self.is_occupied(start_pos[0], start_pos[1]+1):
                        founded_trap_positions.append([start_pos[0]-1, start_pos[1]+1])


                if trap_type == 1:
                    if self.is_occupied(start_pos[0]-1, start_pos[1]+2):
                        founded_trap_positions.append([start_pos[0]-2, start_pos[1]+2])


        return founded_trap_positions


    def find_standard_best_option(self, sign:str, number_of_occurrence:int) -> list[list[int]]:
        possible_standard_moves = []
        self.check_rows(sign, number_of_occurrence)
        for row, start, end in self.founded_sign_positions:


                if self.can_move_to(0,start-1):
                    if start - 3 >= 0 or sign == number_of_occurrence * self.opponent_sign:
                        if self.is_occupied(row+1, start-1) and self.can_move_to(row, start-1):
                            possible_standard_moves.append([row, start-1])


                if self.can_move_to(0, end+1):
                    if start + 3 < self.board.number_of_columns or sign == number_of_occurrence * self.opponent_sign:

                        if self.is_occupied(row+1, end+1) and self.can_move_to(row, end+1):
                            possible_standard_moves.append([row, end+1])


        self.check_columns(sign, number_of_occurrence)

        for col, start, end in self.founded_sign_positions:

            if end-4 >= 0 or sign == number_of_occurrence*self.opponent_sign:
                if self.can_move_to(0, col):
                    if self.can_move_to(start-1, col):
                        possible_standard_moves.append([start-1, col])


        self.check_diagonals(sign, number_of_occurrence)
        for diagonal_type, start_pos, end_pos in self.founded_sign_positions:
            if diagonal_type == 0:
                if self.can_move_to(0, start_pos[1]-1):
                    if self.is_occupied(start_pos[0], start_pos[1]-1) and self.can_move_to(start_pos[0]-1, start_pos[1]-1):
                        possible_standard_moves.append([start_pos[0]-1, start_pos[1]-1])


                if self.can_move_to(0, end_pos[1]+1):
                    if self.is_occupied(end_pos[0]+2, end_pos[1]+1) and self.can_move_to(end_pos[0]+1, end_pos[1]+1):
                        possible_standard_moves.append([end_pos[0]+1, end_pos[1]+1])

            else:

                if self.can_move_to(0,start_pos[1]-1):
                    if self.is_occupied(start_pos[0] +2, start_pos[1]-1) and self.can_move_to(start_pos[0]+1, start_pos[1]-1):
                        possible_standard_moves.append([start_pos[0]+1, start_pos[1]-1])


                if self.can_move_to(0, end_pos[1]+1):
                    if self.is_occupied(end_pos[0], end_pos[1]+1) and self.can_move_to(end_pos[0]-1, end_pos[1]+1):
                        possible_standard_moves.append([end_pos[0]-1, end_pos[1]+1])
        return possible_standard_moves


    def move(self) -> None:
        nonstandard_position_to_win_1 = self.find_trap_positions(self.sign + '_' + 2*self.sign, 4, 0)
        nonstandard_position_to_win_2 = self.find_trap_positions(2*self.sign + '_' + self.sign, 4, 1)
        standard_position_to_win = self.find_standard_best_option(3 * self.sign, 3)
        standard_position_to_block_opponent = self.find_standard_best_option(3 * self.opponent_sign, 3)
        non_standard_position_to_block_opponent_1 = self.find_trap_positions(self.opponent_sign + '_' + 2*self.opponent_sign, 4, 0)
        non_standard_position_to_block_opponent_2 = self.find_trap_positions(2*self.opponent_sign + '_' + self.opponent_sign, 4, 1)
        non_standard_position_to_block_opponent_3 = self.prepare_trap_position(2*'_'+2*self.opponent_sign+'_', 5, 2)
        non_standard_position_to_block_opponent_4 = self.prepare_trap_position('_' + 2*self.opponent_sign + 2*'_', 5, 3)
        position_to_make_trap1 =  self.prepare_trap_position('__'+2*self.sign, 4, 0)
        position_to_make_trap2 = self.prepare_trap_position(2 * self.sign +'__' , 4, 1)
        position_to_make_trap3 = self.prepare_trap_position(2*'_'+2*self.sign+'_', 5, 2)
        position_to_make_trap4 = self.prepare_trap_position('_' + 2*self.sign + 2*'_', 5, 3)
        position_to_future_win_chance = self.find_standard_best_option(2 * self.sign, 2)
        position_to_continue_play =  self.find_standard_best_option(self.sign, 1)
        start_position = self.get_start_position()

        all_possible_moves = [
            nonstandard_position_to_win_1,
            nonstandard_position_to_win_2,
            standard_position_to_win,
            standard_position_to_block_opponent,
            non_standard_position_to_block_opponent_1,
            non_standard_position_to_block_opponent_2,
            non_standard_position_to_block_opponent_3,
            non_standard_position_to_block_opponent_4,
            position_to_make_trap1,
            position_to_make_trap2,
            position_to_make_trap3,
            position_to_make_trap4,
            position_to_future_win_chance,
            position_to_continue_play,
            start_position
        ]

        for possibles_moves in all_possible_moves:
            for pm in possibles_moves:

                if pm:

                    if all_possible_moves.index(possibles_moves) > 7:
                        if not self.can_opponent_win_in_the_next_move(pm):

                            self.update(pm[0], pm[1])
                            return
                    else:
                        self.update(pm[0], pm[1])
                        return

