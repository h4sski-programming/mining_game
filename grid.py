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
    
    def click_on(self, mouse_pos: tuple[int], time: int) -> None:
        cell = self.get_cell_from_position(mouse_pos[0], mouse_pos[1]-TOP_BAR_HEIGHT)
        if not cell.digging:
            cell.start_digging(time)
    
    def update(self, time: int) -> None:
        for r in self.grid_list:
            for cell in r:
                cell.update(time)
    
    def draw(self, surface) -> None:
        # cell.draw(surface) for cell in row for row in self.grid_list
        for r in self.grid_list:
            for cell in r:
                cell.draw(surface)

    def get_cell_from_position(self, x: int, y: int):
        col = x // GRID_CELL_SIZE
        row = y // GRID_CELL_SIZE
        return self.grid_list[row][col]


cell_types = {
    'rock': {
        'probability': 0.3,
        'color': (90, 90, 90),
        'digging_time': 5_000,
        'value': 5,
        },
    'granite': {
        'probability': 0.03,
        'color': (190, 190, 190),
        'digging_time': 25_000,
        'value': 25,
        },
    'marble': {
        'probability': 0.02,
        'color': (170, 250, 170),
        'digging_time': 20_000,
        'value': 20,
        },
    'diamond': {
        'probability': 0.001,
        'color': (50, 170, 250),
        'digging_time': 50_000,
        'value': 50,
        },
}

class Cell():
    def __init__(self, col: int, row: int) -> None:
        self.col = col
        self.row = row
        self.position = (self.col*GRID_CELL_SIZE, self.row*GRID_CELL_SIZE)
        self.get_random_type()
        self.digging = False
        self.revealed = False
    
    def get_random_type(self):
        self.type = random.choices(list(cell_types.keys()), weights=[l['probability'] for l in list(cell_types.values())], k=1000)[0]
        self.color = cell_types[self.type]['color']
        self.digging_time = cell_types[self.type]['digging_time']
        self.value = cell_types[self.type]['value']
    
    def update(self, time: int) -> None:
        if self.digging:
            self.digging_countdown = self.digging_ends - time
            if self.digging_countdown <= 0:
                self.stop_digging()
            
    
    def draw(self, surface) -> None:
        if not self.revealed:
            rect = pygame.Rect(self.position, (GRID_CELL_SIZE-2, GRID_CELL_SIZE-2))
            pygame.draw.rect(surface=surface, rect=rect, color=self.color)
        
            if self.digging:
                text = pygame.font.SysFont('Comic Sans MS', 18).render(f'{self.digging_countdown // 1_000}', False, 'black')
                surface.blit(text, self.position)
    
    def start_digging(self, time: int) -> None:
        self.digging = True
        self.digging_started = time
        self.digging_ends = time + self.digging_time
    
    def stop_digging(self) -> None:
        self.digging = False
        self.revealed = True