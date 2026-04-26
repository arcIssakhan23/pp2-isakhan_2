import pygame
import sys

from racer import run_game, WIDTH, HEIGHT
from persistence import load_settings, save_settings, load_leaderboard
from ui import (
    Button,
    ask_username,
    draw_center_text,
    draw_leaderboard,
    draw_settings,
    draw_game_over
)


def main_menu(screen, clock, settings):
    """Main menu screen."""
    font_big = pygame.font.SysFont(None, 60)
    font = pygame.font.SysFont(None, 34)

    play_button = Button(300, 210, 200, 55, "Play")
    leaderboard_button = Button(300, 285, 200, 55, "Leaderboard")
    settings_button = Button(300, 360, 200, 55, "Settings")
    quit_button = Button(300, 435, 200, 55, "Quit")

    while True:
        screen.fill((235, 235, 235))
        draw_center_text(screen, font_big, "TSIS3 Racer Game", 120)

        play_button.draw(screen, font)
        leaderboard_button.draw(screen, font)
        settings_button.draw(screen, font)
        quit_button.draw(screen, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if play_button.clicked(event):
                return "play"
            if leaderboard_button.clicked(event):
                return "leaderboard"
            if settings_button.clicked(event):
                return "settings"
            if quit_button.clicked(event):
                return "quit"

        clock.tick(60)


def leaderboard_screen(screen, clock):
    """Leaderboard screen."""
    back_button = Button(300, 610, 200, 50, "Back")

    while True:
        leaderboard = load_leaderboard()
        draw_leaderboard(screen, leaderboard, back_button)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if back_button.clicked(event):
                return "menu"

        clock.tick(60)


def settings_screen(screen, clock, settings):
    """Settings screen with sound, color, difficulty."""
    font = pygame.font.SysFont(None, 32)

    sound_button = Button(300, 290, 200, 45, "Toggle Sound")
    color_button = Button(300, 350, 200, 45, "Change Color")
    difficulty_button = Button(300, 410, 200, 45, "Difficulty")
    back_button = Button(300, 500, 200, 50, "Back")

    buttons = [sound_button, color_button, difficulty_button, back_button]

    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        draw_settings(screen, settings, buttons)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if sound_button.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if color_button.clicked(event):
                index = colors.index(settings["car_color"])
                settings["car_color"] = colors[(index + 1) % len(colors)]
                save_settings(settings)

            if difficulty_button.clicked(event):
                index = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                save_settings(settings)

            if back_button.clicked(event):
                return "menu"

        clock.tick(60)


def game_over_screen(screen, clock, result, settings):
    """Game over screen."""
    font_big = pygame.font.SysFont(None, 60)
    font = pygame.font.SysFont(None, 34)

    retry_button = Button(300, 390, 200, 55, "Retry")
    menu_button = Button(300, 465, 200, 55, "Main Menu")

    while True:
        draw_game_over(
            screen,
            font_big,
            font,
            result["score"],
            result["distance"],
            result["coins"],
            retry_button,
            menu_button
        )
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry_button.clicked(event):
                return "retry"

            if menu_button.clicked(event):
                return "menu"

        clock.tick(60)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS3 Racer Game")
    clock = pygame.time.Clock()

    settings = load_settings()

    while True:
        action = main_menu(screen, clock, settings)

        if action == "quit":
            break

        elif action == "leaderboard":
            result = leaderboard_screen(screen, clock)
            if result == "quit":
                break

        elif action == "settings":
            result = settings_screen(screen, clock, settings)
            if result == "quit":
                break

        elif action == "play":
            username = ask_username(screen, clock)

            if username is None:
                continue

            while True:
                result = run_game(screen, clock, settings, username)

                if result is None:
                    pygame.quit()
                    sys.exit()

                after_game = game_over_screen(screen, clock, result, settings)

                if after_game == "retry":
                    continue

                if after_game == "quit":
                    pygame.quit()
                    sys.exit()

                if after_game == "menu":
                    break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()