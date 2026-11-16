import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import chess
import threading
from ai_engine import choose_move

# Modern slate / blue palette inspired by the supplied reference.
BG = "#2d3441"
PANEL = "#394252"
PANEL_DARK = "#303846"
LIGHT = "#d2d6df"
DARK = "#697383"
ACCENT = "#6d98c5"
ACCENT_HOVER = "#82acd6"
TEXT = "#edf1f7"
MUTED = "#aeb8c7"
HIGHLIGHT = "#e6cf69"
LEGAL = "#7eae91"
CHECK = "#d66b6b"

PIECES = {
    "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟"
}
PIECE_VALUES = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
}


class ModernChess:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Chess")
        self.root.geometry("1180x820")
        self.root.minsize(950, 700)
        self.root.configure(bg=BG)

        self.board = chess.Board()
        self.selected = None
        self.legal_targets = []
        self.flipped = False
        self.mode = tk.StringVar(value="Player vs Player")
        self.difficulty = tk.StringVar(value="Medium")
        self.ai_thinking = False
        self.game_over = False
        self.history_san = []
        self.captured_white = []
        self.captured_black = []
        self.last_move = None
        self.clock_enabled = tk.BooleanVar(value=False)
        self.clock_seconds = {chess.WHITE: 600, chess.BLACK: 600}
        self.clock_job = None
        self.ai_job_token = 0

        self._build_ui()
        self._draw_board()
        self._refresh_panel()
        self._tick_clock()

    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=22, pady=(14, 10))
        tk.Label(header, text="Modern Chess", bg=BG, fg=TEXT,
                 font=("Segoe UI", 25, "bold")).pack()

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.board_area = tk.Frame(body, bg=BG)
        self.board_area.pack(side="left", fill="both", expand=True, padx=(0, 18))

        self.canvas = tk.Canvas(self.board_area, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _e: self._draw_board())
        self.canvas.bind("<Button-1>", self._on_board_click)

        self.panel = tk.Frame(body, bg=PANEL, width=350, padx=18, pady=16)
        self.panel.pack(side="right", fill="y")
        self.panel.pack_propagate(False)

        self.turn_label = tk.Label(self.panel, text="White's turn", bg=PANEL,
                                   fg=TEXT, font=("Segoe UI", 19, "bold"))
        self.turn_label.pack(fill="x", pady=(0, 14))

        controls = tk.Frame(self.panel, bg=PANEL)
        controls.pack(fill="x")
        self._button(controls, "New Game", self.new_game, 0, 0)
        self._button(controls, "Undo", self.undo, 0, 1)
        self._button(controls, "Flip Board", self.flip_board, 1, 0)
        self._button(controls, "Resign", self.resign, 1, 1)

        options = tk.Frame(self.panel, bg=PANEL)
        options.pack(fill="x", pady=(12, 8))
        tk.Label(options, text="Game mode", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        mode_box = ttk.Combobox(options, textvariable=self.mode, state="readonly",
                                values=("Player vs Player", "Player vs Computer"))
        mode_box.grid(row=1, column=0, sticky="ew", pady=(3, 8))
        mode_box.bind("<<ComboboxSelected>>", lambda _e: self.new_game())

        tk.Label(options, text="AI difficulty", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w")
        self.difficulty_box = ttk.Combobox(
            options, textvariable=self.difficulty, state="readonly",
            values=("Easy", "Medium", "Hard"))
        self.difficulty_box.grid(row=3, column=0, sticky="ew", pady=(3, 8))
        options.columnconfigure(0, weight=1)

        clock_row = tk.Frame(self.panel, bg=PANEL)
        clock_row.pack(fill="x", pady=(0, 8))
        tk.Checkbutton(clock_row, text="10-minute clock", variable=self.clock_enabled,
                       command=self._toggle_clock, bg=PANEL, fg=TEXT,
                       activebackground=PANEL, activeforeground=TEXT,
                       selectcolor=PANEL_DARK, font=("Segoe UI", 10)).pack(side="left")
        self.clock_label = tk.Label(clock_row, text="10:00  |  10:00",
                                    bg=PANEL, fg=TEXT, font=("Consolas", 11, "bold"))
        self.clock_label.pack(side="right")

        self.message_label = tk.Label(self.panel, text="White to move",
                                      bg=PANEL, fg=ACCENT_HOVER,
                                      font=("Segoe UI", 11, "bold"), anchor="w")
        self.message_label.pack(fill="x", pady=(2, 10))

        self._section_title("Captured by White")
        self.white_captured_label = tk.Label(self.panel, text="—", bg=PANEL,
                                             fg=TEXT, font=("Segoe UI Symbol", 19),
                                             anchor="w")
        self.white_captured_label.pack(fill="x", pady=(2, 10))

        self._section_title("Captured by Black")
        self.black_captured_label = tk.Label(self.panel, text="—", bg=PANEL,
                                             fg=TEXT, font=("Segoe UI Symbol", 19),
                                             anchor="w")
        self.black_captured_label.pack(fill="x", pady=(2, 10))

        self._section_title("Move History")
        history_wrap = tk.Frame(self.panel, bg=PANEL_DARK)
        history_wrap.pack(fill="both", expand=True, pady=(4, 0))
        self.history = tk.Text(history_wrap, height=10, wrap="word",
                               bg=PANEL_DARK, fg=TEXT, insertbackground=TEXT,
                               relief="flat", font=("Consolas", 10),
                               padx=9, pady=8, state="disabled")
        scrollbar = ttk.Scrollbar(history_wrap, command=self.history.yview)
        self.history.configure(yscrollcommand=scrollbar.set)
        self.history.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        footer = tk.Label(self.panel, text="Python • Tkinter • python-chess",
                          bg=PANEL, fg=MUTED, font=("Segoe UI", 8))
        footer.pack(anchor="w", pady=(10, 0))

    def _button(self, parent, label, command, row, col):
        b = tk.Button(parent, text=label, command=command,
                      bg=ACCENT, fg="white", activebackground=ACCENT_HOVER,
                      activeforeground="white", relief="flat", bd=0,
                      font=("Segoe UI", 10, "bold"), padx=10, pady=9,
                      cursor="hand2")
        b.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
        parent.columnconfigure(col, weight=1)
        return b

    def _section_title(self, title):
        tk.Label(self.panel, text=title, bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", pady=(8, 0))
        tk.Frame(self.panel, bg="#505b6c", height=1).pack(fill="x", pady=(4, 2))

    def _board_metrics(self):
        w = max(self.canvas.winfo_width(), 500)
        h = max(self.canvas.winfo_height(), 500)
        size = min(w - 34, h - 34)
        size = max(360, size)
        x0 = (w - size) / 2
        y0 = (h - size) / 2
        return x0, y0, size / 8

    def _square_at(self, x, y):
        x0, y0, cell = self._board_metrics()
        file_ = int((x - x0) // cell)
        rank_from_top = int((y - y0) // cell)
        if not (0 <= file_ < 8 and 0 <= rank_from_top < 8):
            return None
        if self.flipped:
            file_, rank_from_top = 7 - file_, 7 - rank_from_top
        return chess.square(file_, 7 - rank_from_top)

    def _draw_board(self):
        if not hasattr(self, "canvas"):
            return
        c = self.canvas
        c.delete("all")
        x0, y0, cell = self._board_metrics()
        size = cell * 8

        checked_king = self.board.king(self.board.turn) if self.board.is_check() else None
        for display_r in range(8):
            for display_f in range(8):
                if self.flipped:
                    file_, rank_ = 7 - display_f, display_r
                else:
                    file_, rank_ = display_f, 7 - display_r
                sq = chess.square(file_, rank_)
                x1, y1 = x0 + display_f * cell, y0 + display_r * cell
                x2, y2 = x1 + cell, y1 + cell
                color = LIGHT if (file_ + rank_) % 2 == 1 else DARK

                if self.last_move and sq in (self.last_move.from_square, self.last_move.to_square):
                    color = "#b6b078"
                if sq == self.selected:
                    color = HIGHLIGHT
                if sq == checked_king:
                    color = CHECK

                c.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

                if sq in self.legal_targets:
                    if self.board.piece_at(sq):
                        c.create_oval(x1+5, y1+5, x2-5, y2-5,
                                      outline=LEGAL, width=5)
                    else:
                        r = cell * 0.105
                        cx, cy = (x1+x2)/2, (y1+y2)/2
                        c.create_oval(cx-r, cy-r, cx+r, cy+r,
                                      fill=LEGAL, outline=LEGAL)

                piece = self.board.piece_at(sq)
                if piece:
                    glyph = PIECES[piece.symbol()]
                    fg = "#f8f9fc" if piece.color == chess.WHITE else "#17202c"
                    outline = "#263447" if piece.color == chess.WHITE else "#d5dce7"
                    c.create_text((x1+x2)/2, (y1+y2)/2,
                                  text=glyph, fill=fg, font=("Segoe UI Symbol", int(cell*.72)),
                                  tags=("piece",))
                    # subtle square edge keeps pieces legible on both tones
                    c.create_text((x1+x2)/2, (y1+y2)/2,
                                  text="", fill=outline)

                # Coordinate labels
                if display_f == 0:
                    rank_label = str(rank_ + 1)
                    c.create_text(x1+7, y2-7, text=rank_label, anchor="sw",
                                  fill="#f5f5f5" if color == DARK else "#596273",
                                  font=("Segoe UI", 8, "bold"))
                if display_r == 7:
                    file_label = chess.FILE_NAMES[file_]
                    c.create_text(x2-6, y2-5, text=file_label, anchor="se",
                                  fill="#f5f5f5" if color == DARK else "#596273",
                                  font=("Segoe UI", 8, "bold"))

        c.create_rectangle(x0-2, y0-2, x0+size+2, y0+size+2,
                           outline="#566174", width=2)

    def _on_board_click(self, event):
        if self.game_over or self.ai_thinking:
            return
        if self.mode.get() == "Player vs Computer" and self.board.turn == chess.BLACK:
            return
        sq = self._square_at(event.x, event.y)
        if sq is None:
            return

        piece = self.board.piece_at(sq)
        if self.selected is None:
            if piece and piece.color == self.board.turn:
                self._select(sq)
            return

        if piece and piece.color == self.board.turn:
            self._select(sq)
            return

        candidate = next((m for m in self.board.legal_moves
                          if m.from_square == self.selected and m.to_square == sq), None)
        if candidate:
            if candidate.promotion:
                choice = simpledialog.askstring(
                    "Pawn promotion", "Promote to: q (Queen), r (Rook), b (Bishop), n (Knight)",
                    parent=self.root)
                p = {"q": chess.QUEEN, "r": chess.ROOK, "b": chess.BISHOP,
                     "n": chess.KNIGHT}.get((choice or "q").lower(), chess.QUEEN)
                candidate = chess.Move(candidate.from_square, candidate.to_square, promotion=p)
            self._make_move(candidate)
        else:
            self.selected = None
            self.legal_targets = []
            self._draw_board()

    def _select(self, sq):
        self.selected = sq
        self.legal_targets = [m.to_square for m in self.board.legal_moves
                              if m.from_square == sq]
        self._draw_board()

    def _make_move(self, move):
        if move not in self.board.legal_moves:
            return
        san = self.board.san(move)
        captured = self.board.piece_at(move.to_square)
        if self.board.is_en_passant(move):
            captured = chess.Piece(chess.PAWN, not self.board.turn)
        mover = self.board.turn
        if captured:
            glyph = PIECES[captured.symbol()]
            (self.captured_white if mover == chess.WHITE else self.captured_black).append(glyph)
        self.board.push(move)
        self.history_san.append((mover, san))
        self.last_move = move
        self.selected = None
        self.legal_targets = []
        self._refresh_panel()
        self._draw_board()
        self._check_end()
        if (not self.game_over and self.mode.get() == "Player vs Computer"
                and self.board.turn == chess.BLACK):
            self._start_ai_move()

    def _refresh_panel(self):
        turn = "White" if self.board.turn == chess.WHITE else "Black"
        self.turn_label.config(text=f"{turn}'s turn")
        if self.board.is_check():
            self.message_label.config(text=f"{turn} is in check!")
        elif self.ai_thinking:
            self.message_label.config(text="Computer is thinking...")
        else:
            self.message_label.config(text=f"{turn} to move")

        self.white_captured_label.config(text=" ".join(self.captured_white) or "—")
        self.black_captured_label.config(text=" ".join(self.captured_black) or "—")
        self.history.configure(state="normal")
        self.history.delete("1.0", "end")
        for i in range(0, len(self.history_san), 2):
            white = self.history_san[i][1]
            black = self.history_san[i+1][1] if i+1 < len(self.history_san) else ""
            line = f"{i//2 + 1:>2}.  {white:<9} {black}\n"
            self.history.insert("end", line)
        self.history.see("end")
        self.history.configure(state="disabled")
        self._update_clock_label()

    def _check_end(self):
        if not self.board.is_game_over(claim_draw=True):
            return
        self.game_over = True
        result = self.board.result(claim_draw=True)
        if self.board.is_checkmate():
            winner = "White" if self.board.turn == chess.BLACK else "Black"
            msg = f"Checkmate — {winner} wins!"
        elif self.board.is_stalemate():
            msg = "Draw — stalemate."
        elif self.board.is_insufficient_material():
            msg = "Draw — insufficient material."
        else:
            msg = f"Game over — {result}"
        self.turn_label.config(text=msg)
        self.message_label.config(text="Start a new game to play again.")
        messagebox.showinfo("Game Over", msg)

    def _start_ai_move(self):
        if self.ai_thinking or self.game_over:
            return
        self.ai_thinking = True
        self._refresh_panel()
        self.ai_job_token += 1
        token = self.ai_job_token
        board_copy = self.board.copy()
        level = self.difficulty.get().lower()

        def worker():
            move = choose_move(board_copy, level)
            self.root.after(0, lambda: self._finish_ai_move(token, move))
        threading.Thread(target=worker, daemon=True).start()

    def _finish_ai_move(self, token, move):
        if token != self.ai_job_token or self.game_over:
            return
        self.ai_thinking = False
        if move and move in self.board.legal_moves:
            self._make_move(move)
        else:
            self._refresh_panel()

    def new_game(self):
        self.ai_job_token += 1
        self.ai_thinking = False
        self.board.reset()
        self.selected = None
        self.legal_targets = []
        self.last_move = None
        self.history_san = []
        self.captured_white = []
        self.captured_black = []
        self.game_over = False
        self.clock_seconds = {chess.WHITE: 600, chess.BLACK: 600}
        self._draw_board()
        self._refresh_panel()

    def undo(self):
        if not self.board.move_stack or self.ai_thinking:
            return
        # In computer mode, undo the computer move and the player's preceding move.
        count = 2 if self.mode.get() == "Player vs Computer" and len(self.board.move_stack) >= 2 else 1
        for _ in range(count):
            if self.board.move_stack:
                self.board.pop()
            if self.history_san:
                self.history_san.pop()
        self._rebuild_captured()
        self.last_move = self.board.peek() if self.board.move_stack else None
        self.selected = None
        self.legal_targets = []
        self.game_over = False
        self._draw_board()
        self._refresh_panel()

    def _rebuild_captured(self):
        self.captured_white = []
        self.captured_black = []
        temp = chess.Board()
        for move in self.board.move_stack:
            captured = temp.piece_at(move.to_square)
            if temp.is_en_passant(move):
                captured = chess.Piece(chess.PAWN, not temp.turn)
            if captured:
                glyph = PIECES[captured.symbol()]
                (self.captured_white if temp.turn == chess.WHITE else self.captured_black).append(glyph)
            temp.push(move)

    def flip_board(self):
        self.flipped = not self.flipped
        self._draw_board()

    def resign(self):
        if self.game_over:
            return
        player = "White" if self.board.turn == chess.WHITE else "Black"
        if messagebox.askyesno("Resign", f"{player}, do you want to resign?"):
            self.game_over = True
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            self.turn_label.config(text=f"{winner} wins by resignation")
            self.message_label.config(text="Game ended by resignation.")

    def _toggle_clock(self):
        if self.clock_enabled.get():
            self.clock_seconds = {chess.WHITE: 600, chess.BLACK: 600}
        self._update_clock_label()

    def _update_clock_label(self):
        def fmt(sec):
            return f"{max(0, sec)//60:02d}:{max(0, sec)%60:02d}"
        self.clock_label.config(
            text=f"{fmt(self.clock_seconds[chess.WHITE])}  |  {fmt(self.clock_seconds[chess.BLACK])}")

    def _tick_clock(self):
        if self.clock_enabled.get() and not self.game_over and not self.ai_thinking:
            side = self.board.turn
            self.clock_seconds[side] -= 1
            if self.clock_seconds[side] <= 0:
                self.clock_seconds[side] = 0
                self.game_over = True
                winner = "Black" if side == chess.WHITE else "White"
                self.turn_label.config(text=f"{winner} wins on time")
                self.message_label.config(text="Time expired.")
            self._update_clock_label()
        self.root.after(1000, self._tick_clock)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernChess(root)
    root.mainloop()
