import platform
import random
from board import Board
from player import Player
import time
import os

from gmpy2 import mpz

# TODO: We left off on implementing features on the game loop, specifically the choices, and making sure that the menu is linked to all the possible features
#       From there, we can start implementing the actual features of the game, so far we've done most of the "busy" work.
#       
#       So we should start finishing up the "busy" work by completing the menu system, and then begin implementing the features from easy to hard

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


# In Monopoly, if a player is unable to pay taxes when they are required to do so, they must sell or mortgage properties, 
# or sell houses or hotels, in order to raise the necessary funds. If the player is still unable to pay the taxes after 
# selling or mortgaging their properties, they must declare bankruptcy and be eliminated from the game.

# When a player declares bankruptcy, they must turn over all of their cash, properties, and other assets to the player to 
# whom they owe money. For example, if a player owes taxes to the Bank and is unable to pay, they must turn over all of their 
# cash and properties to the Bank. If a player owes rent to another player and is unable to pay, they must turn over all of their cash and 
# properties to that player.

# Once a player has declared bankruptcy and been eliminated from the game, the remaining players continue to 
# play as normal. The game ends when only one player remains, at which point they are declared the winner.


#############################################################################
# Functional Methods:
# These methods are unrelated to the game
#############################################################################
def error_message(message, duration) -> None:
    clear_screen()
    print(message)
    time.sleep(duration)
    clear_screen()

def clear_screen() -> None:
    os_name = platform.system()
    if os_name == "Windows" or os_name == "Linux":
        os.system('cls')
    elif os_name == "Darwin":
        os.system('clear')

def print_message(message, duration):
    clear_screen()
    print(message)
    time.sleep(duration)
    clear_screen()

#############################################################################
# Functional Game Methods 
#############################################################################
def create_player(amount) -> list:
    players = []
    tokens = ["Car", "Hat", "Dog", "Shoe", "Thimble", "Wheelbarrow", "Horse", "Battleship"]
    for i in range(0, amount):
        name = "Player " + str(i + 1)
        players.append(Player(name, tokens.pop(random.randint(1, len(tokens) - 1))))
    
    print(players)
    return players

# Function to: 
# 1. Roll the dice
# 2. Animate the rolling die
# 3. Output where the player has landed on
# Returns a tuple 
def roll_dice(player) -> tuple:
    def roll():
        # Print the rolling animation
        for i in range(5):
            # Clear the screen
            clear_screen()
        
            # Generate a random dice roll
            dice = random.randint(1, 6)
            print(f"Rolling die... {dice}")
            time.sleep(0.09)
        return dice

    # Clear the screen
    clear_screen()
    dice1 = roll()
    dice2 = roll()

    clear_screen()
    print(f"{player.name} rolled {dice1} and {dice2}!")
    time.sleep(2.25)

    return (dice1, dice2)

# 
def display_player_turn(player) -> None:
    print_message("It is now your turn, " + player.name, duration=2.25)

#
def display_normal_menu() -> int:
    print("\n<1> Roll the dice")
    print("<2> Mortgage a currently owned property")
    print("<3> Trade with another player")
    print("<4> Inspect another player's assets")
    print("<5> Sell a currently owned property")
    print("<6> End your current turn")
    choice = input("\nWhat would you like to do? ")
    return choice

#
def display_jail_menu(player) -> int:
    print(f"\n\n* TURNS LEFT IN JAIL: {player.turns_in_jail}")
    print("<1> Roll the dice")
    print("<2> Mortgage a currently owned property")
    print("<3> Trade with another player")
    print("<4> Inspect another player's assets")
    print("<5> Sell a currently owned property")
    print("<6> End your current turn")
    print(f"<7> Pay ${player.turns_in_jail * 50} to leave")

    if "Get out of Jail free - This card may be kept until needed, or traded/sold" in player.inventory.keys(): 
        print("<7> Use your 'Get out of Jail' card")

    choice = input("What would you like to do? ")
    return choice

#
def display_player_info(player) -> None:
    # Print the player's money and properties
    print("Name:  ----------------------", player.name)
    print("Token: ----------------------", player.token)
    print("Total Money: ----------------", player.money)
    print("Total Accumulated Wealth: ---", player.wealth)
    print("Currently Owned Properties: -", player.properties)

#
def display_player_position(tile) -> None:
    print("\n* You are at " + tile)

#
def display_tile_info(player, game_board) -> None:
    tile = game_board.board[player.position]
    if tile in game_board.properties.keys(): 
        print("Price of property: ----------", game_board.properties[tile]["price"])
        print("Cost per house: -------------", game_board.properties[tile]["house_price"])
        print("Color: ----------------------", game_board.properties[tile]["group"])
        print("Current Owner: --------------", game_board.properties[tile]["owner"])
    elif tile in game_board.railroads.keys():
        print("Price of property: ----------", game_board.railroads[tile]["price"])
        print("Cost of rent: ---------------", game_board.railroads[tile]["rent"])
        print("Type: -----------------------", game_board.railroads[tile]["group"])
        print("Current Owner: --------------", game_board.railroads[tile]["owner"])
    elif tile in game_board.utilities.keys():
        print("Price of property: ----------", game_board.utilities[tile]["price"])
        print("Cost of rent: ---------------", game_board.utilities[tile]["rent"])
        print("Type: -----------------------", game_board.utilities[tile]["group"])
        print("Current Owner: --------------", game_board.utilities[tile]["owner"])

#
def player_in_jail(player, game_board) -> None:
    # If the current player is in jail, then we want to display a different menu
    if not player.in_jail:
        return False
    else:
        tile = game_board.board[player.position]
        print("\n* You are on Tile: ----------", tile)
        choice = display_jail_menu(player)

        # <1> Roll the dice
        if choice == "1":
            roll_dice(player=player)
        
        # <2> Mortgage a currently owned property
        elif choice == "2":
            pass

        # <3> Trade with another player
        elif choice == "3":
            pass
        
        # <4> Inspect another player's assets
        elif choice == "4":
            pass

        # <5> Sell a currently owned property
        elif choice == "5":
            pass

        # <6> Pay $50 to leave
        elif choice == "6":
            pass

        # <7> Use your 'Get out of Jail' card
        elif choice == "7" and "Get out of Jail free - This card may be kept until needed, or traded/sold" in player.inventory.keys():
            pass

        # Invalid choice 
        else:
            player_in_jail(player=player, game_board=game_board)
    
    return True

def update_player_position(player):
    dice = roll_dice(player=player)
    # Move the player's token the appropriate number of spaces
    player.position = (player.position + dice[0] + dice[1]) % 40    

#############################################################################
# Game Feature Methods 
#############################################################################
# If you mortgage a property, you'll get half the value back 
# and you retain ownership of the mortgaged property. 
# You only need to repay that half plus 10% to unmortgage it.
def mortgage_property(player, game_board):
    pass

# Selling houses is as simple as returning them to the bank, 
# and taking the cash value for the number of houses sold.
#  
# The house's sale value is half that of the purchase value. 
# In this game, you can only sell houses during your turn.
def sell_property(player, game_board):
    pass

def begin_trade(player1, player2):
    pass

#############################################################################
# Game Feature Methods <EVENTS>
#############################################################################
# TODO: 12/13/22 Finish this function
def check_property_tile(player, game_board) -> bool:
    tile = game_board.board[player.position]

    # We can reduce overhead code using this initial edge case statement
    if tile not in game_board.properties.keys():
        return False
    
    # Checks if the tile is a property that has no owner, if so then the player has "discovered" it
    # This triggers an event that will prompt the user if they want to purchase this set of land
    if game_board.properties[tile]["owner"] is None:
        print_message(message=player.name + " has discovered " + tile + "!", duration=2.25)
        
        if player.money >= game_board.properties[tile]["price"]:
            while True:
                display_tile_info(player=player, game_board=game_board)
                print("___________________________________________________")
                print("| \n| <Y> to purchase\n| <N> to move on")
                choice = input(f"| \n| Would you like to purchase {tile}?\n| ...> ").lower()
                if choice == "y":
                    break
                elif choice == "n":
                    break
                else:
                    print_message(message="Invalid option, try again.", duration=1.25)
        else:
            print_message(message="The top G says that you're a brokie that doesn't even have enough money to buy this cheap plot of land!", duration=1.75)
            print_message(message="... Get out of here!", duration=1.75)

    # If the tile the player has landed on is owned by another person, then we trigger the "rent" feature
    elif game_board.properties[tile]["owner"] is not None:
        print_message(message=player.name + " has landed on " + tile + "!", duration=2.25)

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
def check_railroad_tile(player, game_board) -> bool:
    tile = game_board.board[player.position]

    # If the current tile is not a railroad, then we do not need to execute the following statements, we can just return False
    if tile not in game_board.railroads.keys():
        return False

    # After the edge case, we can reduce overhead code and check if the current railroad has an owner "player"
    # Checks if the tile is a property that has no owner, if so then the player has "discovered" it
    # This triggers an event that will prompt the user if they want to purchase this set of land
    if game_board.railroads[tile]["owner"] is None:
        print_message(message=player.name + " has discovered " + tile + "!", duration=2.25)
        
        if player.money >= game_board.railroads[tile]["price"]:
            while True:
                display_tile_info(player=player, game_board=game_board)
                print("___________________________________________________")
                print("| \n| <Y> to purchase\n| <N> to move on")
                choice = input(f"| \n| Would you like to purchase {tile}?\n| ...> ").lower()
                if choice == "y":
                    break
                elif choice == "n":
                    break
                else:
                    print_message(message="Invalid option, try again.", duration=1.25)

        else:
            print_message(message="Brokie beta male isn't sigma alpha phi kappa enough to buy this cheap railroad!", duration=1.75)
            print_message(message="... Get out of my sight loser!", duration=1.75)

    # If the tile the player has landed on is owned by another person, then we trigger the "rent" feature
    elif game_board.railroads[tile]["owner"] is not None:
        print_message(message=player.name + " has landed on " + tile + "!", duration=2.25)

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
def check_utilities_tile(player, game_board) -> bool:
    tile = game_board.board[player.position]
    
    # If the current tile is not a utility, then we do not need to execute the following statements, we can just return False
    if tile not in game_board.utilities.keys():
        return False

    # After the edge case, we can reduce overhead code and check if the current utility has an owner "player"
    if game_board.utilities[tile]["owner"] is None:
        print_message(message=player.name + " has discovered " + tile + "!", duration=2.25)
        
        if player.money >= game_board.utilities[tile]["price"]:
            while True:
                display_tile_info(player=player, game_board=game_board)
                print("___________________________________________________")
                print("| \n| <Y> to purchase\n| <N> to move on")
                choice = input(f"| \n| Would you like to purchase {tile}?\n| ...> ").lower()
                if choice == "y":
                    break
                elif choice == "n":
                    break
                else:
                    print_message(message="Invalid option, try again.", duration=1.25)

    elif game_board.utilities[tile]["owner"] is not None:
        print_message(message=player.name + " has landed on " + tile + "!", duration=2.25)

        owner = game_board.utilities[tile]["owner"]
        print(f"You now owe rent to {owner}!")

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
def check_events_tile(player, game_board):
    tile = game_board.board[player.position]

    if tile == "Income Tax":
        pass

    elif tile == "Chance":
        pass

    elif tile == "Community Chest":
        pass

    elif tile == "Go To Jail":
        pass

    elif tile == "Free Parking":
        pass

    elif tile == "Luxury Tax":
        pass

# Function is designed to discover a tile that a player
# has not yet bought or owned, or trigger all possible event
def discover_tile(player, game_board):
    tile = game_board.board[player.position]

    if   check_property_tile(player=player, game_board=game_board):  return
    elif check_railroad_tile(player=player, game_board=game_board):  return
    elif check_utilities_tile(player=player, game_board=game_board): return
    elif check_events_tile(player=player, game_board=game_board):    return


def main():
    # This is the game loop
    running = True
    print(" ____________________________________________________")
    print("|                                                    |")
    print("|    Welcome to my text-based version of Monopoly!   |")
    print("|    This engine can only hold 2-8 players at most   |")
    print("|____________________________________________________|")            
    amount = mpz(input("\nTo start a new game, how many players would you like to create? "))
    if amount < 2 or amount > 8:
        clear_screen()
        error_message(message="INVALID, enter a value between 2 and 8.", duration=2.25)
        clear_screen()
        main()
    
    game_board = Board()
    players = create_player(amount)
    while running:

        # Loops infinitely and checks each players until a player has "won" the game
        for i in range(len(players)):
            current_player = players[i]
            display_player_turn(player=current_player)

            # TODO: Create another while loop that allows the player to keep making moves, until they have ended their turn
            while True:
                clear_screen()
                # Displays all the information the player needs to play this game, like current tile, and playercard info    
                display_player_info(player=current_player)
                display_tile_info(player=current_player, game_board=game_board)
                display_player_position(tile=game_board.board[current_player.position])

                # Then we check if the player is in jail, if they are, then we display another menu inside of this function
                if not current_player.in_jail:
                    choice = display_normal_menu()

                    # Only let the player roll the dice if they have not rolled it already
                    # <1> Roll the dice
                    if choice == "1" and not current_player.rolled_dice:
                        update_player_position(player=current_player)
                        discover_tile(player=current_player, game_board=game_board)
                        current_player.rolled_dice = True
                    
                    # If they have already rolled it, then display a message telling them to select another option
                    elif choice == "1" and current_player.rolled_dice:
                        print_message(message="You have already rolled this turn, please select another option", duration=2.25)
                        continue
                    
                    # <2> Mortgage a currently owned property
                    elif choice == "2":
                        mortgage_property(player=current_player, game_board=game_board)

                    # <3> Trade with another player
                    elif choice == "3":
                        pass
                    
                    # <4> Inspect another player's assets
                    elif choice == "4":
                        pass

                    # <5> Sell a currently owned property
                    elif choice == "5":
                        sell_property(player=current_player, game_board=game_board)
                    
                    # <6> End a player's turn
                    elif choice == "6":
                        current_player.rolled_dice = False
                        break

                    else:
                        error_message(message="Invalid option", duration=1.25)
                else:
                    player_in_jail(player=current_player, game_board=game_board)

if __name__ == '__main__':
    main()




