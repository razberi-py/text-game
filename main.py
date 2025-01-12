# adventure.py
# Made by Raz

import sys
import time
import random
from colorama import init, Fore, Style

# colorama
init(autoreset=True)

def slow_print(text, delay=0.02):
    """Prints text to the console slowly for dramatic effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Newline at the end

def print_separator():
    print(Fore.YELLOW + "-" * 50 + Style.RESET_ALL)

class Room:
    def __init__(self, name, description, connections, items=None, ascii_art=None):
        self.name = name
        self.description = description
        self.connections = connections  # Dict of directions to room names
        self.items = items if items else []
        self.ascii_art = ascii_art if ascii_art else ""

class Game:
    def __init__(self):
        self.rooms = {}
        self.current_room = None
        self.inventory = []
        self.is_running = True
        self.setup_rooms()

    def setup_rooms(self):
        """Initialize all rooms and their connections."""
        # ASCII Art for rooms
        entrance_art = r"""
         __________
        /          \
       /  ENTRANCE  \
      /______________\
        """
        hallway_art = r"""
        |-------------|
        |   HALLWAY   |
        |-------------|
        """
        treasure_art = r"""
         ___________
        | TREASURE |
        |   ROOM   |
        |___________|
        """
        exit_art = r"""
         _______
        | EXIT  |
        |_______|
        """
        dark_room_art = r"""
        .   .
         \_/ 
        / | \
         / \
        """
        # Define rooms
        self.rooms['Entrance'] = Room(
            name='Entrance',
            description='You stand at the entrance of a dark and foreboding cave. The air is thick with mystery.',
            connections={'north': 'Hallway'},
            items=['Torch'],
            ascii_art=entrance_art
        )
        self.rooms['Hallway'] = Room(
            name='Hallway',
            description='A narrow hallway stretches before you. The walls are damp, and the faint sound of dripping water echoes.',
            connections={'south': 'Entrance', 'east': 'Treasure Room', 'west': 'Dark Room'},
            items=[],
            ascii_art=hallway_art
        )
        self.rooms['Treasure Room'] = Room(
            name='Treasure Room',
            description='Gold and jewels glitter from every corner. A pedestal stands in the center with a mysterious artifact.',
            connections={'west': 'Hallway'},
            items=['Artifact'],
            ascii_art=treasure_art
        )
        self.rooms['Dark Room'] = Room(
            name='Dark Room',
            description='Total darkness surrounds you. You can hear the faint scurrying of creatures.',
            connections={'east': 'Hallway'},
            items=['Key'],
            ascii_art=dark_room_art
        )
        self.rooms['Exit'] = Room(
            name='Exit',
            description='A beam of sunlight streams through the exit, offering freedom from the cave.',
            connections={'north': 'Treasure Room'},
            items=[],
            ascii_art=exit_art
        )
        self.current_room = self.rooms['Entrance']

    def display_current_room(self):
        """Display the current room's description and available actions."""
        print_separator()
        # ASCII Art
        if self.current_room.ascii_art:
            print(Fore.CYAN + self.current_room.ascii_art + Style.RESET_ALL)
        # Room Name
        slow_print(Fore.GREEN + f"Location: {self.current_room.name}" + Style.RESET_ALL)
        print_separator()
        # Room Description
        slow_print(self.current_room.description)
        # Items in the Room
        if self.current_room.items:
            slow_print(Fore.BLUE + f"You see the following items: {', '.join(self.current_room.items)}" + Style.RESET_ALL)
        print_separator()
        # Available Directions
        available_directions = ', '.join(self.current_room.connections.keys())
        slow_print(Fore.YELLOW + f"Available directions: {available_directions}" + Style.RESET_ALL)
        # Inventory
        if self.inventory:
            slow_print(Fore.MAGENTA + f"Your inventory: {', '.join(self.inventory)}" + Style.RESET_ALL)
        print_separator()

    def get_player_input(self):
        """Prompt the player for input and return the command."""
        command = input(Fore.CYAN + "Enter your command: " + Style.RESET_ALL).strip().lower()
        return command

    def move_player(self, direction):
        """Move the player to a different room if possible."""
        if direction in self.current_room.connections:
            next_room_name = self.current_room.connections[direction]
            self.current_room = self.rooms[next_room_name]
            slow_print(Fore.GREEN + f"You move {direction} to the {self.current_room.name}." + Style.RESET_ALL)
        else:
            slow_print(Fore.RED + "You can't go that way." + Style.RESET_ALL)

    def take_item(self, item):
        """Allow the player to take an item from the room."""
        if item.capitalize() in self.current_room.items:
            self.inventory.append(item.capitalize())
            self.current_room.items.remove(item.capitalize())
            slow_print(Fore.BLUE + f"You have taken the {item.capitalize()}." + Style.RESET_ALL)
        else:
            slow_print(Fore.RED + f"There is no {item.capitalize()} here." + Style.RESET_ALL)

    def use_item(self, item):
        """Allow the player to use an item from the inventory."""
        if item.capitalize() in self.inventory:
            if item.capitalize() == 'Key' and self.current_room.name == 'Treasure Room':
                slow_print(Fore.GREEN + "You use the Key to unlock a hidden compartment, revealing the exit!" + Style.RESET_ALL)
                self.rooms['Treasure Room'].connections['south'] = 'Exit'
                self.inventory.remove('Key')
            else:
                slow_print(Fore.RED + f"You can't use the {item.capitalize()} here." + Style.RESET_ALL)
        else:
            slow_print(Fore.RED + f"You don't have a {item.capitalize()} in your inventory." + Style.RESET_ALL)

    def show_inventory(self):
        """Display the player's inventory."""
        if self.inventory:
            slow_print(Fore.MAGENTA + f"Your inventory: {', '.join(self.inventory)}" + Style.RESET_ALL)
        else:
            slow_print(Fore.MAGENTA + "Your inventory is empty." + Style.RESET_ALL)

    def help_menu(self):
        """Display available commands."""
        print_separator()
        slow_print(Fore.YELLOW + "Available commands:" + Style.RESET_ALL)
        slow_print("- go [direction] (e.g., go north)")
        slow_print("- take [item] (e.g., take torch)")
        slow_print("- use [item] (e.g., use key)")
        slow_print("- inventory")
        slow_print("- help")
        slow_print("- quit")
        print_separator()

    def check_win_condition(self):
        """Check if the player has met the win condition."""
        if self.current_room.name == 'Exit':
            slow_print(Fore.GREEN + "Congratulations! You have successfully navigated the Mystic Cave and found freedom!" + Style.RESET_ALL)
            self.is_running = False

    def process_command(self, command):
        """Process the player's command."""
        if command.startswith('go '):
            direction = command.split(' ')[1]
            self.move_player(direction)
        elif command.startswith('take '):
            item = command.split(' ', 1)[1]
            self.take_item(item)
        elif command.startswith('use '):
            item = command.split(' ', 1)[1]
            self.use_item(item)
        elif command == 'inventory':
            self.show_inventory()
        elif command == 'help':
            self.help_menu()
        elif command == 'quit':
            slow_print(Fore.RED + "Thanks for playing! Goodbye." + Style.RESET_ALL)
            self.is_running = False
        else:
            slow_print(Fore.RED + "Invalid command. Type 'help' to see available commands." + Style.RESET_ALL)

    def run(self):
        """Main game loop."""
        slow_print(Fore.GREEN + "Welcome to the Mystic Cave Adventure!" + Style.RESET_ALL)
        self.help_menu()
        while self.is_running:
            self.display_current_room()
            command = self.get_player_input()
            self.process_command(command)
            self.check_win_condition()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
