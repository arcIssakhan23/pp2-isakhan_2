import pygame
from clock import draw_clock

pygame.init()

screen = pygame.display.set_mode((1000,850))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_clock(screen)

    pygame.display.update()

    clock.tick(60)

pygame.quit()