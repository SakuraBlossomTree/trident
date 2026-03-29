# All the different imports

import chess
from chess import Board 
import sys
import math
import time

# Global constants

board = Board()
nodes_searched = 0
search_start = 0
time_limit = 0

# Piece values and PST 
# https://www.chessprogramming.org/Simplified_Evaluation_Function  Got them from this link

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

pawnEvalWhite = [
    0,  0,  0,  0,  0,  0,  0,  0,   
    5, 10, 10,-20,-20, 10, 10,  5,   
    5, -5,-10,  0,  0,-10, -5,  5,   
    0,  0,  0, 20, 20,  0,  0,  0,   
    5,  5, 10, 25, 25, 10,  5,  5,   
    10, 10, 20, 30, 30, 20, 10, 10,  
    50, 50, 50, 50, 50, 50, 50, 50,  
    0,  0,  0,  0,  0,  0,  0,  0    
]

pawnEvalBlack = list(reversed(pawnEvalWhite))

knightEval = [
    -50,-40,-30,-30,-30,-30,-40,-50,  
    -40,-20,  0,  5,  5,  0,-20,-40,  
    -30,  5, 10, 15, 15, 10,  5,-30,  
    -30,  0, 15, 20, 20, 15,  0,-30,  
    -30,  5, 15, 20, 20, 15,  5,-30,  
    -30,  0, 10, 15, 15, 10,  0,-30,  
    -40,-20,  0,  0,  0,  0,-20,-40,  
    -50,-40,-30,-30,-30,-30,-40,-50   
]


bishopEvalWhite = [
    -20,-10,-10,-10,-10,-10,-10,-20,  
    -10,  5,  0,  0,  0,  0,  5,-10,  
    -10, 10, 10, 10, 10, 10, 10,-10,  
    -10,  0, 10, 10, 10, 10,  0,-10,  
    -10,  5,  5, 10, 10,  5,  5,-10,  
    -10,  0,  5, 10, 10,  5,  0,-10,  
    -10,  0,  0,  0,  0,  0,  0,-10,  
    -20,-10,-10,-10,-10,-10,-10,-20   
]

bishopEvalBlack = list(reversed(bishopEvalWhite))

rookEvalWhite = [
    0,  0,  0,  5,  5,  0,  0,  0,    
    -5,  0,  0,  0,  0,  0,  0, -5,   
    -5,  0,  0,  0,  0,  0,  0, -5,   
    -5,  0,  0,  0,  0,  0,  0, -5,   
    -5,  0,  0,  0,  0,  0,  0, -5,   
    -5,  0,  0,  0,  0,  0,  0, -5,   
    5, 10, 10, 10, 10, 10, 10,  5,   
    0,  0,  0,  0,  0,  0,  0,  0    
]

rookEvalBlack = list(reversed(rookEvalWhite))

queenEval = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20

]

kingEvalWhite = [
    20, 30, 10,  0,  0, 10, 30, 20,  
    20, 20,  0,  0,  0,  0, 20, 20,  
    -10,-20,-20,-20,-20,-20,-20,-10, 
    -20,-30,-30,-40,-40,-30,-30,-20, 
    -30,-40,-40,-50,-50,-40,-40,-30, 
    -30,-40,-40,-50,-50,-40,-40,-30, 
    -30,-40,-40,-50,-50,-40,-40,-30, 
    -30,-40,-40,-50,-50,-40,-40,-30  
]

kingEvalBlack = list(reversed(kingEvalWhite))

kingEvalEndGameWhite = [
    -50,-30,-30,-30,-30,-30,-30,-50,  
    -30,-30,  0,  0,  0,  0,-30,-30,  
    -30,-10, 20, 30, 30, 20,-10,-30,  
    -30,-10, 30, 40, 40, 30,-10,-30,  
    -30,-10, 30, 40, 40, 30,-10,-30,  
    -30,-10, 20, 30, 30, 20,-10,-30,  
    -30,-20,-10,  0,  0,-10,-20,-30,  
    -50,-40,-30,-20,-20,-30,-40,-50   
]
kingEvalEndGameBlack = list(reversed(kingEvalEndGameWhite))

# Evaluate piece 
# We check what the piece type is and based on that we return the table and also used flipped variants for black and if end_game is True then we use the king end_game variable
def evaluate_piece(piece, square, end_game):
    piece_type = piece.piece_type
    mapping = []
    if piece_type == chess.PAWN:
        mapping = pawnEvalWhite if piece.color == chess.WHITE else pawnEvalBlack
    if piece_type == chess.KNIGHT:
        mapping = knightEval
    if piece_type == chess.BISHOP:
        mapping = bishopEvalWhite if piece.color == chess.WHITE else bishopEvalBlack
    if piece_type == chess.ROOK:
        mapping = rookEvalWhite if piece.color == chess.WHITE else rookEvalBlack
    if piece_type == chess.QUEEN:
        mapping = queenEval
    if piece_type == chess.KING:
        if end_game:
            mapping = (
                kingEvalEndGameWhite
                if piece.color == chess.WHITE
                else kingEvalEndGameBlack
            )
        else:
            mapping = kingEvalWhite if piece.color == chess.WHITE else kingEvalBlack

    return mapping[square]

# We then evaluate the board
# We do this by first checking the endgame, if there are no queens left then we are in endgame 
# We then check for every square in the board that is there a piece (I know this is very expensive but that is all I can think about)
# We then get the the value of the piece and it's positional value and add those up, we also flip the value for black
# We then calculate the mobility, which is done by seeing how many legal_moves are there and calculate for both white and black
# We then return the final_eval

def evaluate_board(board):
    total = 0

    is_endgame = (
        not board.pieces(chess.QUEEN, chess.WHITE) and
        not board.pieces(chess.QUEEN, chess.BLACK)
    )

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue
        
        value = piece_values[piece.piece_type] + evaluate_piece(piece, square, is_endgame)
        total += value if piece.color == chess.WHITE else -value

    def count_mobility(board, color):
        original_turn = board.turn
        board.turn = color
        mobility = len(list(board.legal_moves))
        board.turn = original_turn
        return mobility

    white_mob = count_mobility(board, chess.WHITE)
    black_mob = count_mobility(board, chess.BLACK)
    mobility = 2 * (white_mob - black_mob)

    final_eval = total + mobility

    # final_eval = total

    if board.turn == chess.WHITE:
        return final_eval
    else:
        return -final_eval

# This uses MVV-LVA (https://www.chessprogramming.org/MVV-LVA)
# We give it a capture bonus
# We then calculate the score (capture bonus + victim value - attacker value)

def get_move_score(board, move, depth=0):
    CAPTURE_BONUS = 100000

    score = 0

    if board.is_capture(move):
        attacker = board.piece_at(move.from_square)
        attacker_value = piece_values[attacker.piece_type]

        if board.is_en_passant(move):
            victim_value = piece_values[chess.PAWN]
        else:
            victim = board.piece_at(move.to_square)
            victim_value = piece_values[victim.piece_type] if victim else 0

        score = CAPTURE_BONUS + victim_value - attacker_value

    if move.promotion:
        score += piece_values[move.promotion] + 50

    return score

# We then get the moves and sort them by good first (usually captures)

def get_ordered_moves(board, captures_only=False):
    if captures_only:
        moves = [move for move in board.legal_moves if board.is_capture(move)]
    else:
        moves = list(board.legal_moves)

    moves.sort(key=lambda move: get_move_score(board, move), reverse=True)
    return moves

# When we reach the depth 0, that's when quiescene search happens
# We basically keep searching if we missed a good move or not
# https://www.chessprogramming.org/Quiescence_Search

def quiescene_search(board, alpha, beta):
    static_eval = evaluate_board(board)
    best_value = static_eval
    if best_value >= beta:
        return best_value
    if best_value > alpha:
        alpha = best_value

    
    for move in get_ordered_moves(board, captures_only=True):

        if not board.is_capture(move):
            continue

        board.push(move)
        score = -quiescene_search(board, -beta, -alpha)
        board.pop()
        
        if score >= beta:
            return score
        if score > best_value:
            best_value = score
        if score > alpha:
            alpha = score

    return best_value

# This is the search logic it uses negamax as the search algorithm
# We use alpha-beta pruning to not search if a board position gives opponenet an advantage
# This is also an implementation of fail-hard

def negamax(board, depth, alpha, beta):
    
    global nodes_searched
    nodes_searched += 1 
    MATE_SCORE = 99999999 
    
    if time.time() - search_start >= time_limit:
        raise TimeoutError
    
    if board.is_checkmate():
        return -(MATE_SCORE + depth)
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_repetition():
        return 0
    
    if depth == 0: 
        return quiescene_search(board, alpha, beta)
    
    for move in get_ordered_moves(board):
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score 

    return alpha

# This is the find_best_move which is also the root negamax call as well
# We do the same thing as we did in negamax 

def find_best_move(board, max_depth):
    best_move = None
    best_score = -float('inf')

    alpha = -float("inf")
    beta = float("inf")

    for move in get_ordered_moves(board):
        board.push(move)
        score = -negamax(board, max_depth - 1, -beta, -alpha)
        board.pop()
        
        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)

    return best_move, best_score

    
# Writing logs for debugging purposes

# def log_message(message: str):
#     with open("engine_log.txt", "a") as f:
#         f.write(message + "\n")

# the uci loop which is used by many GUI to communicate with chess engines

def uci_loop():

    banner_logged = False
    
    while True:
        try:
            line = sys.stdin.readline().strip()
            if not line:
                continue

            # log_message(f"GUI -> Engine: {line}")
            
            parts = line.split()
            command = parts[0]
            
            if command == "uci":
                sys.stdout.write("id name Tridentv1\n")
                sys.stdout.write("id author SakuraBlossomTree\n")
                sys.stdout.write("uciok\n")
                sys.stdout.flush()
            
            elif command == "isready":
                sys.stdout.write("readyok\n")
                sys.stdout.flush()

            elif command == "ucinewgame":
                board.reset()

            elif command == "position":
                if "startpos" in parts:
                    board.reset()
                    moves_start_index = parts.index("moves") + 1 if "moves" in parts else -1
                elif "fen" in parts:
                    fen_start_index = parts.index("fen") + 1
                    fen_parts = parts[fen_start_index : fen_start_index + 6]
                    fen = " ".join(fen_parts)
                    board.set_fen(fen)
                    moves_start_index = parts.index("moves") + 1 if "moves" in parts else -1
                else:
                    moves_start_index = -1

                if moves_start_index != -1:
                    for move_str in parts[moves_start_index:]:
                        try:
                            board.push_uci(move_str)
                        except ValueError:
                            # log_message(f"ERROR: Invalid move {move_str} for position {board.fen()}")
                            pass

            elif command == "go":                
                global nodes_searched, time_limit, search_start
                nodes_searched = 0
                start_time = time.time()
                # MAX_DEPTH = 4 

                wtime = btime = None
                winc = binc = 0 

                if "wtime" in parts:
                    wtime = int(parts[parts.index("wtime") + 1])
                if "btime" in parts:
                    btime = int(parts[parts.index("btime") + 1])
                if "winc" in parts:
                    winc = int(parts[parts.index("winc") + 1])
                if "binc" in parts:
                    binc = int(parts[parts.index("binc") + 1])

                if board.turn == chess.WHITE:
                    base = wtime
                    inc = winc
                else:
                    base = btime
                    inc = binc

                time_limit = base / 20 + inc / 2
                time_limit /= 1000
                search_start = time.time()

                if not banner_logged:
                    # log_message("--- Trident Engine v1.2 with depth 4 (endgame fix and quiescene optimization) ---")
                    banner_logged = True

                # best_move, best_score = find_best_move(board, max_depth=MAX_DEPTH)

                depth = 1
                best_move = None
                best_score = 0
                while True:
                    try:
                        move, score = find_best_move(board, depth)
                        if move:
                            best_move = move
                            best_score = score
                        elapsed = time.time() - search_start
                        sys.stdout.write(
                            f"info depth {depth} score cp {int(score)} nodes {nodes_searched} time {int(elapsed*1000)}\n"
                        )
                        sys.stdout.flush()
                        depth += 1
                        if time.time() - search_start >= time_limit:
                            break
                    except TimeoutError:
                        break

                end_time = time.time()
                search_duration = end_time - start_time
                nps = int(nodes_searched / search_duration) if search_duration > 0 else 0

                # log_message(f"Search complete: {nodes_searched} nodes in {search_duration:.2f}s ({nps} NPS)")
                # log_message(f"info depth {MAX_DEPTH} score cp {int(best_score)}")

                sys.stdout.write(f"info depth {depth - 1} score cp {int(best_score)}\n")
                sys.stdout.write(f"bestmove {best_move.uci()}\n")
                sys.stdout.flush()

            elif command == "quit":
                # log_message("Engine told to quit.")
                break
                
        except Exception as e:
            # log_message(f"ERROR: An exception occurred: {e}")
            pass

if __name__ == "__main__":
    uci_loop()