import platform
import random
from board import Board
from menu import Menu
from player import Player
import time
import os

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
# Functional Game Methods 
#############################################################################
def create_player(amount) -> list:
    players = []
    tokens = ["Car", "Hat", "Dog", "Shoe", "Thimble", "Wheelbarrow", "Horse", "Battleship"]
    for i in range(0, amount):
        name = "Player " + str(i + 1)
        players.append(Player(name, tokens.pop(random.randint(0, len(tokens) - 1))))
    
    print(players)
    return players

#
def player_in_jail(current_player, players, game_board, menu) -> None:
    # If the current current_player is in jail, then we want to display a different menu
    if not current_player.in_jail:
        return False
    else:
        # Keep this loop running, as we want to let current_players in jail continue making whatever moves they want until their turn ends
        while True:
            menu.clear_screen()
            menu.display_player_info(current_player)
            tile = game_board.board[current_player.position]
            print("\n* You are on Tile: ----------", tile)
            choice = menu.display_jail_menu(current_player)

            # <1> Roll the dice
            if choice == "1" and not current_player.rolled_dice:
                dice = game_board.roll_dice(current_player)

                # If the current_player has rolled a dice and it is a double
                if dice[0] != dice[1]:
                    current_player.rolled_dice = True
                    current_player.turns_in_jail -= 1
                else:
                    menu.print_message(message=f"You have rolled a {dice[0]} and {dice[1]} have escaped jail!", duration=2.25)

                    # current_player is no longer in jail
                    current_player.in_jail = False

                    # current_player no needs anymore turns in jail
                    current_player.turns_in_jail = 0
                    
                    # Then we can move the current_player 
                    game_board.update_player_position(player=current_player, dice=dice)
                    game_board.discover_tile(current_player)
                    current_player.rolled_dice = False
                    return True
                    
            # If they have already rolled it, then display a message telling them to select another option
            elif choice == "1" and current_player.rolled_dice:
                menu.print_message(message="You have already rolled this turn, please select another option", duration=2.25)
            
            # <2> Mortgage a currently owned property
            elif choice == "2":
                current_player.mortgage(game_board=game_board, menu=menu)

            # <3> Trade with another player
            elif choice == "3":
                if current_player.assets:
                    while True:
                        menu.clear_screen()
                        for i in range(len(players)):
                            if current_player is not players[i]:
                                print(f"<{i + 1}> {players[i].name}: {players[i].token}")

                        other_player = int(input("Which player would you like to trade with? "))
                        menu.clear_screen()
                        if other_player > len(players) or other_player < 0:
                            menu.error_message(message="Invalid option, try again.", duration=2.25)
                        elif current_player == players[other_player]:
                            menu.error_message(message="You can't trade with yourself idiot, select a valid option.", duration=2.25)
                        else:
                            current_player.trade(players[other_player])
                            break
                else:
                    menu.print_message(message="You don't have anything to trade, buy something first or get luckier.", duration=2.25)
            
            # <4> Inspect another player's assets
            elif choice == "4":
                pass

            # <5> Sell a currently owned property
            elif choice == "5":
                current_player.sell(game_board=game_board, menu=menu)

            # <6> View all owned assets
            elif choice == "6":
                menu.display_player_assets(current_player)
                input("Press any key to leave...")

            # <7> Upgrade an asset
            elif choice == "7":
                current_player.upgrade_assets(game_board=game_board, menu=menu)

            # <8> Do not allow the player to end their turn without rolling the dice
            elif choice == "8" and not current_player.rolled_dice:
                menu.print_message(message="You have not yet rolled your dice", duration=2.25)

            # <8> End your current turn only if the player has rolled the dice
            elif choice == "8" and current_player.rolled_dice:
                if current_player.turns_in_jail == 0:
                    menu.print_message(message="You have no more turns left in jail, cough up $50 punk!", duration=2.25)
                    current_player.money -= 50
                    current_player.in_jail = False

                current_player.rolled_dice = False
                return True
            
            # <9> Pay ${player.turns_in_jail * 50} to leave
            elif choice == "9":
                menu.print_message(message="Okay, we'll let you leave then stupid. I hope you don't regret this... >:)", duration=2.25)
                current_player.money -= current_player.turns_in_jail * 50
                current_player.in_jail = False
                current_player.turns_in_jail = 0
                current_player.rolled_dice = False
                return True

            # <0> Use your 'Get out of Jail' card
            elif choice == "0" and "Get out of Jail free - This card may be kept until needed, or traded/sold" in current_player.inventory.keys():
                menu.print_message(message="WHAT... Okay, if the bank says so, then we have no choice but to comply...", duration=2.25)
                current_player.in_jail = False
                current_player.turns_in_jail = 0
                current_player.rolled_dice = False
                return True

            # Invalid choice 
            else:
                menu.error_message(message="Invalid choice, please try again", duration=2.25)

def main():
    print(" ____________________________________________________")
    print("|                                                    |")
    print("|    Welcome to my text-based version of Monopoly!   |")
    print("|    This engine can only hold 2-8 players at most   |")
    print("|____________________________________________________|")            
    amount = int(input("\nTo start a new game, how many players would you like to create? "))
    menu = Menu()
    if amount < 2 or amount > 8:
        menu.error_message(message="INVALID, enter a value between 2 and 8.", duration=2.25)
        main()
    
    game_board = Board()
    players = create_player(amount)
    
    # This is the game loop
    running = True
    while running:

        # Loops infinitely and checks each players until a player has "won" the game
        for i in range(len(players)):
            current_player = players[i]
            menu.display_player_turn(current_player)

            # TODO: Create another while loop that allows the player to keep making moves, until they have ended their turn
            while True:
                menu.clear_screen()
                # Displays all the information the player needs to play this game, like current tile, and playercard info    
                menu.display_player_info(current_player)
                menu.display_player_position(game_board.board[current_player.position])

                # Then we check if the player is in jail, if they are, then we display another menu inside of this function
                if not current_player.in_jail:
                    choice = menu.display_normal_menu()

                    # Only let the player roll the dice if they have not rolled it already
                    # <1> Roll the dice
                    if choice == "1" and not current_player.rolled_dice:
                        dice = game_board.roll_dice(current_player)
                        
                        # If the die rolled is a double, then we allow the player to roll again
                        if dice[0] == dice[1]:
                            menu.print_message(message="You rolled a double! You receive another free roll!", duration=2)
                        else:
                            current_player.rolled_dice = True
                        
                        game_board.update_player_position(current_player=current_player, dice=dice)
                        game_board.discover_tile(current_player)

                        # If the current_player ends up going to jail, their turn will now forcibly end.
                        if current_player.in_jail:
                            break
                    
                    # If they have already rolled it, then display a message telling them to select another option
                    elif choice == "1" and current_player.rolled_dice:
                        menu.print_message(message="You have already rolled this turn, please select another option", duration=2.25)
                        continue
                    
                    # <2> Mortgage a currently owned property
                    elif choice == "2":
                        current_player.mortgage(game_board=game_board, menu=menu)

                    # <3> Trade with another player
                    elif choice == "3":
                        if current_player.assets:
                            while True:
                                menu.clear_screen()
                                for i in range(len(players)):
                                    # Player cannot trade with themself and the player being traded must have assets available
                                    if current_player is not players[i] and players[i].assets:
                                        print(f"<{i + 1}> {players[i].name}: {players[i].token}")

                                other_player = int(input("Which player would you like to trade with? ")) - 1
                                menu.clear_screen()
                                if other_player > len(players) or other_player < 0:
                                    menu.error_message(message="Invalid option, try again.", duration=2.25)
                                elif current_player == players[other_player]:
                                    menu.error_message(message="You can't trade with yourself idiot, select a valid option.", duration=2.25)
                                else:
                                    if players[other_player].assets:
                                        current_player.trade(other_player=players[other_player], game_board=game_board, menu=menu)
                                    else:
                                        menu.print_message(message=f"{players[other_player].name} has no available assets to trade!", duration=2.25)
                                    break
                        else:
                            menu.print_message(message="You don't have anything to trade, buy something first or get luckier.", duration=2.25)
                    
                    # <4> Inspect another player's assets
                    elif choice == "4":
                        current_player.inspect_player(players=players, game_board=game_board, menu=menu)

                    # <5> Sell a currently owned property
                    elif choice == "5":
                        current_player.sell(game_board=game_board, menu=menu)
                    
                    # print("<6> View all owned assets")
                    elif choice == "6":
                        menu.display_player_assets(current_player)
                        input("Press any key to leave...")

                    # print("<7> Upgrade an asset")
                    elif choice == "7" and len(current_player.assets) > 0:
                        current_player.upgrade_assets(game_board=game_board, menu=menu)
                    
                    elif choice == "7" and len(current_player.assets) == 0:
                        menu.print_message(message="No assets to upgrade! Purchase a property first!", duration=2.25)

                    # <8> End a player's turn
                    elif choice == "8" and current_player.rolled_dice:
                        current_player.rolled_dice = False
                        break

                    else:
                        menu.error_message(message="Invalid option", duration=1.25)
                else:
                    player_in_jail(player=current_player, game_board=game_board, menu=menu)
                    break
                
                # Update method for wealth
                # current_player.wealth = current_player.money + current_player.assets

if __name__ == '__main__':
    main()




