import pygame
from pygame.locals import *
import Player
from Player import *

screen_mode = (640, 480)
background = 255,255,255 #white
black = 0,0,0
blue = 0,0,255
p = Player()    
z = []
obj = Object()


ii=0
while ii<10:
    z.append(Zombie())
    ii = ii+1
    


class Game:
# this gets called first
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_mode) 
        pygame.display.set_caption("Zombie")
        self.quit = False
# put game update code here
    def update(self): return
    # put drawing code here
    def draw(self): 
        self.screen.fill(background)
        
        p.draw(self.screen)
        
        obj.draw(self.screen)
        
        for zombie in z:
            zombie.draw(self.screen)
        


        pygame.display.flip()
    # the main game loop
    def mainLoop(self): 
        while not self.quit:
            
            #fps
            clock = pygame.time.Clock()
            clock.tick(140)
            
            
            
            # handle events
            for zombie in z:
                zombie.zMove(p.givePosition(),obj.givePosition(), zombie.givePosition())
            
            
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                p.moveRight()
            if keys[pygame.K_LEFT]:
                p.moveLeft()
            if keys[pygame.K_UP]:
                p.moveUp()
            if keys[pygame.K_DOWN]:
                p.moveDown()
                
                
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit = True
                
                    
            
                    
            self.update()
            self.draw()
if __name__ == '__main__' :
    game = Game()
    game.mainLoop()