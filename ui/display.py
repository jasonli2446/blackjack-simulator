from game.hand import Hand


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
        # Check if hand contains an Ace that could be counted as 1 or 11
        has_ace = any(card.rank == "A" for card in hand.cards)
        ace_counts_as_11 = has_ace and value <= 21 and value - 10 != hand.get_value()

        if has_ace and ace_counts_as_11:
            alt_value = value - 10  # Value if Ace counted as 1 instead of 11
            print(f"Value: {alt_value}/{value}")  # Show both possible values
        else:
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


def display_input_method(use_video):
    """
    Display the current input method.

    Args:
        use_video (bool): Whether video input is enabled
    """
    if use_video:
        print("Input Method: Video Gestures (with keyboard fallback)")
        print(
            "Gestures: Hit = Tap twice, Stand = Wave, Double = One finger up, Split = V sign"
        )
    else:
        print("Input Method: Keyboard")
