import pygame
from time import sleep
from pygame import Surface
from pygame import gfxdraw
from pygame.font import Font
from dataclasses import dataclass, field


@dataclass
class Rectangle:
    position:list[int]
    sign:str
    window:Surface

    def update(self, new_state:str) -> None:
        self.sign = new_state

    def draw(self) -> None:
        pygame.draw.rect(self.window, (0, 255, 255), self.position)


@dataclass
class GuiBoard:
    number_of_rows:int
    number_of_columns:int
    rect_width:int
    rect_height:int
    window:Surface
    spacing:int = 10
    list_of_rectangles: list[Rectangle] = field(default_factory=list)
    rect_to_update:tuple[int, str] = None

    def get_total_matrix_dimension(self) -> tuple[int, int]:
        total_matrix_width = self.number_of_columns * self.rect_width + (self.number_of_columns - 1) * self.spacing
        total_matrix_height = self.number_of_rows * self.rect_height + (self.number_of_rows - 1) * self.spacing
        return total_matrix_width, total_matrix_height


    def get_start_position(self) ->tuple[int, int]:
        total_matrix_width, total_matrix_height = self.get_total_matrix_dimension()
        start_x = (self.window.get_width() - total_matrix_width) // 2
        start_y = (self.window.get_height() - total_matrix_height) // 2
        return start_x, start_y


    def get_col_idx(self, position:tuple[int, int]) -> int:
        start_x, start_y = self.get_start_position()

        if position[0] < start_x or position[0] > self.window.get_width()-start_x:
            return -1
        if position[1] < start_y or position[1] > self.window.get_height()-start_y:
            return -1
        col_width_with_spacing = self.rect_width + self.spacing

        col_idx = (position[0] - start_x) // col_width_with_spacing

        return col_idx


    def create_rectangles(self) -> None:
        start_x, start_y = self.get_start_position()

        for row in range(self.number_of_rows):
            for col in range(self.number_of_columns):
                rect_x = start_x + col * (self.rect_width + self.spacing)
                rect_y = start_y + row * (self.rect_height + self.spacing)

                self.list_of_rectangles.append(Rectangle([rect_x, rect_y, self.rect_width, self.rect_height], '_',self.window ))


    def draw_outside_lines(self) -> None:
        total_matrix_width, total_matrix_height = self.get_total_matrix_dimension()
        start_x, start_y = self.get_start_position()


        for col in range(1, self.number_of_columns):
            line_x = start_x + col * (self.rect_width + self.spacing) - self.spacing // 2
            pygame.draw.line(self.window, (0, 0, 0), (line_x-1, start_y), (line_x-1, start_y + total_matrix_height), self.spacing+2)


        for row in range(1, self.number_of_rows):

            line_y = start_y + row * (self.rect_height + self.spacing) - self.spacing // 2
            pygame.draw.line(self.window, (0, 0 ,0), (start_x, line_y-1), (start_x + total_matrix_width, line_y-1), self.spacing+2)

        pygame.draw.rect(
            self.window,
            (0, 0 ,0),
            (
            start_x - self.spacing,
            start_y - self.spacing,
            total_matrix_width + 2*self.spacing,
            total_matrix_height + 2*self.spacing
            ),
            self.spacing
                         )

    def draw_first_sign(self, position:list[int], line_size:int) -> None:
        pygame.draw.line(self.window, (0, 0, 0), (position[0] - line_size // 2, position[1] - line_size // 2),
                         (position[0] + line_size // 2, position[1]+ line_size // 2), 5)

        pygame.draw.line(self.window, (0, 0, 0), (position[0] - line_size // 2, position[1] + line_size // 2),
                         (position[0]+ line_size // 2, position[1]- line_size // 2), 5)



    def draw_second_sign(self,position:list[int], radius:int) -> None:

        for i in range(5):

            gfxdraw.aacircle(self.window,  position[0],position[1],  radius-i, (0, 0 ,0))



    def mark_win(self, start_rect, end_rect, line_width:int) -> None:
        start_pos = (start_rect.position[0]+start_rect.position[2]//2,start_rect.position[1]+start_rect.position[3]//2 )
        end_pos = (end_rect.position[0]+end_rect.position[2]//2,end_rect.position[1]+end_rect.position[3]//2)

        p1v = pygame.math.Vector2(start_pos)
        p2v = pygame.math.Vector2(end_pos)
        lv = (p2v - p1v).normalize()
        lnv = pygame.math.Vector2(-lv.y, lv.x) * line_width // 2
        pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]

        pygame.draw.polygon(self.window, (255, 0, 0), pts)
        pygame.draw.circle(self.window, (255, 0, 0), start_pos, line_width//2)
        pygame.draw.circle(self.window, (255, 0, 0), end_pos, line_width//2)
        pygame.display.update()

    @staticmethod
    def get_font(font_path:str,size:int) -> Font:
        return Font(font_path, size)

    def show_game_settling(self, winner_name:str) -> None:
        WINNER_TEXT =  self.get_font("font/main_font.ttf", 40).render(winner_name, True, (255, 167, 200))
        WINNER_RECT = WINNER_TEXT.get_rect(center=(self.window.get_width() // 2, 30))
        self.window.blit(WINNER_TEXT, WINNER_RECT)
        pygame.display.update()
        sleep(6)


    def initialize(self) -> None:
        self.create_rectangles()
        for rect in self.list_of_rectangles:
            rect.draw()
        self.draw_outside_lines()
        pygame.display.update()


    def draw(self) -> None:
        rect = self.list_of_rectangles[self.rect_to_update[0]]

        position = [rect.position[0] + rect.position[2]//2 , rect.position[1] + rect.position[3]//2]

        if self.rect_to_update[1] == 'o':
            self.draw_second_sign(position, self.rect_width // 2 -10)
        else:
            self.draw_first_sign(position, self.rect_height -30)

        pygame.display.update()

