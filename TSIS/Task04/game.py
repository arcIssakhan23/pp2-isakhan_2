import pygame
import random
import sys
pygame.init()
from db import create_tables, get_or_create_player, get_personal_best, get_top_scores, save_game
from config import load_settings, save_settings
settings = load_settings()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

#some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (27, 36, 117)
DARK_ORANGE = (211, 84, 0)
DARK_PURPLE = (137, 5, 209)

#movement
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)


#about snake
class Snake:
    def __init__(self):
        self.positions = [
            [GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE],
            [GRID_WIDTH // 2 * GRID_SIZE - GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE],
            [GRID_WIDTH // 2 * GRID_SIZE - 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE]
        ]
        self.direction = RIGHT
        self.grow_flag = False
        self.color = tuple(settings["snake_color"])
        self.head_color = (0, 200, 0)

    def move(self):
        head = self.positions[0].copy()
        head[0] += self.direction[0] * GRID_SIZE
        head[1] += self.direction[1] * GRID_SIZE
        
        self.positions.insert(0, head)
        
        if not self.grow_flag:
            self.positions.pop()
        else:
            self.grow_flag = False

    def change_direction(self, new_direction):
        if (new_direction[0] != -self.direction[0] or 
            new_direction[1] != -self.direction[1]):
            self.direction = new_direction

    def grow(self):
        self.grow_flag = True

    def check_self_collision(self):
        head = self.positions[0]
        return head in self.positions[1:]

    def check_border_collision(self):
        head = self.positions[0]
        return (head[0] < 0 or head[0] >= SCREEN_WIDTH or
                head[1] < 0 or head[1] >= SCREEN_HEIGHT)

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            if i == 0:
                pygame.draw.rect(surface, self.head_color, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, WHITE, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE), 2)
            else:
                pygame.draw.rect(surface, self.color, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, BLACK, 
                               (pos[0], pos[1], GRID_SIZE, GRID_SIZE), 1)

    def check_wall_collision(self, walls):
        return self.positions[0] in walls.positions

#about food
class Food:
    def __init__(self, snake_positions, walls_positions=[]):
        self.position = [0, 0]
        self.walls_positions = walls_positions
        self.spawn_time = pygame.time.get_ticks()

        
        self.colors = [
            RED,
            ORANGE,
            YELLOW,
            DARK_GREEN,
            PURPLE
        ]

        self.color = random.choice(self.colors)
        self.respawn(snake_positions, walls_positions)

    def respawn(self, snake_positions, walls_positions=[]):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

            if [x, y] not in snake_positions and [x, y] not in walls_positions:
                self.position = [x, y]
                self.spawn_time = pygame.time.get_ticks()
                self.color = random.choice(self.colors)
                break

    def update(self):
        current_time = pygame.time.get_ticks()
        time_alive = current_time - self.spawn_time

        if time_alive > 10000:
            return "RESPAWN"

        return time_alive

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                         (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, WHITE,
                         (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE), 2)
           

class PowerUp:
    def __init__(self, snake_positions, walls_positions):
        self.types = ["speed", "slow", "shield"]
        self.type = random.choice(self.types)

        self.position = [0, 0]
        self.spawn_time = pygame.time.get_ticks()

        self.respawn(snake_positions, walls_positions)

    def respawn(self, snake_positions, walls_positions):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

            if [x, y] not in snake_positions and [x, y] not in walls_positions:
                self.position = [x, y]
                self.spawn_time = pygame.time.get_ticks()
                break

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 8000  # 8 sec

    def draw(self, surface):
        if self.type == "speed":
            color = DARK_BLUE
        elif self.type == "slow":
            color = DARK_ORANGE
        else:
            color = DARK_PURPLE

        pygame.draw.rect(surface, color,
                         (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

#about border and labyrint 
class Walls:
    def __init__(self):
        self.positions = []

    def generate(self, level):
        if level < 2:
            return

        
        if level % 2 == 0:
            base_x = random.randint(3, GRID_WIDTH - 8) * GRID_SIZE
            base_y = random.randint(3, GRID_HEIGHT - 8) * GRID_SIZE

            shape_type = random.choice([0, 1, 2, 3])
            new_blocks = []

            if shape_type == 0:  
                for i in range(5):
                    new_blocks.append([base_x, base_y + i * GRID_SIZE])
                for i in range(5):
                    new_blocks.append([base_x + i * GRID_SIZE, base_y])

            elif shape_type == 1:  
                for i in range(5):
                    new_blocks.append([base_x, base_y + i * GRID_SIZE])
                for i in range(5):
                    new_blocks.append([base_x - i * GRID_SIZE, base_y])

            elif shape_type == 2:  
                for i in range(5):
                    new_blocks.append([base_x, base_y - i * GRID_SIZE])
                for i in range(5):
                    new_blocks.append([base_x + i * GRID_SIZE, base_y])

            else:  
                for i in range(5):
                    new_blocks.append([base_x, base_y - i * GRID_SIZE])
                for i in range(5):
                    new_blocks.append([base_x - i * GRID_SIZE, base_y])

            for block in new_blocks:
                if block not in self.positions:
                    self.positions.append(block)

        
        else:
            for _ in range(3):  
                x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
                y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

                if [x, y] not in self.positions:
                    self.positions.append([x, y])



    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, LIGHT_BLUE,
                             (pos[0], pos[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, WHITE,
                             (pos[0], pos[1], GRID_SIZE, GRID_SIZE), 1)

def show_game_over(screen, score, level):
    screen.fill(BLACK)
    
    game_over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    level_text = font.render(f"Level Reached: {level}", True, YELLOW)
    restart_text = font.render("Press SPACE to restart", True, GREEN)
    quit_text = font.render("Press ESC to quit", True, GREEN)
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 150))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
    screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 300))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 400))
    screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 450))
    
    pygame.display.flip()

def leaderboard_screen(screen):
    running = True

    while running:
        screen.fill(BLACK)

        title = big_font.render("LEADERBOARD", True, YELLOW)
        screen.blit(title, (200, 50))

        scores = get_top_scores()

        y = 150
        rank = 1

        for row in scores:
            username, score, level, date = row

            text = font.render(
                f"{rank}. {username} | {score} | Lvl {level}",
                True,
                WHITE
            )
            screen.blit(text, (150, y))
            y += 40
            rank += 1

        back = font.render("Press ESC to go back", True, GREEN)
        screen.blit(back, (250, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False



def color_name(rgb):
    if rgb == [0, 255, 0]:
        return "GREEN"
    elif rgb == [255, 0, 0]:
        return "RED"
    elif rgb == [0, 0, 255]:
        return "BLUE"
    elif rgb == [255, 255, 0]:
        return "YELLOW"
    return str(rgb)

def run_game(player_id, username, personal_best):
    snake = Snake()
    snake.color = GREEN
    food = Food(snake.positions)
    powerup = None
    power_effect = None
    power_end_time = 0
    shield_active = False
    
    score = 0
    level = 1
    walls = Walls()
    walls.generate(level)
    foods_eaten = 0
    FOODS_PER_LEVEL = 3
    
    base_speed = 10
    current_speed = base_speed
    
    running = True
    game_active = True
    
    while running:
        clock.tick(current_speed)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_active:
                    # Arrow keys + WASD controls
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    # Key F to fix problem with stacked food
                    elif event.key == pygame.K_f:
                        food.respawn(snake.positions, walls.positions)


                else:
                    if event.key == pygame.K_SPACE:
                        score = 0
                        level = 1
                        foods_eaten = 0
                        current_speed = base_speed

                        snake = Snake()
                        food = Food(snake.positions)

                        walls = Walls()
                        walls.generate(level)

                        game_active = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        
        if game_active:
            snake.color = tuple(settings["snake_color"])
            snake.head_color = tuple(settings["snake_color"])
            snake.move()

            result = food.update()
            if result == "RESPAWN":
                food.respawn(snake.positions, walls.positions)
            
            if powerup is None:
                if random.randint(0, 200) == 1:  
                    powerup = PowerUp(snake.positions, walls.positions)


            if powerup and snake.positions[0] == powerup.position:

                if powerup.type == "speed":
                    current_speed += 5
                    power_effect = "speed"
                    power_end_time = pygame.time.get_ticks() + 5000

                elif powerup.type == "slow":
                    current_speed = max(5, current_speed - 5)
                    power_effect = "slow"
                    power_end_time = pygame.time.get_ticks() + 5000

                elif powerup.type == "shield":
                    shield_active = True

                powerup = None


            if power_effect and pygame.time.get_ticks() > power_end_time:
                current_speed = base_speed + (level * 2)
                power_effect = None

            if powerup and powerup.is_expired():
                powerup = None
            collision = (
                snake.check_border_collision() or
                snake.check_self_collision() or
                snake.check_wall_collision(walls)
            )

            if collision:
                if shield_active:
                    shield_active = False  # consume shield
                else:
                    from db import save_game
                    save_game(player_id, score, level)

                    game_active = False
                    continue
            
            if snake.positions[0] == food.position:
    
                if food.color == PURPLE:
        
                    # if len(snake.positions) <= 3:  #poison
                    #     game_active = False
                    #     continue
                    save_game(player_id, score, level)

                    game_active = False
                    continue
                    
                    if len(snake.positions) > 3:
                        snake.positions.pop()

                    score -= 10  

                else:
                    snake.grow()
                    score += 10
                    foods_eaten += 1

                    if foods_eaten >= FOODS_PER_LEVEL:
                        level += 1
                        foods_eaten = 0
                        current_speed = base_speed + (level * 2)
                        walls.generate(level)

                food.respawn(snake.positions, walls.positions)
                
                if foods_eaten >= FOODS_PER_LEVEL:
                    level += 1
                    foods_eaten = 0
                    current_speed = base_speed + (level * 2)

                    walls.generate(level)   
                
                food.respawn(snake.positions)
            
            screen.fill(BLACK)
            
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                if settings["grid"]:
                    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                        pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
                    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                        pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))
                pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))
            
            walls.draw(screen)
            snake.draw(screen)
            food.draw(screen)
            
            if powerup:
                powerup.draw(screen)

            score_text = font.render(f"Score: {score}", True, WHITE)
            level_text = font.render(f"Level: {level}", True, YELLOW)
            speed_text = font.render(f"Speed: {current_speed}", True, CYAN)
            
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))
            screen.blit(speed_text, (10, 90))
            
            foods_left_text = font.render(f"Next Level: {foods_eaten}/{FOODS_PER_LEVEL}", True, PURPLE)
            screen.blit(foods_left_text, (10, 130))
            name_text = font.render(f"Player: {username}", True, WHITE)
            screen.blit(name_text, (600, 10))

            best_text = font.render(f"Best: {personal_best}", True, GREEN)
            screen.blit(best_text, (600, 50))
            
            
            
        else:
            show_game_over(screen, score, level)
        



        pygame.display.flip()
    
    pygame.quit()
    sys.exit()





def main():
    create_tables()

    while True:
        choice, username = main_menu(screen, font, big_font)

        if choice == "leaderboard":
            leaderboard_screen(screen)
            continue

        if choice == "settings":
            settings_screen(screen)
            continue

        # PLAY selected
        player_id = get_or_create_player(username)
        personal_best = get_personal_best(player_id)

        run_game(player_id, username, personal_best)
    
    

def main_menu(screen, font, big_font):
    username = ""
    entering_name = True

    while True:
        screen.fill((0, 0, 0))

        title = big_font.render("SNAKE GAME", True, (0, 255, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        if entering_name:
            text = font.render("Enter Username: " + username, True, (255, 255, 255))
            hint = font.render("Press ENTER to continue", True, (150, 150, 150))

            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 250))
            screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 300))

        else:
            # BUTTONS (rectangles)
            play_rect = pygame.Rect(300, 250, 200, 40)
            leaderboard_rect = pygame.Rect(300, 300, 200, 40)
            settings_rect = pygame.Rect(300, 350, 200, 40)

            pygame.draw.rect(screen, (50, 50, 50), play_rect)
            pygame.draw.rect(screen, (50, 50, 50), leaderboard_rect)
            pygame.draw.rect(screen, (50, 50, 50), settings_rect)

            play = font.render("Play", True, (255, 255, 255))
            leaderboard = font.render("Leaderboard", True, (255, 255, 255))
            settings = font.render("Settings", True, (255, 255, 255))

            screen.blit(play, (play_rect.x + 60, play_rect.y + 5))
            screen.blit(leaderboard, (leaderboard_rect.x + 20, leaderboard_rect.y + 5))
            screen.blit(settings, (settings_rect.x + 40, settings_rect.y + 5))

        pygame.display.flip()

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if entering_name:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username != "":
                        entering_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    if event.unicode.isprintable():
                        if len(username) < 12:
                            username += event.unicode

            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if play_rect.collidepoint(mouse_pos):
                        return "play", username

                    if leaderboard_rect.collidepoint(mouse_pos):
                        return "leaderboard", username

                    if settings_rect.collidepoint(mouse_pos):
                        return "settings", username


def settings_screen(screen):
    global settings

    colors = [
        (0, 255, 0),
        (255, 0, 0),
        (0, 0, 255),
        (255, 255, 0)
    ]

    index = 0

    running = True
    while running:
        screen.fill(BLACK)

        title = big_font.render("SETTINGS", True, WHITE)
        screen.blit(title, (250, 80))

        color_text = font.render(
            f"Snake Color: {color_name(settings['snake_color'])}",
            True,
            WHITE   
        )
        grid_text = font.render(f"Grid: {settings['grid']}", True, WHITE)
        sound_text = font.render(f"Sound: {settings['sound']}", True, WHITE)

        screen.blit(color_text, (200, 200))
        screen.blit(grid_text, (200, 250))
        screen.blit(sound_text, (200, 300))

        hint = font.render("C = change color | G = grid | S = sound | ENTER = save", True, YELLOW)
        screen.blit(hint, (80, 450))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c:
                    index = (index + 1) % len(colors)
                    settings["snake_color"] = list(colors[index])

                if event.key == pygame.K_g:
                    settings["grid"] = not settings["grid"]

                if event.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]

                if event.key == pygame.K_RETURN:
                    save_settings(settings)
                    running = False

        