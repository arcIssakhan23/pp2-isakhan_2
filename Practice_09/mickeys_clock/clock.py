import pygame
import datetime

def draw_clock(screen):

    clock_img = pygame.image.load("images/mickeyclock.png").convert_alpha()
    minute_img = pygame.image.load("images/_minute_hand.png").convert_alpha()
    second_img = pygame.image.load("images/_second_hand.png").convert_alpha()

    screen.fill((255,255,255))

    clock_rect = clock_img.get_rect(center=(500,500))
    screen.blit(clock_img, clock_rect)

    now = datetime.datetime.now()

    seconds = now.second
    minutes = now.minute

    sec_angle = -seconds * 6
    min_angle = -minutes * 6

    sec_hand = pygame.transform.rotate(second_img, sec_angle)
    min_hand = pygame.transform.rotate(minute_img, min_angle)

    center = (500,420)

    sec_rect = sec_hand.get_rect(center=center)
    min_rect = min_hand.get_rect(center=center)

    screen.blit(min_hand, min_rect)
    screen.blit(sec_hand, sec_rect)