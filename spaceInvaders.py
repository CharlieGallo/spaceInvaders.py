import sys, pygame
import random
import math
from pygame import mixer

# Initialise the pygame
pygame.init()

# create the screen - width x height
# Top, left corner = 0
# X, Y co-ordinates
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

#Background Music
mixer.music.load('background.wav')
mixer.music.play(-1) #-1 means the sound will play on a loop

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')  # 64 pixels
playerX = 370  # Take in to account the size of the image
playerY = 480
playerX_change = 0  # create variable to use in event for loop

# Enemy
# Use lists to create multiple enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))  # 64 pixels
    enemyX.append(random.randint(0, 735))  # Enemy randomly placed on screen
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')  # 32 pixels
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score on screen
score_value = 0
font = pygame.font.Font('darkhornet.ttf', 32)
textX = 10
textY = 10

# Game Over text
game_over_font = pygame.font.Font('darkhornet.ttf', 64)


# Display score on screen using render() and then blit()
# String value, set True to display in screen, (colour of font)
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (250, 250))

# Function to display and move player image at set X, Y co-ordinates
# blit() method draws image - assigns pixels to X, Y pos.
def player(x, y):
    screen.blit(playerImg, (x, y))


# Function to display and move enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))
    # You add so the image does not appear to come from the centre of the spaceship but the top


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        (math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))
    )
    if distance < 27:
        return True
    else:
        return False


# game loop - keeps displaying screen and playing images
running = True
while running:

    # Drawing the screen must come first
    # Everything else is drawsn on top of the screen
    # Change background colour - must be in running loop
    screen.fill((0, 0, 0))  # RGB values

    # Background image
    screen.blit(background, (0, 0))

    # Changing the value of X and Y so player moves in constant direction
    # playerX += 0.1
    # playerY -= 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for keystroke press event
        if event.type == pygame.KEYDOWN:
            # Check what key was pressed
            if event.key == pygame.K_LEFT:
                # print('Left arrow')
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                # print('Right arrow')
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Plays bullet sound
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Gets current X co-ord of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # Check for keystroke release event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print('Keystroke has been released')
                playerX_change = 0.0  # Stops player moving

    ##PLAYER MOVEMENT
    # Change X co-ordinate passed to player() function
    playerX += playerX_change
    # Create boundaries to screen - player can't go off screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    ##ENEMY MOVEMENT
    # For loop to handle multiple enemies
    for i in range(num_of_enemies):

        #Game Over
        # If enemy hits the ship then all the enemies will be removed from the screen
        # and the game_over_text function is called
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()

        # Change X co-ordinate passed to enemy() function
        enemyX[i] += enemyX_change[i]
        # When enemy meets boundary of screen it goes back in opposite direction
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # COLLISION
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Plays explosion sound when enemy is destroyed
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Call enemy() function to display player image on screen
        enemy(enemyX[i], enemyY[i], i)

    ##BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Call player() function to display player image on screen
    player(playerX, playerY)

    # Call show_score function to display on screen
    show_score(textX, textY)

    # Update changes to the display
    pygame.display.update()
