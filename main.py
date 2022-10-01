from ctypes.wintypes import HDESK
import pygame
import os

CWD = os.getcwd()
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255,255,255)

pygame.display.set_caption("Spaceship Battles⚔️")
pygame_icon = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'red_spaceship.png'))
pygame.display.set_icon(pygame_icon)

FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 70
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'red_spaceship.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
GREEN_SPACESHIP_IMAGE = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'green_spaceship.png'))
GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
SPACE_IMG = pygame.transform.scale(pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'space.jpg')), (WIDTH, HEIGHT))




def display_window(red, green):
    # WIN.fill(WHITE)
    WIN.blit(SPACE_IMG, (0,0))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))
    pygame.display.update()


def start_game():
    red = pygame.Rect(100, HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    green = pygame.Rect(WIDTH-100-SPACESHIP_WIDTH, HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
        
        # red.x += 5
        display_window(red, green)

    pygame.quit()

if __name__=="__main__":
    start_game()
