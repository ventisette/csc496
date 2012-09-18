import screen
import thread
import time
import character
import pygame
pygame.init()#Need to work this out, main should not need to know about pygame.
             

window = screen.Window(800, 800, "Enter Window Title Here", (255,255,255))
window.set_font("jfdfahjdfjkalkdfjk", 12)

player = character.hero(32, 32, 50, 50, window.SCREEN_WIDTH/2, window.SCREEN_HEIGHT/2, (255, 0, 0))
# EX2 :: player.set_IMG((255, 0, 0))
pygame.key.set_repeat(1, 1)

def main(args):
    while True:
        keys_pressed = pygame.key.get_pressed()
        # EX2 :: r = player.IMG.get_rect()
        # EX2 :: r.center = player.move(keys_pressed, (window.SCREEN_WIDTH, window.SCREEN_HEIGHT))
        # EX2 :: hero_source, hero_destination = player.IMG, r
        
        player.move(keys_pressed, (window.SCREEN_WIDTH, window.SCREEN_HEIGHT))
        hero_source, hero_destination = player.rotate_towards_cursor()
        
        window.draw_background()
        try:
            window.draw(hero_source, hero_destination)
            window.write("Window Template", (window.SCREEN_WIDTH - 40, window.SCREEN_HEIGHT - 8), (0, 0, 255))
            window.write("Window Template", (window.SCREEN_WIDTH - 40, window.SCREEN_HEIGHT - 16), (255, 0, 255))
            window.write(player.HEALTH, (player.X, player.Y - 35), (255, 0, 0), 100)
        except Exception as e:
            pass
        window.check_quit_event()
        window.update()

main(None)
