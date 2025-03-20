import time
from game import Game
from strategy import Strategy


def display_hand(hand, hide_second_card=False):
    """
    Display a hand with formatting.

    Args:
        hand: The hand to display.
        hide_second_card (bool, optional): Whether to hide the second card. Defaults to False.
    """
    cards = []
    for i, card in enumerate(hand.cards):
        if i == 1 and hide_second_card:
            cards.append("?")
        else:
            cards.append(str(card))

    print(f"Cards: {', '.join(cards)}")

    if not hide_second_card:
        value = hand.get_value()
        print(f"Value: {value}")
        if value > 21:
            print("BUST!")


def display_game_state(game, hide_dealer=True):
    """
    Display the current game state.

    Args:
        game: The game object.
        hide_dealer (bool, optional): Whether to hide the dealer's second card. Defaults to True.
    """
    print("\n" + "=" * 50)
    print(f"Player's Balance: ${game.player.balance:.2f}")
    print(f"Current Bet: ${game.bet:.2f}")
    print("-" * 50)

    print("Player Hand:")
    display_hand(game.player.hand)

    print("\nDealer Hand:")
    display_hand(game.dealer.hand, hide_dealer)
    print("=" * 50 + "\n")


def play_game(show_strategy=True):
    """Main function to play the blackjack game."""
    game = Game()

    print("Welcome to Blackjack!")
    print(
        "In this game, you'll see the perfect strategy in action."
        if show_strategy
        else "In this game, you'll play without strategy suggestions."
    )
    print("Your initial balance is $1000.00.\n")

    while game.player.balance > 0:
        print(f"Current Balance: ${game.player.balance:.2f}")

        # Get bet amount
        while True:
            try:
                bet_input = input("Enter bet amount (or 'q' to quit): ")
                if bet_input.lower() == "q":
                    print(
                        f"\nThank you for playing! Final balance: ${game.player.balance:.2f}"
                    )
                    return

                bet_amount = float(bet_input)
                if bet_amount <= 0:
                    print("Bet amount must be positive.")
                elif bet_amount > game.player.balance:
                    print(
                        f"Bet amount exceeds your balance of ${game.player.balance:.2f}."
                    )
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Start the round
        result, player_hand, dealer_hand, bet, win_amount = game.play_round(bet_amount)

        # Display initial state
        print("\nDealing cards...")
        time.sleep(1)
        display_game_state(game)

        # Debugging: Print hands after dealing initial cards
        print(f"DEBUG: Player hand after dealing: {game.player.hand.cards}")
        print(f"DEBUG: Dealer hand after dealing: {game.dealer.hand.cards}")

        # Check for blackjack
        if result == "player_blackjack":
            print("Blackjack! You win 3:2.")
            time.sleep(1)
            display_game_state(game, hide_dealer=False)
            continue

        elif result == "dealer_blackjack":
            print("Dealer has Blackjack. You lose.")
            time.sleep(1)
            display_game_state(game, hide_dealer=False)
            continue

        elif result == "push" and player_hand.is_blackjack():
            print("Both have Blackjack. Push.")
            time.sleep(1)
            display_game_state(game, hide_dealer=False)
            continue

        elif result != "continue":
            # Something unexpected happened
            continue

        # Player's turn
        print("\nPlayer's turn...")
        time.sleep(1)

        first_action = True
        while True:
            if show_strategy:
                action = game.player.decide_action(game.dealer.upcard, first_action)
                print(f"The strategy suggests to {action.upper()}.")
            else:
                action = input(
                    "Choose your action (hit, stand, double, split): "
                ).lower()

            if action == Strategy.HIT:
                time.sleep(1)
                game.player.hand.add_card(game.deck.deal_card())
                display_game_state(game)

                if game.player.hand.get_value() > 21:
                    print("Bust! You lose.")
                    break

                first_action = False

            elif action == Strategy.STAND:
                time.sleep(1)
                break

            elif action == Strategy.DOUBLE:
                additional_bet = min(bet_amount, game.player.balance)
                if additional_bet > 0:
                    print(f"Bet increased to ${bet_amount + additional_bet:.2f}")
                    game.player.balance -= additional_bet
                    game.bet += additional_bet
                else:
                    print(
                        "Cannot double down due to insufficient balance. The strategy defaults to HIT."
                    )

                time.sleep(1)
                game.player.hand.add_card(game.deck.deal_card())
                display_game_state(game)

                if game.player.hand.get_value() > 21:
                    print("Bust! You lose.")

                break

            elif action == Strategy.SPLIT:
                print(
                    "Splitting is not fully implemented in this version. The strategy defaults to HIT."
                )
                time.sleep(1)
                game.player.hand.add_card(game.deck.deal_card())
                display_game_state(game)

                if game.player.hand.get_value() > 21:
                    print("Bust! You lose.")
                    break

                first_action = False

        if game.player.hand.get_value() > 21:
            # Player busts, end the round
            continue

        # Dealer's turn
        print("\nDealer's turn...")
        time.sleep(1)
        display_game_state(game, hide_dealer=False)

        while game.dealer.should_hit():
            print("Dealer hits...")
            time.sleep(1)
            game.dealer.hand.add_card(game.deck.deal_card())
            display_game_state(game, hide_dealer=False)

        # Debugging: Print dealer's hand after dealer's turn
        print(f"DEBUG: Dealer's hand after dealer's turn: {game.dealer.hand.cards}")

        if game.dealer.hand.get_value() > 21:
            print("Dealer busts! You win.")
        else:
            # Determine winner
            player_value = game.player.hand.get_value()
            dealer_value = game.dealer.hand.get_value()

            print(f"DEBUG: Player's hand: {game.player.hand.cards}")
            print(f"DEBUG: Dealer's hand: {game.dealer.hand.cards}")

            if player_value > dealer_value:
                print(f"You win! {player_value} beats dealer's {dealer_value}.")
            elif dealer_value > player_value:
                print(f"You lose. Dealer's {dealer_value} beats your {player_value}.")
            else:
                print(f"Push. Both have {player_value}.")

        # Wait for user to continue
        input("\nPress Enter to continue...")

    print("\nYou're out of money! Game over.")


def main():
    """Main entry point for the program."""
    print("=" * 60)
    print("BLACKJACK SIMULATION PROGRAM")
    print("=" * 60)
    print("1. Play Blackjack Game with Strategy Suggestions")
    print("2. Play Blackjack Game without Strategy Suggestions")
    print("3. Run House Edge Simulation")
    print("4. Exit")
    print("=" * 60)

    while True:
        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            play_game(show_strategy=True)
        elif choice == "2":
            play_game(show_strategy=False)
        elif choice == "3":
            from simulation import run_simulation

            run_simulation()
        elif choice == "4":
            print("\nThank you for using the Blackjack Simulation Program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
