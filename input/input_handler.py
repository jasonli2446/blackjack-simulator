from abc import ABC, abstractmethod


class InputHandler(ABC):
    """Abstract base class for handling player input."""

    @abstractmethod
    def get_action(self):
        """
        Get the player's action.

        Returns:
            str: The action to take (hit, stand, double, split)
        """
        pass

    @abstractmethod
    def is_quit(self):
        """
        Check if the player wants to quit.

        Returns:
            bool: True if quit requested, False otherwise
        """
        pass

    @abstractmethod
    def get_bet_amount(self, current_balance):
        """
        Get the bet amount from the player.

        Args:
            current_balance (float): Player's current balance

        Returns:
            float: The bet amount
        """
        pass

    @abstractmethod
    def setup(self):
        """
        Setup the input handler.
        """
        pass

    @abstractmethod
    def cleanup(self):
        """
        Clean up resources used by the input handler.
        """
        pass
