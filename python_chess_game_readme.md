# Python Chess Game

A fully functional, 2D graphical chess application built in Python. This project features a complete playable board, turn-based mechanics, and dynamic move highlighting to help players visualize their strategies.

## Features

* **Turn Tracking:** The UI automatically tracks and displays whether it is "White to move" or "Black to move."
* **Visual Highlighting:** Click on a piece to highlight it (yellow) and see its valid destination squares (green).
* **Clean Interface:** A minimalist and intuitive design for distraction-free gameplay.
* **Full Chess Logic:** Evaluates legal moves for all piece types on a standard 8x8 matrix.

## Screenshots

### Starting Position
![Initial Board Setup] 
<img width="932" height="1078" alt="Screenshot 2026-11-15 213028" src="https://github.com/user-attachments/assets/9c31b944-6fe3-4e0c-9fb4-adf84bf16928" />


### Mid-Game (Black to Move)
![Black's Turn]
<img width="933" height="1078" alt="Screenshot 2026-11-15 213143" src="https://github.com/user-attachments/assets/f85856a7-3b66-4d04-b5e7-7832454f28f8" />


### Move Highlighting (White to Move)
![Highlighting Valid Moves]
<img width="927" height="1078" alt="Screenshot 2026-11-15 213213" src="https://github.com/user-attachments/assets/1f694765-b340-4fc2-be60-e5f7f16083a1" />


## Installation and Setup

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   ```
2. Navigate into the project directory:
   ```bash
   cd your-repo-name
   ```
3. Run the main Python script to launch the game:
   ```bash
   python game.py 
   ```
   *(Note: If your main script has a different name, replace `game.py` with the correct filename).*

## How to Play

* **Select a Piece:** Left-click on any of your pieces to select it. The square will highlight to indicate it is active.
* **Make a Move:** Left-click on a valid destination square to move your piece. 
* **Turns:** The game will automatically pass the turn to the opponent after a successful move.
