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

import math
import time
import random
from player import Player
from chance import Chance
from community_chest import Community_Chest
from menu import Menu

class Board:
    def __init__(self):
        self.menu = Menu()
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
                "mortgaged": False,          
                "house_qty": 0,      
                "house_price": 50,
                "rent": [2, 10, 30, 90, 160, 250],
                "group": "Brown",
                "owner": None
            },
            "Baltic Avenue": {
                "price": 60,
                "mortgaged": False,
                "house_qty": 0,  
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
                "mortgaged": False,
                "house_qty": 0,                
                "house_price": 50,
                "rent": [6, 30, 90, 270, 400, 550],
                "group": "Cyan",
                "owner": None
            },
            "Vermont Avenue": {
                "price": 100,
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 50,
                "rent": [6, 30, 90, 270, 400, 550],
                "group": "Cyan",
                "owner": None
            },
            "Connecticut Avenue": {
                "price": 120,
                "mortgaged": False,
                "house_qty": 0,                
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
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 100,
                "rent": [10, 50, 150, 450, 625, 750],
                "group": "Magenta",
                "owner": None
            },
            "States Avenue": {
                "price": 140,
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 100,
                "rent": [10, 50, 150, 450, 625, 750],
                "group": "Magenta",
                "owner": None
            },
            "Virginia Avenue": {
                "price": 160,
                "mortgaged": False,
                "house_qty": 0,
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
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 100,
                "rent": [14, 70, 200, 550, 750, 950],
                "group": "Orange",
                "owner": None
            },
            "Tennessee Avenue": {
                "price": 180,
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 100,
                "rent": [14, 70, 200, 550, 750, 950],
                "group": "Orange",
                "owner": None
            },
            "New York Avenue": {
                "price": 200,
                "mortgaged": False,
                "house_qty": 0,
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
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 150,
                "rent": [18, 90, 250, 700, 875, 1050],
                "group": "Red",
                "owner": None
            },
            "Indiana Avenue": {
                "price": 220,
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 150,
                "rent": [18, 90, 250, 700, 875, 1050],
                "group": "Red",
                "owner": None
            },
            "Illinois Avenue": {
                "price": 240,
                "mortgaged": False,
                "house_qty": 0,
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
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 150,
                "rent": [22, 110, 330, 800, 975, 1150],
                "group": "Yellow",
                "owner": None
            },
            "Ventnor Avenue": {
                "price": 260,
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 150,
                "rent": [22, 110, 330, 800, 975, 1150],
                "group": "Yellow",
                "owner": None
            },
            "Marvin Gardens": {
                "price": 280,
                "mortgaged": False,
                "house_qty": 0,
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
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 200,
                "rent": [26, 130, 390, 900, 1100, 1275],
                "group": "Green",
                "owner": None
            },
            "North Carolina Avenue": {
                "price": 300,
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 200,
                "rent": [26, 130, 390, 900, 1100, 1275],
                "group": "Green",
                "owner": None
            },
            "Pennsylvania Avenue": {
                "price": 320,
                "mortgaged": False,
                "house_qty": 0,
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
                "mortgaged": False,
                "house_qty": 0,
                "house_price": 200,
                "rent": [35, 175, 500, 1100, 1300, 1500],
                "group": "Dark Blue",
                "owner": None
            },
            "Boardwalk": {
                "price": 400,
                "mortgaged": False,
                "house_qty": 0,
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
                "mortgaged": False,
                "rent": [25, 50, 100, 200],
                "group": "Railroad",
                "owner": None
            },
            "Pennsylvania Railroad": {
                "price": 200,
                "mortgaged": False,
                "rent": [25, 50, 100, 200],
                "group": "Railroad",
                "owner": None
            },
            "B. & O. Railroad": {
                "price": 200,
                "mortgaged": False,
                "rent": [25, 50, 100, 200],
                "group": "Railroad",
                "owner": None
            },
            "Short Line Railroad": {
                "price": 200,
                "mortgaged": False,
                "rent": [25, 50, 100, 200],
                "group": "Railroad",
                "owner": None
            },
        }

        # This is a special tile, we calculate the rent by:
        # 1. If a player owns 1 tile, and another player lands on it, it is 4x the amount the total number from both rolled die
        # 2. If a player owns both tiles, and another player lands on it, it is 10x the amount the total number from both rolled die
        self.utilities = {
            "Electric Company": {
                "price": 150,
                "mortgaged": False,
                "group": "Company",
                "owner": None
            },
            "Water Works": {
                "price": 150,
                "mortgaged": False,
                "group": "Company",
                "owner": None
            },
        }

        self.chance_card = Chance()
        self.community_chest_card = Community_Chest()
    
    # Call this method when we want to move a player to a certain position
    def move_player(self, player) -> None:
        pass

    # Function to: 
    # 1. Roll the dice
    # 2. Animate the rolling die
    # 3. Output where the player has landed on
    # Returns a tuple 
    def roll_dice(self, player) -> tuple:
        def roll():
            # Print the rolling animation
            for i in range(5):
                # Clear the screen
                self.menu.clear_screen()
            
                # Generate a random dice roll
                dice = random.randint(1, 6)
                print(f"Rolling die... {dice}")
                time.sleep(0.09)
            return dice

        # Clear the screen
        self.menu.clear_screen()
        dice1 = roll()
        dice2 = roll()

        self.menu.clear_screen()
        print(f"{player.name} rolled {dice1} and {dice2}!")
        time.sleep(2.25)

        return (dice1, dice2)

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

    #############################################################################
    # Game Feature Methods <EVENTS>
    #############################################################################
    # TODO: 12/13/22 Finish this function
    def check_property_tile(self, player) -> bool:
        tile = self.board[player.position]

        # We can reduce overhead code using this initial edge case statement
        if tile not in self.properties.keys():
            return False
        
        # Checks if the tile is a property that has no owner, if so then the player has "discovered" it
        # This triggers an event that will prompt the user if they want to purchase this set of land
        if self.properties[tile]["owner"] is None:
            self.menu.print_message(message=player.name + " has discovered " + tile + "!", duration=2.25)
            
            if player.money >= self.properties[tile]["price"]:
                while True:
                    self.menu.display_property_tile_info(self.properties[tile])
                    print("___________________________________________________")
                    print("| \n| <Y> to purchase\n| <N> to move on")
                    choice = input(f"| \n| Would you like to purchase {tile}?\n| ...> ").lower()
                    if choice == "y":
                        property_price = self.properties[tile]["price"]
                        
                        # Take money out of the players account
                        self.menu.print_message(message=f"Deducting ${property_price} from your balance...", duration=2.25)
                        player.money -= self.properties[tile]["price"]     

                        # Then we set the owner of the tile to the player's token
                        self.properties[tile]["owner"] = player.name

                        # Then we proceed to add the tile to the player assets inventory
                        player.assets.append(tile)
                        self.menu.print_message(message=f"Successfully bought {tile}!", duration=2.25)
                        self.menu.clear_screen()
                        break
                    elif choice == "n":
                        break
                    else:
                        self.menu.print_message(message="Invalid option, try again.", duration=1.25)
                self.menu.clear_screen()
            else:
                self.menu.print_message(message="The top G says that you're a brokie that doesn't even have enough money to buy this cheap plot of land!", duration=1.75)
                self.menu.print_message(message="... Get out of here!", duration=1.75)

        # If the tile is mortgaged, then we do not allow the player to collect rent or buy the tile
        elif self.properties[tile]["mortgaged"]:
            self.menu.print_message(message=player.name + " has landed on " + tile + "!", duration=2.25)

        # If the tile the player has landed on is owned by another person, then we trigger the "rent" feature
        elif self.properties[tile]["owner"] is not None:
            self.menu.print_message(message=player.name + " has landed on " + tile + "!", duration=2.25)
            
            owner = self.properties[tile]["owner"]
            print(f"You now owe rent to {owner}!")
            # 1. We inform the player that they must pay rent
            # 2. We check if the current player can "afford" to pay rent
            # 2a. Check if the player will be busted from this, if so, hand over all assets to the other player, and then remove this player from the game
            # 2b. Then we check how many players are still alive, if the amount is > 2, then we keep playing, otherwise the last player will be declared the winner
            # 2c. If they cannot, check if the player has any assets they would like to sell to pay rent
            # 2d. If they still cannot pay, check if they are able to hand over any assets 
            # 3. We deduct the amount of money from the current player
            # 4. We increment the amount of money to the owed player
        
        return True
        
    # TODO: 12/13/22 Finish this function
    def check_railroad_tile(self, player) -> bool:
        tile = self.board[player.position]

        # If the current tile is not a railroad, then we do not need to execute the following statements, we can just return False
        if tile not in self.railroads.keys():
            return False

        # After the edge case, we can reduce overhead code and check if the current railroad has an owner "player"
        # Checks if the tile is a property that has no owner, if so then the player has "discovered" it
        # This triggers an event that will prompt the user if they want to purchase this set of land
        if self.railroads[tile]["owner"] is None:
            self.menu.print_message(message=player.name + " has discovered " + tile + "!", duration=2.25)
            
            if player.money >= self.railroads[tile]["price"]:
                while True:
                    self.menu.display_railroad_tile_info(self.railroads[tile])
                    print("___________________________________________________")
                    print("| \n| <Y> to purchase\n| <N> to move on")
                    choice = input(f"| \n| Would you like to purchase {tile}?\n| ...> ").lower()
                    if choice == "y":
                        price = self.railroads[tile]["price"]
                        
                        # Take money out of the players account
                        self.menu.print_message(message=f"Deducting ${price} from your balance...", duration=2.25)
                        player.money -= self.railroads[tile]["price"]     

                        # Then we set the owner of the tile to the player's token
                        self.railroads[tile]["owner"] = player.token

                        # Then we proceed to add the tile to the player assets inventory
                        player.assets.append(tile)
                        self.menu.print_message(message=f"Successfully bought {tile}!", duration=2.25)
                        break
                    elif choice == "n":
                        break
                    else:
                        self.menu.print_message(message="Invalid option, try again.", duration=1.25)
                self.menu.clear_screen()

            else:
                self.menu.print_message(message="Brokie beta male isn't sigma alpha phi kappa enough to buy this cheap railroad!", duration=1.75)
                self.menu.print_message(message="... Get out of my sight loser!", duration=1.75)

        # If the tile the player has landed on is mortgaged, then we do not allow the player to pay rent and do not allow them to purchase this property.
        elif self.railroads[tile]["mortgaged"]:
            self.menu.print_message(message=player.name + " has landed on " + tile + "!", duration=2.25)

        # If it is owned by another person, then we trigger the "rent" feature
        elif self.railroads[tile]["owner"] is not None:
            self.menu.print_message(message=player.name + " has landed on " + tile + "!", duration=2.25)

            # 1. We inform the player that they must pay rent
            # 2. We check if the current player can "afford" to pay rent
            # 2a. Check if the player will be busted from this, if so, hand over all assets to the other player, and then remove this player from the game
            # 2b. Then we check how many players are still alive, if the amount is > 2, then we keep playing, otherwise the last player will be declared the winner
            # 2c. If they cannot, check if the player has any assets they would like to sell to pay rent
            # 2d. If they still cannot pay, check if they are able to hand over any assets 
            # 3. We deduct the amount of money from the current player
            # 4. We increment the amount of money to the owed player

        return True

    # TODO: 12/13/22 Finish this function
    def check_utilities_tile(self, player) -> bool:
        tile = self.board[player.position]
        
        # If the current tile is not a utility, then we do not need to execute the following statements, we can just return False
        if tile not in self.utilities.keys():
            return False

        # After the edge case, we can reduce overhead code and check if the current utility has an owner "player"
        if self.utilities[tile]["owner"] is None:
            self.menu.print_message(message=player.name + " has discovered " + tile + "!", duration=2.25)

            if player.money >= self.utilities[tile]["price"]:
                while True:
                    self.menu.display_utility_tile_info(self.utilities[tile])
                    print("___________________________________________________")
                    print("| \n| <Y> to purchase\n| <N> to move on")
                    choice = input(f"| \n| Would you like to purchase {tile}?\n| ...> ").lower()
                    if choice == "y":
                        price = self.utilities[tile]["price"]
                        
                        # Take money out of the players account
                        self.menu.print_message(message=f"Deducting ${price} from your balance...", duration=2.25)
                        player.money -= self.utilities[tile]["price"]     

                        # Then we set the owner of the tile to the player's token
                        self.utilities[tile]["owner"] = player.token

                        # Then we proceed to add the tile to the player assets inventory
                        player.assets.append(tile)
                        self.menu.print_message(message=f"Successfully bought {tile}!", duration=2.25)
                        self.menu.clear_screen()
                        break
                    elif choice == "n":
                        break
                    else:
                        self.menu.print_message(message="Invalid option, try again.", duration=1.25)
                self.menu.clear_screen()

        # If the tile is mortgaged, then we do not allow the player to collect rent or buy the tile
        elif self.utilities[tile]["mortgaged"]:
            self.menu.print_message(message=player.name + " has landed on " + tile + "!", duration=2.25)
        
        elif self.utilities[tile]["owner"] is not None:
            self.menu.print_message(message=player.name + " has landed on " + tile + "!", duration=2.25)

            owner = self.utilities[tile]["owner"]
            print(f"You now owe rent to {owner}!")

            # if player.deduct_money()

            # 1. We inform the player that they must pay rent
            # 2. We check if the current player can "afford" to pay rent
            # 2a. Check if the player will bust from this, if so, hand over all assets to the other player, and then remove this player from the game
            # 2b. Then we check how many players are still alive, if the amount is > 2, then we keep playing, otherwise the last player will be declared the winner
            # 2c. If they cannot, check if the player has any assets they would like to sell to pay rent
            # 2d. If they still cannot pay, check if they are able to hand over any assets 
            # 3. We deduct the amount of money from the current player
            # 4. We increment the amount of money to the owed player
        
        return True

    # Checks all possible events unrelated to properties, utilities, and railroads
    # E.g. chance events like pulling a card, going to jail, free parking, etc.
    # For this function, we do not need an edge case, since we have already confirmed
    # -that this tile HAS to be an event tile
    def check_events_tile(self, player):
        tile = self.board[player.position]

        self.menu.print_message(message=f"You landed at {tile}!", duration=2.25)
        if tile == "Income Tax":
            self.menu.print_message("Oof! You must now owe $100 to the bank!", duration=2.25)
            player.money -= 100
            # 1. We inform the player that they must pay taxes
            # 2. We check if the current player can "afford" to pay taxes
            # 2a. Check if the player will bust from this, if so, hand over all assets to the other player, and then remove this player from the game
            # 2b. Then we check how many players are still alive, if the amount is > 2, then we keep playing, otherwise the last player will be declared the winner
            # 2c. If they cannot, check if the player has any assets they would like to sell to pay rent
            pass

        elif tile == "Chance":
            self.chance_event(player)

        elif tile == "Community Chest":
            self.community_chest_event(player)
            
        elif tile == "Go To Jail":
            self.menu.print_message(message="The pigs are here to haul your sorry ass to jail!", duration=2.25)
            self.go_to_jail(player)

        elif tile == "Free Parking":
            # Do nothing
            pass

        elif tile == "Luxury Tax":
            self.menu.print_message(f"Oof! You must now owe $100 to the bank!")
            # 2. We check if the current player can "afford" to pay rent
            # 2a. Check if the player will bust from this, if so, hand over all assets to the other player, and then remove this player from the game
            # 2b. Then we check how many players are still alive, if the amount is > 2, then we keep playing, otherwise the last player will be declared the winner
            # 2c. If they cannot, check if the player has any assets they would like to sell to pay rent
            pass
    
    def chance_event(self, player):
        number = self.chance_card.obtain_chance_card()
        card = self.chance_card.chance_cards[number]
        self.menu.print_message(message=card, duration=3.25)

        # 1: "Advance to Go (Collect $200)",
        if number == 1:
            player.position = 0
            player.money += 200
        
        # 2: "Advance to Illinois Ave. - If you pass Go, collect $200",
        elif number == 2:
            if player.position == 7:
                self.menu.print_message(message="You have passed Go! Collecting $200", duration=2.25)
                player.money += 200

            player.position = 24
            self.check_property_tile(player)
        
        # 3: "Advance to St. Charles Place - If you pass Go, collect $200",
        elif number == 3:
            if player.position >= 36:
                self.menu.print_message(message="You have passed Go! Collecting $200", duration=2.25)
                player.money += 200

            player.position = 11
            self.check_property_tile(player)
        
        # 4: "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times the amount thrown.",
        elif number == 4:
            # Check which chance tile they are on
            # If the player is on the 7th tile, then advance them to electric company
            if player.position == 7:
                self.menu.print_message(message="Advancing to Electric Company...", duration=2.25)
                player.position = 12

            # Otherwise, advance them to Water Works
            elif player.position >= 22:
                self.menu.print_message(message="Advancing to Water Works...", duration=2.25)
                player.position = 28
            
            # Then we check the tile, allowing the player to either purchase or punishing them
            self.check_utilities_tile(player)
        
        # 5: "Advance token to the nearest Railroad and pay owner twice the rental to which he/she is otherwise entitled. If Railroad is unowned, you may buy it from the Bank.",
        elif number == 5:
            # Check which chance tile they are on
            # If the player is on the 7th tile, then advance them to reading railroad
            if player.position == 7:
                self.menu.print_message(message="Advancing to Reading Railroad...", duration=2.25)
                player.position = 5

            # Otherwise, advance them to B. & O. Railroad
            elif player.position == 22:
                self.menu.print_message(message="Advancing to B. & O. Railroad...", duration=2.25)
                player.position = 25
            
            # Otherwise, advance them to Short Line Railroad
            elif player.position == 36:
                self.menu.print_message(message="Advancing to Short Line Railroad...", duration=2.25)
                player.position = 35
            
            # Then we check the tile, allowing the player to either purchase or punishing them
            self.check_railroad_tile(player)
        
        # 6: "Bank pays you dividend of $50",
        elif number == 6:
            player.money += 50
        
        # 7: "Get out of Jail free - This card may be kept until needed, or traded/sold",
        elif number == 7:
            pass
        
        # 8: "Go Back Three Spaces",
        elif number == 8:
            player.position -= 3
            self.discover_tile(player)

        # 9: "Go to Jail - Go directly to Jail - Do not pass Go, do not collect $200",
        elif number == 9:
            self.go_to_jail(player)
        
        # 10: "Make general repairs on all your property - For each house pay $25 - For each hotel $100",
        elif number == 10:
            pass
        
        # 11: "Pay poor tax of $15",
        elif number == 11:
            player.money -= 15
        
        # 12: "Take a trip to Reading Railroad - If you pass Go, collect $200",
        elif number == 12:
            if player.position > 19:
                self.menu.print_message(message="You have passed Go! Collecting $200", duration=2.25)
                player.money += 200

            player.position = 5
            self.check_railroad_tile(player)
        
        # 13: "Take a walk on the Boardwalk - Advance token to Boardwalk",
        elif number == 13:
            player.position = 39
            self.check_property_tile(player)
        
        # 14: "You have been elected Chairman of the Board - Pay each player $50",
        elif number == 14:
            pass

        # 15: "Your building loan matures - Collect $150",
        elif number == 15:
            player.money += 150
        
        # 16: "You have won a crossword competition - Collect $100"
        elif number == 16:
            player.money += 100
    
    def community_chest_event(self, player):
        number = self.community_chest_card.obtain_community_chest_card()
        card = self.community_chest_card.community_chest_cards[number]
        self.menu.print_message(message=card, duration=3.25)

        # 1: "Advance to Go (Collect $200)",
        if number == 1:
            player.position = 0
            player.money += 200
        
        # 2: "Bank error in your favor - Collect $200",
        elif number == 2:
            player.money += 200
        
        # 3: "Doctor's fee - Pay $50",
        elif number == 3:
            player.money -= 50
        
        # 4: "From sale of stock you get $50",
        elif number == 4:
            player.money += 50
        
        # 5: "Get out of Jail free - This card may be kept until needed, or traded/sold",
        elif number == 5:
            pass
        
        # 6: "Go to Jail - Go directly to Jail - Do not pass Go, do not collect $200",
        elif number == 6:
            self.send_player_to_jail(player)
        
        # 7: "Grand Opera Night - Collect $50 from every player for opening night seats",
        elif number == 7:
            pass
        
        # 8: "Holiday Fund matures - Receive $100",
        elif number == 8:
            player.money += 100

        # 9: "Go to Jail - Go directly to Jail - Do not pass Go, do not collect $200",
        elif number == 9:
            self.go_to_jail(player)
        
        # 10: "Make general repairs on all your property - For each house pay $25 - For each hotel $100",
        elif number == 10:
            pass
        
        # 11: "Pay poor tax of $15",
        elif number == 11:
            player.money -= 15
        
        # 12: "Take a trip to Reading Railroad - If you pass Go, collect $200",
        elif number == 12:
            if player.position == 33:
                self.menu.print_message(message="You have passed Go! Collecting $200", duration=2.25)
                player.money += 200
            
            player.position = 5
            self.check_railroad_tile(player)
        
        # 13: "Take a walk on the Boardwalk - Advance token to Boardwalk",
        elif number == 13:            
            player.position = 39
            self.check_property_tile(player)
        
        # 14: "You have been elected Chairman of the Board - Pay each player $50",
        elif number == 14:
            pass

        # 15: "Your building loan matures - Collect $150",
        elif number == 15:
            player.money += 150
        
        # 16: "You have won second prize in a beauty contest - Collect $10"
        elif number == 16:
            player.money += 10

    # Function is designed to discover a tile that a player
    # has not yet bought or owned, or trigger all possible event
    def discover_tile(self, player):
        tile = self.board[player.position]

        if   self.check_property_tile(player=player): return
        elif self.check_railroad_tile(player=player): return
        elif self.check_utilities_tile(player=player): return
        elif self.check_events_tile(player=player): return

    def income_tax(self, player):
        print("You've landed on the Income Tax Tile!\n<1> Pay $200\n<2>Pay 10% of all total assets\n")
        choice = input("Pick your poison: ")

        if choice == "1":
            player.money -= 200
        elif choice == "2":
            player.wealth = player.wealth - (player.wealth * 0.1)
        else:
            self.menu.print_message(message="Invalid choice, please choose from either <1> or <2>", duration=2.25)
            self.income_tax(player)

    def update_player_position(self, player, dice) -> None:
        # Move the player's token the appropriate number of spaces
        player.position = (player.position + dice[0] + dice[1]) % 40


    def calculate_luxury_tax(self, player):
        # The luxury tax is $100
        tax = 100

        # Deduct the tax from the player's money
        player.money -= tax

        # Return the amount of tax paid
        return tax




