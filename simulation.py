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

        # Set essentially infinite balance to ensure player can always double/split
        initial_balance = 100000000000.0
        self.game.player.balance = initial_balance

        # Track total bets separately to calculate house edge
        total_bets_placed = 0.0
        total_net_outcome = 0.0

        # Adjust update frequency based on total number of hands
        if num_hands > 100000:
            update_frequency = 20000
        elif num_hands > 50000:
            update_frequency = 10000
        elif num_hands > 10000:
            update_frequency = 2000
        elif num_hands > 5000:
            update_frequency = 1000
        else:
            update_frequency = 100

        for i in range(num_hands):
            # Update progress with the new frequency
            if display_progress and i > 0 and i % update_frequency == 0:
                progress = i / num_hands * 100
                elapsed_time = time.time() - start_time
                estimated_total = elapsed_time / i * num_hands
                remaining_time = estimated_total - elapsed_time

                print(f"Progress: {progress:.1f}% ({i}/{num_hands} hands)")
                print(
                    f"Elapsed time: {elapsed_time:.1f}s, Estimated time remaining: {remaining_time:.1f}s"
                )
                current_edge = (
                    -total_net_outcome / (total_bets_placed) * 100
                    if total_bets_placed > 0
                    else 0
                )
                print(f"Current house edge: {current_edge:.4f}%")
                print("-" * 50)

            # No need to check player balance - it's infinite

            # Track initial bet
            initial_bet = self.bet_size
            total_bets_placed += initial_bet

            # Record the balance before this hand
            balance_before_hand = self.game.player.balance

            # Play a hand - initial deal and blackjack check
            result, player_hand, dealer_hand, bet, win_amount = self.game.play_round(
                self.bet_size
            )

            # Complete the round if it's not already resolved by blackjack
            if result == "continue":
                # Play through player turn using perfect strategy
                player_bust = self.game.player_turn()

                if hasattr(self.game, "split_results"):
                    # Process split results correctly
                    split_data = self.game.split_results

                    # Track additional bets from splitting
                    for hand_index in range(len(split_data["hand_results"])):
                        if (
                            hand_index > 0
                        ):  # First hand is already counted in initial bet
                            total_bets_placed += initial_bet

                    # Loop through all split hands to count them properly
                    for hand_result in split_data["hand_results"]:
                        if hand_result == "win":
                            self.normal_wins += 1
                        elif hand_result == "blackjack":
                            self.blackjacks_won += 1
                        elif hand_result == "push":
                            self.pushes += 1
                        elif hand_result == "loss":
                            self.losses += 1

                    # We've already counted the original hand as played,
                    # need to add the additional split hands
                    self.hands_played += len(split_data["hand_results"]) - 1

                    # Remove the split results
                    delattr(self.game, "split_results")
                    continue  # Skip the normal result processing

                if player_bust:
                    result = "dealer_wins"
                else:
                    # Play through dealer turn
                    dealer_bust = self.game.dealer_turn()

                    # Determine the winner
                    if dealer_bust:
                        result = "player_wins"
                        self.game.player.receive_winnings(
                            self.game.bet * 2
                        )  # Return bet + win
                    else:
                        # Compare hands
                        player_value = self.game.player.hand.get_value()
                        dealer_value = self.game.dealer.hand.get_value()

                        if player_value > dealer_value:
                            result = "player_wins"
                            self.game.player.receive_winnings(
                                self.game.bet * 2
                            )  # Return bet + win
                        elif dealer_value > player_value:
                            result = "dealer_wins"
                        else:
                            result = "push"
                            self.game.player.receive_winnings(
                                self.game.bet
                            )  # Return the bet

            # Update statistics
            self.hands_played += 1
            hand_profit = self.game.player.balance - balance_before_hand
            total_net_outcome += hand_profit

            # Update win/loss statistics by result type
            if result == "player_blackjack":
                self.blackjacks_won += 1
            elif result == "player_wins":
                self.normal_wins += 1
            elif result == "push":
                self.pushes += 1
            elif result == "dealer_wins" or result == "split_processed":
                self.losses += 1

        # Calculate house edge based on total bets placed and net outcome
        self.total_profit = total_net_outcome
        house_edge = (
            -total_net_outcome / total_bets_placed * 100 if total_bets_placed > 0 else 0
        )

        # Display final statistics
        if display_progress:
            print("\nSimulation complete!")
            print(f"Hands played: {self.hands_played}")
            print(f"Total bets placed: ${total_bets_placed:.2f}")
            print(f"Total profit/loss: ${total_net_outcome:.2f}")
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
        # We now use total_profit directly as set in the run method
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
