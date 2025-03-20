import random
from card import Card


class Deck:
    """
    Represents an infinite deck of cards with replacement.

    In this implementation, cards are randomly selected each time,
    effectively simulating an infinite deck (cards are replaced after being dealt).
    """

    # All possible card ranks in a standard deck
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        """Initialize the infinite deck."""
        pass  # No initialization needed for an infinite deck

    def deal_card(self):
        """
        Deal a random card from the deck.

        Returns:
            Card: A randomly selected card.
        """
        # Randomly select a rank from the available ranks
        rank = random.choice(self.RANKS)
        card = Card(rank)
        print(f"DEBUG: Dealt card: {card}")
        return card
