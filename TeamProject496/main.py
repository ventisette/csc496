import screen
import thread
import time
import pygame
import sys
import math
import random
import os
from wpn import *
from pygame.locals import *
from image import *
from menu import *

os.environ['SDL_VIDEO_CENTERED'] = '1' # Center the game window.
pygame.init()#Need to work this out, main should not need to know about pygame.

window = screen.Window(800, 600, "TeamProject 496", (0,0,0)) # Create game window.
#window.set_font(((12, None), (24, None))) <- Another example of the two statements below
window.set_font(12, None) # index 0
window.set_font(24, None) # index 1

mif = "images/cursor.png"
pygame.mouse.set_visible(False)                  #hides the cursor so only the cross hair is seen
mouse_c = pygame.image.load(mif).convert_alpha()  #For converting images to types that are usable by python

def check_significant_keypresses(keys_pressed, window, player, items, fired, enemies):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if keys_pressed[114] == 1:
            player.weapon.reloadWeapon()
        elif keys_pressed[102] == 1:            
            pygame.key.set_repeat(0, 0)
            for item in items:
                if player.collidesWith(item):
                    items.remove(item)
                    pickedUp = player.pickUp(item)
                    if not pickedUp == None:
                        items.extend([pickedUp])   
        elif keys_pressed[112] == 1:
            pauseMenu()
            #window.set_background("images/field.jpg")
        pygame.key.set_repeat(1, 1)
            
"""
gets current position of the mouse
sets the mouse image position, the cursor is set to the center of theimage
copies the mouse image created earlier to the screen
"""
def setupCrossHairCursor():    
    X, Y = pygame.mouse.get_pos()    
    mouse_block = mouse_c.get_rect()
    mouse_block.center = (X - mouse_block[2]/2, Y - mouse_block[3]/2)
    X -= mouse_c.get_width()
    Y -= mouse_c.get_height()
    return mouse_block

def gameAndLogic():
    clock = pygame.time.Clock()
    m_sec = 0
    fired = []
    items = []
    z = []
    i = 0
    MAXNUM = 1
    isPaused = False
    player = Player((window.SCREEN_WIDTH/2, window.SCREEN_HEIGHT/2)) # Init the player.
    weapons = [AssaultRifle, Handgun, Flamethrower, Sawshot] # List of weapons we want in the game.
    window.set_background("images/field.jpg")
    quitGame = False
    while player.isAlive():
        if len(z) == 0:
            while i < MAXNUM:
                z.append(Zombie((random.randrange(0,window.SCREEN_WIDTH),random.randrange(0,window.SCREEN_HEIGHT))))
                i += 1
            MAXNUM = MAXNUM * 2
            i = 0

        #***********************************************************************
        # Keep stable frame rate.
        m_sec = clock.tick(140)
        fps = round(clock.get_fps())#maybe good idea to make player speed fn of fps
        #***********************************************************************
        
        keys_pressed = pygame.key.get_pressed() # Get the pressed keys for events
        #***********************************************************************
        # Self explanatory
        check_significant_keypresses (keys_pressed, window, player, items, fired, z)
        #***********************************************************************


        



        #***********************************************************************
        # Player movement, weapon carrying and drawing structures placed here.
        lastx = player.x # If player tries to move and collides with an enemy 
        lasty = player.y # revert him back to his previous spot
        player.move(keys_pressed, (window.SCREEN_WIDTH, window.SCREEN_HEIGHT))
        for enemy in z:
            if player.collidesWith(enemy):
                player.x = lastx
                player.y = lasty
        hero_source, hero_destination = player.rotateTowardObject(pygame.mouse.get_pos())
        fired = player.weapon.shoot((window.SCREEN_WIDTH, window.SCREEN_HEIGHT),\
                                    (window.OLD_SCREEN_WIDTH, window.OLD_SCREEN_HEIGHT))
        player.carry()
        w = player.weapon
        #gun_source, gun_destination = w.img, (player.x - player.width/3, player.y - player.height/3)
        gun_source, gun_destination = w.rotateTowardObject(pygame.mouse.get_pos())
        #***********************************************************************


        px = player.x - window.SCREEN_WIDTH/2
        py = player.y - window.SCREEN_HEIGHT/2
        for item in items:
            item.x -= px
            item.y -= py
        for enemy in z:
            enemy.x -= px
            enemy.y -= py
        player.x = window.SCREEN_WIDTH/2
        player.y = window.SCREEN_HEIGHT/2




           
        #***********************************************************************
        # Drawing functionality
        window.draw_background()
        player.healthBar(window.SCREEN, (window.SCREEN_WIDTH, window.SCREEN_HEIGHT))
        player.ammoBar(window.SCREEN, (window.SCREEN_WIDTH, window.SCREEN_HEIGHT))
        

        try:# Make sure there are never more than 20 items on the game board.
            while len(items) > 20:   
                needsRemoved = items[0]
                items.remove(needsRemoved) 
        except Exception as e:
            print str(e) + " Item removal"
            
        try: # Draw dropped items that are on the map
            for item in items:
                item_source, item_destination = item.img, item.getPosition()
                window.draw(item_source, item_destination)
        except Exception as e:
            print str(e) + " Item drawing"
            
        try:
            for enemy in z:
                if not enemy.collidesWith(player):
                    enemy.notAttacking()
                    enemy.move(player.getPosition(), ((-999,-999), (-999,-999)))
                else:
                    player.takeDamage(enemy.attack())
                window.draw(enemy.rotateTowardObject(player))
        except Exception as e:
            print str(e) + " Enemy Drawing"
            
        try: # Draw bullets and check for their collision
            for bullet in fired:
                round_in_bound = bullet.inBounds((window.SCREEN_WIDTH, window.SCREEN_HEIGHT))
                if round_in_bound == True:
                    bullet.move()
                    round_source, round_dest = bullet.handleProjectile()
                    window.draw(round_source, round_dest)
                    for enemy in z:
                        if bullet.isDestroyed:
                            fired.remove(bullet)
                        elif bullet.collidesWith(enemy):
                            enemy.takeDamage(bullet.dmg)
                            if not bullet.isDestroyed:
                                fired.remove(bullet)
                            if enemy.isAlive() == False:
                                dropped = enemy.drop()
                                if not dropped == None:
                                    items.append(dropped)
                                z.remove(enemy)
                            break
                else:
                    fired.remove(bullet)
                player.weapon.activeRounds = fired
        except Exception as e:
            pass #print str(e) + " Bullet drawing and collisions"

        try:  
            window.draw(gun_source, gun_destination) 
            window.draw(hero_source,hero_destination)            
            #window.write(fps, (window.SCREEN_WIDTH - 40, window.SCREEN_HEIGHT - 8), (0, 0, 255), 1)
            #window.write(str(player.weapon.currClip) + "/" + str(player.weapon.ammo),\
            #             (window.SCREEN_WIDTH - 40, window.SCREEN_HEIGHT - 16), (255, 0, 255), 1)
            #window.write(player.health, (player.x, player.y - 35), (255,  0, 0), 0)
            window.draw(mouse_c, setupCrossHairCursor().center)
        except Exception as e:
            pass
        
        window.update()
#************************************************************************

#*********************************Main Menu Function***************************************
def mainMenu():
    state = 0
    prev_state = 1
    rect_list = []
    continueGame = True
    image1 = load_image('ammobelt.jpg', 'images')
    mainMenu = cMenu(50,50, 10,10, 'vertical', 10, window.SCREEN,
                 [('Play Game',         1, image1, (250,40)),
                  ('Leaderboards',      2, image1, (250,40)),
                  ('Options',           3, image1, (250,40)),
                  ('Exit',              4, image1, (250,40))])    
    pygame.key.set_repeat(0, 0)
    window.set_background("images/field.jpg")
    window.draw_background()
    while continueGame:
        if prev_state != state:        
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state

        l = pygame.event.wait()
        k = pygame.key.get_pressed()
        if k[pygame.K_DOWN] == 1 or k[pygame.K_UP] == 1 or \
           l.type == EVENT_CHANGE_STATE or k[pygame.K_RETURN] == 1:
            if state == 0: 
                rect_list, state = mainMenu.update(l, state)
            if state == 1:                
                pygame.key.set_repeat(1, 1)
                gameAndLogic()
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))       
                pygame.key.set_repeat(0, 0)
                window.set_background("images/field.jpg")
                window.draw_background()
                #print "Exited Game"
                state = 0
            elif state == 2:                
                pass
                state = 0
            elif state == 3:
                optionsMenu()
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                state = 0
            elif state == 4:                    
                pygame.quit()
                exit()
                
        if l.type == QUIT:
            pygame.quit()
            exit()                 
        window.update()

#*********************************Main Menu Function***************************************
def pauseMenu():
    state = 0
    prev_state = 1
    rect_list = []
    paused = True
    image1 = load_image('ammobelt.jpg', 'images')
    pauseMenu = cMenu(50,50, 10,10, 'vertical', 10, window.SCREEN,
                 [('Resume',         1, image1, (250,40)),
                  ('Options',        2, image1, (250,40)),
                  ('Fullscreen',     3, image1, (250,40)),
                  ('Quit Game',      4, image1, (250,40)),
                  ('Exit Game',      5, image1, (250,40))])
        
    pygame.key.set_repeat(0, 0)
    window.set_background((0,255,0))
    window.draw_background()
    while paused:
        if prev_state != state:        
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state

        l = pygame.event.wait()
        k = pygame.key.get_pressed()
        if k[pygame.K_DOWN] == 1 or k[pygame.K_UP] == 1 or \
           l.type == EVENT_CHANGE_STATE or k[pygame.K_RETURN] == 1:
            if state == 0:
                rect_list, state = pauseMenu.update(l, state)
            if state == 1:                
                paused = False
                state = 0
            elif state == 2:
                optionsMenu()
                pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
                state = 0
            elif state == 3:
                if not window.isFullScreened:
                    window.full_screen()
                else:                    
                    window.exit_full_screen(800,600)
                state = 0
            elif state == 4:
                state = 0
            elif state == 5:                    
                pygame.quit()
                exit()
                
        if l.type == QUIT:
            pygame.quit()
            exit()
            
        window.update()
    pygame.key.set_repeat(1, 1)

#*********************************Main Menu Function***************************************
def optionsMenu():
    state = 0
    prev_state = 1
    rect_list = []
    exitOptions = True
    image1 = load_image('ammobelt.jpg', 'images')
    optionsMenu = cMenu(50,50, 10,10, 'vertical', 10, window.SCREEN,
                 [('Controls',          1, image1, (250,40)),
                  ('New Setting',       2, image1, (250,40)),
                  ('Back',              3, image1, (250,40))])
        
    window.draw_background()
    while exitOptions:
        if prev_state != state:
            window.draw_background()        
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state

        l = pygame.event.wait()
        k = pygame.key.get_pressed()
        if k[pygame.K_DOWN] == 1 or k[pygame.K_UP] == 1 or \
           l.type == EVENT_CHANGE_STATE or k[pygame.K_RETURN] == 1:
            if state == 0:
                rect_list, state = optionsMenu.update(l, state)
            if state == 1:
                pass
                state = 0
            elif state == 2:
                pass
                state = 0
            elif state == 3:
                exitOptions = False
                
        if l.type == QUIT:
            pygame.quit()
            exit()
            
        window.update()
    
def main(args):
    mainMenu()
main(None)


