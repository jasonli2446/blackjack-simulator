import time
import cv2
from game.game import Game
from game.strategy import Strategy
from game.hand import Hand
from game.card import Card
from ui.display import display_hand, display_game_state, display_input_method
from input.keyboard_input import KeyboardInputHandler
from input.video_input import VideoInputHandler
from config import Config


def get_input_handler(config):
    """
    Get the appropriate input handler based on configuration.

    Args:
        config (Config): Configuration manager

    Returns:
        InputHandler: The configured input handler
    """
    use_video = config.get("input", "use_video", False)

    if use_video:
        display_video = config.get("input", "display_video", True)
        keyboard_fallback = config.get("input", "keyboard_fallback", True)
        handler = VideoInputHandler(
            keyboard_fallback=keyboard_fallback, display_video=display_video
        )

        # Try to set up video input
        if not handler.setup():
            print("Failed to set up video input. Falling back to keyboard.")
            return KeyboardInputHandler()

        return handler
    else:
        return KeyboardInputHandler()


def settings_menu(config):
    """
    Display and update settings.

    Args:
        config (Config): Configuration manager
    """
    while True:
        print("\n" + "=" * 60)
        print("SETTINGS")
        print("=" * 60)
        print(
            f"1. Input Method: {'Video Gestures' if config.get('input', 'use_video') else 'Keyboard'}"
        )
        print(
            f"2. Display Video: {'Yes' if config.get('input', 'display_video') else 'No'}"
        )
        print(
            f"3. Keyboard Fallback: {'Yes' if config.get('input', 'keyboard_fallback') else 'No'}"
        )
        print(
            f"4. Show Strategy Suggestions: {'Yes' if config.get('game', 'show_strategy') else 'No'}"
        )
        print(f"5. Initial Balance: ${config.get('game', 'initial_balance')}")
        print(f"6. Default Bet: ${config.get('game', 'default_bet')}")
        print(
            f"7. Auto-Betting: {'Enabled' if config.get('game', 'auto_bet_enabled', False) else 'Disabled'}"
        )
        print(
            f"8. Auto-Bet Amount: ${config.get('game', 'auto_bet_amount', config.get('game', 'default_bet'))}"
        )
        print("9. Back to Main Menu")
        print("=" * 60)

        choice = input("\nEnter your choice (1-9): ")

        if choice == "1":
            use_video = not config.get("input", "use_video")
            config.set("input", "use_video", use_video)
            print(
                f"Input method set to {'Video Gestures' if use_video else 'Keyboard'}"
            )

            # Check if OpenCV and MediaPipe are available
            if use_video:
                try:
                    import cv2
                    import mediapipe

                    # Test camera access
                    cap = cv2.VideoCapture(0)
                    ret, _ = cap.read()
                    cap.release()
                    if not ret:
                        print(
                            "Warning: Could not access camera. Video input may not work."
                        )
                except ImportError:
                    print(
                        "Warning: Required packages not found. Please install OpenCV and MediaPipe:"
                    )
                    print("pip install opencv-python mediapipe")
                    config.set("input", "use_video", False)

            # Add pause to let user read the message
            print("\nReturning to settings menu...")
            time.sleep(1.5)

        elif choice == "2":
            display_video = not config.get("input", "display_video")
            config.set("input", "display_video", display_video)
            print(f"Display video set to {'Yes' if display_video else 'No'}")
            print("\nReturning to settings menu...")
            time.sleep(1)

        elif choice == "3":
            keyboard_fallback = not config.get("input", "keyboard_fallback")
            config.set("input", "keyboard_fallback", keyboard_fallback)
            print(f"Keyboard fallback set to {'Yes' if keyboard_fallback else 'No'}")
            print("\nReturning to settings menu...")
            time.sleep(1)

        elif choice == "4":
            show_strategy = not config.get("game", "show_strategy")
            config.set("game", "show_strategy", show_strategy)
            print(f"Strategy suggestions set to {'Yes' if show_strategy else 'No'}")
            print("\nReturning to settings menu...")
            time.sleep(1)

        elif choice == "5":
            try:
                balance = float(input("Enter initial balance: "))
                if balance > 0:
                    config.set("game", "initial_balance", balance)
                    print(f"Initial balance set to ${balance}")
                else:
                    print("Balance must be positive.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            print("\nReturning to settings menu...")
            time.sleep(1)

        elif choice == "6":
            try:
                bet = float(input("Enter default bet: "))
                if bet > 0:
                    config.set("game", "default_bet", bet)
                    print(f"Default bet set to ${bet}")
                else:
                    print("Bet must be positive.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            print("\nReturning to settings menu...")
            time.sleep(1)

        elif choice == "7":
            auto_bet_enabled = not config.get("game", "auto_bet_enabled", False)
            config.set("game", "auto_bet_enabled", auto_bet_enabled)
            print(
                f"Auto-betting set to {'Enabled' if auto_bet_enabled else 'Disabled'}"
            )
            print("\nReturning to settings menu...")
            time.sleep(1)

        elif choice == "8":
            try:
                auto_bet_amount = float(input("Enter auto-bet amount: "))
                if auto_bet_amount > 0:
                    config.set("game", "auto_bet_amount", auto_bet_amount)
                    # Also enable auto-betting if it wasn't already
                    if not config.get("game", "auto_bet_enabled", False):
                        config.set("game", "auto_bet_enabled", True)
                        print("Auto-betting has been enabled.")
                    print(f"Auto-bet amount set to ${auto_bet_amount}")
                else:
                    print("Bet amount must be positive.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            print("\nReturning to settings menu...")
            time.sleep(1)

        elif choice == "9":
            print("Returning to main menu...")
            time.sleep(1)
            break

        else:
            print("Invalid choice. Please enter 1-9.")
            time.sleep(1)


def play_game():
    """Main function to play the blackjack game with configurable input."""
    # Load configuration
    config = Config()

    # Get the appropriate input handler
    input_handler = get_input_handler(config)

    # Initialize game
    game = Game()

    # Set initial balance from config
    initial_balance = config.get("game", "initial_balance", 1000.0)
    game.player.balance = initial_balance

    # Get show strategy setting from config
    show_strategy = config.get("game", "show_strategy", True)

    # Get auto-betting settings
    auto_bet = config.get("game", "auto_bet_enabled", False)
    auto_bet_amount = config.get(
        "game", "auto_bet_amount", config.get("game", "default_bet")
    )

    print("Welcome to Blackjack!")
    print(
        "In this game, you'll see the perfect strategy in action."
        if show_strategy
        else "In this game, you'll play without strategy suggestions."
    )
    print(f"Your initial balance is ${initial_balance:.2f}.\n")

    # Display input method
    display_input_method(config.get("input", "use_video", False))

    # Display auto-betting status
    if auto_bet:
        print(f"Auto-betting is enabled with amount: ${auto_bet_amount:.2f}")
    else:
        print("Auto-betting is disabled. You'll be prompted for bet amounts.")
    print()

    try:
        # Main game loop
        while game.player.balance > 0:
            print(f"Current Balance: ${game.player.balance:.2f}")

            # Get bet amount
            if auto_bet:
                # Use auto-bet amount
                bet_amount = min(auto_bet_amount, game.player.balance)
                print(f"Auto-betting ${bet_amount:.2f}")
            else:
                print("\n" + "=" * 40)
                print("BETTING")
                print("=" * 40)
                print("Enter a number to bet that amount")
                print("Enter 'q' to quit the game")
                print("Enter 'a' to enable auto-betting")
                print("=" * 40)

                while True:
                    bet_input = input_handler.get_bet_amount(game.player.balance)

                    if bet_input == "q":
                        print(
                            f"\nThank you for playing! Final balance: ${game.player.balance:.2f}"
                        )
                        return
                    elif bet_input == "a":
                        try:
                            auto_bet_amount = float(
                                input("Enter your auto-bet amount: ")
                            )
                            if auto_bet_amount <= 0:
                                print("Bet amount must be positive.")
                                continue
                            auto_bet = True
                            # Save the auto-bet settings to config
                            config.set("game", "auto_bet_enabled", True)
                            config.set("game", "auto_bet_amount", auto_bet_amount)
                            bet_amount = min(auto_bet_amount, game.player.balance)
                            print(f"Auto-bet set to ${auto_bet_amount:.2f}")
                            break
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                            continue

                    if isinstance(bet_input, float) or isinstance(bet_input, int):
                        bet_amount = bet_input
                        if bet_amount <= 0:
                            print("Bet amount must be positive.")
                        elif bet_amount > game.player.balance:
                            all_in = input(
                                f"Bet exceeds your balance of ${game.player.balance:.2f}. Go all in? (y/n): "
                            ).lower()
                            if all_in in ["y", "yes"]:
                                bet_amount = game.player.balance
                                print(f"Going all in with ${bet_amount:.2f}!")
                                break
                        else:
                            break
                    else:
                        print("Invalid input. Please enter a number.")

            # Start the round
            result, player_hand, dealer_hand, bet, win_amount = game.play_round(
                bet_amount
            )

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

                # Get action from input handler
                action = input_handler.get_action()

                if action is None:
                    print("Invalid action. Please try again.")
                    continue

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
                    # The split logic remains the same - just a snippet shown for brevity
                    # In a real implementation, you would include the full split logic here
                    if (
                        not game.player.hand.is_pair()
                        or len(game.player.hand.cards) != 2
                    ):
                        print(
                            "Cannot split: must have exactly two cards of the same rank."
                        )
                        first_action = False
                        continue

                    if game.player.balance < bet_amount:
                        print("Cannot split: insufficient balance for additional bet.")
                        first_action = False
                        continue

                    print("Splitting hand...")
                    time.sleep(1)

                    # ... rest of split logic ...

                    # For brevity, let's simulate a quick resolution
                    print("Split hands played.")
                    round_completed = True
                    break

            # ... rest of player and dealer turn logic ...

            if round_completed:
                continue

            # ... dealer's turn logic ...

        print("\nYou're out of money! Game over.")

    finally:
        # Clean up resources
        input_handler.cleanup()


def main():
    """Main entry point for the program."""
    # Load configuration
    config = Config()

    while True:
        print("\n" + "=" * 60)
        print("BLACKJACK SIMULATION PROGRAM")
        print("=" * 60)
        print("1. Play Blackjack Game")
        print("2. Run House Edge Simulation")
        print("3. Settings")
        print("4. Exit")
        print("=" * 60)

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            play_game()
            print("\nReturning to main menu...")
            time.sleep(1.5)
        elif choice == "2":
            from simulation import run_simulation

            run_simulation()
            print("\nReturning to main menu...")
            time.sleep(1.5)
        elif choice == "3":
            settings_menu(config)
            # No need for another message here as settings_menu already shows one
        elif choice == "4":
            print("\nThank you for using the Blackjack Simulation Program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
            time.sleep(1)


if __name__ == "__main__":
    main()
