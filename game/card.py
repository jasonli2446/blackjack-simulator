class Card:
    """
    Represents a playing card in a standard deck.

    Attributes:
        rank (str): The rank of the card ('2', '3', ..., 'A').
        value (int): The blackjack value of the card.
    """

    def __init__(self, rank):
        """
        Initialize a card with a given rank.

        Args:
            rank (str): The rank of the card ('2', '3', ..., 'A').
        """
        self.rank = rank
        self.value = self._calculate_value()

    def _calculate_value(self):
        """
        Calculate the blackjack value of the card.

        Returns:
            int: The value of the card in blackjack.
        """
        if self.rank in ("J", "Q", "K"):
            return 10
        elif self.rank == "A":
            # Ace initially has a value of 11, but this can be adjusted to 1 in the Hand class
            return 11
        else:
            return int(self.rank)

    def __repr__(self):
        """
        Return a string representation of the card.

        Returns:
            str: The string representation of the card.
        """
        return f"{self.rank}"
