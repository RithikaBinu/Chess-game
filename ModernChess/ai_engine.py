import chess
import random

VALUES = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 335,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
}

def evaluate(board):
    """Positive scores favor Black (the computer); negative scores favor White."""
    if board.is_checkmate():
        return 100000 if board.turn == chess.BLACK else -100000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for piece_type, value in VALUES.items():
        score += len(board.pieces(piece_type, chess.BLACK)) * value
        score -= len(board.pieces(piece_type, chess.WHITE)) * value

    # Small positional bonuses: center control and piece activity.
    center = [chess.D4, chess.E4, chess.D5, chess.E5]
    for sq in center:
        p = board.piece_at(sq)
        if p:
            score += (18 if p.color == chess.BLACK else -18)

    score += (len(list(board.legal_moves)) * 2) * (1 if board.turn == chess.BLACK else -1)
    return score

def ordered_moves(board):
    moves = list(board.legal_moves)
    def priority(move):
        score = 0
        victim = board.piece_at(move.to_square)
        attacker = board.piece_at(move.from_square)
        if victim:
            score += 10 * VALUES[victim.piece_type] - VALUES[attacker.piece_type]
        if move.promotion:
            score += VALUES[move.promotion]
        if board.gives_check(move):
            score += 40
        return score
    return sorted(moves, key=priority, reverse=True)

def minimax(board, depth, alpha, beta):
    if depth == 0 or board.is_game_over(claim_draw=True):
        return evaluate(board), None

    best_move = None
    # Black maximizes, White minimizes.
    maximizing = board.turn == chess.BLACK
    best_score = -10**9 if maximizing else 10**9

    for move in ordered_moves(board):
        board.push(move)
        score, _ = minimax(board, depth - 1, alpha, beta)
        board.pop()

        if maximizing:
            if score > best_score:
                best_score, best_move = score, move
            alpha = max(alpha, best_score)
        else:
            if score < best_score:
                best_score, best_move = score, move
            beta = min(beta, best_score)

        if beta <= alpha:
            break

    return best_score, best_move

def choose_move(board, level="medium"):
    """Choose a legal move for Black. Easy is randomized; higher levels search deeper."""
    legal = list(board.legal_moves)
    if not legal:
        return None

    if level == "easy":
        # Prefer captures/promotions, but retain some variety.
        good = [m for m in legal if board.is_capture(m) or m.promotion]
        return random.choice(good if good and random.random() < 0.65 else legal)

    depth = 2 if level == "medium" else 3
    _, move = minimax(board, depth, -10**9, 10**9)
    return move or random.choice(legal)
