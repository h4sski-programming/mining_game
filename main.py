import pygame

from settings import *
from grid import Grid


class Game():
    def __init__(self) -> None:
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption('Mining game @ h4sski')
        self.mouse = pygame.mouse
        
        self.grid = Grid()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        if self.mouse.get_pressed()[0]:
            self.grid.update(self.mouse.get_pos())
    
    def update(self):
        # self.grid.update(self.mouse.get_pos())
        pass
    
    
    def draw(self):
        self.window.fill(0)
        
        # create 3 parts of the screen
        self.top_bar = pygame.Surface((RESOLUTION[0], TOP_BAR_HEIGHT))
        self.bottom_bar = pygame.Surface((RESOLUTION[0], BOTTOM_BAR_HEIGHT))
        self.middle_bar = pygame.Surface((RESOLUTION[0], 
                                          RESOLUTION[1] - TOP_BAR_HEIGHT - BOTTOM_BAR_HEIGHT))
        
        # draw top bar
        self.top_bar.fill((70,70,70))
        
        # draw middle bar
        self.middle_bar.fill((20, 20, 20))
        self.grid.draw(self.middle_bar)
        
        # draw bottom bar
        self.bottom_bar.fill((200, 200, 200))
        
        
        # put /blit/ all bars into the main window surface
        self.window.blit(self.top_bar, (0,0))
        self.window.blit(self.middle_bar, (0,TOP_BAR_HEIGHT))
        self.window.blit(self.top_bar, (0, RESOLUTION[1] - BOTTOM_BAR_HEIGHT))
                
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