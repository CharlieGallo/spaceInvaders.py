import sys, pygame
import random
import math

# Initialise the pygame
pygame.init()

# create the screen - width x height
# Top, left corner = 0
# X, Y co-ordinates
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

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
enemyImg = pygame.image.load('enemy.png')  # 64 pixels
enemyX = random.randint(0, 736)  # Enemy randomly placed on screen
enemyY = random.randint(50, 150)
enemyX_change = 3
enemyY_change = 40

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')  # 32 pixels
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score = 0

# Function to display and move player image at set X, Y co-ordinates
# blit() method draws image - assigns pixels to X, Y pos.
def player(x, y):
    screen.blit(playerImg, (x, y))


# Function to display and move enemy
def enemy(x, y):
    screen.blit(enemyImg, (x, y))


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


# game loop
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
                if bullet_state is "ready":
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
    # Change X co-ordinate passed to enemy() function
    enemyX += enemyX_change
    # When enemy meets boundary of screen it goes back in opposite direction
    if enemyX <= 0:
        enemyX_change = 3
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -3
        enemyY += enemyY_change

    ##BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #COLLISION - must come after the enemy and bullet co-ords are set
    collision = is_collision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score += 1
        print(score)

    # Call player() function to display player image on screen
    player(playerX, playerY)
    # Call enemy() function to display player image on screen
    enemy(enemyX, enemyY)

    # Update changes to the display
    pygame.display.update()
