import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
background = pygame.image.load("background.jpg")

mixer.music.load('background_music.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

img_player = pygame.image.load("rocket.png")
player_x = 368
player_y = 500
player_x_change = 0

img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 8

for e in range(number_of_enemies):
    img_enemy.append(pygame.image.load("monster.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(1)
    enemy_y_change.append(50)

img_bullet = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 500
bullet_y_change = 1
visible_bullet = False

score = 0
my_font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

end_font = pygame.font.Font('freesansbold.ttf', 40)


def final_text():
    my_final_font = end_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(my_final_font, (200, 200))


def show_score(x, y):
    text = my_font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (x, y))


def player(x, y):
    screen.blit(img_player, (x, y))


def enemy(x, y, en):
    screen.blit(img_enemy[en], (x, y))


def shoot_bullet(x, y):
    global visible_bullet
    visible_bullet = True
    screen.blit(img_bullet, (x + 16, y + 10))


def there_is_a_collision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y2 - y1, 2))
    return distance < 27


is_running = True
while is_running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE:
                if not visible_bullet:
                    bullet_sound = mixer.Sound('shot.mp3')
                    bullet_sound.play()
                    bullet_x = player_x
                    shoot_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:  # Fixed boundary condition
        player_x = 736

    for enem in range(number_of_enemies):
        if enemy_y[enem] > 500:
            for k in range(number_of_enemies):
                enemy_y[k] = 1000
            final_text()
            pygame.display.update()
            pygame.time.delay(2000)
            is_running = False
            break

        enemy_x[enem] += enemy_x_change[enem]

        if enemy_x[enem] <= 0:
            enemy_x_change[enem] = 1
            enemy_y[enem] += enemy_y_change[enem]
        elif enemy_x[enem] >= 736:  # Fixed enemy movement logic
            enemy_x_change[enem] = -1
            enemy_y[enem] += enemy_y_change[enem]

        collision = there_is_a_collision(enemy_x[enem], enemy_y[enem], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('punch.mp3')
            collision_sound.play()
            bullet_y = 500
            visible_bullet = False
            score += 1
            enemy_x[enem] = random.randint(0, 736)
            enemy_y[enem] = random.randint(50, 200)

        enemy(enemy_x[enem], enemy_y[enem], enem)

    if bullet_y <= 64:
        bullet_y = 500
        visible_bullet = False

    if visible_bullet:
        shoot_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
