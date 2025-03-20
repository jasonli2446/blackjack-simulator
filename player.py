from hand import Hand
from strategy import Strategy


class Player:
    """
    Represents a player in the blackjack game.

    Attributes:
        hand (Hand): The player's current hand.
        split_hands (list): List of split hands if the player splits.
        strategy (Strategy): The strategy object for decision-making.
        balance (float): Player's current balance.
    """

    def __init__(self, initial_balance=1000.0):
        """
        Initialize a player with an empty hand and the specified balance.

        Args:
            initial_balance (float, optional): Initial player balance. Defaults to 1000.0.
        """
        self.hand = Hand()
        self.split_hands = []
        self.strategy = Strategy()
        self.balance = initial_balance

    def place_bet(self, amount):
        """
        Place a bet with the specified amount.

        Args:
            amount (float): The bet amount.

        Returns:
            float: The bet amount if successful, 0 if insufficient balance.
        """
        if amount <= self.balance:
            self.balance -= amount
            return amount
        return 0

    def decide_action(self, dealer_upcard, first_hand=True):
        """
        Decide the action to take based on strategy.

        Args:
            dealer_upcard (Card): The dealer's face-up card.
            first_hand (bool, optional): Whether this is the first hand.
                                         Defaults to True.

        Returns:
            str: The decided action (hit, stand, double, split).
        """
        action = self.strategy.decide_action(self.hand, dealer_upcard)

        # If it's not the first action or there are split hands,
        # we cannot double or split
        if not first_hand or self.split_hands:
            if action == Strategy.DOUBLE:
                action = Strategy.HIT
            elif action == Strategy.SPLIT:
                action = Strategy.HIT

        return action

    def receive_winnings(self, amount):
        """
        Receive winnings to add to the balance.

        Args:
            amount (float): The amount to add to the balance.
        """
        self.balance += amount

    def clear_hands(self):
        """Clear the player's hand and split hands."""
        self.hand.clear()
        self.split_hands = []
