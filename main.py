# Name: Devin Walton
"""
Features and Improvements:
1. Death Room - Introduces a special room that ends the game upon entry.
2. Inspect Item Command - Allows players to examine items closely, uncovering details and hints.
3. Randomized Item Assignment - Places items in different rooms each playthrough for variety.
4. Randomized Traps - Randomly assigns traps to rooms, challenging players with changing obstacles.
5. Map of Explored Rooms - Shows a map that updates as players discover new rooms.
6. Status Class for Game State Management - A new Status class to manage the game's current state and handle conditions like win/loss or other game-ending scenarios.
7. Unlockable Keys - Introduces keys that players can collect and use to unlock locked doors or chests within the game.
8. Handle Unlock Method - Implements a method to manage the unlocking process, allowing players to interact with locks effectively.
"""
# Date: 10/25/2024
# Description: Room Adventure Game with a GUI

from tkinter import Tk
from game import Game

window = Tk()
window.title("Room Adventure Game")
game = Game(window)
game.play()
window.mainloop()

