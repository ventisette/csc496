import pygame
import math#, projectiles
from pygame.locals import *
pygame.init()

"""
Holds methods and values to give functionality to the hero character
"""
class hero:
    
    X = 0           #used to for players coordinates/speed of character movement
    Y = 0           #used to for players coordinates/speed of character movement
    MOUSE_X, MOUSE_Y = pygame.mouse.get_pos() #used for mouse coordinates
    IMG = None #stores converted hero image
    PI = math.pi    #stores the value of PI, used for hero rotation
    ROTATED_DEGREE = 0 #stores the degrees rotated by the character
    HEALTH = 0      #stores the players health
    MAX_HEALTH = 0
    MAX_MANA = 0
    MANA = 0
    OLD_RECTANGLE = None
    WIDTH = 0
    HEIGHT = 0
    SHELL = []
    WAIT = 0
    X_RATIO = 0  #x and y ratios use to store values to make sure that the ratio 
    Y_RATIO = 0  #does not change unless the option menu has been closed.
    
    """
    sets the hero's img, this should be uses as a python.Surface value that
    has an image pre-assigned then passed in
    params:
    img; the surface image to assign to IMG
    """
    def set_IMG(self, img):
        if isinstance(img, tuple):
            self.IMG = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.IMG.fill((255,255,255))
            self.IMG.fill((img), pygame.Rect((1,1), (self.WIDTH, self.HEIGHT)))
        else:
            self.IMG = img

    """
    intializes the hero class
    params:
    starting_x; the starting x value of the hero
    starting_y; the starting y value of the hero    
    """
    def __init__(self, width = 0, height = 0, health = 0, mana = 0, x = 0, y = 0, img = (0, 0, 0)):
        self.HEALTH = health
        self.MANA = mana
        self.MAX_HEALTH = health
        self.MAX_MANA = mana
        self.WIDTH = width
        self.HEIGHT = height
        self.X = x
        self.Y = y
        self.MOVESPEEDX = .2
        self.MOVESPEEDY = .2
        self.MOVESPEEDDIAG = ( self.MOVESPEEDX / math.sqrt(self.MOVESPEEDX**2) ) * self.MOVESPEEDX
        self.set_IMG(img)
        self.IMG.get_rect().center = (self.X, self.Y)

    def size(self, screen_size, old_screen_size):
        if old_screen_size[0] != 0 or old_screen_size[1] != 0:
            x_ratio = round((self.X + (self.WIDTH/2)) / old_screen_size[0], 10)
            y_ratio = round((self.Y + (self.HEIGHT/2)) / old_screen_size[1], 10)
        else:
            x_ratio = round((float(screen_size[0])/float((screen_size[0]*2))), 1)
            y_ratio = round((float(screen_size[1])/float((screen_size[1]*2))), 1)
        self.WIDTH = screen_size[0]/32 + 10
        self.HEIGHT = screen_size[0]/32 + 10  
        self.X = (screen_size[0] * x_ratio) - self.WIDTH/2
        self.Y = (screen_size[1] * y_ratio) - self.HEIGHT/2
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), self.IMG)
        self.IMG = pygame.transform.smoothscale(self.IMG, (self.WIDTH, self.HEIGHT), surf) 
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), 0, self.IMG)
        return self.IMG
                                               
    """
    handles the movement keys of the hero character
    params:
    keys_pressed;the pygame (or any) array retrieved with values
        of the keys stored in the array ex: [q, w, e, r, t, y, ...]
    """
    def move(self, keys_pressed, screen_size):
        if(keys_pressed[119] == 1):
            if self.in_bounds(0, self.Y - 1, False):
                if(keys_pressed[97] == 1):
                    self.X -= self.MOVESPEEDDIAG
                    self.Y -= self.MOVESPEEDDIAG
                elif(keys_pressed[100] == 1):                              
                    self.X += self.MOVESPEEDDIAG
                    self.Y -= self.MOVESPEEDDIAG
                else:
                    self.Y -= self.MOVESPEEDY
        elif(keys_pressed[97] == 1):
            if self.in_bounds(0, self.X - 1, False):
                if(keys_pressed[119] == 1):
                    self.X -= self.MOVESPEEDDIAG
                    self.Y -= self.MOVESPEEDDIAG
                elif(keys_pressed[115] == 1):                              
                    self.X -= self.MOVESPEEDDIAG
                    self.Y += self.MOVESPEEDDIAG
                else:
                    self.X -= self.MOVESPEEDX
        elif(keys_pressed[115] == 1):
            if self.in_bounds(screen_size[1], self.Y + 1, True):
                if(keys_pressed[97] == 1):
                    self.X -= self.MOVESPEEDDIAG
                    self.Y += self.MOVESPEEDDIAG
                elif(keys_pressed[100] == 1):                              
                    self.X += self.MOVESPEEDDIAG
                    self.Y += self.MOVESPEEDDIAG
                else:
                    self.Y += self.MOVESPEEDY
        elif(keys_pressed[100] == 1):
            if self.in_bounds(screen_size[0], self.X + 1, True):
                if(keys_pressed[119] == 1):
                    self.X += self.MOVESPEEDDIAG
                    self.Y -= self.MOVESPEEDDIAG
                elif(keys_pressed[115] == 1):                              
                    self.X += self.MOVESPEEDDIAG
                    self.Y += self.MOVESPEEDDIAG
                else:                    
                    self.X += self.MOVESPEEDX
        return self.X, self.Y

    def in_bounds(self, bound, amt_moved, greaterThan):
        if greaterThan:
            if amt_moved > bound:
                return False
        else:
            if amt_moved < bound:
                return False
        return True
        
    """
    logic for the hero character to face the mouse based the starting position
    of the hero characters img to start facing south (towards bottom of screen)
    params:
    SCREEN; the screen that the rotating hero character is being drawn on
    returns:
    rotated_Surf; surface of the image, this gets drawn to pos of rectangle
    rotated_Rect; destination of the surface image
    """
    def rotate_towards_cursor(self):
        self.MOUSE_X, self.MOUSE_Y = pygame.mouse.get_pos() #get mouse positions
        try:
            #get radians from the differencs between hero and the mouse for both x and y
            angle = math.atan2((self.Y - self.MOUSE_Y), (self.MOUSE_X - self.X)) / self.PI * 3.0
            self.ROTATED_DEGREE = math.degrees(angle) #get degrees from the angle radians
            self.ROTATED_DEGREE += 90 + (17/360) #needs to be rotated an extra 90 degrees to follow cursor accurately
        except Exception as e:   
            pass #attempt to play it off as though nothing has happened
        oldCenter = (self.X , self.Y)  #find center of the calling surface rectangle
        rotated_Surf = pygame.transform.rotate(self.IMG, self.ROTATED_DEGREE)  #rotate based on degrees
                    #of the mouse and the character, steps listed above
        rotated_Rect = rotated_Surf.get_rect()  #get the surfaces current rectangle
        rotated_Rect.center = oldCenter         #set that rectangles center to the original incoming rectangles
                                                #center, must be done or heros center stays in the corner
        return rotated_Surf, rotated_Rect       #returns the source and the destination of the source
        
    """
    shows the values of important values of the hero
    """
    def get_x(self):
        return self.X
    
    def get_y(self):
        return self.Y
    
    def get_health(self):
        return self.HEALTH
    
    def get_mana(self):
        return self.MANA
    
    def get_rotation(self):
        return self.ROTATED_DEGREE
    
    def health_bar(self, screen, dmg, screen_size):
        if self.HEALTH > 0:
            self.HEALTH -= dmg
        health_border_rect = pygame.draw.rect(screen, (255, 255, 255), (screen_size[1]/50-2, screen_size[1]/50-2, (screen_size[0]/800) * self.MAX_HEALTH*2 + 4, math.ceil(screen_size[0]/80.0)+4))
        health_back_rect = pygame.draw.rect(screen, (0, 0, 0), (screen_size[1]/50, screen_size[1]/50, (screen_size[0]/800) * self.MAX_HEALTH*2, math.ceil(screen_size[0]/80.0)))
        health_rect = pygame.draw.rect(screen, (255, 0, 0), (screen_size[1]/50, screen_size[1]/50, (screen_size[0]/800) * self.HEALTH*2, math.ceil(screen_size[0]/80.0)))
        return health_rect
        
    def mana_bar(self, screen, mana_gained, screen_size):
        if(self.MANA == 100):
            pass
        else:
            self.MANA += mana_gained
        mana_border_rect = pygame.draw.rect(screen, (255, 255, 255), (screen_size[1]/50-2, screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0) - 2, (screen_size[0]/800) * self.MAX_MANA + 4, (math.ceil(screen_size[0]/80.0)/2.0)+4))
        mana_back_rect = pygame.draw.rect(screen, (0, 0, 0), (screen_size[1]/50, screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0), (screen_size[0]/800) * self.MAX_MANA, math.ceil(screen_size[0]/80.0)/2.0))
        mana_rect = pygame.draw.rect(screen, (0, 191, 255), (screen_size[1]/50, screen_size[1]/50 + math.ceil((screen_size[0]/80.0)/2.0), (screen_size[0]/800) * self.MANA, math.ceil((screen_size[0]/80.0)/2.0)))
        return mana_rect

    def blink(self, mouse_x, mouse_y):
        if self.MANA == 100:
            self.MANA = 0
            self.X = float(mouse_x)
            self.Y = float(mouse_y)
        else:
            pass

    def shoot(self, screen_size, old_screen_size):
        pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if pressed[0] == 1:
            img = "images/fireball.png"
            surf = pygame.image.load(img).convert_alpha()
            shell = projectiles.fireball(screen_size, mouse_pos, (self.X, self.Y), surf)
            shell.size(screen_size, old_screen_size)
            self.SHELL.append(shell)
        return self.SHELL

    def projectile_in_bounds(self, shell, screen_size):
        if shell.X > screen_size[0]or shell.X < 0 or shell.Y < 0 or shell.Y > screen_size[1]:
            self.SHELL.remove(shell)
            return False
        return True

    
    def get_active_rounds(self):
        return len(self.SHELL)

    def get_shells(self):
        return self.SHELL
