from tkinter import(
    #Widgets
    Frame, Label, Button,Text,PhotoImage, Entry,    #Basic widgets
    
    #Constants
    X, Y, BOTH,
    BOTTOM,RIGHT, LEFT,
    DISABLED, NORMAL,END,
    
    #Additional stuff for typehints
    Tk
)

from room import Room
import os

class Game(Frame):
    #Some constants
    EXIT_ACTIONS = ["exit", "quit", "bye","stop","goodbye","leave","end"]


    
    class Status:
        DEFAULT = "I don't understand. Try verb-noun. Valid verbs are go, look and take."
        DEAD = "You are dead. Game Over."
        BAD_EXIT = "Invalid exit. Try again."
        ROOM_CHANGE = "Room Changed"
        GRABBED = "Item grabbed"
        BAD_GRABBABLE = "I can't grab that"
        BAD_ITEM = "I don't see that item"
        BAD_INSPECT = "I can't inspect that"
        DOOR_UNLOCKED = "The door is unlocked"
        DOOR_LOCKED = "The door is locked"
        NEW_KEY = "A new key has been created"
        
    # Game dimensions
    WIDTH = 800
    HEIGHT = 600
    
    def __init__(self, parent: Tk):
        """ 
        Initializes the Game object
        @param parent: Tk- The parent widget representing the main window
        """
        self.inventory = []
        Frame.__init__(self, parent)
        self.pack(fill = BOTH, expand = 1) # Fill the parent widget
        
    def setup_game(self):
        """
        Sets up the game
        """
        #Create the rooms
        r1 = Room("Room 1", os.path.join("images","room1.gif"))
        print("Room 1 created")
        r2 = Room("Room 2", os.path.join("images","room2.gif"))
        print("Room 2 created")
        r3 = Room("Room 3", os.path.join("images","room3.gif"))
        print("Room 3 created")
        r4 = Room("Room 4", os.path.join("images","room4.gif"))
        print("Room 4 created")
        deathroom = Room("Death", os.path.join("images","death.gif"))
        print("Death room created")

        
        # Add exits to the rooms
        r1.add_exit("east", r2)
        r1.add_exit("south", r3)
        
        r2.add_exit("west", r1)
        r2.add_exit("south", r4)
        
        r3.add_exit("north", r1)
        r3.add_exit("east", r4)
        
        r4.add_exit("west", r3)
        r4.add_exit("north", r2)
        r4.add_exit("south", deathroom)
        
        # Add items to the rooms
        r1.add_item("chair", "a beanbag chair")
        r1.add_item("tv", "Its playing a movie")
        print("default items added to room 1")
        
        r2.add_item("knife", "a bloody knife")
        r2.add_item("radio", "a radio playing ominous music")
        print("default items added to room 2")
        
        r3.add_item("book", "a book with a strange symbol on the cover")
        r3.add_item("teacup", "a teacup with warm tea (someone was here recently)")
        print("default items added to room 3")
        
        r4.add_item("key", "a key")
        r4.add_item("note", "a note with a strange message -- type look note to read it")
        print("default items added to room 4")
        
        # Add grabbables to the rooms
        r1.add_grabbable("tv")
        r2.add_grabbable("knife")
        r3.add_grabbable("book")
        r4.add_grabbable("note")
        r4.add_grabbable("key")
        
        #Add inspectables to the rooms -COME BACK TO THIS
        r1.add_inspectable("tv", os.path.join("images","tv_inspect.png"))
        r2.add_inspectable("knife", os.path.join("images","knife_inspect.png"))
        r3.add_inspectable("book", os.path.join("images","book_inspect.png")) # "The book is written in a strange language. You can't read it."
        r4.add_inspectable("note", os.path.join("images","note_inspect.png")) # "You've made it far in my strange game. I'm impressed. But you won't make it out alive. -The Game Master
        
        # Set the starting room for the game
        self.current_room = r1
        
    # Add the GUI elements
    def setup_gui(self):
        
        # Input element (bottom of the screen)
        self.player_input = Entry(self, bg = "black", fg = "white")
        self.player_input.bind("<Return>", self.process_input)
        self.player_input.pack(side = BOTTOM, fill = X)
        self.player_input.focus()
        
        # Image element (room image)
        img = None
        img_width = Game.WIDTH // 2
        self.image_container = Label(
            self, 
            image = img, 
            width = img_width, 
            height = Game.HEIGHT
        )
        self.image_container.image = img # Keep a reference to the image so the garbage collector doesn't delete it
        self.image_container.pack(side = LEFT, fill = Y) # Fill the left side of the screen
        self.image_container.pack_propagate(False) # Prevent resizing
        
        # The info area (right side of the screen)
        text_container_width = Game.WIDTH // 2 # Width of the text area
        text_container = Frame(self, width = text_container_width) # Create a frame for the text area
        
        self.text = Text(
            text_container, # Parent widget
            bg = "lightgrey", # Background color
            fg = "black",      # Text color
            state = DISABLED
        )
        self.text.pack(fill = BOTH, expand = 1) # Fill the text area
        text_container.pack(side = RIGHT, fill = Y) # Fill the right side of the screen
        text_container.pack_propagate(False) # Prevent resizing


    def set_image(self):
        if self.current_room is None:
            img = PhotoImage(file="images/skull.gif")
        elif self.current_room == "Death":
            img = PhotoImage(file="images/skull.gif")
        else:
            img = PhotoImage(file=self.current_room.image)

        # Update the image container with the new room image
        self.image_container.config(image=img)
        self.image_container.image = img  # Keep a reference to prevent garbage collection

    
    # def set_image(self):
    #     if self.current_room == None:
    #         img = PhotoImage(file = "images/skull.gif")
        
    #     elif self.current_room == "Death":
    #         img = PhotoImage(file = "images/skull.gif")
            
    #     else:
    #         img = PhotoImage(file = self.current_room.image)
        
        
    #     self.image_container.config(image = img)
    #     self.image_container.image = img
    
    def set_status(self, status:str):
        self.text.config(state = NORMAL) # Make the text editable
        self.text.delete(1.0, END)
        
        if self.current_room == None or self.current_room == "Death":
            self.text.insert(END, Game.Status.DEAD) #I have different method
        else:
            content = f"{self.current_room}\n"
            content += f"You are carrying: {self.inventory}\n\n"
            content += status
            self.text.insert(END, content)
            
        self.text.config(state = DISABLED)
    
    def clear_entry(self):
        self.player_input.delete(0,END)
    
    # def handle_go(self, destination):
    #     if Room.Key in self.inventory:
    #         print("Key found in inventory")
    #         Room.Key.door_unlocked = True
    #         status = Game.Status.DOOR_UNLOCKED
    #         if destination in self.current_room.exits:
    #             self.current_room = self.current_room.exits[destination]
    #             status = Game.Status.ROOM_CHANGE
        
    #     elif not Room.Key.door_unlocked:
    #         print("Key not found in inventory")
    #         status = Game.Status.DOOR_LOCKED
        
    #     else:
    #         status = Game.Status.BAD_EXIT
    #         print(not Room.Key.door_unlocked)
    #         print(Room.Key in self.inventory)
    
    def handle_go(self, destination):
        # Check if the key is in the inventory
        if "key" in self.inventory:
            print("Key found in inventory")
            Room.Key.door_unlocked = True
            status = Game.Status.DOOR_UNLOCKED

            # If the destination exists in the current room's exits
            if destination in self.current_room.exits:
                self.current_room = self.current_room.exits[destination]
                status = Game.Status.ROOM_CHANGE
                if "key" in self.inventory:
                    self.inventory.remove("key")
            else:
                status = Game.Status.BAD_EXIT
                print("Invalid exit:", destination)
        
        # If the door is locked and the player does not have the key
        elif not Room.Key.door_unlocked:
            print("Key not found in inventory")
            status = Game.Status.DOOR_LOCKED

        # If neither condition is met, it's likely an invalid exit
        else:
            status = Game.Status.BAD_EXIT
            print("Neither key found in inventory nor door unlocked")

        # Set the final status and update the image
        self.set_status(status)
        self.set_image()


        # self.set_status(status)
        # self.set_image()
    
    def handle_look(self, item):
        status = Game.Status.BAD_ITEM
        if item in self.current_room.items:
            status = self.current_room.items[item]
        self.set_status(status)
    
    def handle_take(self, grabbable):
        status = Game.Status.BAD_GRABBABLE
        if grabbable in self.current_room.grabbables: # This is just a list not a dict
            self.inventory.append(grabbable)
            self.current_room.delete_grabbable(grabbable)
            status = Game.Status.GRABBED
        self.set_status(status)
        
        
############################################################################################################################################################################
    # Need to edit the exit_inspect function to handle the Escape key press
    # Needed changes are between the hash-lines
    # @dieg00tfb @ALittleRustyyy @SonofCar33        
        
    def handle_inspect(self, inspectable):
        self.inspected = False
        status = Game.Status.BAD_INSPECT
        if inspectable in self.current_room.inspectables and self.current_room.inspect_img is not None:
            self.inspected = True
            print(f"Inspecting {inspectable}")
            img = PhotoImage(file=self.current_room.inspectables[inspectable])
            self.image_container.config(image=img)
            self.image_container.image = img
            
        else:
            self.status = Game.Status.BAD_INSPECT
            self.set_status(status)
        self.image_container.bind("<Escape>", self.exit_inspect)
            
    # @dieg00tfb @ALittleRustyyy @SonofCar33  
    # This is currently wrong, but I'm trying to bind the Escape key to the exit_inspect function. 
    # It should only work when the player is in inspect mode. Maybe we can use a flag to check if the player is in inspect mode.         
    def exit_inspect(self, event=None):
        print("Exiting inspect mode")
        if self.inspected == True:
            self.current_room.create_key("key")
            print(f"Key created for {self.current_room}")
            self.current_room.add_grabbable("key")
            

        self.set_image()
        self.inspected = False
        status = Game.Status.NEW_KEY
        self.set_status(status)
        
        
        

    # @dieg00tfb @ALittleRustyyy @SonofCar33
    # Wrong implementation, the above code is more right
# Failed Try #1    
    # def exit_inspect(event):
    #     print("Exiting inspect mode")
    #     if self.inspected:
    #         # Room.Key.create_key is used to create or unlock a key
    #         Room.Key.create_key(f"key-{self.current_room}")
    #         print(f"Key created for {self.current_room}")
    #     # Reset the image to the room image
    #     self.set_image()  
    #     # Unbind the Escape key after use
    #     self.image_container.unbind("<Escape>")

    # # Bind the Escape key to the exit_inspect function
    # self.image_container.bind("<Escape>", exit_inspect)
    
# Failed Try #2   
# def handle_inspect(self, inspectable):
#     self.inspected = False  # Set inspected to False initially
#     status = Game.Status.BAD_INSPECT
#     if inspectable in self.current_room.inspectables and self.current_room.inspect_img is not None:
#         self.inspected = True
#         print(f"Inspecting {inspectable}")
#         img = PhotoImage(file=self.current_room.inspectables[inspectable])
#         self.image_container.config(image=img)
#         self.image_container.image = img

#         # Define the exit_inspect function to handle inspect mode exit
#         def exit_inspect():
#             print("Exiting inspect mode")
#             if self.inspected:
#                 # Room.Key.create_key is used to create or unlock a key
#                 Room.Key.create_key(f"key-{self.current_room}")
#                 print(f"Key created for {self.current_room}")
#             # Reset the image to the room image
#             self.set_image()  
#             # Set inspected to False to allow program to continue
#             self.inspected = False

#         # Wait for the player to press Enter to exit inspect mode
#         print("Press Enter to exit inspect mode.")
#         input()  # This waits until the player presses Enter
#         exit_inspect()  # Call the exit_inspect function after input

#     else:
#         self.status = Game.Status.BAD_INSPECT


############################################################################################################################################################################
    
    # Can consider adding functions like eat, drink, etc.
    
    def handle_default(self):
        self.set_status(Game.Status.DEFAULT)
        self.clear_entry()
        
    
    def play(self):
        """ Instantiates the game and starts the game loop """
        self.setup_game()
        self.setup_gui() # Create this method
        self.set_image()
        self.set_status("")
    
    def process_input(self, event):
        action = self.player_input.get()
        action = action.lower()
        
        if action in Game.EXIT_ACTIONS:
            exit()
        if self.current_room == None or self.current_room == "Death":
            self.clear_entry()
            return
        
        words = action.split() # Creates a list, splits at space
        
        if len(words) != 2:
            self.handle_default()
            return
        
        verb = words[0]
        noun = words[1]
        
        match verb:
            case "go": self.handle_go(noun)
            case "look": self.handle_look(noun)
            case "take": self.handle_take(noun)
            case "inspect": self.handle_inspect(noun)
            
        self.clear_entry()