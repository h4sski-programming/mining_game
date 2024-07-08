import pygame
import random

from settings import *


class Grid():
    def __init__(self, player) -> None:
        self.cols = RESOLUTION[0] // GRID_CELL_SIZE
        self.rows = RESOLUTION[1] // GRID_CELL_SIZE
        self.player = player
        self.generate_grid()
        self.value_collected = 0
        self.revealing_cells = 1
    
    def generate_grid(self) -> None:
        self.grid_list = [ [Cell(col=c, row=r) for c in range(self.cols)] for r in range(self.rows) ]
    
    def clicked(self, mouse_pos: tuple[int], time: int) -> None:
        cell = self.get_cell_from_position(mouse_pos[0], mouse_pos[1]-TOP_BAR_HEIGHT)
        if self.revealing_cells >= self.player.revealing_points:
            return
        # elif cell.revealed:
        cell.clicked(time)
    
    def update(self, time: int) -> None:
        revealing_cells = 0
        for r in self.grid_list:
            for cell in r:
                if cell.digged and cell.value>0:
                    self.value_collected += cell.collect_value()
                if cell.countingdown and not cell.revealed:
                    # pass
                    revealing_cells += 1
                if revealing_cells < self.player.revealing_points:
                    cell.update(time)
        self.revealing_cells = revealing_cells
    
    def draw(self, surface) -> None:
        # cell.draw(surface) for cell in row for row in self.grid_list
        for r in self.grid_list:
            for cell in r:
                cell.draw(surface)

    def get_cell_from_position(self, x: int, y: int):
        col = x // GRID_CELL_SIZE
        row = y // GRID_CELL_SIZE
        return self.grid_list[row][col]
    
    def get_number_revealing_cells(self) -> int:
        ret = 0
        for row in self.grid_list:
            for cell in row:
                if cell.countingdown and not cell.revealed:
                    ret += 1
        return ret

##################
### Cell class ###
##################
class Cell():
    def __init__(self, col: int, row: int) -> None:
        self.col = col
        self.row = row
        self.position = (self.col*GRID_CELL_SIZE, self.row*GRID_CELL_SIZE)
        self.get_random_type()
        self.digged = False
        self.revealed = False
        self.countingdown = False
        self.stop_countdown = 0
        self.countdown = 0
        self.color = (70, 70, 70)
    
    def get_random_type(self):
        self.type = random.choices(list(cell_types.keys()), weights=[l['probability'] for l in list(cell_types.values())], k=1000)[0]
        self.color = cell_types[self.type]['color']
        self.digging_time = cell_types[self.type]['digging_time']
        self.value = cell_types[self.type]['value']
    
    def update(self, time: int) -> None:
        # if self.digging:
        #     self.digging_countdown = self.digging_ends - time
        #     if self.digging_countdown <= 0:
        #         self.stop_digging()
        if self.countingdown:
            self.countdown = self.stop_countdown - time
            if self.countdown < 0:
                self.countingdown = False
                if not self.revealed:
                    self.revealed = True
                    self.color = cell_types[self.type]['color']
                elif not self.digged:
                    self.digged = True
                    
            
    
    def draw(self, surface) -> None:
        if not self.digged:
            rect = pygame.Rect(self.position, (GRID_CELL_SIZE-2, GRID_CELL_SIZE-2))
            pygame.draw.rect(surface=surface, rect=rect, color=self.color)
            
            if self.countingdown:
                text = pygame.font.SysFont('Comic Sans MS', 18).render(f'{self.countdown // 1_000}', False, 'black')
                surface.blit(text, self.position)
                
    
    def clicked(self, time)-> None:
        if not self.countingdown and not self.digged:
            self.countingdown = True
            if self.revealed:
                self.stop_countdown = time + cell_types[self.type]['digging_time']
            else:
                self.stop_countdown = time + 5_000
    
    def collect_value(self) -> int:
        v = self.value
        self.value = 0
        return v


cell_types = {
    'rock': {
        'probability': 0.3,
        'color': (130, 130, 130),
        'digging_time': 5_000,
        'value': 800,
        },
    'granite': {
        'probability': 0.04,
        'color': (250, 50, 170),
        'digging_time': 25_000,
        'value': 2_400,
        },
    'marble': {
        'probability': 0.06,
        'color': (170, 250, 50),
        'digging_time': 15_000,
        'value': 1_800,
        },
    'diamond': {
        'probability': 0.001,
        'color': (50, 170, 250),
        'digging_time': 90_000,
        'value': 6_000,
        },
}