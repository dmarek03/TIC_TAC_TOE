import time
import pygame
from board.Board import Board
from entity.Player import Player
from dataclasses import dataclass
from gui.Gui import GuiBoard, Rectangle
from entity.AiPlayer import  AiPlayer
from entity.RealPlayer import RealPlayer


@dataclass
class Game:
    board: Board
    number_of_sign_to_win:int
    gui: GuiBoard = None
    first_player:Player = None
    second_player:Player = None
    updated_position:tuple[int, str] = (None, None)
    start_rect_to_mark:Rectangle = None
    end_rect_to_mark:Rectangle = None


    def register_player(self, player:Player) -> None:
        if not self.board.game_board :
            self.board.initialize_game_board()
        if not self.first_player:
            self.first_player = player
            self.first_player.board = self.board
            print(f'Player number one registered')
        elif not self.second_player:
            self.second_player = player
            self.second_player.board = self.board
            print(f'Player number two registered')
        else:
            print(f'Max allowed number of players was registered')

    def _check_rows(self,sign:str, number_of_occurrence:int) -> bool:
        for row in range(self.board.number_of_rows):
            s = "".join(self.board.game_board[row][col] for col in range(self.board.number_of_columns))
            x =  s.find(number_of_occurrence * sign)
            if x >= 0:
                if number_of_occurrence == self.number_of_sign_to_win:
                    self.start_rect_to_mark = self.gui.list_of_rectangles[row*self.board.number_of_columns + x]
                    self.end_rect_to_mark = self.gui.list_of_rectangles[row*self.board.number_of_columns +x + number_of_occurrence-1]
                return True
        return False

    def _check_columns(self , sign:str, number_of_occurrence:int) -> bool:
        for col in range(self.board.number_of_rows):
            s = "".join(self.board.game_board[row][col] for row in range(self.board.number_of_rows))
            y = s.find(number_of_occurrence * sign)
            if  y >= 0:
                if number_of_occurrence == self.number_of_sign_to_win:
                    self.start_rect_to_mark = self.gui.list_of_rectangles[y*self.board.number_of_columns + col]
                    self.end_rect_to_mark = self.gui.list_of_rectangles[(y + number_of_occurrence-1)*self.board.number_of_columns +col]
                return True
        return False

    def _check_diagonals(self, sign: str, number_of_occurrence: int) -> bool:
        directions = [(1, 1), (1, -1)]
        for direction in directions:
            for start_row in range(self.board.number_of_rows):
                for start_col in range(self.board.number_of_columns):
                    diagonal = []
                    row, col = start_row, start_col
                    while 0 <= row < self.board.number_of_rows and 0 <= col < self.board.number_of_columns:
                        diagonal.append(self.board.game_board[row][col])
                        row += direction[0]
                        col += direction[1]
                    s = "".join(diagonal)
                    idx = s.find(number_of_occurrence * sign)
                    if idx >= 0:
                        start_rect_idx = (start_row + idx * direction[0]) * self.board.number_of_columns + (
                                    start_col + idx * direction[1])
                        end_rect_idx = (start_row + (idx + number_of_occurrence - 1) * direction[
                            0]) * self.board.number_of_columns + (
                                                   start_col + (idx + number_of_occurrence - 1) * direction[1])
                        self.start_rect_to_mark = self.gui.list_of_rectangles[start_rect_idx]
                        self.end_rect_to_mark = self.gui.list_of_rectangles[end_rect_idx]
                        return True


        return False

    def is_end(self, sign:str, number_of_occurrence:int) -> bool|tuple[tuple[list[int], bool]]:
        return (
                self._check_rows(sign, number_of_occurrence) or
                self._check_columns(sign, number_of_occurrence) or
                self._check_diagonals(sign, number_of_occurrence)
        )


    def is_tie(self) -> bool:
        return all(x != '_' for row in self.board.game_board for x in row)



    def execute_move(self, player:Player) -> bool:

        time.sleep(0.5)
        player.move()
        self.gui.rect_to_update = player.updated_position
        self.gui.draw()
        self.board.draw()
        pygame.display.update()



        if self.is_end(player.sign, self.number_of_sign_to_win):
            print(f'{player.name} win\n')
            self.gui.mark_win(self.start_rect_to_mark, self.end_rect_to_mark, 10)
            self.gui.show_game_settling(player.name + " win")

            return True

        if self.is_tie():
            print("Game end with tie\n")
            self.gui.show_game_settling("Game end with tie")
            return True


    def _bot_vs_bot(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()


            if  self.execute_move(self.first_player):
                break
            if self.execute_move(self.second_player):
                break

            pygame.display.flip()

    def _bot_vs_real_player(self) -> None:
        is_first_player_real = isinstance(self.first_player, RealPlayer)
        can_ai_move= True


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()


                if is_first_player_real:

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        col_idx = self.gui.get_col_idx(mouse_position)

                        if col_idx >= 0:
                            self.first_player.chosen_column = col_idx
                            if self.execute_move(self.first_player):
                                return


                        if self.execute_move(self.second_player):
                           return


                else:

                    if can_ai_move:
                        can_ai_move = not can_ai_move
                        if self.execute_move(self.first_player):

                            return


                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        col_idx = self.gui.get_col_idx(mouse_position)

                        if col_idx >= 0:
                            self.second_player.chosen_column = col_idx
                            if self.execute_move(self.second_player):
                                return
                            can_ai_move = not can_ai_move


                pygame.display.flip()

    def _real_player_vs_real_player(self) -> None:
        first_player_move = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if first_player_move:
                        first_player_move = not first_player_move
                        mouse_position = pygame.mouse.get_pos()
                        first_player_col_idx  =  self.gui.get_col_idx(mouse_position)
                        print(f'{first_player_col_idx=}')

                        if first_player_col_idx >= 0:

                            self.first_player.chosen_column = first_player_col_idx
                            if self.execute_move(self.first_player):
                                return

                    else:
                        first_player_move = not first_player_move

                        mouse_position = pygame.mouse.get_pos()
                        second_player_col_idx = self.gui.get_col_idx(mouse_position)
                        print(f'{second_player_col_idx=}')
                        if second_player_col_idx >= 0:

                            self.second_player.chosen_column = second_player_col_idx

                            self.execute_move(self.second_player)


                        pygame.display.flip()

    def play(self) -> None :
        self.gui.initialize()

        if isinstance(self.first_player, AiPlayer) and isinstance(self.second_player, AiPlayer):
            self._bot_vs_bot()

        if (
                (isinstance(self.first_player, AiPlayer) and isinstance(self.second_player, RealPlayer)) or
                isinstance(self.first_player, RealPlayer) and isinstance(self.second_player, AiPlayer)
        ):
            self._bot_vs_real_player()


        if isinstance(self.first_player, RealPlayer) and isinstance(self.second_player, RealPlayer):
            self._real_player_vs_real_player()
