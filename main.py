import time
from game import Game
from strategy import Strategy
from hand import Hand


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

    # Auto-bet setup
    auto_bet = input("Would you like to enable auto-betting? (y/n): ").lower() == "y"
    auto_bet_amount = 0

    if auto_bet:
        while True:
            try:
                auto_bet_amount = float(input("Enter your auto-bet amount: "))
                if auto_bet_amount <= 0:
                    print("Bet amount must be positive.")
                else:
                    print(f"Auto-bet set to ${auto_bet_amount:.2f}")
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")

    while game.player.balance > 0:
        print(f"Current Balance: ${game.player.balance:.2f}")

        # Get bet amount
        if auto_bet and auto_bet_amount > 0:
            # Use auto-bet amount
            bet_amount = min(auto_bet_amount, game.player.balance)
            print(f"Auto-betting ${bet_amount:.2f}")

        if not auto_bet or auto_bet_amount <= 0:
            while True:
                try:
                    bet_input = input(
                        "Enter bet amount (or 'q' to quit, 'a' to enable auto-bet): "
                    )
                    if bet_input.lower() == "q":
                        print(
                            f"\nThank you for playing! Final balance: ${game.player.balance:.2f}"
                        )
                        return
                    elif bet_input.lower() == "a":
                        try:
                            auto_bet_amount = float(
                                input("Enter your auto-bet amount: ")
                            )
                            if auto_bet_amount <= 0:
                                print("Bet amount must be positive.")
                                continue
                            auto_bet = True
                            bet_amount = min(auto_bet_amount, game.player.balance)
                            print(f"Auto-bet set to ${auto_bet_amount:.2f}")
                            break
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                            continue

                    bet_amount = float(bet_input)
                    if bet_amount <= 0:
                        print("Bet amount must be positive.")
                    elif bet_amount > game.player.balance:
                        all_in = input(
                            f"Bet exceeds your balance of ${game.player.balance:.2f}. Go all in? (y/n): "
                        )
                        if all_in.lower() == "y":
                            bet_amount = game.player.balance
                            print(f"Going all in with ${bet_amount:.2f}!")
                            break
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
            # Don't ask for action if player has 21
            if game.player.hand.get_value() == 21:
                print("Player has 21. Standing.")
                break

            # Show strategy suggestion if enabled
            if show_strategy:
                suggested_action = game.player.decide_action(
                    game.dealer.upcard, first_action
                )
                print(f"The strategy suggests to {suggested_action.upper()}.")

            # Always ask for player input regardless of strategy mode
            action = input("Choose your action (hit, stand, double, split): ").lower()

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
                # Only allow doubling on two cards and when total is less than 12
                if (
                    len(game.player.hand.cards) != 2
                    or game.player.hand.get_value() >= 12
                ):
                    print(
                        "Cannot double: only allowed on first two cards with value under 12."
                    )
                    first_action = False
                    continue

                additional_bet = min(bet_amount, game.player.balance)
                if additional_bet > 0:
                    print(f"Bet increased to ${bet_amount + additional_bet:.2f}")
                    game.player.balance -= additional_bet
                    game.bet += additional_bet
                else:
                    print(
                        "Cannot double down due to insufficient balance. Default to HIT."
                    )

                time.sleep(1)
                game.player.hand.add_card(game.deck.deal_card())
                display_game_state(game)

                if game.player.hand.get_value() > 21:
                    print("Bust! You lose.")

                break

            elif action == Strategy.SPLIT:
                # Check if split is allowed (must have exactly 2 cards of the same rank)
                if not game.player.hand.is_pair() or len(game.player.hand.cards) != 2:
                    print("Cannot split: must have exactly two cards of the same rank.")
                    first_action = False
                    continue

                # Check if player has enough balance for the additional bet
                if game.player.balance < bet_amount:
                    print("Cannot split: insufficient balance for additional bet.")
                    first_action = False
                    continue

                # Split the hand
                print("Splitting hand...")
                time.sleep(1)

                # Get the exact cards before splitting for clarity
                original_first_card = game.player.hand.cards[0]
                original_second_card = game.player.hand.cards[1]

                # Create the split hand with the second card
                split_hand = Hand()
                split_hand.add_card(original_second_card)

                # Keep only the first card in the original hand
                game.player.hand.cards = [original_first_card]

                # Place additional bet for the split hand
                game.player.balance -= bet_amount
                split_bet = bet_amount

                # Deal one more card to each hand
                first_new_card = game.deck.deal_card()
                second_new_card = game.deck.deal_card()

                game.player.hand.add_card(first_new_card)
                split_hand.add_card(second_new_card)

                print(
                    f"\n=== Playing first hand ({original_first_card} + {first_new_card}) ==="
                )
                display_game_state(game)

                # Continue playing the first hand (this continues in the main loop)
                first_action = False

                # After the first hand is complete, play the split hand
                print(
                    f"\n=== Playing split hand ({original_second_card} + {second_new_card}) ==="
                )

                # Save the original hand temporarily
                original_hand = game.player.hand
                original_bet = game.bet

                # Use the split hand for the second round
                game.player.hand = split_hand
                game.bet = split_bet

                # Display the current state with the split hand
                display_game_state(game)

                # Play the split hand
                split_first_action = True
                split_hand_bust = False

                while True:
                    # Don't ask for action if split hand has 21
                    if game.player.hand.get_value() == 21:
                        print("Split hand has 21. Standing.")
                        break

                    # Show strategy for split hand
                    if show_strategy:
                        suggested_action = game.player.decide_action(
                            game.dealer.upcard, split_first_action
                        )
                        print(
                            f"The strategy suggests to {suggested_action.upper()} for split hand."
                        )

                    # Get action for split hand
                    split_action = input(
                        "Choose action for split hand (hit, stand, double): "
                    ).lower()

                    if split_action == Strategy.HIT:
                        time.sleep(1)
                        game.player.hand.add_card(game.deck.deal_card())
                        display_game_state(game)

                        if game.player.hand.get_value() > 21:
                            print("Split hand busts!")
                            split_hand_bust = True
                            break

                        split_first_action = False

                    elif split_action == Strategy.STAND:
                        time.sleep(1)
                        break

                    elif split_action == Strategy.DOUBLE:
                        # Check if doubling is allowed
                        if (
                            len(game.player.hand.cards) != 2
                            or game.player.hand.get_value() >= 12
                        ):
                            print(
                                "Cannot double: only allowed on first two cards with value under 12."
                            )
                            split_first_action = False
                            continue

                        # Check if player has enough balance
                        additional_bet = min(split_bet, game.player.balance)
                        if additional_bet > 0:
                            print(
                                f"Split hand bet increased to ${split_bet + additional_bet:.2f}"
                            )
                            game.player.balance -= additional_bet
                            game.bet += additional_bet
                            split_bet += additional_bet
                        else:
                            print("Cannot double down due to insufficient balance.")

                        time.sleep(1)
                        game.player.hand.add_card(game.deck.deal_card())
                        display_game_state(game)

                        if game.player.hand.get_value() > 21:
                            print("Split hand busts!")
                            split_hand_bust = True

                        break

                    else:
                        print("Invalid action. Please choose hit, stand, or double.")

                # Store split hand result
                split_value = game.player.hand.get_value()

                # Restore the original hand
                game.player.hand = original_hand
                game.bet = original_bet

                # Process the dealer's turn only after both hands are played
                if game.player.hand.get_value() <= 21 or not split_hand_bust:
                    # Dealer's turn
                    print("\nDealer's turn...")
                    time.sleep(1)
                    print("Dealer reveals second card...")
                    display_game_state(game, hide_dealer=False)

                    # Handle dealer's actions
                    dealer_bust = False

                    if game.dealer.should_hit():
                        while game.dealer.should_hit():
                            print("Dealer hits...")
                            time.sleep(1)
                            game.dealer.hand.add_card(game.deck.deal_card())
                            display_game_state(game, hide_dealer=False)

                            if game.dealer.hand.get_value() > 21:
                                print("Dealer busts!")
                                dealer_bust = True
                                break

                    # Determine results for both hands
                    dealer_value = game.dealer.hand.get_value()
                    player_value = game.player.hand.get_value()

                    # First hand result
                    print("\n=== First Hand Result ===")
                    if player_value > 21:
                        print("First hand busts. You lose this bet.")
                    elif dealer_bust:
                        print("Dealer busts! First hand wins.")
                        game.player.receive_winnings(game.bet * 2)
                    elif player_value > dealer_value:
                        print(
                            f"First hand wins! {player_value} beats dealer's {dealer_value}."
                        )
                        game.player.receive_winnings(game.bet * 2)
                    elif dealer_value > player_value:
                        print(
                            f"First hand loses. Dealer's {dealer_value} beats your {player_value}."
                        )
                    else:
                        print(f"First hand push. Both have {player_value}.")
                        game.player.receive_winnings(game.bet)

                    # Split hand result
                    print("\n=== Split Hand Result ===")
                    if split_value > 21:
                        print("Split hand busts. You lose this bet.")
                    elif dealer_bust:
                        print("Dealer busts! Split hand wins.")
                        game.player.receive_winnings(split_bet * 2)
                    elif split_value > dealer_value:
                        print(
                            f"Split hand wins! {split_value} beats dealer's {dealer_value}."
                        )
                        game.player.receive_winnings(split_bet * 2)
                    elif dealer_value > split_value:
                        print(
                            f"Split hand loses. Dealer's {dealer_value} beats your {split_value}."
                        )
                    else:
                        print(f"Split hand push. Both have {split_value}.")
                        game.player.receive_winnings(split_bet)
                else:
                    # Both hands busted, nothing to do
                    print("\nBoth hands bust. You lose both bets.")

                continue  # Skip to the next round

        if game.player.hand.get_value() > 21:
            # Player busts, end the round
            continue

        # Dealer's turn
        print("\nDealer's turn...")
        time.sleep(1)
        print("Dealer reveals second card...")
        display_game_state(game, hide_dealer=False)

        # Handle dealer's actions and determine winner
        dealer_bust = False

        # Only enter hit loop if dealer actually needs to hit
        if game.dealer.should_hit():
            while game.dealer.should_hit():
                print("Dealer hits...")
                time.sleep(1)
                game.dealer.hand.add_card(game.deck.deal_card())
                display_game_state(game, hide_dealer=False)

                if game.dealer.hand.get_value() > 21:
                    print("Dealer busts! You win.")
                    dealer_bust = True
                    break

        # Determine winner if dealer didn't bust
        if dealer_bust:
            # Player wins because dealer busted
            game.player.receive_winnings(game.bet * 2)  # Return bet + win amount
        else:
            # Compare hands
            player_value = game.player.hand.get_value()
            dealer_value = game.dealer.hand.get_value()

            if player_value > dealer_value:
                print(f"You win! {player_value} beats dealer's {dealer_value}.")
                game.player.receive_winnings(game.bet * 2)  # Return bet + win amount
            elif dealer_value > player_value:
                print(f"You lose. Dealer's {dealer_value} beats your {player_value}.")
                # No balance change needed as bet was already deducted
            else:
                print(f"Push. Both have {player_value}.")
                game.player.receive_winnings(game.bet)  # Return the bet on push

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
