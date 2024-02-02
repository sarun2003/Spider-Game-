# Import all required libraries
import pygame
import random
import sys

# Initialize Pygame and mixer for sound effects
pygame.init()
pygame.mixer.init()

# Constants for screen dimension and color
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CYAN = (0, 255, 255)
BULLET_SIZE = (10, 20)

# to load sound effects
beep_sound = pygame.mixer.Sound("beep.wav")        # Sound played when spider is hit
drum_sound = pygame.mixer.Sound("drum.wav")        # Sound played when you lose health

# Base class for game object
class GameObject:
    def __init__(self, x, y, image, speed):
        self.x = x           # Horizontal position
        self.y = y           # Vertical position
        self.image = image   # Visual representation of object
        self.speed = speed   # for movement speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))    # Draw object on-screen

# Wizard class
class Wizard(GameObject):
    def move(self, direction):
        # to move wizard horizontally within screen
        if 0 <= self.x + direction * self.speed <= SCREEN_WIDTH - 30:
            self.x += direction * self.speed

# Spider class
class Spider(GameObject):
    def update(self):
        # to move spider horizontally across screen
        self.x += self.speed
        # to reset spider to left side with a new vertical position if it moves off right edge
        if self.x > SCREEN_WIDTH:
            self.reset()

    def reset(self):
        # to place spider at left edge with random height
        self.x = 0
        self.y = random.randint(0, SCREEN_HEIGHT // 2)

# Bullet class for projectiles fired by wizard
class Bullet(GameObject):
    def update(self):
        # to move bullet up.
        self.y -= self.speed

# Utility function to load images
def load_scaled_image(file, size):
    image = pygame.image.load(file)
    return pygame.transform.scale(image, size)

# Function to display start page
def start_page(screen):
    start_bg = pygame.image.load("Start.png").convert()
    start_bg = pygame.transform.scale(start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running:
        screen.blit(start_bg, (0, 0))  # to display start page background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False       # exit start page on a click

        pygame.display.flip()    # Update display
        pygame.time.delay(100)   # Wait short time before next frame

# the game loop
def game_loop(screen):
    running = True
    clock = pygame.time.Clock()

    # Create game object
    wizard = Wizard(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, load_scaled_image("wizard.png", (30, 30)), 5)
    spider = Spider(0, random.randint(0, SCREEN_HEIGHT // 2), load_scaled_image("spider.png", (30, 30)), 2)
    bullets = []  # List to track bullet

    # Game variable
    score = 0
    health = 5
    font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # to move wizard or fire a bullet based on key press
                if event.key == pygame.K_LEFT:
                    wizard.move(-1)
                elif event.key == pygame.K_RIGHT:
                    wizard.move(1)
                elif event.key == pygame.K_SPACE:
                    # Add new bullet at wizard's position
                    bullets.append(Bullet(wizard.x + 15, wizard.y, load_scaled_image("bullet.png", BULLET_SIZE), 17))

        # Update game object
        spider.update()
        for bullet in bullets[:]:  # Make a copy to modify list while going thorugh it again.
            bullet.update()
            # to remove bullets that move off-screen
            if bullet.y < 0:
                bullets.remove(bullet)

        # Check for collisions between bullets and enemy.
        for bullet in bullets[:]:  # recapitulate over slice copy to modify list while going again.
            bullet.update()
            # Check if bullet is within of spider's position
            if spider.x < bullet.x < spider.x + 30 and spider.y < bullet.y < spider.y + 30:
                bullets.remove(bullet)         # Remove bullet that hit target
                spider.reset()                 # Reset spider to a new position
                score += 10                    # Increase score for hitting target
                beep_sound.play()              # Play sound effect for hitting target
                break                          # Exit loop after hitting enemy.

        # Check if spider reaches right edge on screen
        if spider.x >= SCREEN_WIDTH:
            spider.reset()        # Reset spider to new position
            health -= 1           # Decrease health for missing target
            drum_sound.play()     # Play sound effect for missing target
            if health <= 0:
                running = False   # End game if health is at zero

        # Clear screen and set background color
        screen.fill(CYAN)
        # Draw game objects on-screen
        wizard.draw(screen)
        spider.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Render score, health texts and display on screen
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))       # Black for score text
        health_text = font.render(f"Health: {health}", True, (255, 0, 0))  # Red for health text
        screen.blit(score_text, (SCREEN_WIDTH - 150, 20))                  # Position of score text
        screen.blit(health_text, (20, 20))                                 # Position of health text

        # Update display to show changes
        pygame.display.flip()
        # to control game loop
        clock.tick(30)

    # Quit Pygame and exit program when game loop ends
    pygame.quit()
    sys.exit()

# Main execution
if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # Create game window
    pygame.display.set_caption("Shoot the Spider Reloaded")            # Set window title
     
    # Display start page until click
    start_page(screen)  
    # Enter main game loop
    game_loop(screen)   
