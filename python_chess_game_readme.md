# Python Chess Game

A fully functional, 2D graphical chess application built in Python. This project features a complete playable board, turn-based mechanics, and dynamic move highlighting to help players visualize their strategies.

## Features

* **Turn Tracking:** The UI automatically tracks and displays whether it is "White to move" or "Black to move."
* **Visual Highlighting:** Click on a piece to highlight it (yellow) and see its valid destination squares (green).
* **Clean Interface:** A minimalist and intuitive design for distraction-free gameplay.
* **Full Chess Logic:** Evaluates legal moves for all piece types on a standard 8x8 matrix.

## Screenshots

### Starting Position
![Initial Board Setup](image_76d266.png)

### Mid-Game (Black to Move)
![Black's Turn](Screenshot%202026-11-15%20213143.png)

### Move Highlighting (White to Move)
![Highlighting Valid Moves](Screenshot%202026-11-15%20213213.png)

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