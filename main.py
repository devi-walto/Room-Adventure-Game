# Name: Devin Walton
"""
@dieg00tfb @ALittleRustyyy @SonofCar33
Possible Features and Improvements:
1. Death Room - Introduces a special room that ends the game upon entry. ### COMPLETE ###
2. Status Class for Game State Management - A new Status class to manage the game's current state and handle conditions like win/loss or other game-ending scenarios. ### COMPLETE ###

3. Unlockable Keys - Introduces keys that players can collect and use to unlock locked doors or chests within the game. ### IN PROGRESS ###
4. Handle Unlock Method - Implements a method to manage the unlocking process, allowing players to interact with locks effectively.### IN PROGRESS ###
5. Inspect Item Command - Allows players to examine items closely, uncovering details and hints. ### IN PROGRESS ###

Nice to Have but Not Required:
* Bind Text box to right frame
* Make text box larger
* Change the bg color of the text box

6. Randomized Item Assignment - Places items in different rooms each playthrough for variety. ### STILL DECIDING ###
7. Randomized Traps - Randomly assigns traps to rooms, challenging players with changing obstacles. ### DECIDED AGAINST ###
8. Map of Explored Rooms - Shows a map that updates as players discover new rooms. ### STILL DECIDING ###

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

