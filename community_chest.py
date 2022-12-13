import random

class Community_Chest:
    def __init__(self):
        # This dictionary associates each Community Chest card with its corresponding action or effect. 
        # When a player draws a Community Chest card, the program can look up the corresponding value in the dictionary 
        # (e.g. "Bank error in your favor - Collect $200") and take the appropriate action.
        self.used_community_chest_cards = set()
        self.community_chest_cards = {
            1: "Advance to Go (Collect $200)",
            2: "Bank error in your favor - Collect $200",
            3: "Doctor's fee - Pay $50",
            4: "From sale of stock you get $50",
            5: "Get out of Jail free - This card may be kept until needed, or traded/sold",
            6: "Go to Jail - Go directly to Jail - Do not pass Go, do not collect $200",
            7: "Grand Opera Night - Collect $50 from every player for opening night seats",
            8: "Holiday Fund matures - Receive $100",
            9: "Income tax refund - Collect $20",
            10: "It is your birthday - Collect $10 from every player",
            11: "Life insurance matures - Collect $100",
            12: "Pay hospital fees of $100",
            13: "Pay school fees of $150",
            14: "Receive $25 consultancy fee",
            15: "You are assessed for street repairs - $40 per house, $115 per hotel",
            16: "You have won second prize in a beauty contest - Collect $10"
        }

    # Method is private and used to generate a random number between 1 - 16 and ensures that no duplicate cards are selected
    def __generate_random_community_chest_card(self):
        if len(self.used_community_chest_cards) == 16:
            self.used_community_chest_cards.clear()
        else:
            while True:
                number = random.randint(1, 16)
                if number not in self.used_community_chest_cards:
                    self.used_community_chest_cards.add(number)
                    return number

    def obtain_community_chest_card(self, player):
        number = self.__generate_random_community_chest_card()