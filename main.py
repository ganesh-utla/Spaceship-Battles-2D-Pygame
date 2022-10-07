
#              xxxxx                 SPACESHIP BATTLES 2D                 xxxxx

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
RED = (255, 0, 0)
GREEN = (0, 255, 0)

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

# You can add your images and sound according to you!

# IMAGES
# Scaling and rotating the image by our desires
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
# NOTE: The below sounds may not be work at your end. Set your own sound effects if it not works!

PLAYER_SHOT = pygame.mixer.Sound(os.path.join(CWD, 'Assets', 'sound', 'lazer.mp3'))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join(CWD, 'Assets', 'sound', 'explosion.ogg'))
ENEMY_SHOT = pygame.mixer.Sound(os.path.join(CWD, 'Assets', 'sound', 'player_shot.mp3'))
# ENEMY_SHOT = pygame.mixer.Sound(os.path.join(CWD, 'Assets', 'sound', 'enemy_shot.mp3'))
# OPENING = pygame.mixer.Sound(os.path.join(CWD, 'Assets', 'sound', 'opening.mp3'))

# NOTE: sound_variables.play() - used for the play the sound
# NOTE: sound_variables.stop() - used for the stop the sound
# NOTE: sound_variables.pause() - used for the pause the sound
# NOTE: sound_variables.unpause() - used for the resume the sound
# I've used play() and stop() functions in the below code. 
# So don't need worry about that and I hope that you understood the above functions 


# LASER Class
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        # masking the image: hiding or revealing the parts(pixels) of the image
        self.mask = pygame.mask.from_surface(self.img) 
    
    # draws the laser on given coordinates
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    # moves the laser by given velocity
    def move(self, vel):
        self.y += vel
    
    # returns True if laser is out of the screen otherwise return False
    def off_screen(self, height):
        return (self.y < 0 and self.y > height)
    
    # returns True if laser is collided with given object otherwise returns False
    def collision(self, obj):
        return collide(self, obj)
    
# SPACESHIP Class
class Spaceship:
    COOL_DOWN = 30 # It is used for controlling the shooting of no. of lasers at one time 
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        # setting the health for the player(YOU)
        self.health = health
        # Img of the spaceship
        self.img = None
        # Laser image of the spaceship
        self.laser_img = None
        # No. of lasers of the spaceship
        self.lasers = []
        self.cool_down_counter = 0

    # Draws all the lasers shooted by the spacehip
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # Moves all the lasers by given velocity and 
    # removes the lasers if it is gone out of the screen or collided with any obj (spaceship)
    # health of the player is decreased if the laser is collided with player's spaceship
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            if laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    
    # resets or sets the cool down counter
    # i.e. maintains the time gap(COOL_DOWN no. of pixels) between the laser shoots
    def cooldown(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0 
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # Shoots the laser if and only if cool down counter is zero
    def shoot(self):
        if self.cool_down_counter==0:
            laser = Laser(self.x-26, self.y, self.laser_img)
            PLAYER_SHOT.play()
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # returns the width of the spaceship
    def get_width(self):
        return self.img.get_width()
    
    # returns the height of the spaceship
    def get_height(self):
        return self.img.get_height()


# PLAYER class inherited from SPACESHIP class
class Player(Spaceship):
    # Attributes and functions same as the Spaceship class but with some changes
    def __init__(self, x, y, score=0, health=100):
        super().__init__(x, y, health)
        self.img = RED_SPACESHIP
        self.laser_img = RED_LASER
        self.mask = pygame.mask.from_surface(self.img)
        self.max_health = health
        self.score = score
    
    # This function is same as the the function with same name in the Spaceship class
    # But in the Spaceship class, we checked for the particular object (Player spaceship)
    # Now, we are checking for the many objects (Enemy spaceships)
    def move_lasers(self, vel, objs):
        self.cooldown()
        # Checking that player's laser is out of the screen or not
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                # Checking that player's laser is collided with any of the enemies or not
                for obj in objs:
                    if laser.collision(obj):
                        EXPLOSION_SOUND.play()
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            self.score += 5
    
    # Draws the lasers shooted by the player as well as draws the healthbar
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    # Health bar is added to display the health status of the player
    def healthbar(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y + self.img.get_height() + 10, self.img.get_width(), 10))
        pygame.draw.rect(window, GREEN, (self.x, self.y + self.img.get_height() + 10, self.img.get_width() * (self.health/self.max_health), 10))


# ENEMY class inherited from SPACESHIP class
class Enemy(Spaceship):
    # Mapping the colors of the Enemy spaceships with their images for further use
    COLOR_MAP = {
        "orange": ORANGE_SPACESHIP,
        "green": GREEN_SPACESHIP,
        "blue": BLUE_SPACESHIP,
        "purple": PURPLE_SPACESHIP
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        # Now, using the color map for getting the image of the particular Enemy spaceship
        self.img, self.laser_img = self.COLOR_MAP[color], YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.img)
    
    # Moves the spaceship by given velocity
    def move(self, vel):
        self.y += vel
    
    # Shoots the laser of the Enemy spaceship at given coordinates if and only if cool down counter is zero
    def shoot(self):
        if self.cool_down_counter==0:
            laser = Laser(self.x - 24, self.y, self.laser_img)
            ENEMY_SHOT.play()
            self.lasers.append(laser)
            self.cool_down_counter = 1
        

# Collide class: returns the coordinates of the overlapping part(pixels) if the both objects overlaps 
# with each other otherwise returns None
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # Now masking is used for getting the pixels of the image that exists
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


mx_score = -1

# Our main function to run the game
def game():
    run = True
    # setting the FPS of our clock
    FPS = 60
    # setting the lives for our player
    lives = 5

    # This font is used for displaying lives, health and score 
    main_font = pygame.font.SysFont('comicsans', 50)

    # This font is used for displaying the total score at the end or after the player runs out of lives or health
    lost_font = pygame.font.SysFont('comicsans', 60)

    # Setting the enemies list for storing the enemies
    enemies = []

    # Wave length is using for the setting the no. of enemies or 
    # you can say as levels (For level 1 - 5 enemies, level 2 - 10 enemies)
    wave_length = 5

    # Velocity of the enemy spaceships
    enemy_vel = 1

    # Velocity of the player spaceship
    player_vel = 5
    
    # Velocity of the Laser
    laser_vel = 5

    # Creating the instance player spaceship at the random coordinates
    player = Player(600, 600)

    # Using the clock for setting FPS
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0 # storing the count of the loses or no. of the games played by the user

    def redraw_window():
        # setting the Space background
        WIN.blit(SPACE_IMG, (0,0))

        # labels for the lives, health and score
        lives_text = main_font.render(f"Lives: {lives}", 1, WHITE)
        health_text = main_font.render(f"Health: {player.health}", 1, WHITE)
        score_text = main_font.render(f"Score: {player.score}", 1, WHITE)

        # Now displaying the labels of the lives with heart image, health and score
        WIN.blit(HEART_IMG, (40, 35))
        WIN.blit(lives_text, (40 + HEART_IMG.get_width() + 20, 25))
        WIN.blit(health_text, (WIDTH//2 - health_text.get_width()//2, 25))
        WIN.blit(score_text, (WIDTH-score_text.get_width()-40, 35))

        # Drawing all the enemy spaceships in the enemies list
        for enemy in enemies:
            enemy.draw(WIN)
        
        # Drawing the player's spaceship
        player.draw(WIN)
        
        # Displaying the score label as well as the high score label till now, if the player runs out of lives or health
        if lost:
            global mx_score
            mx_score = max(mx_score, player.score)
            lost_label = lost_font.render(f"Your SCORE: {player.score}", 2, YELLOW)
            mx_score_label = lost_font.render(f"MAX SCORE: {mx_score}", 2, YELLOW)
            WIN.blit(lost_label, (WIDTH//2 - lost_label.get_width()//2, HEIGHT//2 - lost_label.get_height()//2))
            WIN.blit(mx_score_label, (WIDTH//2 - lost_label.get_width()//2, HEIGHT//2 + lost_label.get_height()))
        
        # Updating the display at the end
        pygame.display.update()
    
    while run:
        # setted the FPS 
        clock.tick(FPS)

        # called the above function 
        redraw_window()

        # increases the lost count by 1 if the player runs out of lives or health
        if lives<=0 or player.health==0:
            # OPENING.play()
            lost = True
            lost_count += 1
        
        # You can give whatever condition you like for the setting max number of times the user can play the game
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        
        # Enemy spaceships are increased if the enemies for the particular wavelength are done
        if len(enemies)==0:
            wave_length += 5
            # Creating wavelength no. of instances of the enemy spaceship 
            for _ in range(wave_length):
                # Using the random module for the setting eange of the x,y coordinates of the enemy spaceship with random color
                enemy = Enemy(random.randrange(50, WIDTH-50), random.randrange(-1500, -100), random.choice(["orange", "blue", "green", "purple"]))
                enemies.append(enemy)
        
        for event in pygame.event.get():
            # Game can be closed at any time using close/quit button 
            if event.type==pygame.QUIT:
                quit()
        
        # Controlling Player handle movements
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x - player_vel > 0: # LEFT
            player.x -= player_vel
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + player_vel + player.get_height() + 15 < HEIGHT: # DOWN
            player.y += player_vel
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_vel + player.get_width() < WIDTH: # RIGHT
            player.x += player_vel
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y - player_vel > 0: # UP
            player.y -= player_vel
        if keys[pygame.K_SPACE]: # SHOOT
            player.shoot()
        
        # Moving the enemy spaceships in the enemies list as well as moving its lasers 
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            # shoots when given condition satisfies: (setting the some probability to shoot) 
            if random.randrange(4 * 60)==1:
                enemy.shoot()
            
            # Checking that any collsion occuerd with player or not 
            if collide(enemy, player):
                EXPLOSION_SOUND.play()
                player.health -= 10
                enemies.remove(enemy)
            
            # Checking that enemy spaceship is out of the screen or not
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
            EXPLOSION_SOUND.stop()
        
        # Moving the lasers of the player
        player.move_lasers(-laser_vel, enemies)


# This the function to start the game
def main():
    # Labels for the Title and the description
    press_font = pygame.font.SysFont('comicsans', 30)
    title_font = pygame.font.SysFont('comicSans', 50)

    run = True

    while run:
        # Setting Space background
        WIN.blit(SPACE_IMG, (0,0))

        # Now displaying the labels of the title and description
        title_text = title_font.render(f"X SPACESHIP BATTLES!! X", 1, WHITE)
        press_text = press_font.render(f"Press the mouse button to continue..", 1, WHITE)
        # OPENING.play()

        WIN.blit(title_text,(WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - title_text.get_height()//2))
        WIN.blit(press_text,(WIDTH//2 - title_text.get_width()//2, HEIGHT//2 + title_text.get_height()))

        # Upating the display
        pygame.display.update()

        for event in pygame.event.get():
            # Game can be closed/quit using close button
            if event.type==pygame.QUIT:
                run = False
            # Game starts only when user clicks the mouse down button
            if event.type==pygame.MOUSEBUTTONDOWN:
                # OPENING.stop()
                game() # calling the function to run the game
    
    # Quits the game if user closes the game
    pygame.quit()


if __name__=="__main__":
    main() # calling the function to start the game


    #               xxxxx           THANK YOU!! Hope you liked it!          xxxxx