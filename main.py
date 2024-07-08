import pygame

from settings import *
from grid import Grid
from player import Player

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption('Dig or die @ h4sski')
        self.mouse = pygame.mouse
        
        self.player = Player(pygame.time.get_ticks())
        self.grid = Grid(self.player)
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # if self.mouse.get_pressed()[0]:
        self.grid.clicked(self.mouse.get_pos(), pygame.time.get_ticks())
    
    def update(self):
        self.grid.update(time=pygame.time.get_ticks())
        if pygame.time.get_ticks() > self.player.end_time:
            self.running = False
        self.player.end_time += self.grid.value_collected
        self.grid.value_collected = 0
    
    
    def draw(self):
        self.window.fill(0)
        
        # create 3 parts of the screen
        self.top_bar = pygame.Surface((RESOLUTION[0], TOP_BAR_HEIGHT))
        self.bottom_bar = pygame.Surface((RESOLUTION[0], BOTTOM_BAR_HEIGHT))
        self.middle_bar = pygame.Surface((RESOLUTION[0], 
                                          RESOLUTION[1] - TOP_BAR_HEIGHT - BOTTOM_BAR_HEIGHT))
        
        # draw top bar
        self.top_bar.fill((80,80,80))
        
        # draw middle bar
        self.middle_bar.fill((20, 20, 20))
        # self.middle_bar.fill((50, 200, 20))
        self.grid.draw(self.middle_bar)
        
        # draw bottom bar
        self.bottom_bar.fill((80, 80, 80))
        margin_x = 5
        margin_y = 2
        time_left_width = (RESOLUTION[0] - margin_x*2) * pygame.time.get_ticks() / self.player.end_time
        rect = pygame.Rect((margin_x, 2),
                           (time_left_width, BOTTOM_BAR_HEIGHT - margin_y*2))
        pygame.draw.rect(surface=self.bottom_bar, rect=rect, color='red')
            
        
        # put /blit/ all bars into the main window surface
        self.window.blit(self.top_bar, (0,0))
        self.window.blit(self.middle_bar, (0,TOP_BAR_HEIGHT))
        self.window.blit(self.bottom_bar, (0, RESOLUTION[1] - BOTTOM_BAR_HEIGHT))
                
        pygame.display.flip()
    
    def main(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.main()