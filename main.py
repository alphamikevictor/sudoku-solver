import pygame
import sys
from functools import lru_cache
import time

class Color():
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0

class SudokuDrawer():

    def __init__(self):
        self._drawn = False

    def draw(self, table, filled, screen):
        if not self._drawn:
            screen.fill(Color.WHITE)
            for line in self._lines():
                pygame.draw.rect(screen, Color.RED, line)

        for x in range(9):
            for y in range(9):
                font = pygame.font.Font('freesansbold.ttf', (600//9)-(600//90))
                color = Color.RED
                if (x,y) in filled:
                    color = Color.BLACK
                text_to_render = str(table[x][y]).replace("0", "  ")
                text = font.render(text_to_render, True, color)
                textRect = text.get_rect()
                textRect.center = (y*600//9) + (600//18) +2, (x*600//9)+(600//18)+2
                if color == Color.BLACK and not self._drawn:
                    screen.blit(text, textRect)
                if color == Color.RED:
                    pygame.draw.rect(screen, Color.WHITE, textRect)
                    screen.blit(text, textRect)

        pygame.display.flip()
        self._drawn = True
                   

    @lru_cache(maxsize=10)
    def _lines(self):
        return self._external_borders() + self._main_squares() + self._little_squares()
    
    def _external_borders(self):
        return [
            pygame.Rect(0,0,2,600),
            pygame.Rect(0,0,600,2),
            pygame.Rect(598,0,2,600),
            pygame.Rect(0,598,600,2)
        ]
    def _main_squares(self):
        return [
            pygame.Rect(200,0,2,600),
            pygame.Rect(400,0,2,600),
            pygame.Rect(0,200,600,2),
            pygame.Rect(0,400,600,2)
        ]
    
    def _little_squares(self):
        return  self._little_squares_horizontal() + self._little_squares_vertical()
               
    def _little_squares_horizontal(self):
        return [pygame.Rect(0,i*600//9,600,1) for i in range(1,9) if i%3!=0]

    def _little_squares_vertical(self):
        return [pygame.Rect(i*600//9,0,1,600) for i in range(1,9) if i%3!=0]

def sudoku_solver(sudoku, filled, sudoku_drawer, screen):
    time.sleep(0.1)
    freepositions = ( (x,y) for x in range(9) for y in range(9) if sudoku[x][y] == 0)
    try:
        (pos_x, pos_y) = freepositions.__next__()
    except StopIteration:
        return True
    possible_solutions = set(x for x in range(1,10))
    possible_solutions = possible_solutions.difference(set(sudoku[pos_x][y] for y in range(9)))
    possible_solutions = possible_solutions.difference(set(sudoku[x][pos_y] for x in range(9)))
    current_square_top_left = (pos_x-pos_x%3, pos_y-pos_y%3)
    possible_solutions = possible_solutions.difference(
                                set(sudoku[x][y]
                                        for x in range(current_square_top_left[0],current_square_top_left[0]+3)
                                        for y in range(current_square_top_left[1],current_square_top_left[1]+3)
                                )
                                )
    for number in possible_solutions:
        sudoku[pos_x][pos_y] = number
        sudoku_drawer.draw(sudoku, filled, screen)
        if sudoku_solver(sudoku, filled, sudoku_drawer, screen):
            return True
    sudoku[pos_x][pos_y]=0
    return False



pygame.init()

# SUDOKU = [
#     [0, 0, 0, 0, 9, 5, 1, 0, 4],
#     [0, 5, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 4, 2, 0, 0, 3, 0, 8],
#     [0, 0, 0, 0, 2, 0, 0, 7, 0],
#     [0, 0, 9, 8, 0, 6, 2, 0, 0],
#     [0, 8, 0, 0, 7, 0, 0, 0, 0],
#     [4, 0, 5, 0, 0, 3, 7, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0],
#     [1, 0, 2, 9, 5, 0, 0, 0, 0]
# ]

SUDOKU = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 1, 0, 9, 0, 0, 6, 0, 3],
    [9, 0, 4, 0, 0, 2, 0, 0, 7],
    [4, 0, 0, 0, 6, 7, 0, 0, 0],
    [0, 0, 5, 0, 0, 0, 7, 0, 0],
    [0, 0, 0, 1, 2, 0, 0, 0, 4],
    [8, 0, 0, 7, 0, 0, 2, 0, 1],
    [6, 0, 1, 0, 0, 5, 0, 3, 8],
    [2, 0, 0, 0, 0, 0, 0, 0, 0]
]


filled = [ (x,y) for x in range(9) for y in range(9) if SUDOKU[x][y] != 0 ]

size = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sudoku")

sudoku_drawer = SudokuDrawer()
sudoku_drawer.draw(SUDOKU, filled, screen)
sudoku_solver(SUDOKU, filled, sudoku_drawer, screen)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos()
            print("Mouse is in position", position)
print("Out of business")
pygame.quit()