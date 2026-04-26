import pygame

def draw_button(surface, text, x, y, w, h, color):
    font = pygame.font.SysFont("Verdana", 25)  # moved here

    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (0, 0, 0), rect, 2)

    txt = font.render(text, True, (0, 0, 0))
    surface.blit(txt, (
        x + w // 2 - txt.get_width() // 2,
        y + h // 2 - txt.get_height() // 2
    ))
    return rect


def show_main_menu(surface):
    surface.fill((255, 255, 255))

    title_font = pygame.font.SysFont("Verdana", 40)
    title = title_font.render("RACER", True, (0, 0, 0))
    surface.blit(title, (120, 100))

    play = draw_button(surface, "Play", 120, 200, 160, 40, (0, 255, 0))
    lead = draw_button(surface, "Leaderboard", 120, 260, 160, 40, (255, 255, 0))
    seti = draw_button(surface, "Settings", 120, 320, 160, 40, (200, 200, 200))
    quitb = draw_button(surface, "Quit", 120, 380, 160, 40, (255, 0, 0))

    return play, lead, seti, quitb


def show_leaderboard(surface, data):
    font = pygame.font.SysFont("Verdana", 20)  # moved here

    surface.fill((255, 255, 255))

    y = 100
    for i, d in enumerate(data):
        txt = font.render(f"{i+1}. {d['name']} - {d['score']}", True, (0, 0, 0))
        surface.blit(txt, (80, y))
        y += 30