import pygame
import sys
import math

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
TOOLBAR_HEIGHT = 80

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Modes
MODE_BRUSH = "brush"
MODE_LINE = "line"
MODE_RECT = "rectangle"
MODE_SQUARE = "square"
MODE_CIRCLE = "circle"
MODE_RIGHT_TRIANGLE = "right_triangle"
MODE_EQUILATERAL = "equilateral"
MODE_ISO_TRI = "isosceles"
MODE_RHOMBUS = "rhombus"
MODE_ERASER = "eraser"
MODE_BUCKET = "bucket"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Program - With Brush Size")
clock = pygame.time.Clock()


class Button:
    def __init__(self, x, y, w, h, color, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 18)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        if self.text:
            txt = self.font.render(self.text, True, BLACK)
            surface.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class ColorPalette:
    def __init__(self, x, y):
        self.colors = [BLACK, WHITE, RED, GREEN, BLUE, YELLOW,
                       CYAN, MAGENTA, ORANGE, PURPLE, GRAY]
        self.rects = []
        self.selected = BLACK

        for i, c in enumerate(self.colors):
            r = pygame.Rect(x + i * 35, y, 30, 30)
            self.rects.append((r, c))

    def draw(self, surf):
        for r, c in self.rects:
            pygame.draw.rect(surf, c, r)
            pygame.draw.rect(surf, BLACK, r, 1)
            if c == self.selected:
                pygame.draw.rect(surf, WHITE, r, 3)

    def check(self, pos):
        for r, c in self.rects:
            if r.collidepoint(pos):
                self.selected = c
                return True
        return False


# ---------- HELPERS ----------

def norm_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2),
                       abs(x2 - x1), abs(y2 - y1))


def draw_right_triangle(surface, color, start, end, w):
    x1, y1 = start
    x2, y2 = end
    pygame.draw.polygon(surface, color, [(x1, y1), (x2, y2), (x1, y2)], w)


def draw_equilateral_triangle(surface, color, start, end, w):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    side = math.hypot(dx, dy)
    if side == 0:
        return

    h = (math.sqrt(3) / 2) * side

    ux = -dy / side
    uy = dx / side

    apex = (mx + ux * h, my + uy * h)

    pygame.draw.polygon(surface, color, [(x1, y1), (x2, y2), apex], w)


def draw_isosceles_triangle(surface, color, start, end, w):
    x1, y1 = start
    x2, y2 = end

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    dx = x2 - x1
    dy = y2 - y1

    side = math.hypot(dx, dy)
    if side == 0:
        return

    h = side * 0.6

    ux = -dy / side
    uy = dx / side

    apex = (mx + ux * h, my + uy * h)

    pygame.draw.polygon(surface, color, [(x1, y1), (x2, y2), apex], w)


def draw_rhombus(surface, color, start, end, w):
    x1, y1 = start
    x2, y2 = end

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    points = [
        (mx, y1),
        (x2, my),
        (mx, y2),
        (x1, my)
    ]

    pygame.draw.polygon(surface, color, points, w)


def flood_fill(surface, pos, target, replacement):
    if target == replacement:
        return

    w, h = surface.get_size()
    stack = [pos]

    while stack:
        x, y = stack.pop()

        if x < 0 or y < 0 or x >= w or y >= h:
            continue

        if surface.get_at((x, y))[:3] != target:
            continue

        surface.set_at((x, y), replacement)

        stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])


# ---------- PREVIEW ----------

def preview(surface, mode, color, start, end, w):
    if not start or not end:
        return

    x1, y1 = start
    x2, y2 = end

    if mode == MODE_RECT:
        pygame.draw.rect(surface, LIGHT_GRAY,
                         norm_rect(x1, y1, x2, y2), w)

    elif mode == MODE_SQUARE:
        size = max(abs(x2 - x1), abs(y2 - y1))
        x = x1 if x2 >= x1 else x1 - size
        y = y1 if y2 >= y1 else y1 - size
        pygame.draw.rect(surface, LIGHT_GRAY, (x, y, size, size), w)

    elif mode == MODE_LINE:
        pygame.draw.line(surface, LIGHT_GRAY, start, end, w)

    elif mode == MODE_CIRCLE:
        r = int(((x2-x1)**2 + (y2-y1)**2)**0.5)
        pygame.draw.circle(surface, LIGHT_GRAY, start, r, w)

    elif mode == MODE_RIGHT_TRIANGLE:
        pygame.draw.polygon(surface, LIGHT_GRAY,
                            [(x1, y1), (x2, y2), (x1, y2)], w)

    elif mode == MODE_EQUILATERAL:
        draw_equilateral_triangle(surface, LIGHT_GRAY, start, end, w)

    elif mode == MODE_ISO_TRI:
        draw_isosceles_triangle(surface, LIGHT_GRAY, start, end, w)

    elif mode == MODE_RHOMBUS:
        draw_rhombus(surface, LIGHT_GRAY, start, end, w)


# ---------- MAIN ----------

def main():
    canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    drawing = False
    start = None
    current = None

    mode = MODE_BRUSH
    color = BLACK

    # 🔥 NEW SIZE SYSTEM
    brush_size = 6
    eraser_size = 20

    buttons = [
        Button(10, 5, 60, 25, GRAY, "Brush"),
        Button(75, 5, 60, 25, GRAY, "Line"),
        Button(140, 5, 60, 25, GRAY, "Rect"),
        Button(205, 5, 60, 25, GRAY, "Square"),
        Button(270, 5, 60, 25, GRAY, "Circle"),
        Button(335, 5, 70, 25, GRAY, "R-Tri"),
        Button(410, 5, 70, 25, GRAY, "E-Tri"),
        Button(485, 5, 70, 25, GRAY, "Rhombus"),
        Button(560, 5, 60, 25, GRAY, "Eraser"),
        Button(625, 5, 60, 25, WHITE, "Clear"),
        Button(690, 5, 70, 25, GRAY, "Bucket"),
        Button(765, 5, 70, 25, GRAY, "Iso-Tri")
    ]

    # 🔥 SIZE BUTTONS
    plus_btn = Button(860, 5, 30, 25, GRAY, "+")
    minus_btn = Button(860, 35, 30, 25, GRAY, "-")

    palette = ColorPalette(10, 40)

    running = True

    while running:
        mx, my = pygame.mouse.get_pos()
        cy = my - TOOLBAR_HEIGHT

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos

                if y < TOOLBAR_HEIGHT:

                    for i, b in enumerate(buttons):
                        if b.clicked(e.pos):
                            if i == 0: mode = MODE_BRUSH
                            elif i == 1: mode = MODE_LINE
                            elif i == 2: mode = MODE_RECT
                            elif i == 3: mode = MODE_SQUARE
                            elif i == 4: mode = MODE_CIRCLE
                            elif i == 5: mode = MODE_RIGHT_TRIANGLE
                            elif i == 6: mode = MODE_EQUILATERAL
                            elif i == 7: mode = MODE_RHOMBUS
                            elif i == 8: mode = MODE_ERASER
                            elif i == 9: canvas.fill(WHITE)
                            elif i == 10: mode = MODE_BUCKET
                            elif i == 11: mode = MODE_ISO_TRI

                    # size control
                    if plus_btn.clicked(e.pos):
                        brush_size = min(50, brush_size + 2)
                        eraser_size = min(60, eraser_size + 2)

                    if minus_btn.clicked(e.pos):
                        brush_size = max(1, brush_size - 2)
                        eraser_size = max(5, eraser_size - 2)

                    palette.check(e.pos)
                    color = palette.selected

                else:
                    if mode == MODE_BUCKET:
                        target = canvas.get_at((x, cy))[:3]
                        flood_fill(canvas, (x, cy), target, color)
                        continue

                    drawing = True
                    start = (x, cy)
                    current = start

                    if mode == MODE_BRUSH:
                        pygame.draw.circle(canvas, color, start, brush_size)

                    elif mode == MODE_ERASER:
                        pygame.draw.circle(canvas, WHITE, start, eraser_size)

            elif e.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == MODE_BRUSH:
                        pygame.draw.line(canvas, color, start, (mx, cy), brush_size*2)
                        start = (mx, cy)

                    elif mode == MODE_ERASER:
                        pygame.draw.line(canvas, WHITE, start, (mx, cy), eraser_size*2)
                        start = (mx, cy)

                    current = (mx, cy)

            elif e.type == pygame.MOUSEBUTTONUP:
                if drawing and start and current:

                    if mode == MODE_LINE:
                        pygame.draw.line(canvas, color, start, current, 3)

                    elif mode == MODE_RECT:
                        pygame.draw.rect(canvas, color,
                                         norm_rect(*start, *current), 3)

                    elif mode == MODE_SQUARE:
                        x1, y1 = start
                        x2, y2 = current
                        size = max(abs(x2-x1), abs(y2-y1))
                        x = x1 if x2 >= x1 else x1 - size
                        y = y1 if y2 >= y1 else y1 - size
                        pygame.draw.rect(canvas, color, (x, y, size, size), 3)

                    elif mode == MODE_CIRCLE:
                        x1, y1 = start
                        x2, y2 = current
                        r = int(((x2-x1)**2 + (y2-y1)**2)**0.5)
                        pygame.draw.circle(canvas, color, start, r, 3)

                    elif mode == MODE_RIGHT_TRIANGLE:
                        draw_right_triangle(canvas, color, start, current, 3)

                    elif mode == MODE_EQUILATERAL:
                        draw_equilateral_triangle(canvas, color, start, current, 3)

                    elif mode == MODE_ISO_TRI:
                        draw_isosceles_triangle(canvas, color, start, current, 3)

                    elif mode == MODE_RHOMBUS:
                        draw_rhombus(canvas, color, start, current, 3)

                drawing = False
                start = None
                current = None

        # ---------- DRAW ----------
        screen.fill(GRAY)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        if drawing:
            temp = screen.copy()
            preview(temp, mode, color, start, current, 3)
            screen.blit(temp, (0, 0))

        pygame.draw.rect(screen, (200, 200, 200),
                         (0, 0, SCREEN_WIDTH, TOOLBAR_HEIGHT))

        for b in buttons:
            b.draw(screen)

        plus_btn.draw(screen)
        minus_btn.draw(screen)

        palette.draw(screen)

        # SIZE DISPLAY
        font = pygame.font.Font(None, 22)
        screen.blit(font.render(f"Brush: {brush_size}", True, BLACK), (720, 33))
        screen.blit(font.render(f"Eraser: {eraser_size}", True, BLACK), (720, 55))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()