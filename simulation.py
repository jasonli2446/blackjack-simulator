import time
import numpy as np
from game import Game


class Simulation:
    """
    Runs a simulation of many blackjack hands to estimate the house edge.

    Attributes:
        game (Game): The game object.
        bet_size (float): The size of each bet.
        hands_played (int): Number of hands played in the simulation.
        total_profit (float): Total profit or loss.
        blackjacks_won (int): Number of hands won with blackjack.
        normal_wins (int): Number of hands won without blackjack.
        pushes (int): Number of pushes.
        losses (int): Number of losses.
    """

    def __init__(self, bet_size=100.0):
        """
        Initialize a new simulation.

        Args:
            bet_size (float, optional): The bet size for each hand. Defaults to 100.0.
        """
        self.game = Game()
        self.bet_size = bet_size
        self.reset_stats()

    def reset_stats(self):
        """Reset the simulation statistics."""
        self.hands_played = 0
        self.total_profit = 0.0
        self.blackjacks_won = 0
        self.normal_wins = 0
        self.pushes = 0
        self.losses = 0

    def run(self, num_hands=1000, display_progress=True):
        """
        Run the simulation for a specified number of hands.

        Args:
            num_hands (int, optional): The number of hands to simulate. Defaults to 1000.
            display_progress (bool, optional): Whether to display progress. Defaults to True.

        Returns:
            float: The calculated house edge.
        """
        self.reset_stats()
        start_time = time.time()

        for i in range(num_hands):
            # Update progress every 100 hands
            if display_progress and i > 0 and i % 100 == 0:
                progress = i / num_hands * 100
                elapsed_time = time.time() - start_time
                estimated_total = elapsed_time / i * num_hands
                remaining_time = estimated_total - elapsed_time

                print(f"Progress: {progress:.1f}% ({i}/{num_hands} hands)")
                print(
                    f"Elapsed time: {elapsed_time:.1f}s, Estimated time remaining: {remaining_time:.1f}s"
                )
                print(f"Current house edge: {self.calculate_house_edge():.4f}%")
                print("-" * 50)

            # Ensure the player has enough balance
            if self.game.player.balance < self.bet_size:
                self.game.player.balance = 1000.0  # Reset balance

            # Play a hand
            result, _, _, bet, win_amount = self.game.play_round(self.bet_size)

            # Update statistics
            self.hands_played += 1

            if result == "player_blackjack":
                self.blackjacks_won += 1
                self.total_profit += 1.5 * self.bet_size  # 3:2 payout
            elif result == "player_wins":
                self.normal_wins += 1
                self.total_profit += self.bet_size
            elif result == "push":
                self.pushes += 1
                # No change to total profit
            else:  # dealer_wins
                self.losses += 1
                self.total_profit -= self.bet_size

        # Calculate house edge
        house_edge = self.calculate_house_edge()

        # Display final statistics
        if display_progress:
            print("\nSimulation complete!")
            print(f"Hands played: {self.hands_played}")
            print(f"Total profit/loss: ${self.total_profit:.2f}")
            print(f"House edge: {house_edge:.4f}%")
            print("\nWin/Loss Statistics:")
            print(
                f"Blackjacks: {self.blackjacks_won} ({self.blackjacks_won / self.hands_played * 100:.2f}%)"
            )
            print(
                f"Normal wins: {self.normal_wins} ({self.normal_wins / self.hands_played * 100:.2f}%)"
            )
            print(
                f"Pushes: {self.pushes} ({self.pushes / self.hands_played * 100:.2f}%)"
            )
            print(
                f"Losses: {self.losses} ({self.losses / self.hands_played * 100:.2f}%)"
            )

        return house_edge

    def calculate_house_edge(self):
        """
        Calculate the house edge based on the simulation results.

        Returns:
            float: The house edge as a percentage.
        """
        if self.hands_played == 0:
            return 0.0

        # House edge is the expected loss per bet as a percentage
        return -self.total_profit / (self.hands_played * self.bet_size) * 100


def run_simulation():
    """Run the blackjack simulation with user input."""
    print("Welcome to the Blackjack Simulation!")
    print(
        "This simulation will estimate the house edge by playing many hands using perfect strategy."
    )

    # Get simulation parameters
    while True:
        try:
            num_hands = int(
                input("\nEnter the number of hands to simulate (recommended: 10000+): ")
            )
            if num_hands <= 0:
                print("Number of hands must be positive.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            bet_size = float(
                input("Enter the bet size for each hand (default: 100.0): ") or "100.0"
            )
            if bet_size <= 0:
                print("Bet size must be positive.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Run the simulation
    print(
        f"\nRunning simulation with {num_hands} hands and ${bet_size:.2f} bet size..."
    )
    print("This may take a while for large numbers of hands.")

    simulation = Simulation(bet_size)
    house_edge = simulation.run(num_hands)

    print("\nSimulation Results Summary:")
    print(f"House Edge: {house_edge:.4f}%")
    print(
        f"Player's Expected Loss Per ${bet_size:.2f} Bet: ${house_edge * bet_size / 100:.2f}"
    )

    return house_edge


if __name__ == "__main__":
    run_simulation()
