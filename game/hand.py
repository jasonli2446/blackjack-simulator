class Hand:
    """
    Represents a blackjack hand.

    Attributes:
        cards (list): List of Card objects in the hand.
    """

    def __init__(self):
        """Initialize an empty hand."""
        self.cards = []

    def add_card(self, card):
        """
        Add a card to the hand.

        Args:
            card (Card): The card to add to the hand.
        """
        self.cards.append(card)

    def clear(self):
        """Clear all cards from the hand."""
        self.cards = []

    def get_value(self):
        """
        Calculate the value of the hand, accounting for aces.

        Returns:
            int: The value of the hand.

        Note:
            Aces are counted as 11 unless this would cause the hand to bust,
            in which case they count as 1.
        """
        value = sum(card.value for card in self.cards)

        # Count aces and adjust value if necessary to avoid busting
        ace_count = sum(1 for card in self.cards if card.rank == "A")
        while value > 21 and ace_count > 0:
            value -= 10  # Reduce ace value from 11 to 1
            ace_count -= 1

        return value

    def is_blackjack(self):
        """
        Check if the hand is a natural blackjack (an ace and a 10-value card).

        Returns:
            bool: True if the hand is a natural blackjack, False otherwise.
        """
        return len(self.cards) == 2 and self.get_value() == 21

    def is_pair(self):
        """
        Check if the hand consists of exactly two cards of the same rank.

        Returns:
            bool: True if the hand is a pair, False otherwise.
        """
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def is_soft(self):
        """
        Check if the hand is a soft hand (contains an ace counting as 11).

        Returns:
            bool: True if the hand is soft, False otherwise.
        """
        for card in self.cards:
            if card.rank == "A":
                # Calculate value without this ace
                other_cards_value = sum(c.value for c in self.cards if c != card)
                # If counting this ace as 11 doesn't bust, it's a soft hand
                if other_cards_value + 11 <= 21:
                    return True
        return False

    def __repr__(self):
        """
        Return a string representation of the hand.

        Returns:
            str: The string representation of the hand.
        """
        return (
            f"Hand({', '.join(str(card) for card in self.cards)}): {self.get_value()}"
        )
