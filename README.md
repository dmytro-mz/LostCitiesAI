# Lost Cities AI

An independent, unofficial implementation of the classic card game **Lost Cities** with a focus on reinforcement learning (RL) agents. The project aims to provide a research and experimentation platform for AI agents, as well as allow human users to play against trained RL agents.

## Features

- Full game logic for two-player Lost Cities (classical rules)
- Modular codebase for easy extension and experimentation
- Baseline agents:
  - Random agent
  - Simple heuristic agent
- RL agent skeleton with model input encoding and action selection
- **Not yet implemented:**
  - Main script/CLI for running games or training
  - RL agent training loop
  - Human vs RL agent console interface
  - Output/logging and model saving

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd LostCitiesAI
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

- **Testing/Debugging:**
  - You can run the `if __name__ == "__main__"` blocks in `src/players/random_player.py` or `src/players/simple_player.py` to test the game logic and baseline agents.
- **Main scripts for training, evaluation, or human play are not yet implemented.**
- Future usage will include:
  - Training RL agents
  - Playing as a human against an RL agent in the console
  - Evaluating agent performance

## Planned Features / TODO

- [ ] Main script/CLI for running games, training, and evaluation
- [ ] Complete RL agent logic and training loop
- [ ] Human vs RL agent console interface
- [ ] Output/logging and model saving
- [ ] Enhanced documentation and examples
- [ ] (Optional) Support for additional variants or features

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Reference

Lost Cities is a card game designed by Reiner Knizia and published by Kosmos. This project is an independent, unofficial implementation for research and educational purposes. For more information about the original game, see [BoardGameGeek - Lost Cities](https://boardgamegeek.com/boardgame/50/lost-cities).
