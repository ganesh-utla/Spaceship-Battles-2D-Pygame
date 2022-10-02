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
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),0)
GREEN_SPACESHIP_IMAGE = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'green_spaceship.png'))
GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),180)
SPACE_IMG = pygame.transform.scale(pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'space.jpg')), (WIDTH, HEIGHT))
SPACESHIP_VEL = 5
BORDER = pygame.Rect(0, HEIGHT-300, WIDTH, 10)


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x-SPACESHIP_VEL > 0:
        red.x -= SPACESHIP_VEL
    if keys_pressed[pygame.K_d] and red.x+SPACESHIP_VEL+SPACESHIP_WIDTH < WIDTH:
        red.x += SPACESHIP_VEL
    if keys_pressed[pygame.K_w] and red.y-SPACESHIP_VEL > BORDER.y+SPACESHIP_HEIGHT:
        red.y -= SPACESHIP_VEL
    if keys_pressed[pygame.K_s] and red.y+SPACESHIP_VEL+SPACESHIP_HEIGHT < HEIGHT:
        red.y += SPACESHIP_VEL

def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_LEFT] and green.x-SPACESHIP_VEL > 0:
        green.x -= SPACESHIP_VEL
    if keys_pressed[pygame.K_RIGHT] and green.x+SPACESHIP_VEL+SPACESHIP_WIDTH < WIDTH:
        green.x += SPACESHIP_VEL
    if keys_pressed[pygame.K_UP] and green.y-SPACESHIP_VEL > 0:
        green.y -= SPACESHIP_VEL
    if keys_pressed[pygame.K_DOWN] and green.y+SPACESHIP_VEL+SPACESHIP_HEIGHT < BORDER.y:
        green.y += SPACESHIP_VEL


def display_window(red, green):
    # WIN.fill(WHITE)
    WIN.blit(SPACE_IMG, (0,0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))
    pygame.display.update()


def start_game():
    red = pygame.Rect(WIDTH//2-SPACESHIP_WIDTH//2, HEIGHT-100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    green = pygame.Rect(WIDTH//2-SPACESHIP_WIDTH//2, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
        

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        green_handle_movement(keys_pressed, green)
        
        
        
        display_window(red, green)

    pygame.quit()

if __name__=="__main__":
    start_game()
