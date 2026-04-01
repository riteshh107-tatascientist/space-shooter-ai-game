import pygame
import os
import random
import time
import csv

pygame.init()

# 🔊 SOUND SETUP (SAFE)
try:
    pygame.mixer.init()
    pygame.mixer.set_num_channels(20)
    laser_sound = pygame.mixer.Sound("assets/laser.wav")
    laser_sound.set_volume(0.7)
except:
    laser_sound = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# WINDOW
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Shooter PRO MAX")

# LOAD IMAGES
def load_img(name):
    return pygame.image.load(os.path.join(BASE_DIR, "assets", name))

RED = load_img("pixel_ship_red_small.png")
GREEN = load_img("pixel_ship_green_small.png")
BLUE = load_img("pixel_ship_blue_small.png")
YELLOW = load_img("pixel_ship_yellow.png")

RED_LASER = load_img("pixel_laser_red.png")
GREEN_LASER = load_img("pixel_laser_green.png")
BLUE_LASER = load_img("pixel_laser_blue.png")
YELLOW_LASER = load_img("pixel_laser_yellow.png")

BG = pygame.transform.scale(load_img("background-black.png"), (WIDTH, HEIGHT))

# COLORS
WHITE = (255,255,255)
YELLOW_COLOR = (255,255,0)
CYAN = (0,255,255)
RED_COLOR = (255,0,0)
GREEN_COLOR = (0,255,0)
EXPLOSION = (255,120,0)

# LASER
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self):
        return not (0 <= self.y <= HEIGHT)

    def collision(self, obj):
        return obj.mask.overlap(self.mask, (self.x - obj.x, self.y - obj.y)) != None


# SHIP
class Ship:
    COOLDOWN = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, win):
        win.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(win)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            if laser_sound:
                laser_sound.play()

    def move_lasers(self, vel, enemies):
        self.cooldown()
        for laser in self.lasers[:]:
            laser.move(vel)

            if laser.off_screen():
                self.lasers.remove(laser)

            for enemy in enemies[:]:
                if laser.collision(enemy):
                    enemies.remove(enemy)
                    if laser in self.lasers:
                        self.lasers.remove(laser)
                    return True
        return False


# PLAYER
class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img = YELLOW
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)

    def draw(self, win):
        super().draw(win)
        self.healthbar(win)

    def healthbar(self, win):
        pygame.draw.rect(win, RED_COLOR,
                         (self.x, self.y + self.ship_img.get_height() + 10,
                          self.ship_img.get_width(), 10))
        pygame.draw.rect(win, GREEN_COLOR,
                         (self.x, self.y + self.ship_img.get_height() + 10,
                          self.ship_img.get_width() * (self.health/100), 10))


# ENEMY
class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED, RED_LASER),
        "green": (GREEN, GREEN_LASER),
        "blue": (BLUE, BLUE_LASER)
    }

    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    return obj1.mask.overlap(obj2.mask, (obj2.x - obj1.x, obj2.y - obj1.y)) != None


# MAIN GAME
def main():
    clock = pygame.time.Clock()
    run = True

    level = 0
    lives = 5
    score = 0
    paused = False
    lost = False

    font = pygame.font.SysFont("comicsans", 40)
    big_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    player = Player(300, 630)

    # CSV
    file = open("game_data.csv", "a", newline="")
    writer = csv.writer(file)
    if os.stat("game_data.csv").st_size == 0:
        writer.writerow(["score","level","lives","time"])

    while run:
        clock.tick(60)
        WIN.blit(BG, (0,0))

        # UI
        WIN.blit(font.render(f"Lives: {lives}",1,WHITE),(10,10))
        WIN.blit(font.render(f"Level: {level}",1,CYAN),(WIDTH-200,10))
        WIN.blit(font.render(f"Score: {score}",1,YELLOW_COLOR),(WIDTH//2-80,10))

        # Spawn
        if len(enemies) == 0:
            level += 1
            for i in range(5 + level):
                enemies.append(Enemy(random.randrange(50,WIDTH-100),
                                     random.randrange(-1500,-100),
                                     random.choice(["red","green","blue"])))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r and lost:
                    main()

        if paused:
            WIN.blit(big_font.render("PAUSED",1,WHITE),(WIDTH//2-100,350))
            pygame.display.update()
            continue

        if lives <= 0 or player.health <= 0:
            if not lost:
                writer.writerow([score,level,lives,time.time()])
                file.close()
            lost = True
            WIN.blit(big_font.render("GAME OVER",1,RED_COLOR),(WIDTH//2-150,300))
            WIN.blit(font.render("Press R to Restart",1,WHITE),(WIDTH//2-150,380))
            pygame.display.update()
            continue

        keys = pygame.key.get_pressed()

        # MOVEMENT
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player.ship_img.get_width():
            player.x += 5
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= 5
        if keys[pygame.K_DOWN] and player.y < HEIGHT - player.ship_img.get_height():
            player.y += 5

        if keys[pygame.K_SPACE]:
            player.shoot()

        # ENEMY LOGIC
        for enemy in enemies[:]:
            enemy.move(2)
            enemy.draw(WIN)

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # LASERS
        hit = player.move_lasers(-5, enemies)
        if hit:
            score += 10

        player.draw(WIN)

        pygame.display.update()

    pygame.quit()


# MENU
def main_menu():
    run = True
    font = pygame.font.SysFont("comicsans", 60)

    while run:
        WIN.blit(BG, (0,0))
        WIN.blit(font.render("Click to Start",1,WHITE),(WIDTH//2-180,350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()


main_menu()