from calendar import c
import imghdr
import wave
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


# LASER Class
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
    
# SPACESHIP Class
class Spaceship:
    COOL_DOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            if laser.collision(obj):
                obj.health -= 20
                self.lasers.remove(laser)
        
    def cooldown(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0 
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter==0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.img.get_width()
    
    def get_height(self):
        return self.img.get_height()


# PLAYER class inherited from SPACESHIP class
class Player(Spaceship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.img = RED_SPACESHIP
        self.laser_img = RED_LASER
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health
    
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width() * (self.health/self.max_health), 10))


# ENEMY class inherited from SPACESHIP class
class Enemy(Spaceship):
    COLOR_MAP = {
        "orange": ORANGE_SPACESHIP,
        "green": GREEN_SPACESHIP,
        "blue": BLUE_SPACESHIP,
        "purple": PURPLE_SPACESHIP
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.img, self.laser_img = self.COLOR_MAP[color], YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.img)
    
    def move(self, vel):
        self.y += vel
    
    def shoot(self):
        if self.cool_down_counter==0:
            laser = Laser(self.x - self.img.get_width()//2, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
        

# Collide class: returns the coordinates of the overlapping part if the both objects overlaps 
# with each other otherwise returns None
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def game():
    run = True
    FPS = 60
    score = 0
    lives = 5
    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    player = Player(600, 600)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(SPACE_IMG, (0,0))

        lives_text = main_font.render(f"Lives: {lives}", 1, WHITE)
        score_text = main_font.render(f"Lives: {score}", 1, WHITE)

        WIN.blit(HEART_IMG, (40, 35))
        WIN.blit(lives_text, (40 + HEART_IMG.get_width() + 20, 25))
        WIN.blit(score_text, (WIDTH-score_text.get_width()-40, 35))

        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render(f"Your SCORE: {score}", 2, YELLOW)
            WIN.blit(lost_label, (WIDTH//2 - lost_label.get_width()//2, HEIGHT//2 - lost_label.get_height()//2))
        
        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives<=0 or player.health==0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        
        if len(enemies)==0:
            wave_length += 5
            for _ in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-50), random.randrange(-1500, -100), random.choice(["orange", "blue", "green", "purple"]))
                enemies.append(enemy)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
        
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - player_vel > 0:
            player.x -= player_vel
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(2 * 60)==1:
                enemy.shoot()
            
            if collide(enemy, player):
                player.health -= 20
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        
        player.move_lasers(-laser_vel, enemies)

def main():
    title_font = pygame.font.SysFont('comicsans', 50)
    run = True
    while run:
        WIN.blit(SPACE_IMG, (0,0))
        title_text = title_font.render("Press the mouse button to continue.. ", 1, WHITE)
        WIN.blit(title_text,(WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - title_text.get_height()//2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
            if event.type==pygame.MOUSEBUTTONDOWN:
                game()
    pygame.quit()


if __name__=="__main__":
    main()