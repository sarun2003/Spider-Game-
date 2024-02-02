# Import all the necessary libraries
import pygame
import random
import sys

# Initialize Pygame and mixer for sound when you kill or skip the spider
pygame.init()
pygame.mixer.init()

# Constants for screen dimension and the colors in game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CYAN = (0, 255, 255)
BULLET_SIZE = (10, 20)

# to load sound effects for game
beep_sound = pygame.mixer.Sound("beep.wav")  # Sound will play when the spider is hit
drum_sound = pygame.mixer.Sound("drum.wav")  # Sound will play when you lose a health

# The base class for all objects in game
class GameObject:
    def __init__(self, x, y, image, speed):
        self.x = x           #it is horizontal position
        self.y = y           #it is vertical position
        self.image = image   #it is visual representation of object
        self.speed = speed   #Movement speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  #to draw object on screen

# Wizard being the hero class 
class Wizard(GameObject):
    def move(self, direction):
        # to move wizard horizontally within screen
        if 0 <= self.x + direction * self.speed <= SCREEN_WIDTH - 30:
            self.x += direction * self.speed

# Spider being the enemy class
class Spider(GameObject):
    def update(self):
        #to move spider horizontally across screen
        self.x += self.speed
        #to reset spider to left side with new position
        if self.x > SCREEN_WIDTH:
            self.reset()

    def reset(self):
        #to place spider at left edge with random height in screen
        self.x = 0
        self.y = random.randint(0, SCREEN_HEIGHT // 2)

#for bullet class for projectiles fired by wizard
class Bullet(GameObject):
    def update(self):
        #to move bullet upwards
        self.y -= self.speed

# Utility function for loadimg and scale images
def load_scaled_image(file, size):
    image = pygame.image.load(file)
    return pygame.transform.scale(image, size)

# Function to display start page
def start_page(screen):
    start_bg = pygame.image.load("Start.png").convert()
    start_bg = pygame.transform.scale(start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running:
        screen.blit(start_bg, (0, 0))      #it will display start page background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False          #this will exit start page on mouse click

        pygame.display.flip()    # will update display
        pygame.time.delay(100)   # Wait a short time before the next frame

# Game loop
def game_loop(screen):
    running = True
    clock = pygame.time.Clock()

    # Creating an game objects
    wizard = Wizard(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, load_scaled_image("wizard.png", (30, 30)), 5)
    spider = Spider(0, random.randint(0, SCREEN_HEIGHT // 2), load_scaled_image("spider.png", (30, 30)), 2)
    bullets = []       # List to track all bullets

    # These are the game state variable
    score = 0
    health = 5
    font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                #to move wizard or fire bullet based on key press
                if event.key == pygame.K_LEFT:
                    wizard.move(-1)
                elif event.key == pygame.K_RIGHT:
                    wizard.move(1)
                elif event.key == pygame.K_SPACE:
                    # Add new bullet at wizard position asap
                    bullets.append(Bullet(wizard.x + 15, wizard.y, load_scaled_image("bullet.png", BULLET_SIZE), 17))

        # Update game objects
        spider.update()
        for bullet in bullets[:]:  # Make copy to modify list while going over it again
            bullet.update()
            #to remove bullets which move off-screen
            if bullet.y < 0:
                bullets.remove(bullet)

        # TO check for collisions between bullets and the spider
        for bullet in bullets[:]:  # Recapiculate over slice copy to modify list while going over it again...
            bullet.update()
            # Check if fired bullet is within bounds of spider's position
            if spider.x < bullet.x < spider.x + 30 and spider.y < bullet.y < spider.y + 30:
                bullets.remove(bullet)         # to remove bullet that hits enemy
                spider.reset()                 # to reset spider to new position
                score += 10                    # Increase score for hitting spider
                beep_sound.play()              # Play sound effect for hitting spider
                break                          # Exit loop after hitting enemy.

        # Check if spider reaches right edge of screen
        if spider.x >= SCREEN_WIDTH:
            spider.reset()        # Reset spider to new position
            health -= 1           # Decrease health for missing target
            drum_sound.play()     # Play sound effect for missing target
            if health <= 0:
                running = False   # End game if health is finished

        # Clear screen and set background color
        screen.fill(CYAN)
        # Draw game objects on screen
        wizard.draw(screen)
        spider.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Render score and health texts and display them on screen
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))       # using black for score text
        health_text = font.render(f"Health: {health}", True, (255, 0, 0))  # using red for health text
        screen.blit(score_text, (SCREEN_WIDTH - 150, 20))                  # to position score text
        screen.blit(health_text, (20, 20))                                 # to position health text

        # Update display to show changes
        pygame.display.flip()
        # to control game loop timing
        clock.tick(30)

    # to quit Pygame and exit as soon as game loop ends
    pygame.quit()
    sys.exit()

# Main execution
if __name__ == "__main__":
    # to create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    
    # to set window title
    pygame.display.set_caption("Shoot the Spider Reloaded")            
    
    # to display start page until a mouse click
    start_page(screen)  
    #to enter the main game loop
    game_loop(screen)   