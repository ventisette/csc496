import screen
import thread
import time
import character
import pygame
import sys
import math
import random
import os
from wpn import *
from pygame.locals import *

pygame.init()#Need to work this out, main should not need to know about pygame.

window = screen.Window(800, 600, "TeamProject 496", "images/field.jpg") # Create game window.
#window.set_font(((12, None), (24, None))) <- Another example of the two statements below
window.set_font(12, None) # index 0
window.set_font(24, None) # index 1
player = Player((window.SCREEN_WIDTH/2, window.SCREEN_HEIGHT/2)) # Init the player.
pygame.key.set_repeat(1, 1) 

weapons = [AssaultRifle, Handgun, Flamethrower, Sawshot] # List of weapons we want in the game.

def check_significant_keypresses(keys_pressed, window, player, items, fired, enemies):
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            pygame.quit()
        if keys_pressed[114] == 1:
            player.weapon.reloadWeapon()
        elif keys_pressed[102] == 1:
            for item in items:
                if player.collidesWith(item):
                    items.remove(item)
                    pickedUp = player.pickUp(item)
                    if not pickedUp == None:
                        items.extend([pickedUp])
        elif keys_pressed[118] == 1:
            window.full_screen()
        elif keys_pressed[98] == 1:
            window.exit_full_screen(800,600)
            
"""
gets current position of the mouse
sets the mouse image position, the cursor is set to the center of theimage
copies the mouse image created earlier to the screen
"""
def setup_cursor():    
    X, Y = pygame.mouse.get_pos()    
    mouse_block = mouse_c.get_rect()
    mouse_block.center = (X - mouse_block[2]/2, Y - mouse_block[3]/2)
    X -= mouse_c.get_width()
    Y -= mouse_c.get_height()
    return mouse_block

def main(args):
    clock = pygame.time.Clock()
    m_sec = 0
    fired = []
    items = []
    z = []
    i = 0
    MAXNUM = 1
    isPaused = False
    while True:
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
        check_significant_keypresses(keys_pressed, window, player, items, fired, z)
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
                    player.weapon.activeRounds.remove(bullet)   
        except Exception as e:
            print str(e) + " Bullet drawing and collisions"

        try:  
            window.draw(gun_source, gun_destination) 
            window.draw(hero_source,hero_destination)            
            window.write(fps, (window.SCREEN_WIDTH - 40, window.SCREEN_HEIGHT - 8), (0, 0, 255), 1)
            window.write(str(player.weapon.currClip) + "/" + str(player.weapon.ammo),\
                         (window.SCREEN_WIDTH - 40, window.SCREEN_HEIGHT - 16), (255, 0, 255), 1)
            window.write(player.health, (player.x, player.y - 35), (255,  0, 0), 0)
        except Exception as e:
            pass
        
        window.update()
        #************************************************************************

main(None)
