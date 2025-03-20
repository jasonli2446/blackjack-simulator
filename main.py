import time
from game import Game
from strategy import Strategy
from hand import Hand
from card import Card


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
                    bet_input = input("Enter bet amount: ")
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

        # Reset the deck if it's a test deck
        if hasattr(game.deck, "reset"):
            game.deck.reset()

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

        round_completed = False
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

                # Get the cards before splitting
                original_first_card = game.player.hand.cards[0]
                original_second_card = game.player.hand.cards[1]

                # Create a list to store all split hands (including the original)
                all_hands = []
                all_bets = []
                all_results = []

                # Setup first hand (original hand with just the first card)
                first_hand = Hand()
                first_hand.add_card(original_first_card)
                first_hand.add_card(game.deck.deal_card())
                all_hands.append(first_hand)
                all_bets.append(game.bet)

                # Setup second hand with just the second card
                second_hand = Hand()
                second_hand.add_card(original_second_card)
                second_hand.add_card(game.deck.deal_card())
                all_hands.append(second_hand)
                all_bets.append(bet_amount)

                # Check for splitting Aces
                is_splitting_aces = original_first_card.rank == "A"
                if is_splitting_aces:
                    print(
                        "Note: When splitting Aces, you get only one card per hand and must stand."
                    )

                    # Mark all split hands as completed
                    for hand_index, result_hand in enumerate(all_hands):
                        all_results.append(
                            {
                                "hand": result_hand.cards.copy(),
                                "value": result_hand.get_value(),
                                "bust": False,  # Can't bust with Ace + any card
                            }
                        )

                    # Place additional bet for the second hand
                    game.player.balance -= bet_amount

                    # Skip directly to dealer's turn - no need to play each hand
                    # Show split hands for information only
                    for hand_index, split_hand in enumerate(all_hands):
                        hand_number = hand_index + 1
                        print(f"\nSplit Ace Hand {hand_number}:")
                        print(
                            f"Cards: {', '.join(str(card) for card in split_hand.cards)}"
                        )
                        print(f"Value: {split_hand.get_value()}")

                    # Set the first hand as active for dealer display
                    game.player.hand = all_hands[0]

                    # Immediately go to dealer's turn
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

                    # Determine results for each split ace hand
                    print("\n=== Final Results for Split Aces ===")
                    dealer_value = game.dealer.hand.get_value()
                    dealer_busted = dealer_value > 21

                    for hand_index, result in enumerate(all_results):
                        hand_number = hand_index + 1
                        hand_value = result["value"]
                        hand_bet = all_bets[hand_index]

                        print(f"\nSplit Ace Hand {hand_number} Result:")
                        print(
                            f"Cards: {', '.join(str(card) for card in result['hand'])}"
                        )
                        print(f"Value: {hand_value}")

                        if dealer_busted:
                            print(
                                f"Dealer busted! Split Ace Hand {hand_number} wins ${hand_bet:.2f}."
                            )
                            game.player.receive_winnings(hand_bet * 2)
                        elif hand_value > dealer_value:
                            print(
                                f"Split Ace Hand {hand_number} wins! {hand_value} beats dealer's {dealer_value}. You win ${hand_bet:.2f}."
                            )
                            game.player.receive_winnings(hand_bet * 2)
                        elif dealer_value > hand_value:
                            print(
                                f"Split Ace Hand {hand_number} loses. Dealer's {dealer_value} beats your {hand_value}. You lose ${hand_bet:.2f}."
                            )
                        else:
                            print(
                                f"Split Ace Hand {hand_number} push. Both have {hand_value}. Your ${hand_bet:.2f} is returned."
                            )
                            game.player.receive_winnings(hand_bet)

                    # Restore player's main hand
                    game.player.hand = Hand()
                    game.bet = 0
                    round_completed = True
                    break

                # Play each hand separately before revealing the dealer's cards
                for hand_index, current_hand in enumerate(all_hands):
                    hand_number = hand_index + 1
                    current_bet = all_bets[hand_index]

                    print(f"\n=== Playing Hand {hand_number} ===")
                    print(f"Starting with card: {current_hand.cards[0]}")

                    # Set the current hand as the active hand
                    game.player.hand = current_hand
                    game.bet = current_bet

                    # Each hand gets exactly one card to start
                    hand_first_action = True
                    hand_bust = False

                    # Play this hand until stand or bust
                    while True:
                        display_game_state(game)

                        # Don't ask for action if hand has 21
                        if game.player.hand.get_value() == 21:
                            print(f"Hand {hand_number} has 21. Standing.")
                            break

                        # Show strategy for this hand
                        if show_strategy:
                            suggested_action = game.player.decide_action(
                                game.dealer.upcard, hand_first_action
                            )
                            print(
                                f"The strategy suggests to {suggested_action.upper()} for Hand {hand_number}."
                            )

                        # Get action for this hand
                        hand_action = input(
                            f"Choose action for Hand {hand_number} (hit, stand, double): "
                        ).lower()

                        if hand_action == Strategy.HIT:
                            time.sleep(1)
                            game.player.hand.add_card(game.deck.deal_card())

                            if game.player.hand.get_value() > 21:
                                display_game_state(game)
                                print(f"Hand {hand_number} busts!")
                                hand_bust = True
                                break

                            hand_first_action = False

                        elif hand_action == Strategy.STAND:
                            time.sleep(1)
                            break

                        elif hand_action == Strategy.DOUBLE:
                            # Check if doubling is allowed
                            if (
                                not hand_first_action  # Use this instead of card count check
                                or game.player.hand.get_value() >= 12
                            ):
                                print(
                                    "Cannot double: only allowed on first action with value under 12."
                                )
                                continue

                            # Check if player has enough balance
                            additional_bet = min(current_bet, game.player.balance)
                            if additional_bet > 0:
                                print(
                                    f"Hand {hand_number} bet increased to ${current_bet + additional_bet:.2f}"
                                )
                                game.player.balance -= additional_bet
                                game.bet += additional_bet
                                all_bets[hand_index] += additional_bet
                            else:
                                print("Cannot double down due to insufficient balance.")
                                continue

                            # Take exactly one more card and end turn
                            time.sleep(1)
                            game.player.hand.add_card(game.deck.deal_card())
                            display_game_state(game)

                            if game.player.hand.get_value() > 21:
                                print(f"Hand {hand_number} busts!")
                                hand_bust = True

                            break

                        else:
                            print(
                                "Invalid action. Please choose hit, stand, or double."
                            )

                    # Store the final state of this hand
                    all_results.append(
                        {
                            "hand": game.player.hand.cards.copy(),
                            "value": game.player.hand.get_value(),
                            "bust": hand_bust,
                        }
                    )

                # All hands have been played, now dealer plays
                # Only if at least one hand didn't bust
                any_hand_not_bust = any(not result["bust"] for result in all_results)

                if any_hand_not_bust:
                    # Dealer's turn
                    print("\nDealer's turn...")
                    time.sleep(1)
                    print("Dealer reveals second card...")
                    game.player.hand = all_hands[0]  # Restore any hand for display
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

                # Determine results for each hand
                print("\n=== Final Results ===")
                dealer_value = game.dealer.hand.get_value()
                dealer_busted = dealer_value > 21

                for hand_index, result in enumerate(all_results):
                    hand_number = hand_index + 1
                    hand_value = result["value"]
                    hand_bet = all_bets[hand_index]

                    print(f"\nHand {hand_number} Result:")
                    print(f"Cards: {', '.join(str(card) for card in result['hand'])}")
                    print(f"Value: {hand_value}")

                    if result["bust"]:
                        print(f"Hand {hand_number} busted. You lose ${hand_bet:.2f}.")
                    elif dealer_busted:
                        print(
                            f"Dealer busted! Hand {hand_number} wins ${hand_bet:.2f}."
                        )
                        game.player.receive_winnings(hand_bet * 2)
                    elif hand_value > dealer_value:
                        print(
                            f"Hand {hand_number} wins! {hand_value} beats dealer's {dealer_value}. You win ${hand_bet:.2f}."
                        )
                        game.player.receive_winnings(hand_bet * 2)
                    elif dealer_value > hand_value:
                        print(
                            f"Hand {hand_number} loses. Dealer's {dealer_value} beats your {hand_value}. You lose ${hand_bet:.2f}."
                        )
                    else:
                        print(
                            f"Hand {hand_number} push. Both have {hand_value}. Your ${hand_bet:.2f} is returned."
                        )
                        game.player.receive_winnings(hand_bet)

                # Restore player's main hand
                game.player.hand = Hand()
                game.bet = 0
                round_completed = True
                break

        if round_completed:
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


def play_split_test_game():
    """Test game mode that deals pairs to test splitting functionality."""

    # Ask user for the rank to test
    print("\nSPLIT TESTING MODE")
    print("This mode will deal pairs to make splitting easier to test.")

    while True:
        test_rank = input("\nEnter card rank to test (2-10, J, Q, K, A): ").upper()
        if test_rank in [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "J",
            "Q",
            "K",
            "A",
        ]:
            break
        else:
            print("Invalid card rank. Please enter a valid rank.")

    # Create a modified play_game function for testing splits
    def play_test_game(show_strategy=True):
        """Modified play_game function that forces pairs for split testing."""
        game = Game()

        print("Welcome to Blackjack Split Test Mode!")
        print(f"You will be dealt pairs of {test_rank}s to test splitting.")
        print("Your initial balance is $1000.00.\n")

        # Auto-bet setup (same as regular play_game)
        auto_bet = (
            input("Would you like to enable auto-betting? (y/n): ").lower() == "y"
        )
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

        # Main game loop
        while game.player.balance > 0:
            print(f"Current Balance: ${game.player.balance:.2f}")

            # Get bet amount (same as regular play_game)
            if auto_bet and auto_bet_amount > 0:
                bet_amount = min(auto_bet_amount, game.player.balance)
                print(f"Auto-betting ${bet_amount:.2f}")
            else:
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
                            all_in = input(
                                f"Bet exceeds your balance of ${game.player.balance:.2f}. Go all in? (y/n): "
                            )
                            if all_in.lower() in ["y", "yes"]:
                                bet_amount = game.player.balance
                                print(f"Going all in with ${bet_amount:.2f}!")
                                break
                        else:
                            break
                    except ValueError:
                        print("Invalid input. Please enter a number.")

            # Start the round normally
            result, player_hand, dealer_hand, bet, win_amount = game.play_round(
                bet_amount
            )

            # OVERRIDE: Force the player's hand to have a pair of the selected rank
            game.player.hand.cards = [Card(test_rank), Card(test_rank)]

            # Ensure the dealer has consistent cards for testing (10, 6)
            game.dealer.hand.cards = [Card("10"), Card("6")]
            game.dealer.upcard = game.dealer.hand.cards[0]

            # Display the modified hand
            print("\nDealing cards...")
            time.sleep(1)
            display_game_state(game)

            # Skip blackjack checks since we're forcing specific cards

            # Player's turn
            print("\nPlayer's turn...")
            time.sleep(1)

            # Continue with the normal game logic from play_game
            round_completed = False
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
                action = input(
                    "Choose your action (hit, stand, double, split): "
                ).lower()

                # Process player actions (same as regular play_game)
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
                    # Same logic as regular play_game
                    if not first_action or game.player.hand.get_value() >= 12:
                        print(
                            "Cannot double: only allowed on first action with value under 12."
                        )
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
                    # Same split logic as regular play_game
                    # Check if split is allowed (must have exactly 2 cards of the same rank)
                    if (
                        not game.player.hand.is_pair()
                        or len(game.player.hand.cards) != 2
                    ):
                        print(
                            "Cannot split: must have exactly two cards of the same rank."
                        )
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

                    # Get the cards before splitting
                    original_first_card = game.player.hand.cards[0]
                    original_second_card = game.player.hand.cards[1]

                    # Create a list to store all split hands (including the original)
                    all_hands = []
                    all_bets = []
                    all_results = []

                    # Setup first hand (original hand with just the first card)
                    first_hand = Hand()
                    first_hand.add_card(original_first_card)
                    first_hand.add_card(game.deck.deal_card())
                    all_hands.append(first_hand)
                    all_bets.append(game.bet)

                    # Setup second hand with just the second card
                    second_hand = Hand()
                    second_hand.add_card(original_second_card)
                    second_hand.add_card(game.deck.deal_card())
                    all_hands.append(second_hand)
                    all_bets.append(bet_amount)

                    # Check for splitting Aces
                    is_splitting_aces = original_first_card.rank == "A"

                    if is_splitting_aces:
                        print(
                            "Note: When splitting Aces, you get only one card per hand and must stand."
                        )

                        # Mark all split hands as completed
                        for hand_index, result_hand in enumerate(all_hands):
                            all_results.append(
                                {
                                    "hand": result_hand.cards.copy(),
                                    "value": result_hand.get_value(),
                                    "bust": False,  # Can't bust with Ace + any card
                                }
                            )

                        # Place additional bet for the second hand
                        game.player.balance -= bet_amount

                        # Skip directly to dealer's turn - no need to play each hand
                        # Show split hands for information only
                        for hand_index, split_hand in enumerate(all_hands):
                            hand_number = hand_index + 1
                            print(f"\nSplit Ace Hand {hand_number}:")
                            print(
                                f"Cards: {', '.join(str(card) for card in split_hand.cards)}"
                            )
                            print(f"Value: {split_hand.get_value()}")

                        # Set the first hand as active for dealer display
                        game.player.hand = all_hands[0]

                        # Immediately go to dealer's turn
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

                        # Determine results for each split ace hand
                        print("\n=== Final Results for Split Aces ===")
                        dealer_value = game.dealer.hand.get_value()
                        dealer_busted = dealer_value > 21

                        for hand_index, result in enumerate(all_results):
                            hand_number = hand_index + 1
                            hand_value = result["value"]
                            hand_bet = all_bets[hand_index]

                            print(f"\nSplit Ace Hand {hand_number} Result:")
                            print(
                                f"Cards: {', '.join(str(card) for card in result['hand'])}"
                            )
                            print(f"Value: {hand_value}")

                            if dealer_busted:
                                print(
                                    f"Dealer busted! Split Ace Hand {hand_number} wins ${hand_bet:.2f}."
                                )
                                game.player.receive_winnings(hand_bet * 2)
                            elif hand_value > dealer_value:
                                print(
                                    f"Split Ace Hand {hand_number} wins! {hand_value} beats dealer's {dealer_value}. You win ${hand_bet:.2f}."
                                )
                                game.player.receive_winnings(hand_bet * 2)
                            elif dealer_value > hand_value:
                                print(
                                    f"Split Ace Hand {hand_number} loses. Dealer's {dealer_value} beats your {hand_value}. You lose ${hand_bet:.2f}."
                                )
                            else:
                                print(
                                    f"Split Ace Hand {hand_number} push. Both have {hand_value}. Your ${hand_bet:.2f} is returned."
                                )
                                game.player.receive_winnings(hand_bet)

                        # Restore player's main hand
                        game.player.hand = Hand()
                        game.bet = 0
                        round_completed = True
                        break

                    # Play each hand separately before revealing the dealer's cards
                    for hand_index, current_hand in enumerate(all_hands):
                        hand_number = hand_index + 1
                        current_bet = all_bets[hand_index]

                        print(f"\n=== Playing Hand {hand_number} ===")
                        print(f"Starting with card: {current_hand.cards[0]}")

                        # Set the current hand as the active hand
                        game.player.hand = current_hand
                        game.bet = current_bet

                        # Each hand gets exactly one card to start
                        hand_first_action = True
                        hand_bust = False

                        # Play this hand until stand or bust
                        while True:
                            display_game_state(game)

                            # Don't ask for action if hand has 21
                            if game.player.hand.get_value() == 21:
                                print(f"Hand {hand_number} has 21. Standing.")
                                break

                            # Show strategy for this hand
                            if show_strategy:
                                suggested_action = game.player.decide_action(
                                    game.dealer.upcard, hand_first_action
                                )
                                print(
                                    f"The strategy suggests to {suggested_action.upper()} for Hand {hand_number}."
                                )

                            # Get action for this hand
                            hand_action = input(
                                f"Choose action for Hand {hand_number} (hit, stand, double): "
                            ).lower()

                            if hand_action == Strategy.HIT:
                                time.sleep(1)
                                game.player.hand.add_card(game.deck.deal_card())

                                if game.player.hand.get_value() > 21:
                                    display_game_state(game)
                                    print(f"Hand {hand_number} busts!")
                                    hand_bust = True
                                    break

                                hand_first_action = False

                            elif hand_action == Strategy.STAND:
                                time.sleep(1)
                                break

                            elif hand_action == Strategy.DOUBLE:
                                # Check if doubling is allowed
                                if (
                                    not hand_first_action
                                    or game.player.hand.get_value() >= 12
                                ):
                                    print(
                                        "Cannot double: only allowed on first action with value under 12."
                                    )
                                    continue

                                # Check if player has enough balance
                                additional_bet = min(current_bet, game.player.balance)
                                if additional_bet > 0:
                                    print(
                                        f"Hand {hand_number} bet increased to ${current_bet + additional_bet:.2f}"
                                    )
                                    game.player.balance -= additional_bet
                                    game.bet += additional_bet
                                    all_bets[hand_index] += additional_bet
                                else:
                                    print(
                                        "Cannot double down due to insufficient balance."
                                    )
                                    continue

                                # Take exactly one more card and end turn
                                time.sleep(1)
                                game.player.hand.add_card(game.deck.deal_card())
                                display_game_state(game)

                                if game.player.hand.get_value() > 21:
                                    print(f"Hand {hand_number} busts!")
                                    hand_bust = True

                                break

                            else:
                                print(
                                    "Invalid action. Please choose hit, stand, or double."
                                )

                        # Store the final state of this hand
                        all_results.append(
                            {
                                "hand": game.player.hand.cards.copy(),
                                "value": game.player.hand.get_value(),
                                "bust": hand_bust,
                            }
                        )

                # All hands have been played, now dealer plays
                # Only if at least one hand didn't bust
                any_hand_not_bust = any(not result["bust"] for result in all_results)

                if any_hand_not_bust:
                    # Dealer's turn
                    print("\nDealer's turn...")
                    time.sleep(1)
                    print("Dealer reveals second card...")
                    game.player.hand = all_hands[0]  # Restore any hand for display
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

                # Determine results for each hand
                print("\n=== Final Results ===")
                dealer_value = game.dealer.hand.get_value()
                dealer_busted = dealer_value > 21

                for hand_index, result in enumerate(all_results):
                    hand_number = hand_index + 1
                    hand_value = result["value"]
                    hand_bet = all_bets[hand_index]

                    print(f"\nHand {hand_number} Result:")
                    print(f"Cards: {', '.join(str(card) for card in result['hand'])}")
                    print(f"Value: {hand_value}")

                    if result["bust"]:
                        print(f"Hand {hand_number} busted. You lose ${hand_bet:.2f}.")
                    elif dealer_busted:
                        print(
                            f"Dealer busted! Hand {hand_number} wins ${hand_bet:.2f}."
                        )
                        game.player.receive_winnings(hand_bet * 2)
                    elif hand_value > dealer_value:
                        print(
                            f"Hand {hand_number} wins! {hand_value} beats dealer's {dealer_value}. You win ${hand_bet:.2f}."
                        )
                        game.player.receive_winnings(hand_bet * 2)
                    elif dealer_value > hand_value:
                        print(
                            f"Hand {hand_number} loses. Dealer's {dealer_value} beats your {hand_value}. You lose ${hand_bet:.2f}."
                        )
                    else:
                        print(
                            f"Hand {hand_number} push. Both have {hand_value}. Your ${hand_bet:.2f} is returned."
                        )
                        game.player.receive_winnings(hand_bet)

                # Restore player's main hand
                game.player.hand = Hand()
                game.bet = 0
                round_completed = True
                break

            if round_completed:
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
                    game.player.receive_winnings(
                        game.bet * 2
                    )  # Return bet + win amount
                elif dealer_value > player_value:
                    print(
                        f"You lose. Dealer's {dealer_value} beats your {player_value}."
                    )
                    # No balance change needed as bet was already deducted
                else:
                    print(f"Push. Both have {player_value}.")
                    game.player.receive_winnings(game.bet)  # Return the bet on push

        print("\nYou're out of money! Game over.")

    # Run the test game
    play_test_game(show_strategy=True)


def main():
    """Main entry point for the program."""
    print("=" * 60)
    print("BLACKJACK SIMULATION PROGRAM")
    print("=" * 60)
    print("1. Play Blackjack Game with Strategy Suggestions")
    print("2. Play Blackjack Game without Strategy Suggestions")
    print("3. Run House Edge Simulation")
    print("4. Test Splitting (Pairs Mode)")
    print("5. Exit")
    print("=" * 60)

    while True:
        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            play_game(show_strategy=True)
        elif choice == "2":
            play_game(show_strategy=False)
        elif choice == "3":
            from simulation import run_simulation

            run_simulation()
        elif choice == "4":
            play_split_test_game()
        elif choice == "5":
            print("\nThank you for using the Blackjack Simulation Program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
