import json
import os


SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}


def load_json(filename, default_data):
    """Loads JSON data from file. If file does not exist, creates it."""
    if not os.path.exists(filename):
        save_json(filename, default_data)
        return default_data

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        save_json(filename, default_data)
        return default_data


def save_json(filename, data):
    """Saves data to JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_settings():
    """Loads game settings."""
    return load_json(SETTINGS_FILE, DEFAULT_SETTINGS.copy())


def save_settings(settings):
    """Saves game settings."""
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    """Loads leaderboard records."""
    return load_json(LEADERBOARD_FILE, [])


def save_score(name, score, distance):
    """Adds score to leaderboard and keeps only top 10."""
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name,
        "score": score,
        "distance": int(distance)
    })

    leaderboard.sort(key=lambda item: item["score"], reverse=True)
    leaderboard = leaderboard[:10]

    save_json(LEADERBOARD_FILE, leaderboard)


def clear_leaderboard():
    """Clears leaderboard."""
    save_json(LEADERBOARD_FILE, [])