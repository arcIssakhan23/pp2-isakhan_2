import pygame
import random

from persistence import save_score
from ui import draw_hud


WIDTH = 800
HEIGHT = 700

ROAD_LEFT = 180
ROAD_WIDTH = 440
LANES = 4
LANE_WIDTH = ROAD_WIDTH // LANES
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH

FINISH_DISTANCE = 1000000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD = (60, 60, 60)
GRASS = (45, 150, 60)
YELLOW = (240, 210, 40)
RED = (210, 50, 50)
BLUE = (50, 120, 230)
GREEN = (50, 180, 80)
PURPLE = (160, 80, 220)
ORANGE = (240, 140, 40)
BROWN = (120, 80, 40)
GRAY = (120, 120, 120)
CYAN = (50, 210, 220)


CAR_COLORS = {
    "blue": BLUE,
    "red": RED,
    "green": GREEN,
    "yellow": YELLOW
}


DIFFICULTY_SPEED = {
    "easy": 4,
    "normal": 6,
    "hard": 8
}


class Player:
    """Player car."""
    def __init__(self, color_name):
        self.width = 45
        self.height = 70
        self.x = ROAD_LEFT + ROAD_WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 110
        self.speed = 7
        self.color = CAR_COLORS.get(color_name, BLUE)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed

        self.x = max(ROAD_LEFT, min(ROAD_RIGHT - self.width, self.x))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, (self.x + 9, self.y + 8, 27, 18), border_radius=4)


class FallingObject:
    """Base falling object."""
    def __init__(self, lane, y, w, h, kind):
        self.lane = lane
        self.x = ROAD_LEFT + lane * LANE_WIDTH + (LANE_WIDTH - w) // 2
        self.y = y
        self.w = w
        self.h = h
        self.kind = kind
        self.timeout = 420

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self, speed):
        self.y += speed
        self.timeout -= 1

    def off_screen(self):
        return self.y > HEIGHT + 50 or self.timeout <= 0


def draw_object(screen, obj):
    """Draws traffic, obstacle, power-up, road event, or coin."""
    rect = obj.rect

    if obj.kind == "traffic":
        pygame.draw.rect(screen, RED, rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, (obj.x + 8, obj.y + 8, obj.w - 16, 15), border_radius=4)

    elif obj.kind == "barrier":
        pygame.draw.rect(screen, ORANGE, rect)
        pygame.draw.line(screen, BLACK, (obj.x, obj.y), (obj.x + obj.w, obj.y + obj.h), 4)

    elif obj.kind == "oil":
        pygame.draw.ellipse(screen, BLACK, rect)

    elif obj.kind == "pothole":
        pygame.draw.ellipse(screen, BROWN, rect)

    elif obj.kind == "speed_bump":
        pygame.draw.rect(screen, YELLOW, rect, border_radius=5)

    elif obj.kind == "nitro_strip":
        pygame.draw.rect(screen, CYAN, rect, border_radius=5)

    elif obj.kind == "coin":
        pygame.draw.circle(screen, YELLOW, rect.center, obj.w // 2)
        pygame.draw.circle(screen, BLACK, rect.center, obj.w // 2, 2)

    elif obj.kind == "nitro":
        pygame.draw.rect(screen, CYAN, rect, border_radius=8)
        pygame.draw.circle(screen, WHITE, rect.center, 8)

    elif obj.kind == "shield":
        pygame.draw.rect(screen, PURPLE, rect, border_radius=8)
        pygame.draw.circle(screen, WHITE, rect.center, 9, 3)

    elif obj.kind == "repair":
        pygame.draw.rect(screen, GREEN, rect, border_radius=8)
        pygame.draw.line(screen, WHITE, (obj.x + 12, obj.y + obj.h // 2), (obj.x + obj.w - 12, obj.y + obj.h // 2), 4)
        pygame.draw.line(screen, WHITE, (obj.x + obj.w // 2, obj.y + 12), (obj.x + obj.w // 2, obj.y + obj.h - 12), 4)


def lane_is_safe(player, lane):
    """Avoid spawning directly on top of the player lane."""
    player_lane = int((player.x - ROAD_LEFT) // LANE_WIDTH)
    return lane != player_lane


def make_object(kind, player):
    """Creates object with safe spawn logic."""
    lane = random.randint(0, LANES - 1)

    for _ in range(10):
        if lane_is_safe(player, lane):
            break
        lane = random.randint(0, LANES - 1)

    if kind == "traffic":
        return FallingObject(lane, -90, 48, 75, "traffic")
    if kind == "barrier":
        return FallingObject(lane, -40, 70, 28, "barrier")
    if kind == "oil":
        return FallingObject(lane, -35, 65, 35, "oil")
    if kind == "pothole":
        return FallingObject(lane, -35, 60, 35, "pothole")
    if kind == "speed_bump":
        return FallingObject(lane, -25, 80, 20, "speed_bump")
    if kind == "nitro_strip":
        return FallingObject(lane, -25, 80, 20, "nitro_strip")
    if kind == "coin":
        return FallingObject(lane, -30, 26, 26, "coin")

    return FallingObject(lane, -35, 34, 34, kind)


def draw_road(screen, road_offset):
    """Draws grass, road and lane lines."""
    screen.fill(GRASS)
    pygame.draw.rect(screen, ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

    for i in range(1, LANES):
        x = ROAD_LEFT + i * LANE_WIDTH
        for y in range(-40, HEIGHT, 80):
            pygame.draw.rect(screen, WHITE, (x - 3, y + road_offset, 6, 45))

    pygame.draw.rect(screen, BLACK, (ROAD_LEFT - 5, 0, 5, HEIGHT))
    pygame.draw.rect(screen, BLACK, (ROAD_RIGHT, 0, 5, HEIGHT))


def apply_powerup(kind, state):
    """Applies collected power-up. Only one timed power-up at a time."""
    if kind == "nitro":
        state["active_power"] = "Nitro"
        state["power_timer"] = 4.0
    elif kind == "shield":
        state["active_power"] = None
        state["power_timer"] = 0
        state["shield"] = True
    elif kind == "repair":
        if state["objects"]:
            state["objects"].pop(0)
        state["score"] += 30


def run_game(screen, clock, settings, username):
    """Main game loop. Returns game over data."""
    font = pygame.font.SysFont(None, 28)

    player = Player(settings["car_color"])
    base_speed = DIFFICULTY_SPEED.get(settings["difficulty"], 6)

    state = {
        "score": 0,
        "coins": 0,
        "distance": 0,
        "objects": [],
        "active_power": None,
        "power_timer": 0,
        "shield": False
    }

    road_offset = 0
    traffic_timer = 0
    obstacle_timer = 0
    coin_timer = 0
    power_timer = 0
    event_timer = 0

    running = True

    while running:
        dt = clock.tick(60) / 1000

        progress_factor = 1 + state["distance"] / 1800
        speed = base_speed * progress_factor

        if state["active_power"] == "Nitro":
            speed += 4
            state["power_timer"] -= dt
            if state["power_timer"] <= 0:
                state["active_power"] = None

        state["distance"] += speed * 0.55
        state["score"] = int(state["distance"] + state["coins"] * 20)

        if state["distance"] >= FINISH_DISTANCE:
            state["distance"] = FINISH_DISTANCE
            running = False

        road_offset = (road_offset + speed) % 80

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        keys = pygame.key.get_pressed()
        player.move(keys)

        traffic_timer += 1
        obstacle_timer += 1
        coin_timer += 1
        power_timer += 1
        event_timer += 1

        traffic_frequency = max(35, int(95 - state["distance"] / 45))
        obstacle_frequency = max(45, int(120 - state["distance"] / 55))

        if traffic_timer > traffic_frequency:
            state["objects"].append(make_object("traffic", player))
            traffic_timer = 0

        if obstacle_timer > obstacle_frequency:
            state["objects"].append(make_object(random.choice(["barrier", "oil", "pothole"]), player))
            obstacle_timer = 0

        if coin_timer > 70:
            state["objects"].append(make_object("coin", player))
            coin_timer = 0

        if power_timer > 260:
            state["objects"].append(make_object(random.choice(["nitro", "shield", "repair"]), player))
            power_timer = 0

        if event_timer > 330:
            state["objects"].append(make_object(random.choice(["speed_bump", "nitro_strip"]), player))
            event_timer = 0

        for obj in state["objects"][:]:
            obj.update(speed)

            if obj.off_screen():
                state["objects"].remove(obj)
                continue

            if player.rect.colliderect(obj.rect):
                if obj.kind == "coin":
                    state["coins"] += 1
                    state["score"] += 20
                    state["objects"].remove(obj)

                elif obj.kind in ("nitro", "shield", "repair"):
                    apply_powerup(obj.kind, state)
                    state["objects"].remove(obj)

                elif obj.kind == "nitro_strip":
                    state["active_power"] = "Nitro"
                    state["power_timer"] = 3.0
                    state["objects"].remove(obj)

                elif obj.kind == "speed_bump":
                    state["distance"] = max(0, state["distance"] - 20)
                    state["objects"].remove(obj)

                elif obj.kind in ("traffic", "barrier", "oil", "pothole"):
                    if state["shield"]:
                        state["shield"] = False
                        state["objects"].remove(obj)
                    else:
                        running = False

        draw_road(screen, road_offset)

        for obj in state["objects"]:
            draw_object(screen, obj)

        player.draw(screen)

        power_time = state["power_timer"] if state["active_power"] else 0
        draw_hud(
            screen,
            font,
            state["score"],
            state["coins"],
            state["distance"],
            FINISH_DISTANCE,
            state["active_power"],
            power_time,
            state["shield"]
        )

        pygame.display.flip()

    save_score(username, state["score"], state["distance"])

    return {
        "score": state["score"],
        "coins": state["coins"],
        "distance": int(state["distance"])
    }