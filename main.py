from ctypes.wintypes import HDESK
from tkinter.tix import MAX
import pygame
import os

CWD = os.getcwd()
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255,255,255)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)

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
# BORDER = pygame.Rect(0, HEIGHT-300, WIDTH, 10)
BORDER = pygame.Surface((WIDTH, 10))
BORDER.set_alpha(0)
BORDER_x, BORDER_y = 0, HEIGHT-300
BULLET_VEL = 7
MAX_BULLETS = 3
RED_HIT = pygame.USEREVENT + 1
GREEN_HIT = pygame.USEREVENT + 2


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x-SPACESHIP_VEL > 0:
        red.x -= SPACESHIP_VEL
    if keys_pressed[pygame.K_d] and red.x+SPACESHIP_VEL+SPACESHIP_WIDTH < WIDTH:
        red.x += SPACESHIP_VEL
    if keys_pressed[pygame.K_w] and red.y-SPACESHIP_VEL-SPACESHIP_HEIGHT > BORDER_y:
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
    if keys_pressed[pygame.K_DOWN] and green.y+SPACESHIP_VEL+SPACESHIP_HEIGHT < BORDER_y:
        green.y += SPACESHIP_VEL

def handle_bullets(red_bullets, green_bullets, red, green):
    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            red_bullets.remove(bullet)

    for bullet in green_bullets:
        bullet.y += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            green_bullets.remove(bullet)



def display_window(red, green, red_bullets, green_bullets):
    # WIN.fill(WHITE)
    WIN.blit(SPACE_IMG, (0,0))
    WIN.blit(BORDER, (BORDER_x, BORDER_y))
    # pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, ORANGE, bullet)

    for bullet in green_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def start_game():
    red = pygame.Rect(WIDTH//2-SPACESHIP_WIDTH//2, HEIGHT-100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    green = pygame.Rect(WIDTH//2-SPACESHIP_WIDTH//2, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    green_bullets = []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x+red.width//2+1, red.y, 5, 7)
                    red_bullets.append(bullet)

                if event.key==pygame.K_RCTRL and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x+green.width//2+1, green.y+green.height, 5, 7)
                    green_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        green_handle_movement(keys_pressed, green)
        handle_bullets(red_bullets, green_bullets, red, green)
        display_window(red, green, red_bullets, green_bullets)

    pygame.quit()

if __name__=="__main__":
    start_game()
