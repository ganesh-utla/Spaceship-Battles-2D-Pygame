from ctypes.wintypes import HDESK
import pygame
import os

CWD = os.getcwd()

WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Spaceship Battles⚔️")
pygame_icon = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'red_spaceship.png'))
pygame.display.set_icon(pygame_icon)

def start_game():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False

    pygame.quit()

if __name__=="__main__":
    start_game()
