import random
import math

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

class Player:
    def __init__(self, name, token):
        self.name = name            # E.g. Player 1, Player 2 etc. 
        self.token = token          # Unique Token to identify player
        self.position = 0           # Everyone starts on Go!
        self.money = 1_500          # Everyone starts with $1,500
        self.wealth = 1_500         # Total wealth is cash + assets: cash is considered an asset
        self.rolled_dice = False    # By default, this variable is false, ONLY TRIGGER TRUE AFTER PLAYER HAS ROLLED DICE
        self.inventory = {}         # Stores cards
        self.assets = []            # Stores possible bought properties, utilities, and railroads as their names, we cross-reference their names with the variables in board.py
        self.in_jail = False        # Player does not start in jail
        self.turns_in_jail = 0      # Player does not have any moves in jail until they land on a "Go to Jail" tile

    def inspect_player(self, current_player, players, game_board, menu):
        menu.clear_screen()
        for i in range(len(players)):
            if players[i] is not current_player:
                print(f"<{i + 1}> {players[i].name}")
        choice = input("Which player did you want to look at? ")

    def upgrade_assets(self, game_board, menu):
        menu.display_player_assets(self)


    def trade_with_player(self, other_player, property, money):
        self.properties.remove(property)
        self.money += money
        other_player.properties.append(property)
        other_player.money -= money
    
    # Function is broken, need to find some way to calculate all values of all assets
    def __update_wealth(self):
        self.wealth = self.money + math.sum(self.assets.values()["price"])

    def deduct_money(self, amount):
        self.money -= amount
        self.__update_wealth()
        pass


