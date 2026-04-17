# Imports
import pygame
import sys
from pygame.locals import *
import random
import time

# Initialize Pygame
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0
COIN_WEIGHT_TOTAL = 0  # Track total weight for speed increase
COINS_FOR_SPEEDUP = 5  # N = 5 coins for speed increase

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 30)
font_tiny = pygame.font.SysFont("Verdana", 15)

# Game Over text
game_over = font.render("Game Over", True, BLACK)

# Function to load images with error handling
def load_image(filename, default_color=None, width=None, height=None):
    """Load image from images folder or create colored placeholder"""
    try:
        import os
        path = os.path.join("images", filename)
        if os.path.exists(path):
            image = pygame.image.load(path)
        else:
            image = pygame.image.load(filename)
        
        if width and height:
            image = pygame.transform.scale(image, (width, height))
        return image
    except:
        print(f"Warning: Could not load {filename}, creating placeholder")
        if default_color:
            size = (width or 50, height or 50)
            image = pygame.Surface(size)
            image.fill(default_color)
            return image
        return None

# Load images
background = load_image("AnimatedStreet.png", GRAY, SCREEN_WIDTH, SCREEN_HEIGHT)
player_img = load_image("Player.png", BLUE, 50, 80)
enemy_img = load_image("Enemy.png", RED, 50, 80)

# Create display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Racer - Weighted Coins")
DISPLAYSURF.fill(WHITE)

class Player(pygame.sprite.Sprite):
    """Player car class"""
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        self.speed = 7

    def move(self):
        """Handle player movement"""
        pressed_keys = pygame.key.get_pressed()
        
        if (pressed_keys[K_LEFT] or pressed_keys[K_a]) and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        
        if (pressed_keys[K_RIGHT] or pressed_keys[K_d]) and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(self.speed, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    """Enemy car class with speed that increases based on coins collected"""
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.base_speed = SPEED
        self.reset_position()

    def reset_position(self):
        """Reset enemy to top of screen"""
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """Move enemy down the screen with current speed"""
        global SCORE
        current_speed = self.get_current_speed()
        self.rect.move_ip(0, current_speed)
        
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.reset_position()

    def get_current_speed(self):
        """Calculate enemy speed based on coins collected"""
        global COINS_COLLECTED, COINS_FOR_SPEEDUP
        # Increase speed by 20% for every 5 coins collected
        speed_multiplier = 1 + (COINS_COLLECTED // COINS_FOR_SPEEDUP) * 0.2
        return self.base_speed * speed_multiplier

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    """Coin class with different weights - appears rarely"""
    def __init__(self):
        super().__init__()
        # Create initial rect FIRST
        self.rect = pygame.Rect(0, 0, 25, 25)
        self.spawn_delay = random.randint(60, 180)
        self.active = False
        self.delay_counter = 0
        self.weight = 1  # Default weight
        self.reset_position()

    def create_image(self):
        """Create coin image based on weight"""
        size = 25 + self.weight * 3  # Bigger for higher weight
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if self.weight == 1:
            color = BRONZE
        elif self.weight == 2:
            color = SILVER
        else:
            color = GOLD
            
        pygame.draw.circle(self.image, color, (size//2, size//2), size//2)
        pygame.draw.circle(self.image, WHITE, (size//2, size//2), size//2, 2)
        
        # Update rect size while preserving center
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def reset_position(self):
        """Reset coin to random position with random weight"""
        self.rect.center = (
            random.randint(30, SCREEN_WIDTH - 30),
            random.randint(-500, -100)
        )
        # Random weight: 1 (bronze), 2 (silver), 3 (gold)
        self.weight = random.choices([1, 2, 3], weights=[50, 30, 20])[0]
        self.create_image()
        self.active = True

    def move(self):
        """Move coin down the screen"""
        if not self.active:
            self.delay_counter += 1
            if self.delay_counter >= self.spawn_delay:
                self.active = True
                self.delay_counter = 0
                self.spawn_delay = random.randint(120, 300)
            return
        
        self.rect.move_ip(0, SPEED // 2)
        
        if self.rect.top > SCREEN_HEIGHT:
            self.active = False
            self.reset_position()

    def draw(self, surface):
        """Draw coin with weight indicator"""
        if self.active:
            surface.blit(self.image, self.rect)
            # Draw weight number on coin
            weight_text = font_tiny.render(str(self.weight), True, BLACK)
            text_rect = weight_text.get_rect(center=self.rect.center)
            surface.blit(weight_text, text_rect)

def show_game_over(score, coins, total_weight):
    """Display game over screen"""
    DISPLAYSURF.fill(RED)
    
    game_over_text = font.render("GAME OVER", True, BLACK)
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    coins_text = font_medium.render(f"Coins: {coins}", True, YELLOW)
    weight_text = font_small.render(f"Total Weight: {total_weight}", True, WHITE)
    restart_text = font_small.render("Press SPACE to restart", True, GREEN)
    quit_text = font_small.render("Press ESC to quit", True, GREEN)
    
    DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 150))
    DISPLAYSURF.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH//2 - coins_text.get_width()//2, 290))
    DISPLAYSURF.blit(weight_text, (SCREEN_WIDTH//2 - weight_text.get_width()//2, 330))
    DISPLAYSURF.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 400))
    DISPLAYSURF.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 440))
    
    pygame.display.update()

def reset_game():
    """Reset all game variables"""
    global SCORE, COINS_COLLECTED, SPEED, COIN_WEIGHT_TOTAL
    SCORE = 0
    COINS_COLLECTED = 0
    COIN_WEIGHT_TOTAL = 0
    SPEED = 5
    
    P1.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
    E1.reset_position()
    
    for coin in coins:
        coin.active = False
        coin.delay_counter = 0
        coin.spawn_delay = random.randint(120, 300)

# Initialize game objects
P1 = Player()
E1 = Enemy()

# Create sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coin1 = Coin()
coins.add(coin1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(coin1)

# Custom events
INC_SPEED = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(INC_SPEED, 5000)
pygame.time.set_timer(SPAWN_COIN, 8000)  # Spawn additional coin every 8 seconds

# Game states
PLAYING = 0
GAME_OVER = 1
game_state = PLAYING

# Background scrolling
bg_y = 0
bg_scroll_speed = 2

# Main game loop
while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if game_state == PLAYING:
            if event.type == INC_SPEED:
                SPEED += 0.2
                if SPEED > 12:
                    SPEED = 12
            
            elif event.type == SPAWN_COIN:
                # Spawn additional coin if less than 3 coins
                active_coins = [c for c in coins if c.active]
                if len(active_coins) < 3:
                    new_coin = Coin()
                    coins.add(new_coin)
                    all_sprites.add(new_coin)
        
        elif game_state == GAME_OVER:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Clear old coins and create new one
                    coins.empty()
                    coin1 = Coin()
                    coins.add(coin1)
                    all_sprites.empty()
                    all_sprites.add(P1)
                    all_sprites.add(E1)
                    all_sprites.add(coin1)
                    reset_game()
                    game_state = PLAYING
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    if game_state == PLAYING:
        # Scroll background
        bg_y = (bg_y + bg_scroll_speed) % SCREEN_HEIGHT
        DISPLAYSURF.blit(background, (0, bg_y - SCREEN_HEIGHT))
        DISPLAYSURF.blit(background, (0, bg_y))
        
        # Move all sprites
        P1.move()
        E1.move()
        for coin in coins:
            coin.move()
        
        # Check coin collisions
        for coin in coins:
            if coin.active and P1.rect.colliderect(coin.rect):
                COINS_COLLECTED += 1
                COIN_WEIGHT_TOTAL += coin.weight
                SCORE += coin.weight * 10  # Weight affects score
                coin.active = False
                coin.reset_position()
        
        # Check enemy collision
        if P1.rect.colliderect(E1.rect):
            time.sleep(0.5)
            game_state = GAME_OVER
        
        # Draw all sprites
        P1.draw(DISPLAYSURF)
        E1.draw(DISPLAYSURF)
        for coin in coins:
            coin.draw(DISPLAYSURF)
        
        # Draw UI
        score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
        coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
        weight_text = font_small.render(f"Weight: {COIN_WEIGHT_TOTAL}", True, BLACK)
        speed_text = font_small.render(f"Speed: {E1.get_current_speed():.1f}x", True, RED)
        next_speed_text = font_tiny.render(f"Next speed at: {(COINS_COLLECTED // COINS_FOR_SPEEDUP + 1) * COINS_FOR_SPEEDUP} coins", True, RED)
        
        # UI Background
        pygame.draw.rect(DISPLAYSURF, WHITE, (5, 5, 180, 115))
        pygame.draw.rect(DISPLAYSURF, BLACK, (5, 5, 180, 115), 2)
        
        DISPLAYSURF.blit(score_text, (10, 10))
        DISPLAYSURF.blit(coins_text, (10, 35))
        DISPLAYSURF.blit(weight_text, (10, 60))
        DISPLAYSURF.blit(speed_text, (10, 80))
        DISPLAYSURF.blit(next_speed_text, (10, 100))
        
        # Coin legend
        legend_y = SCREEN_HEIGHT - 80
        pygame.draw.rect(DISPLAYSURF, WHITE, (5, legend_y, 180, 75))
        pygame.draw.rect(DISPLAYSURF, BLACK, (5, legend_y, 180, 75), 2)
        
        legend_title = font_tiny.render("Coin Values:", True, BLACK)
        bronze_text = font_tiny.render("Bronze = 10 pts (W:1)", True, BRONZE)
        silver_text = font_tiny.render("Silver = 20 pts (W:2)", True, SILVER)
        gold_text = font_tiny.render("Gold = 30 pts (W:3)", True, GOLD)
        
        DISPLAYSURF.blit(legend_title, (10, legend_y + 5))
        DISPLAYSURF.blit(bronze_text, (10, legend_y + 25))
        DISPLAYSURF.blit(silver_text, (10, legend_y + 45))
        DISPLAYSURF.blit(gold_text, (10, legend_y + 60))
    
    else:
        show_game_over(SCORE, COINS_COLLECTED, COIN_WEIGHT_TOTAL)
    
    pygame.display.update()
    FramePerSec.tick(FPS)