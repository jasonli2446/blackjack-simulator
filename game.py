from deck import Deck
from player import Player
from dealer import Dealer
from strategy import Strategy


class Game:
    """
    Manages the game state and flow for a blackjack game.

    Attributes:
        deck (Deck): The deck of cards.
        player (Player): The player in the game.
        dealer (Dealer): The dealer in the game.
        bet (float): The current bet.
    """

    def __init__(self):
        """Initialize a new game with a deck, player, and dealer."""
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()
        self.bet = 0.0

    def start_round(self, bet_amount):
        """
        Start a new round of blackjack.

        Args:
            bet_amount (float): The amount to bet for this round.

        Returns:
            bool: True if the round starts successfully, False otherwise.
        """
        # Place the bet
        bet = self.player.place_bet(bet_amount)
        if bet == 0:
            return False

        self.bet = bet

        # Clear hands from previous round
        self.player.clear_hands()
        self.dealer.clear_hand()

        # Deal initial cards
        self.player.hand.add_card(self.deck.deal_card())
        self.dealer.hand.add_card(self.deck.deal_card())
        self.player.hand.add_card(self.deck.deal_card())
        self.dealer.hand.add_card(self.deck.deal_card())

        # Set dealer's upcard
        self.dealer.set_upcard()

        return True

    def check_blackjack(self):
        """
        Check for blackjack at the start of the round.

        Returns:
            tuple: (True, result) if the game ends with blackjack, (False, None) otherwise.
                  result is one of "player_blackjack", "dealer_blackjack", or "push".
        """
        player_blackjack = self.player.hand.is_blackjack()
        dealer_blackjack = self.dealer.hand.is_blackjack()

        if player_blackjack and dealer_blackjack:
            # Push - both have blackjack
            self.player.receive_winnings(self.bet)  # Return the bet
            return True, "push"
        elif player_blackjack:
            # Player wins with blackjack (3:2 payout)
            self.player.receive_winnings(self.bet * 2.5)  # Original bet + 1.5x win
            return True, "player_blackjack"
        elif dealer_blackjack:
            # Dealer wins with blackjack
            return True, "dealer_blackjack"

        # No blackjack, continue the game
        return False, None

    def player_turn(self):
        """
        Execute the player's turn according to perfect strategy.

        Returns:
            bool: True if the player busts, False otherwise.
        """
        first_action = True

        while True:
            action = self.player.decide_action(self.dealer.upcard, first_action)

            if action == Strategy.HIT:
                self.player.hand.add_card(self.deck.deal_card())
                if self.player.hand.get_value() > 21:
                    return True  # Player busts
                first_action = False

            elif action == Strategy.STAND:
                return False  # Player stands, no bust

            elif action == Strategy.DOUBLE:
                # Double the bet if balance allows
                additional_bet = min(self.bet, self.player.balance)
                if additional_bet > 0:
                    self.player.balance -= additional_bet
                    self.bet += additional_bet

                # Take exactly one more card and end turn
                self.player.hand.add_card(self.deck.deal_card())
                return self.player.hand.get_value() > 21  # True if bust

            elif action == Strategy.SPLIT:
                # Implementation of split action would go here
                # This is more complex, as it involves creating multiple hands
                # For simplicity in this initial implementation, we'll treat split as hit
                self.player.hand.add_card(self.deck.deal_card())
                if self.player.hand.get_value() > 21:
                    return True  # Player busts
                first_action = False

    def dealer_turn(self):
        """
        Execute the dealer's turn according to fixed rules.

        Returns:
            bool: True if the dealer busts, False otherwise.
        """
        while self.dealer.should_hit():
            self.dealer.hand.add_card(self.deck.deal_card())
            if self.dealer.hand.get_value() > 21:
                return True  # Dealer busts

        return False  # Dealer doesn't bust

    def determine_winner(self):
        """
        Determine the winner of the round and update player's balance.

        Returns:
            str: The result of the round ("player_wins", "dealer_wins", or "push").
        """
        player_value = self.player.hand.get_value()
        dealer_value = self.dealer.hand.get_value()

        if player_value > 21:
            # Player busts, dealer wins
            return "dealer_wins"
        elif dealer_value > 21:
            # Dealer busts, player wins
            self.player.receive_winnings(self.bet * 2)  # Original bet + 1x win
            return "player_wins"
        elif player_value > dealer_value:
            # Player's hand value is higher, player wins
            self.player.receive_winnings(self.bet * 2)  # Original bet + 1x win
            return "player_wins"
        elif dealer_value > player_value:
            # Dealer's hand value is higher, dealer wins
            return "dealer_wins"
        else:
            # Equal values, push
            self.player.receive_winnings(self.bet)  # Return the bet
            return "push"

    def play_round(self, bet_amount):
        """
        Play a complete round of blackjack.

        Args:
            bet_amount (float): The amount to bet for this round.

        Returns:
            tuple: (result, player_hand, dealer_hand, bet, win_amount)
                  result is the outcome of the round.
        """
        # Start the round
        if not self.start_round(bet_amount):
            return "insufficient_balance", None, None, 0, 0

        # Check for blackjack
        blackjack_result, outcome = self.check_blackjack()
        if blackjack_result:
            win_amount = 0
            if outcome == "player_blackjack":
                win_amount = self.bet * 1.5
            elif outcome == "push":
                win_amount = 0
            return outcome, self.player.hand, self.dealer.hand, self.bet, win_amount

        # Return the initial state without playing through player and dealer turns
        return "continue", self.player.hand, self.dealer.hand, self.bet, 0
