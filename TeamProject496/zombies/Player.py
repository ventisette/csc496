import pygame, random        
        
class Player:
    def __init__(self):
        self.x = 10
        self.y = 10
        self.speed = 2 
    def move(self,xAxis,yAxis):
        self.x = xAxis
        self.y = yAxis
    def moveRight(self):
        self.x = self.x + self.speed
    def moveLeft(self):
        self.x = self.x - self.speed
    def moveUp(self):
        self.y = self.y - self.speed
    def moveDown(self):
        self.y = self.y + self.speed    
    def draw(self, screen):
        black = 0,0,0
        pygame.draw.rect(screen, black, (self.x, self.y, 10, 10), 0)
    def givePosition(self):
        return (self.x,self.y)
   
        
class Zombie(Player):
    def __init__(self):
        self.x = 60
        self.y = 60
        self.speed = .5
        self.color = 0,255,0
        
    def zMove(self, p, o, z):
        if(self.intersect(p, z, o[0], o[1])):
            self.moveRandomAI()
        else:
            self.moveSmartAI(p)
            
    def moveRandomAI(self):
        i = random.randrange(0,5)
        if(i==1):
            self.moveRight()
        if(i==2):
            self.moveLeft()
        if(i==3):
            self.moveUp()
        if(i==4):
            self.moveDown()
    def moveSmartAI(self, p):
        
        self.moveRandomAI()
        
        if(random.randrange(0,10) == 5):
            self.becomeSpecial()
        if(random.randrange(0,100) == 5):
            self.becomeSpecial2()
        
        if(p[0]>self.x):
            self.moveRight()
        if(p[1]>self.y):
            self.moveDown()
        if(p[0]<self.x):
            self.moveLeft()
        if(p[1]<self.y):
            self.moveUp()
            
    def becomeSpecial(self):
        self.color = 0,255,0
        if(self.speed > 1):
            self.speed = .5
        else:
            self.speed = 1.5
            
    def becomeSpecial2(self):
            self.speed = 2.5
            self.color = 255,0,0
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 10, 10), 0)
    
    
    
        
    def ccw(self,A,B,C):
        return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])
    
    def intersect(self,A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)
    
    
        
class Object():
    def __init__(self):
        self.x = 180
        self.y = 180
        self.w = 10
        self.h = 100
        self.color = 10,10,10
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), 0)
    def givePosition(self):
        return ((self.x,self.y),(self.x+self.w, self.y+self.h))
