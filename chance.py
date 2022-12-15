import random

class Chance:
    def __init__(self):
        # This dictionary associates each Chance card with its corresponding action or effect. 
        # When a player draws a Chance card, the program can look up the corresponding value in the dictionary 
        # (e.g. "Advance to Go (Collect $200)") and take the appropriate action.
        self.used_chance_cards = set()
        self.chance_cards = {
            1: "Advance to Go (Collect $200)",
            2: "Advance to Illinois Ave. - If you pass Go, collect $200",
            3: "Advance to St. Charles Place - If you pass Go, collect $200",
            4: "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times the amount thrown.",
            5: "Advance token to the nearest Railroad and pay owner twice the rental to which he/she is otherwise entitled. If Railroad is unowned, you may buy it from the Bank.",
            6: "Bank pays you dividend of $50",
            7: "Get out of Jail free - This card may be kept until needed, or traded/sold",
            8: "Go Back Three Spaces",
            9: "Go to Jail - Go directly to Jail - Do not pass Go, do not collect $200",
            10: "Make general repairs on all your property - For each house pay $25 - For each hotel $100",
            11: "Pay poor tax of $15",
            12: "Take a trip to Reading Railroad - If you pass Go, collect $200",
            13: "Take a walk on the Boardwalk - Advance token to Boardwalk",
            14: "You have been elected Chairman of the Board - Pay each player $50",
            15: "Your building loan matures - Collect $150",
            16: "You have won a crossword competition - Collect $100"
        }

    # Method is private and used to generate a random number between 1 - 16 and ensures that no duplicate cards are selected
    def __generate_random_chance_card(self):
        if len(self.used_chance_cards) == 16:
            self.used_chance_cards.clear()
        else:
            while True:
                number = random.randint(1, 16)
                if number not in self.used_chance_cards:
                    self.used_chance_cards.add(number)
                    return number
    
    def obtain_chance_card(self) -> int:
        number = self.__generate_random_chance_card()
        return number