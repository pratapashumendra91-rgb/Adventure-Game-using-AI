# ADVANCED Interactive "Choose Your Own Adventure" Game
# Features:
# - Inventory System
# - Health System
# - Multiple Endings
# - Save/Load Game
# - Sound Effects
# - Typewriter Animation
# - Random Events
# - Advanced Story Branching

import os
import time
import random
import json

# Sound Support (Optional)
try:
    from playsound import playsound
    SOUND = True
except:
    SOUND = False

# Player Data
player = {
    "health": 100,
    "inventory": [],
    "name": "",
    "location": "start"
}

# -----------------------------
# Utility Functions
# -----------------------------

def play_sound(sound):
    if SOUND and os.path.exists(sound):
        playsound(sound)


def typewriter(text, speed=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(speed)
    print()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def save_game():
    with open("savegame.json", "w") as f:
        json.dump(player, f)
    typewriter("\nGame Saved Successfully!")


def load_game():
    global player
    try:
        with open("savegame.json", "r") as f:
            player = json.load(f)
        typewriter("Game Loaded Successfully!")
        game_loop()
    except:
        typewriter("No Save File Found!")


def show_status():
    print("\n" + "="*40)
    print(f"Health: {player['health']}")
    print(f"Inventory: {player['inventory']}")
    print("="*40)

# -----------------------------
# Game Scenes
# -----------------------------

def intro():
    clear()
    play_sound("sounds/intro.mp3")
    typewriter("🌟 THE LOST KINGDOM 🌟")
    player["name"] = input("Enter your name, explorer: ")

    typewriter(f"\nWelcome {player['name']}!")
    typewriter("You enter a mysterious jungle searching for treasure...")

    game_loop()


def game_loop():
    show_status()

    if player["location"] == "start":
        start()
    elif player["location"] == "temple":
        temple()
    elif player["location"] == "cave":
        cave()
    elif player["location"] == "treasure":
        treasure()


def start():
    typewriter("\nYou see two paths ahead.")
    choice = input("Left path or Right path? (left/right/save): ").lower()

    if choice == "left":
        player["location"] = "temple"
    elif choice == "right":
        player["location"] = "cave"
    elif choice == "save":
        save_game()

    game_loop()


def temple():
    typewriter("\nYou enter an ancient temple...")

    if "key" not in player["inventory"]:
        typewriter("You found a golden key!")
        player["inventory"].append("key")

    choice = input("Explore deeper or go back? (explore/back): ").lower()

    if choice == "explore":
        random_event()
        player["location"] = "treasure"
    else:
        player["location"] = "start"

    game_loop()


def cave():
    typewriter("\nYou enter a dark cave...")

    damage = random.randint(5, 20)
    player["health"] -= damage

    typewriter(f"Bats attack you! You lose {damage} health!")

    if player["health"] <= 0:
        lose()
        return

    choice = input("Continue or go back? (continue/back): ").lower()

    if choice == "continue":
        player["location"] = "treasure"
    else:
        player["location"] = "start"

    game_loop()


def treasure():
    typewriter("\nYou discover the treasure chamber!")

    if "key" in player["inventory"]:
        win()
    else:
        typewriter("The chest is locked!")
        player["location"] = "start"
        game_loop()


def random_event():
    event = random.choice(["heal", "trap", "treasure"])

    if event == "heal":
        player["health"] += 10
        typewriter("You found healing herbs! +10 health")

    elif event == "trap":
        damage = random.randint(5, 15)
        player["health"] -= damage
        typewriter(f"Trap triggered! Lose {damage} health")

    else:
        player["inventory"].append("gem")
        typewriter("You found a rare gem!!")

# -----------------------------
# Endings
# -----------------------------

def win():
    play_sound("sounds/win.mp3")
    typewriter("\n🏆 YOU WON THE GAME!!!")
    restart()


def lose():
    play_sound("sounds/lose.mp3")
    typewriter("\n💀 GAME OVER:)")
    restart()


def restart():
    choice = input("Play again? (yes/no/load): ").lower()

    if choice == "yes":
        reset()
        intro()
    elif choice == "load":
        load_game()
    else:
        typewriter("Thanks for playing!!!")


def reset():
    global player
    player = {
        "health": 100,
        "inventory": [],
        "name": "",
        "location": "start"
    }


# -----------------------------
# Start Game
# -----------------------------

if __name__ == "__main__":
    intro()

