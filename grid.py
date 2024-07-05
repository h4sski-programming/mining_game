import pygame
import random

from settings import *


class Grid():
    def __init__(self) -> None:
        self.cols = RESOLUTION[0] // GRID_CELL_SIZE
        self.rows = RESOLUTION[1] // GRID_CELL_SIZE
        self.generate_grid()
    
    def generate_grid(self) -> None:
        self.grid_list = [ [Cell(col=c, row=r) for c in range(self.cols)] for r in range(self.rows) ]
    
    def update(self, mouse_pos: tuple[int]) -> None:
        cell = self.get_cell_from_position(mouse_pos[0], mouse_pos[1]-TOP_BAR_HEIGHT)
        cell.digging = True
    
    def draw(self, surface) -> None:
        # cell.draw(surface) for cell in row for row in self.grid_list
        for r in self.grid_list:
            for cell in r:
                cell.draw(surface)

    def get_cell_from_position(self, x: int, y: int):
        col = x // GRID_CELL_SIZE
        row = y // GRID_CELL_SIZE
        return self.grid_list[row][col]


class Cell():
    def __init__(self, col: int, row: int) -> None:
        self.col = col
        self.row = row
        self.position = (self.col*GRID_CELL_SIZE, self.row*GRID_CELL_SIZE)
        self.type = 'rock'
        self.color = (120, 120, 120)
        self.digging = False
    
    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_CELL_SIZE-2, GRID_CELL_SIZE-2))
        pygame.draw.rect(surface=surface, rect=rect, color=self.color)
        
        if self.digging:
            text = pygame.font.SysFont('Comic Sans MS', 28).render('3', False, 'black')
            surface.blit(text, self.position)
        