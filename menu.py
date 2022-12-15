import os
import platform
import time


class Menu():
    def __init__(self):
        pass

    #############################################################################
    # Functional Methods:
    # These methods are unrelated to the game
    #############################################################################
    def error_message(self, message, duration) -> None:
        self.clear_screen()
        print(message)
        time.sleep(duration)
        self.clear_screen()

    def clear_screen(self) -> None:
        os_name = platform.system()
        if os_name == "Windows" or os_name == "Linux":
            os.system('cls')
        elif os_name == "Darwin":
            os.system('clear')

    def print_message(self, message, duration):
        self.clear_screen()
        print(message)
        time.sleep(duration)
        self.clear_screen()

    # 
    def display_player_turn(self, player) -> None:
        self.print_message("It is now your turn, " + player.name, duration=2.25)

    #
    def display_normal_menu(self) -> int:
        print("\n<1> Roll the dice")
        print("<2> Mortgage a currently owned property")
        print("<3> Trade with another player")
        print("<4> Inspect another player's assets")
        print("<5> Sell a currently owned property")
        print("<6> View all owned assets")
        print("<7> Upgrade an asset")
        print("<8> End your current turn")
        choice = input("\nWhat would you like to do? ")
        return choice

    #
    def display_jail_menu(self, player) -> int:
        print(f"\n\n* TURNS LEFT IN JAIL: {player.turns_in_jail}")
        print("\n<1> Roll the dice")
        print("<2> Mortgage a currently owned property")
        print("<3> Trade with another player")
        print("<4> Inspect another player's assets")
        print("<5> Sell a currently owned property")
        print("<6> View all owned assets")
        print("<7> Upgrade an asset")
        print("<8> End your current turn")
        print(f"<9> Pay ${player.turns_in_jail * 50} to leave")

        if "Get out of Jail free - This card may be kept until needed, or traded/sold" in player.inventory.keys(): 
            print("<0> Use your 'Get out of Jail' card")

        choice = input("What would you like to do? ")
        return choice

    #
    def display_player_info(self, player) -> None:
        # Print the player's money and properties
        print("Name:  ----------------------", player.name)
        print("Token: ----------------------", player.token)
        print("Total Money: ----------------", player.money)
        print("Total Accumulated Wealth: ---", player.wealth)
        # print("Currently Owned Properties: -", player.assets)
    
    def display_player_assets(self, player) -> None:
        self.clear_screen()
        for i in range(len(player.assets)):
            print(f"<{i + 1}> {player.assets[i]}")
        
        input("Press any key to leave...")

    #
    def display_player_position(self, tile) -> None:
        print("\n* You are at " + tile)
    
    def display_tile_info(self, player, game_board) -> None:
        tile = game_board.board[player.position]

        if tile in game_board.properties.keys():
            self.display_property_tile_info(game_board.properties[tile])
        elif tile in game_board.railroads.keys():
            self.display_railroad_tile_info(game_board.railroads[tile])    
        elif tile in game_board.utilities.keys():
            self.display_utility_tile_info(game_board.utilities[tile])
        
    #
    def display_property_tile_info(self, tile) -> None:
        print("Price of property: ----------", tile["price"])
        print("Cost per house: -------------", tile["house_price"])
        print("Color: ----------------------", tile["group"])
        print("Current Owner: --------------", tile["owner"])

    def display_railroad_tile_info(self, tile) -> None:
        print("Price of property: ----------", tile["price"])
        print("Cost of rent: ---------------", tile["rent"])
        print("Type: -----------------------", tile["group"])
        print("Current Owner: --------------", tile["owner"])
    
    def display_utility_tile_info(self, tile) -> None:
        print("* NOTE: ---------------------", "If you own 1/2 properties, the cost of rent is 4x the die roll.")
        print("* ---------------------------", "If both properties are owned, it is 10x the die roll")
        print("\nPrice of property: ----------", tile["price"])
        print("Type: -----------------------", tile["group"])
        print("Current Owner: --------------", tile["owner"])
