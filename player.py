import pygame

from settings import *


class Player():
    def __init__(self, time) -> None:
        self.end_time = time + 30_000
        self.revealing_points = 10
    
    def increase_time(self, add_time: int) -> None:
        self.end_time += add_time
        