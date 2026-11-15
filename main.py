
import tkinter as tk
from tkinter import simpledialog
import chess


class ChessGame:

    def __init__(self, root):
        self.root = root
        self.root.title("Python Chess Game")
        self.root.geometry("750x900")
        self.root.resizable(True, True)
        self.root.minsize(650, 750)

        self.board = chess.Board()
        self.selected_square = None
        self.legal_targets = []
        self.buttons = {}

        self.pieces = {
            "K": "♔", "Q": "♕", "R": "♖",
            "B": "♗", "N": "♘", "P": "♙",
            "k": "♚", "q": "♛", "r": "♜",
            "b": "♝", "n": "♞", "p": "♟"
        }

        self.create_interface()
        self.update_board()

    def create_interface(self):

        title = tk.Label(
            self.root,
            text="CHESS GAME",
            font=("Arial", 25, "bold")
        )
        title.pack(pady=10)

        self.status = tk.Label(
            self.root,
            text="White to move",
            font=("Arial", 15, "bold")
        )
        self.status.pack(pady=5)

        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10, expand=True)

        for row in range(8):
            for col in range(8):

                square = chess.square(col, 7 - row)

                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Segoe UI Symbol", 28),
                    width=2,
                    height=1,
                    relief="flat",
                    command=lambda s=square: self.click_square(s)
                )

                button.grid(row=row, column=col)
                self.buttons[square] = button

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Button(
            control_frame,
            text="Undo",
            font=("Arial", 12),
            width=12,
            command=self.undo_move
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            control_frame,
            text="Restart",
            font=("Arial", 12),
            width=12,
            command=self.restart_game
        ).grid(row=0, column=1, padx=10)

        self.move_label = tk.Label(
            self.root,
            text="Move: 1",
            font=("Arial", 12)
        )
        self.move_label.pack(pady=5)

    def click_square(self, square):

        if self.board.is_game_over():
            return

        piece = self.board.piece_at(square)

        # Select a piece belonging to the current player
        if piece and piece.color == self.board.turn:

            self.selected_square = square

            self.legal_targets = [
                move.to_square
                for move in self.board.legal_moves
                if move.from_square == square
            ]

            self.update_board()
            return

        # Try to move the selected piece
        if self.selected_square is not None:

            possible_moves = [
                move for move in self.board.legal_moves
                if move.from_square == self.selected_square
                and move.to_square == square
            ]

            if possible_moves:
                move = possible_moves[0]

                # Handle pawn promotion
                if move.promotion:
                    choice = simpledialog.askstring(
                        "Pawn Promotion",
                        "Choose promotion: Queen, Rook, Bishop or Knight\n"
                        "Enter q, r, b or n:",
                        parent=self.root
                    )

                    promotion = {
                        "q": chess.QUEEN,
                        "r": chess.ROOK,
                        "b": chess.BISHOP,
                        "n": chess.KNIGHT
                    }.get((choice or "q").lower(), chess.QUEEN)

                    move = chess.Move(
                        move.from_square,
                        move.to_square,
                        promotion=promotion
                    )

                self.board.push(move)

            self.selected_square = None
            self.legal_targets = []
            self.update_board()

    def update_board(self):

        for square, button in self.buttons.items():

            piece = self.board.piece_at(square)

            symbol = ""
            if piece:
                symbol = self.pieces[piece.symbol()]

            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)

            color = (
                "#F0D9B5"
                if (row + col) % 2 == 0
                else "#B58863"
            )

            if square == self.selected_square:
                color = "#F7EC6E"

            elif square in self.legal_targets:
                color = "#A9D18E"

            button.config(
                text=symbol,
                bg=color,
                activebackground=color,
                fg="#171717"
            )

        self.update_status()

    def update_status(self):

        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            message = f"CHECKMATE! {winner} wins!"

        elif self.board.is_stalemate():
            message = "DRAW - Stalemate!"

        elif self.board.is_insufficient_material():
            message = "DRAW - Insufficient material!"

        elif self.board.is_game_over(claim_draw=True):
            message = "GAME OVER - Draw!"

        else:
            player = "White" if self.board.turn else "Black"

            message = f"{player} to move"

            if self.board.is_check():
                message += " - CHECK!"

        self.status.config(text=message)

        self.move_label.config(
            text=f"Move: {self.board.fullmove_number}"
        )

    def undo_move(self):

        if self.board.move_stack:
            self.board.pop()

        self.selected_square = None
        self.legal_targets = []

        self.update_board()

    def restart_game(self):

        self.board.reset()
        self.selected_square = None
        self.legal_targets = []

        self.update_board()


if __name__ == "__main__":

    root = tk.Tk()

    game = ChessGame(root)

    root.mainloop()
