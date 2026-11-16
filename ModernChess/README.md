# Modern Chess ♟

A desktop chess application built with Python, Tkinter, Canvas and `python-chess`.
The interface uses a modern slate/blue theme inspired by the supplied design.

## Features

- Player vs Player on one computer
- Player vs Computer with built-in minimax AI
- Easy, Medium and Hard AI levels
- Click-to-select pieces and legal-move indicators
- Check, checkmate, stalemate and draw detection
- Pawn promotion (Q/R/B/N)
- Undo (undoes a full player/computer turn in computer mode)
- New Game and board flipping
- Captured-piece display
- Move history
- Optional 10-minute chess clock
- Unicode chess pieces; no image assets required

## Requirements

- Python 3.9+
- Tkinter (included with most Windows Python installations)
- python-chess

## Setup

```bash
python -m pip install -r requirements.txt
```

On Windows, if Tkinter is missing, reinstall Python from python.org and enable Tcl/Tk support.

## Run

```bash
python main.py
```

## How to play

1. Choose `Player vs Player` or `Player vs Computer`.
2. In computer mode, White is the human and Black is the computer.
3. Click a piece, then click a highlighted legal destination.
4. Use Undo, New Game or Flip Board as needed.
5. Enable the 10-minute clock checkbox if desired.

## AI note

The built-in AI uses a small material/position evaluation and alpha-beta minimax.
Hard mode searches deeper and may take longer on slower computers. It is a learning-project AI, not a replacement for Stockfish.

## GitHub

Suggested repository name: `Modern-Chess`
