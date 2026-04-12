import pygame
import os

pygame.mixer.init()

class MusicPlayer:

    def __init__(self):

        self.tracks = [
            "music/track1.mp3",
            "music/track2.mp3",
            "music/track3.mp3",
            "music/track4.mp3",
            "music/track5.mp3",
            "music/track6.mp3",
            "music/track7.mp3"
        ]

        self.current = 0

        pygame.mixer.music.load(self.tracks[self.current])

        self.font = pygame.font.SysFont(None, 30)


    def play(self):
        pygame.mixer.music.play()


    def stop(self):
        pygame.mixer.music.stop()


    def next(self):

        self.current += 1
        if self.current >= len(self.tracks):
            self.current = 0

        pygame.mixer.music.load(self.tracks[self.current])
        pygame.mixer.music.play()


    def prev(self):

        self.current -= 1
        if self.current < 0:
            self.current = len(self.tracks) - 1

        pygame.mixer.music.load(self.tracks[self.current])
        pygame.mixer.music.play()


    def draw(self, screen):

        text = self.font.render(
            f"Track: {os.path.basename(self.tracks[self.current])}",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (20, 80))