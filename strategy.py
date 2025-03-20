class Strategy:
    """
    Implements perfect blackjack strategy.

    This class provides decision-making for the player based on perfect strategy,
    using the player's hand and the dealer's upcard as inputs.
    """

    # Actions
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    SPLIT = "split"

    def __init__(self):
        """Initialize the strategy with predefined decision tables."""
        # Define strategy tables according to the specification
        # Hard totals strategy table (player_total -> dealer_upcard -> action)
        self.hard_strategy = {
            8: {
                2: self.HIT,
                3: self.HIT,
                4: self.HIT,
                5: self.HIT,
                6: self.HIT,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            9: {
                2: self.HIT,
                3: self.DOUBLE,
                4: self.DOUBLE,
                5: self.DOUBLE,
                6: self.DOUBLE,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            10: {
                2: self.DOUBLE,
                3: self.DOUBLE,
                4: self.DOUBLE,
                5: self.DOUBLE,
                6: self.DOUBLE,
                7: self.DOUBLE,
                8: self.DOUBLE,
                9: self.DOUBLE,
                10: self.HIT,
                "A": self.HIT,
            },
            11: {
                2: self.DOUBLE,
                3: self.DOUBLE,
                4: self.DOUBLE,
                5: self.DOUBLE,
                6: self.DOUBLE,
                7: self.DOUBLE,
                8: self.DOUBLE,
                9: self.DOUBLE,
                10: self.DOUBLE,
                "A": self.DOUBLE,
            },
            12: {
                2: self.HIT,
                3: self.HIT,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            13: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            14: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            15: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            16: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            17: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.STAND,
                8: self.STAND,
                9: self.STAND,
                10: self.STAND,
                "A": self.STAND,
            },
            18: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.STAND,
                8: self.STAND,
                9: self.STAND,
                10: self.STAND,
                "A": self.STAND,
            },
            19: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.STAND,
                8: self.STAND,
                9: self.STAND,
                10: self.STAND,
                "A": self.STAND,
            },
            20: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.STAND,
                8: self.STAND,
                9: self.STAND,
                10: self.STAND,
                "A": self.STAND,
            },
            21: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.STAND,
                8: self.STAND,
                9: self.STAND,
                10: self.STAND,
                "A": self.STAND,
            },
        }

        # Soft totals strategy table (soft total -> dealer_upcard -> action)
        self.soft_strategy = {
            13: {
                2: self.HIT,
                3: self.HIT,
                4: self.HIT,
                5: self.DOUBLE,
                6: self.DOUBLE,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            14: {
                2: self.HIT,
                3: self.HIT,
                4: self.HIT,
                5: self.DOUBLE,
                6: self.DOUBLE,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            15: {
                2: self.HIT,
                3: self.HIT,
                4: self.DOUBLE,
                5: self.DOUBLE,
                6: self.DOUBLE,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            16: {
                2: self.HIT,
                3: self.HIT,
                4: self.DOUBLE,
                5: self.DOUBLE,
                6: self.DOUBLE,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            17: {
                2: self.HIT,
                3: self.DOUBLE,
                4: self.DOUBLE,
                5: self.DOUBLE,
                6: self.DOUBLE,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            18: {
                2: self.STAND,
                3: self.DOUBLE,
                4: self.DOUBLE,
                5: self.DOUBLE,
                6: self.DOUBLE,
                7: self.STAND,
                8: self.STAND,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            19: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.DOUBLE,
                7: self.STAND,
                8: self.STAND,
                9: self.STAND,
                10: self.STAND,
                "A": self.STAND,
            },
            20: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.STAND,
                8: self.STAND,
                9: self.STAND,
                10: self.STAND,
                "A": self.STAND,
            },
            21: {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.STAND,
                8: self.STAND,
                9: self.STAND,
                10: self.STAND,
                "A": self.STAND,
            },
        }

        # Pairs strategy table (pair_card -> dealer_upcard -> action)
        self.pair_strategy = {
            "2": {
                2: self.SPLIT,
                3: self.SPLIT,
                4: self.SPLIT,
                5: self.SPLIT,
                6: self.SPLIT,
                7: self.SPLIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            "3": {
                2: self.SPLIT,
                3: self.SPLIT,
                4: self.SPLIT,
                5: self.SPLIT,
                6: self.SPLIT,
                7: self.SPLIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            "4": {
                2: self.HIT,
                3: self.HIT,
                4: self.HIT,
                5: self.SPLIT,
                6: self.SPLIT,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            "5": {
                2: self.DOUBLE,
                3: self.DOUBLE,
                4: self.DOUBLE,
                5: self.DOUBLE,
                6: self.DOUBLE,
                7: self.DOUBLE,
                8: self.DOUBLE,
                9: self.DOUBLE,
                10: self.HIT,
                "A": self.HIT,
            },
            "6": {
                2: self.SPLIT,
                3: self.SPLIT,
                4: self.SPLIT,
                5: self.SPLIT,
                6: self.SPLIT,
                7: self.HIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            "7": {
                2: self.SPLIT,
                3: self.SPLIT,
                4: self.SPLIT,
                5: self.SPLIT,
                6: self.SPLIT,
                7: self.SPLIT,
                8: self.HIT,
                9: self.HIT,
                10: self.HIT,
                "A": self.HIT,
            },
            "8": {
                2: self.SPLIT,
                3: self.SPLIT,
                4: self.SPLIT,
                5: self.SPLIT,
                6: self.SPLIT,
                7: self.SPLIT,
                8: self.SPLIT,
                9: self.SPLIT,
                10: self.SPLIT,
                "A": self.SPLIT,
            },
            "9": {
                2: self.SPLIT,
                3: self.SPLIT,
                4: self.SPLIT,
                5: self.SPLIT,
                6: self.SPLIT,
                7: self.STAND,
                8: self.SPLIT,
                9: self.SPLIT,
                10: self.STAND,
                "A": self.STAND,
            },
            "10": {
                2: self.STAND,
                3: self.STAND,
                4: self.STAND,
                5: self.STAND,
                6: self.STAND,
                7: self.STAND,
                8: self.STAND,
                9: self.STAND,
                10: self.STAND,
                "A": self.STAND,
            },
            "A": {
                2: self.SPLIT,
                3: self.SPLIT,
                4: self.SPLIT,
                5: self.SPLIT,
                6: self.SPLIT,
                7: self.SPLIT,
                8: self.SPLIT,
                9: self.SPLIT,
                10: self.SPLIT,
                "A": self.SPLIT,
            },
        }

    def decide_action(self, player_hand, dealer_upcard):
        """
        Determine the best action for the player based on perfect strategy.

        Args:
            player_hand (Hand): The player's current hand.
            dealer_upcard (Card): The dealer's face-up card.

        Returns:
            str: The recommended action (hit, stand, double, split).
        """
        dealer_rank = dealer_upcard.rank

        # Check for pairs first (if exactly 2 cards of the same rank)
        if player_hand.is_pair():
            rank = player_hand.cards[0].rank
            return self.pair_strategy.get(rank, {}).get(dealer_rank, self.HIT)

        # Check for soft hands (if hand contains an ace counting as 11)
        elif player_hand.is_soft():
            total = player_hand.get_value()
            return self.soft_strategy.get(total, {}).get(dealer_rank, self.STAND)

        # Otherwise, use hard strategy
        else:
            total = player_hand.get_value()
            # For low totals not explicitly in our table, default to hit
            if total < 8:
                return self.HIT
            return self.hard_strategy.get(total, {}).get(dealer_rank, self.STAND)
