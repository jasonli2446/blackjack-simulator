# Blackjack Simulator

This project is a Blackjack simulator that allows you to play the game of Blackjack or run simulations to estimate the house edge using perfect strategy.

## Features

- Play Blackjack with or without strategy suggestions.
- Simulate many hands to estimate the house edge.
- Implements perfect Blackjack strategy for decision-making.
- Supports splitting and doubling down.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/jasonli2446/blackjack-simulator.git
   cd blackjack-simulator
   ```

2. Ensure you have Python installed (version 3.6 or higher).

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Playing the Game

To play the Blackjack game with strategy suggestions, run:

```sh
python main.py
```

Follow the on-screen instructions to place bets and make decisions.

### Running Simulations

To run a simulation to estimate the house edge, select the appropriate option from the main menu:

```sh
python main.py
```

Choose the option to run the house edge simulation and follow the prompts to enter the number of hands and bet size.

## Project Structure

- `card.py`: Defines the `Card` class representing a playing card.
- `dealer.py`: Defines the `Dealer` class representing the dealer.
- `deck.py`: Defines the `Deck` class representing an infinite deck of cards.
- `hand.py`: Defines the `Hand` class representing a player's hand.
- `player.py`: Defines the `Player` class representing a player.
- `strategy.py`: Implements the perfect Blackjack strategy.
- `game.py`: Manages the game state and flow.
- `simulation.py`: Runs simulations to estimate the house edge.
- `main.py`: Entry point for playing the game or running simulations.

## Notes

- The simulator assumes an infinite deck of cards with replacement.
- The house edge calculation may vary based on the number of hands simulated and the bet size.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
