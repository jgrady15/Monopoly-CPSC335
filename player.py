import copy
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

    def inspect_player(self, players, game_board, menu):
        menu.clear_screen()
        for i in range(len(players)):
            if players[i] is not self:
                print(f"<{i + 1}> {players[i].name}")
        choice = input("Which player did you want to look at? ")
    
    #############################################################################
    # Game Feature Methods 
    #############################################################################
    # If you mortgage a property, you'll get half the value back 
    # and you retain ownership of the mortgaged property. 
    # You only need to repay that half plus 10% to unmortgage it.
    def mortgage(self, game_board, menu):
        pass

    # Selling houses is as simple as returning them to the bank, 
    # and taking the cash value for the number of houses sold.
    #  
    # The house's sale value is half that of the purchase value. 
    # In this game, you can only sell houses during your turn.
    def sell(game_board, menu):
        pass

    def trade(self, other_player, game_board, menu):
        GOOJ = "Get out of Jail free - This card may be kept until needed, or traded/sold"
        def trading_faq() -> None:
            print("* Here is how trading works! Select from the options listed below.")
            print("* Once you have selected a valid option, you will continue to add things to your")
            print("* 'Offer Window,' from there you must verify that you agree to trade these things.\n")

            print("* Then all that's left is for the other player to make their offer.")
            print("* Once both parties agree, then the trade will be processed!\n")
        
        def display_trading_interface(player, money, assets, inventory, offer_window) -> list:
            while True:
                menu.clear_screen()
                print(f"------------- It is currently {player.name}'s turn -------------")
                trading_faq()
                print("* Current Offer Window: ", offer_window, "\n")
                print("<1> Add from Assets")
                print("<2> Add from Inventory")
                print("<3> Add Money")
                print("<4> Remove from Offer Window")
                print("<C> Confirm Trade")
                print("<Q> Abandon Trade")
                choice = input("\nChoose from the following: ")
                menu.clear_screen()
                trading_faq()
                print("\n")

                # <1> Assets
                if choice == "1" and assets:
                    while True:
                        menu.clear_screen()
                        print(f"------------- It is currently {player.name}'s turn -------------")
                        menu.display_player_assets(player)
                        print("\n* Current Offer Window: ", offer_window, "\n")
                        print("<Q> Back to previous menu")
                        asset_index = input(f"{player.name} is choosing: Which assets would you like to the offer window? ")
                        menu.clear_screen()
                        
                        if asset_index == "q" or asset_index == "Q":
                            break
                        else:
                            asset_index = int(asset_index) - 1

                        if asset_index < 0 or asset_index > len(assets):
                            menu.error_message(message="Invalid option choose again", duration=2.25)
                            continue
                        else:
                            offer_window.append(assets.pop(asset_index))
                
                elif choice == "1" and not assets:
                    menu.print_message("You don't have any assets to trade!", duration=2.25)
                    continue

                # <2> Inventory
                elif choice == "2" and inventory:
                    while True:
                        menu.clear_screen()
                        print(f"------------- It is currently {player.name}'s turn -------------")
                        print(inventory)
                        print("\n* Current Offer Window: ", offer_window, "\n")
                        print("<Q> Back to previous menu")
                        inventory_index = input(f"{player.name} is choosing: How many cards did you want to put in the offer window? ")
                        menu.clear_screen()
                        
                        if inventory_index == "q" or inventory_index == "Q":
                            break
                        else:
                            inventory_index = int(inventory_index) - 1

                        if inventory_index < 0 or inventory_index > inventory.values()[0]:
                            menu.error_message(message="Invalid option choose again", duration=2.25)
                            continue
                        else:
                            temp = {}
                            temp[GOOJ] = inventory_index
                            offer_window.append(temp)
                            inventory[GOOJ] -= inventory_index
                
                elif choice == "2" and not inventory:
                    menu.print_message("You don't have any cards to trade!", duration=2.25)
                    continue

                elif choice == "3":
                    menu.clear_screen()
                    while True:
                        print(f"------------- It is currently {player.name}'s turn -------------")
                        print("Total Money: ", player.money)
                        print("<Q> Back to previous menu")
                        amount = input("How much money are you offering? ")
                        if amount == "q" or amount == "Q":
                            break
                        else:
                            amount = int(amount)
                        
                        if amount < 0 or amount > player.money:
                            menu.print_message("Impossible, you entered an invalid number, stop trying to break the game.", duration=4)
                        else:
                            money -= amount
                            offer_window.append(amount)

                elif choice == "4" and offer_window:
                    menu.clear_screen()
                    print(f"------------- It is currently {player.name}'s turn -------------")
                    for i in range(len(offer_window)):
                        print(f"<{i + 1}> {offer_window[i]}")
                    
                    print("<Q> Back to previous menu")
                    choice = input("What would you like to remove? ")
                    if choice == "q" or choice == "Q":
                        break
                    else:
                        choice = int(choice) - 1

                    if choice < 0 or choice > len(offer_window):
                        menu.error_message() 
                    else:
                        item = offer_window.pop(choice)
                        if item == GOOJ:
                            inventory[item] += item.values()[0]
                        elif item.isnumerical():
                            money += amount
                        else:
                            assets.append(item)

                elif choice == "4" and not offer_window:
                    menu.error_message(message="Nothing to remove, stop trying to break the game.", duration=2.25)
                    continue

                # <C> Confirm Trade
                elif choice == "c" or choice == "C":
                    print(f"------------- It is currently {player.name}'s turn -------------")
                    print("<Y> to confirm")
                    print("<N> to go back")
                    choice = input("Are you sure? This will finalize your offer window, meaning you can no longer change your offer window.\n* NOTE: This does not mean that you can't cancel the trade to prevent scamming.")
                    if choice == "y" or choice == "Y":
                        return offer_window
                    else:
                        continue

                
                # <Q> Abandon Trade
                elif choice == "q" or choice == "Q":
                    return []
                else:
                    menu.error_message(message="Invalid option choose again", duration=2.25)
                    continue

        def swap_assets(self, other_player, game_board, offer_window_other_player, offer_window_current_player):
            # We can start adding items to our inventory 
            for i in range(len(offer_window_other_player)):
                # If the item is an asset: property, railroad, or utility
                if offer_window_other_player[i] in other_player.assets:
                    other_player_index = other_player.assets.index(offer_window_other_player[i])
                    tile = other_player.assets.pop(other_player_index)
                    
                    if tile in game_board.properties:   game_board.properties[tile]["owner"] = self.name
                    elif tile in game_board.railroads:  game_board.railroads[tile]["owner"] = self.name
                    elif tile in game_board.utilities:  game_board.utilities[tile]["owner"] = self.name
                    
                    self.assets.append(tile)

                # If it's a card
                elif offer_window_other_player[i] in other_player.inventory:
                    other_player.inventory[GOOJ] -= offer_window_other_player[i]
                    
                    if self.inventory:
                        self.inventory[GOOJ] += offer_window_other_player[i]
                    else:
                        self.inventory[GOOJ] = offer_window_other_player[i]

                    if other_player.inventory[GOOJ] == 0:
                        other_player.inventory.clear()

                # If it's money
                else:
                    other_player.money -= offer_window_other_player[i]
                    self.money += offer_window_other_player[i]

            # We can start adding items to our inventory 
            for i in range(len(offer_window_current_player)):
                # If the item is an asset: property, railroad, or utility
                if offer_window_current_player[i] in self.assets:
                    self_index = self.assets.index(offer_window_current_player[i])
                    tile = self.assets.pop(self_index)
                    
                    if tile in game_board.properties:   game_board.properties[tile]["owner"] = other_player.name
                    elif tile in game_board.railroads:  game_board.railroads[tile]["owner"] = other_player.name
                    elif tile in game_board.utilities:  game_board.utilities[tile]["owner"] = other_player.name
                    
                    other_player.assets.append(tile)

                # If it's a card
                elif offer_window_current_player[i] in self.inventory:
                    self.inventory[GOOJ] -= offer_window_current_player[i]
                    
                    if other_player.inventory:
                        other_player.inventory[GOOJ] += offer_window_current_player[i]
                    else:
                        other_player.inventory[GOOJ] = offer_window_current_player[i]

                    if self.inventory[GOOJ] == 0:
                        self.inventory.clear()
                    
                # If it's money
                else:
                    self.money -= offer_window_current_player[i]
                    other_player.money += offer_window_current_player[i]
            

        # Create shallow copies of:
        copy_assets_current_player = copy.deepcopy(self.assets)
        copy_inventory_current_player = copy.deepcopy(self.inventory)
        copy_money_current_player = copy.deepcopy(self.money)
        
        copy_assets_other_player = copy.deepcopy(other_player.assets)
        copy_inventory_other_player = copy.deepcopy(other_player.inventory)
        copy_money_other_player = copy.deepcopy(other_player.money)

        offer_window_current_player = []
        offer_window_other_player = []

        offer_window_current_player = display_trading_interface(player=self, 
                                                                money=copy_money_current_player,
                                                                assets=copy_assets_current_player, 
                                                                inventory=copy_inventory_current_player, 
                                                                offer_window=offer_window_current_player)
        
        if not offer_window_current_player:
            return
        
        offer_window_other_player = display_trading_interface(player=other_player, 
                                                              money=copy_money_other_player,
                                                              assets=copy_assets_other_player, 
                                                              inventory=copy_inventory_other_player, 
                                                              offer_window=offer_window_other_player)

        if not offer_window_other_player:
            return

        print("You are offering: ", offer_window_current_player)
        print(f"For {other_player.name}'s assets: ", offer_window_other_player)
        print("<Y> or <N>")

        other_player_accept = input(f"{other_player.name}, do you agree with this trade? ")
        current_player_accept = input(f"{self.name}, do you agree with this trade? ")

        if other_player_accept == "y" or other_player_accept == "Y" and current_player_accept == "y" or current_player_accept == "Y":
            menu.clear_screen()
            swap_assets(self=self, 
                other_player=other_player, 
                game_board=game_board, 
                offer_window_other_player=offer_window_other_player, 
                offer_window_current_player=offer_window_current_player)
        else:
            return

        



        






    def upgrade_assets(self, game_board, menu):
        menu.display_player_assets(self)

    # Function is broken, need to find some way to calculate all values of all assets
    def __update_wealth(self):
        self.wealth = self.money + math.sum(self.assets.values()["price"])

    def deduct_money(self, amount):
        self.money -= amount
        self.__update_wealth()
        pass


