import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

ship_img = pygame.image.load("spaceship.png")  
asteroid_img = pygame.image.load("asteroid.png") 
crystal_img = pygame.image.load("energy_crystal.png")  
bg_music = pygame.mixer.Sound("background_music.wav") 
crash_sound = pygame.mixer.Sound("clash_sound.wav")  
collect_sound = pygame.mixer.Sound("collect_sound.mp3")
background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
opacity = 110

background_img.set_alpha(opacity)

pygame.mixer.music.load("background_music.wav")
pygame.mixer.music.play(-1)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(ship_img, (60, 80))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.mask = pygame.mask.from_surface(self.image)  
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, game_time):
        super().__init__()
        self.size = random.randint(60, 100)
        self.image = pygame.transform.scale(asteroid_img, (self.size, self.size))
        self.image = pygame.transform.rotate(self.image, 50)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), -50))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = random.randint(3, 5) + game_time // 8

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Crystal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(crystal_img, (40, 40))
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), -50))
        self.mask = pygame.mask.from_surface(self.image)  
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
def game_over_screen(score, time_elapsed):
    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 48)
        text = font.render("Game Over", True, RED)
        score_text = font.render(f"Score: {score}", True, WHITE)
        time_text = font.render(f"Time: {int(time_elapsed)}s", True, WHITE)
        retry_text = font.render("Press R to Retry", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 250))
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 300))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

        pygame.display.flip()


player = Player()
player_group = pygame.sprite.GroupSingle(player)
asteroids = pygame.sprite.Group()
crystals = pygame.sprite.Group()

lives = 3
game_time = 0
score = 0
running = True


while running:
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))

  
    if random.randint(1, 50) <= 2:
        asteroids.add(Asteroid(game_time))
    if random.randint(1, 100) == 1:
        crystals.add(Crystal())

  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    keys = pygame.key.get_pressed()
    player_group.update(keys)

    
    asteroids.update()
    crystals.update()

    if pygame.sprite.spritecollide(player, asteroids, True, pygame.sprite.collide_mask):
            pygame.mixer.Sound.play(crash_sound)
            lives -= 1
            if lives == 0:
                game_over_screen(score, game_time)
                score = 0
                game_time = 0
                lives = 3
                player.rect.center = (WIDTH // 2, HEIGHT - 100)
                asteroids.empty()
                crystals.empty()

    if pygame.sprite.spritecollide(player, crystals, True, pygame.sprite.collide_mask):
            pygame.mixer.Sound.play(collect_sound)
            score += 1
            if score % 10 == 0:
                lives += 1


    player_group.draw(screen)
    asteroids.draw(screen)
    crystals.draw(screen)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    timer_text = font.render(f"Time: {int(game_time)}s", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(timer_text, (10, 90))


    game_time += 1 / 60  

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

