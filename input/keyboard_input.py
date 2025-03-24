from input.input_handler import InputHandler
from game.strategy import Strategy


class KeyboardInputHandler(InputHandler):
    """Handles player input from the keyboard."""

    def setup(self):
        """Nothing to setup for keyboard input."""
        pass

    def cleanup(self):
        """Nothing to clean up for keyboard input."""
        pass

    def get_action(self):
        """
        Get the player's action from keyboard input.

        Returns:
            str: The action to take (hit, stand, double, split)
        """
        action = input("Choose your action (hit, stand, double, split): ").lower()
        if action in [Strategy.HIT, Strategy.STAND, Strategy.DOUBLE, Strategy.SPLIT]:
            return action
        return None

    def is_quit(self, input_text=None):
        """
        Check if the player wants to quit.

        Args:
            input_text (str, optional): Input to check. If None, will ask for input.

        Returns:
            bool: True if quit requested, False otherwise
        """
        if input_text is None:
            input_text = ""
        return input_text.lower() == "q"

    def get_bet_amount(self, current_balance):
        """
        Get the bet amount from the player.

        Args:
            current_balance (float): Player's current balance

        Returns:
            float or str: The bet amount or command
        """
        print(f"\nYour balance: ${current_balance:.2f}")
        bet_input = input("Enter bet amount: ")

        if bet_input.lower() == "q":
            return "q"
        elif bet_input.lower() == "a":
            return "a"

        try:
            return float(bet_input)
        except ValueError:
            return -1  # Invalid input
