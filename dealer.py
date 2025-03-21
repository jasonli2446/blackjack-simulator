from hand import Hand


class Dealer:
    """
    Represents the dealer in the blackjack game.

    Attributes:
        hand (Hand): The dealer's current hand.
        upcard (Card): The dealer's face-up card.
    """

    def __init__(self):
        """Initialize a dealer with an empty hand."""
        self.hand = Hand()
        self.upcard = None

    def set_upcard(self):
        """Set the upcard to the first card in the dealer's hand."""
        if self.hand.cards:
            self.upcard = self.hand.cards[0]

    def should_hit(self):
        """
        Determine if the dealer should hit according to fixed rules.
        Returns:
            bool: True if the dealer should hit, False otherwise.
        """
        # Hit on soft 17
        if self.hand.get_value() == 17 and self.hand.is_soft():
            return True
        return self.hand.get_value() < 17

    def clear_hand(self):
        """Clear the dealer's hand and upcard."""
        self.hand.clear()
        self.upcard = None
