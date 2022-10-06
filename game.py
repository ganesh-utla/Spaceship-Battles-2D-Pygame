import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

# Current Working Directory
CWD = os.getcwd()

# Screen Width and Height
WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# COLORS
WHITE = (255,255,255)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)

# FONTS
FONT = pygame.font.SysFont('comicsans', 40)

# WINDOW CAPTION and ICON
pygame.display.set_caption("Spaceship Battles⚔️")
pygame_icon = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'red_spaceship.png'))
pygame.display.set_icon(pygame_icon)

# FPS
FPS = 60

# width and height of PLAYER and ENEMY
PLAYER_WIDTH, PLAYER_HEIGHT = 55, 70
ENEMY_WIDTH, ENEMY_HEIGHT = 45, 60

# IMAGES
SPACE_IMG = pygame.transform.scale(pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'space.jpg')), (WIDTH, HEIGHT))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'red_spaceship.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)),0)
GREEN_SPACESHIP_IMAGE = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'green_spaceship.png'))
GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_SPACESHIP_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT)),180)
ORANGE_SPACESHIP_IMAGE = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'orange_spaceship.png'))
ORANGE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(ORANGE_SPACESHIP_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT)),180)
BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'blue_spaceship.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT)),180)
PURPLE_SPACESHIP_IMAGE = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'purple_spaceship.png'))
PURPLE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(PURPLE_SPACESHIP_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT)),180)
HEART_IMG = pygame.transform.scale(pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'heart.png')), (40, 40))
RED_LASER = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'pixel_laser_red.png'))
YELLOW_LASER = pygame.image.load(os.path.join(CWD, 'Assets', 'img', 'pixel_laser_yellow.png'))

# SOUNDS
BULLET_SOUND = pygame.mixer.Sound(os.path.join(CWD, 'Assets', 'sound', 'lazer.mp3'))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join(CWD, 'Assets', 'sound', 'explosion.ogg'))


# LASER class

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return (self.y < 0 and self.y > height)
    
    def collision(self, obj):
        return collide(self, obj)
    

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None