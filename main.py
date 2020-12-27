import pygame, random, math
from pygame import mixer

# initialize pygame
pygame.init()

# setting the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('batman-logo.png')
icon = pygame.transform.scale(icon, (8, 8))
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('5311.jpg')

# Player
playerImg = pygame.image.load('spaceship.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
player_change = 0

# Enemy
enemyImg = pygame.image.load('superhero.png')
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')

# bulletImg = pygame.transform.scale(bulletImg, (10, 10))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('cat.ttf', 32)

scoreX = 10
scoreY = 10

game_over_font = pygame.font.Font('splash.otf', 64)
def game_over():
    over_text = font.render("GAME OVER", True, (0,0,0))
    screen.blit(over_text, (320, 300))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fireBullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x, y - 40))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False


def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


# game running loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = -10
            elif event.key == pygame.K_RIGHT:
                player_change = 10
            elif event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('bat.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0

    # Player movement
    playerX += player_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 734:
        playerX = 734

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision
    for i in range(num_of_enemies):
        if enemyY[i] >440:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # explosionSound = mixer.Sound("explosion.wav")
            # explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i])

    # Calling player and enemy
    player(playerX, playerY)
    show_score(scoreX, scoreY)

    # if enemyY == playerY - 32 or enemyX != playerX:
    #     enemy(enemyX, enemyY)
    # elif (enemyY, enemyX) == (playerY - 32, playerX):
    #     pass
    pygame.display.update()
