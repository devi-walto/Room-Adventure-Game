class Room:
    
    def __init__(self, name: str, image_filepath:str):
        """
        A Room in the Room Adventure game
        @param name: str- The name of the room
        @param image_filepath: str- The RELATIVE filepath to the image of the room
        """
        self.name  = name
        self.image = image_filepath
        self.exits:dict[str,'Room'] = {}
        self.items:dict[str,str] = {}
        self.grabbables = []
        self.inspectables: dict[str, str] = {}
        
    def add_exit(self, direction:str, room:'Room | None') -> None:
        """
        Adds an exit to the room
        @param direction: str- The direction of the exit (e.g. `north`, `south`, `east`, 'west', 'up', 'down')
        @param room: `Room | None` - The room the exit leads to
        """
        self.exits[direction] = room
    
    def add_item(self, label:str, description:str) -> None:
        self.items[label] = description
    
    def add_grabbable(self, item:str) -> None:
        self.grabbables.append(item)
    
    def delete_grabbable(self, item:str):
        self.grabbables.remove(item)
        
    def add_inspectable(self, inspectable:str, inspect_img:str = None) -> None:
        self.inspectable = inspectable
        self.inspect_img = inspect_img
        self.inspectables[inspectable] = inspect_img

        
    class Key:
        def __init__(self, key:str, room_door:str):
            self.key = key
            self.room_door = room_door
            
        @property
        def door_unlocked(self) -> bool:
            return self._door_unlocked
        
        @door_unlocked.setter
        def door_unlocked(self) -> bool:
            if self.key in Room.grabbables:
                self._door_unlocked = True
            
        def create_key(self, key:str) -> str:
            self.key = key
            Room.add_item(self.key, "A key that unlocks the door")
            Room.add_grabbable(self.key)
            
        

    
    def __str__(self) -> str:
        result = f"You are in the {self.name}\n"
        
        result += "You see: "
        for item in self.items.keys():
            result += item + " "
        result += "\n"
            
        result += "Exits: "
        for direction in self.exits.keys():
            result += direction + " " #This is different than in class
        result += "\n"
        
        return result
            