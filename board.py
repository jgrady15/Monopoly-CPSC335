# A board game engine that can simulate the movement of players around the board and handle the different properties, spaces, and events on the board.
# A function to roll the dice and move the player's token a certain number of spaces around the board.
# A function to manage the purchase and sale of properties, including the ability to buy and sell houses and hotels, and to pay rent to other players.
# A function to handle the various cards that players can draw, such as Chance and Community Chest cards, which can have various effects on the player's position, money, or property.
# A function to handle the various actions that players can take, such as buying properties, building houses, or paying rent.
# A function to manage the players' money and assets, including the ability to collect and pay taxes, fines, or other fees.
# A function to manage the game flow, including the ability to end the game when a player goes bankrupt or reaches a certain level of wealth.
# A function to display the current state of the game, including the positions of the players on the board, the properties they own, and their current money and assets.

# Create a Board class to represent the game board. This class should have a method for each of the spaces on the board, such as go(), jail(), and parking(). 
# Each of these methods should print a message to the user indicating what happens on that space. For example, go() might print "You landed on Go! Collect $200."

# Create a Player class to represent each player in the game. This class should have attributes to track the player's position on the board, their cash balance, 
# and any properties they own. It should also have methods to allow the player to roll the dice, move around the board, and buy properties.

# Create a Game class to control the overall flow of the game. This class should have a method to initialize the game by creating the Board and Player objects, 
# and a method to run the game loop. The game loop should consist of the following steps:
#   Roll the dice and move the player
#   Check if the player has landed on a special space (e.g. Go, Jail, etc.) and take the appropriate action
#   Check if the player has landed on an unowned property and allow them to buy it, if desired
#   Check if the player has landed on a property owned by another player and pay rent, if applicable
#   Allow the player to take any other actions they want (e.g. buy houses, trade properties, etc.)
#   Check if the game is over (e.g. a player has gone bankrupt) and end the game if necessary
#   Finally, create a main() function to run the game. This function should create a Game object and call the run() method to start the game.

import player
import random
from community_chest import Community_Chest
from chance import Chance
import math

class Board:
    def __init__(self):
        # This dictionary associates each space on the Monopoly board with its corresponding name or action. 
        # For example, if a player lands on space 3, the program could look up the corresponding value in the dictionary 
        # (i.e. "Community Chest") and take the appropriate action.
        self.board = {
            0: "Go!",
            1: "Mediterranean Avenue",
            2: "Community Chest",
            3: "Baltic Avenue",
            4: "Income Tax",
            5: "Reading Railroad",
            6: "Oriental Avenue",
            7: "Chance",
            8: "Vermont Avenue",
            9: "Connecticut Avenue",
            10: "Jail",
            11: "St. Charles Place",
            12: "Electric Company",
            13: "States Avenue",
            14: "Virginia Avenue",
            15: "Pennsylvania Railroad",
            16: "St. James Place",
            17: "Community Chest",
            18: "Tennessee Avenue",
            19: "New York Avenue",
            20: "Free Parking",
            21: "Kentucky Avenue",
            22: "Chance",
            23: "Indiana Avenue",
            24: "Illinois Avenue",
            25: "B. & O. Railroad",
            26: "Atlantic Avenue",
            27: "Ventnor Avenue",
            28: "Water Works",
            29: "Marvin Gardens",
            30: "Go To Jail",
            31: "Pacific Avenue",
            32: "North Carolina Avenue",
            33: "Community Chest",
            34: "Pennsylvania Avenue",
            35: "Short Line Railroad",
            36: "Chance",
            37: "Park Place",
            38: "Luxury Tax",
            39: "Boardwalk"
        }
        
        # This dictionary outlines every single possible property on the Monopoly board with its corresponding name and color
        # Players can buy and collect rent from other players. When a player lands on an unowned property, they can buy the property
        # from the bank. When a player lands on an owned property, they must pay rent to the owner of the property. 
        # Players can also build houses and hotels on their properties to increase the rent that other players must pay.
        self.properties = {
            # ----------------------------------
            # ------------- BROWN --------------
            # ----------------------------------
            "Mediterranean Avenue": {
                "price": 60,
                "house_price": 50,
                "rent": [2, 10, 30, 90, 160, 250],
                "group": "Brown",
                "owner": None
            },
            "Baltic Avenue": {
                "price": 60,
                "house_price": 50,
                "rent": [4, 20, 60, 180, 320, 450],
                "group": "Brown",
                "owner": None
            },
            # ----------------------------------
            # -------------- CYAN --------------
            # ----------------------------------
            "Oriental Avenue": {
                "price": 100,
                "house_price": 50,
                "rent": [6, 30, 90, 270, 400, 550],
                "group": "Cyan",
                "owner": None
            },
            "Vermont Avenue": {
                "price": 100,
                "house_price": 50,
                "rent": [6, 30, 90, 270, 400, 550],
                "group": "Cyan",
                "owner": None
            },
            "Connecticut Avenue": {
                "price": 120,
                "house_price": 50,
                "rent": [8, 40, 100, 300, 450, 600],
                "group": "Cyan",
                "owner": None
            },
            # ----------------------------------
            # ----------- MAGENTA --------------
            # ----------------------------------
            "St. Charles Place": {
                "price": 140,
                "house_price": 100,
                "rent": [10, 50, 150, 450, 625, 750],
                "group": "Magenta",
                "owner": None
            },
            "States Avenue": {
                "price": 140,
                "house_price": 100,
                "rent": [10, 50, 150, 450, 625, 750],
                "group": "Magenta",
                "owner": None
            },
            "Virginia Avenue": {
                "price": 160,
                "house_price": 100,
                "rent": [12, 60, 180, 500, 700, 900],
                "group": "Magenta",
                "owner": None
            },
            # ----------------------------------
            # ------------ ORANGE --------------
            # ----------------------------------
            "St. James Place": {
                "price": 180,
                "house_price": 100,
                "rent": [14, 70, 200, 550, 750, 950],
                "group": "Orange",
                "owner": None
            },
            "Tennessee Avenue": {
                "price": 180,
                "house_price": 100,
                "rent": [14, 70, 200, 550, 750, 950],
                "group": "Orange",
                "owner": None
            },
            "New York Avenue": {
                "price": 200,
                "house_price": 100,
                "rent": [16, 80, 220, 600, 800, 1000],
                "group": "Orange",
                "owner": None
            },
            # ----------------------------------
            # -------------- RED ---------------
            # ----------------------------------
            "Kentucky Avenue": {
                "price": 220,
                "house_price": 150,
                "rent": [18, 90, 250, 700, 875, 1050],
                "group": "Red",
                "owner": None
            },
            "Indiana Avenue": {
                "price": 220,
                "house_price": 150,
                "rent": [18, 90, 250, 700, 875, 1050],
                "group": "Red",
                "owner": None
            },
            "Illinois Avenue": {
                "price": 240,
                "house_price": 150,
                "rent": [20, 100, 300, 750, 925, 1100],
                "group": "Red",
                "owner": None
            },
            # ----------------------------------
            # ------------ YELLOW --------------
            # ----------------------------------
            "Atlantic Avenue": {
                "price": 260,
                "house_price": 150,
                "rent": [22, 110, 330, 800, 975, 1150],
                "group": "Yellow",
                "owner": None
            },
            "Ventnor Avenue": {
                "price": 260,
                "house_price": 150,
                "rent": [22, 110, 330, 800, 975, 1150],
                "group": "Yellow",
                "owner": None
            },
            "Marvin Gardens": {
                "price": 280,
                "house_price": 150,
                "rent": [24, 120, 360, 850, 1025, 1200],
                "group": "Yellow",
                "owner": None
            },
            # ----------------------------------
            # ------------- GREEN --------------
            # ----------------------------------
            "Pacific Avenue": {
                "price": 300,
                "house_price": 200,
                "rent": [26, 130, 390, 900, 1100, 1275],
                "group": "Green",
                "owner": None
            },
            "North Carolina Avenue": {
                "price": 300,
                "house_price": 200,
                "rent": [26, 130, 390, 900, 1100, 1275],
                "group": "Green",
                "owner": None
            },
            "Pennsylvania Avenue": {
                "price": 320,
                "house_price": 200,
                "rent": [28, 150, 450, 1000, 1200, 1400],
                "group": "Green",
                "owner": None
            },
            # ----------------------------------
            # ----------- DARK BLUE ------------
            # ----------------------------------
            "Park Place": {
                "price": 350,
                "house_price": 200,
                "rent": [35, 175, 500, 1100, 1300, 1500],
                "group": "Dark Blue",
                "owner": None
            },
            "Boardwalk": {
                "price": 400,
                "house_price": 200,
                "rent": [50, 200, 600, 1400, 1700, 2000],
                "group": "Dark Blue",
                "owner": None
            },
        }   

        # 
        self.railroads = {
            "Reading Railroad": {
                "price": 200,
                "rent": [25, 50, 100, 200],
                "group": "Railroad",
                "owner": None
            },
            "Pennsylvania Railroad": {
                "price": 200,
                "rent": [25, 50, 100, 200],
                "group": "Railroad",
                "owner": None
            },
            "B. & O. Railroad": {
                "price": 200,
                "rent": [25, 50, 100, 200],
                "group": "Railroad",
                "owner": None
            },
            "Short Line Railroad": {
                "price": 200,
                "rent": [25, 50, 100, 200],
                "group": "Railroad",
                "owner": None
            },
        }

        self.utilities = {
            "Electric Company": {
                "price": 60,
                "house_price": 50,
                "rent": [2, 10, 30, 90, 160, 250],
                "mortgage": 30,
                "group": "Company",
                "owner": None
            },
            "Water Works": {
                "price": 60,
                "house_price": 50,
                "rent": [2, 10, 30, 90, 160, 250],
                "mortgage": 30,
                "group": "Company",
                "owner": None
            },
        }

        self.chance_card_ref = Chance()
        self.community_chest_card_ref = Community_Chest()
    
    # Call this method when we want to move a player to a certain position
    def move_player(self, player) -> None:
        pass

    def go_to_jail(self, player) -> None:
        # Move player to jail
        player.position = 11

        # Set player's jail status to True
        player.in_jail = True

        # Set player's turns_in_jail to 3, these are the amount of turns a player must complete before getting out
        # The only way a player can get out is by:
        # 1. Pay the fine of $50 and be released
        # 2. Using a "Get out of Jail card" to escape
        # 3. Rolling a double to be released for free
        # 4. If you have not yet rolled a double on the third turn, then you must pay the $50 fine and are then released
        player.turns_in_jail = 3
    
    def income_tax(self, player):
        print("You've landed on the Income Tax Tile!\n<1> Pay $200\n<2>Pay 10% of all total assets\n")
        choice = input("Pick your poison: ")

        if choice == "1":
            player.money -= 200
        elif choice == "2":
            player.wealth = player.wealth - (player.wealth * 0.1)
        else:
            print("Invalid choice, please choose from either <1> or <2>")
            self.income_tax(player)

    def calculate_luxury_tax(player):
        # The luxury tax is $100
        tax = 100

        # Deduct the tax from the player's money
        player.money -= tax

        # Return the amount of tax paid
        return tax




