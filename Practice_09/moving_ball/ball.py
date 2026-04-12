import pygame

WIDTH = 600
HEIGHT = 400

class Ball:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.radius = 25


    def move(self, dx, dy):

        new_x = self.x + dx
        new_y = self.y + dy

        if new_x - self.radius >= 0 and new_x + self.radius <= WIDTH:
            self.x = new_x

        if new_y - self.radius >= 0 and new_y + self.radius <= HEIGHT:
            self.y = new_y


    def draw(self, screen):

        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)