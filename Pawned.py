# Class for Pieces of the board
#   label - String, name of the pieces, stores colour and number, eg. "W3"
#   location - (row,col), where the piece is located on the board
class Piece():
    def __init__(self, label, row, col):
        self.label = label
        self.row = row
        self.col = col

# Move Class, represents a move command
#   label - String, which piece to move
#   location - (row,col), where on the board to move
class Move():
    def __init__(self, label, row = None, col = None):
        self.label = label
        self.row = row
        self.col = col

# Board Class, represents the state of the game, using a 2D array
#   row/col - integers, dimensions of the board
#   white[] - list of the white pieces
#   black[] - list of the black pieces
class Board():
    def __init__(self, row = 6, col = 5):
        self.board = [["  " for x in range(col)] for x in range(row)]
        self.row = row
        self.col = col
        self.white = []
        self.black = []
        for x in range(col):
            self.board[0][x] = "B"+ str(x)
            self.board[row-1][x] = "W"+ str(x)
            self.white.append(Piece("W"+ str(x),row-1,x))
            self.black.append(Piece("B"+ str(x),0,x))

    # Method to print the current state of the board
    def print_board(self):
        toString = "\n  0  1  2  3  4"
        toString += "\n  -- -- -- -- --"
        for x in range(self.row):
            toString += "\n" + str(x) + "|" 
            for y in range(self.col):
                toString += (self.board[x][y] + "|")
            toString += "\n  -- -- -- -- --"
        print toString + "\n"

    # Method which applies a given move command to the current board, assumes move is valid
    def apply_move(self, move):
        white_moved = False
        black_moved = False
        for piece in self.white:
            if piece.label == move.label:
                self.board[piece.row][piece.col] = "  "
                piece.row = move.row
                piece.col = move.col
                self.board[move.row][move.col] = move.label
                white_moved = True
                break
        for piece in self.black:
            if piece.col == move.col and piece.row == move.row and white_moved:
                self.black.remove(piece)
            elif piece.label == move.label:
                self.board[piece.row][piece.col] = "  "
                piece.row = move.row
                piece.col = move.col
                self.board[move.row][move.col] = move.label
                black_moved = True
                break
        if black_moved and not white_moved:
            for piece in self.white:
                if piece.col == move.col and piece.row == move.row:
                    self.white.remove(piece)

# Function to return a new board that is a copy of a given board
def copy_board(board):
    newBoard = Board()
    newBoard.board = [["  " for x in range(board.col)] for x in range(board.row)]
    newBoard.row = board.row
    newBoard.col = board.col
    newBoard.white = []
    newBoard.black = []
    for piece in board.white:
        newBoard.white.append(Piece(piece.label, piece.row, piece.col))
        newBoard.board[piece.row][piece.col] = piece.label
    for piece in board.black:
        newBoard.black.append(Piece(piece.label, piece.row, piece.col))
        newBoard.board[piece.row][piece.col] = piece.label
    return newBoard

# Successor function, generates possible moves for a player
#   board - The board state
#   Wturn - Bool, whose turn it is
def Successor(board, Wturn):
    successor_moves = []
    if Wturn:
        for piece in board.white:
            if board.board[piece.row-1][piece.col] == "  ":
                successor_moves.append(Move(piece.label, piece.row-1, piece.col))
            if piece.col > 0:
                if board.board[piece.row-1][piece.col-1][0] == "B":
                    successor_moves.append(Move(piece.label, piece.row-1, piece.col-1))
            if piece.col < board.col-1:
                if board.board[piece.row-1][piece.col+1][0] == "B":
                    successor_moves.append(Move(piece.label, piece.row-1, piece.col+1))
    else:
        for piece in board.black:
            if board.board[piece.row+1][piece.col] == "  ":
                successor_moves.append(Move(piece.label, piece.row+1, piece.col))
            if 0 < piece.col:
                if board.board[piece.row+1][piece.col-1][0] == "W":
                    successor_moves.append(Move(piece.label, piece.row+1, piece.col-1))
            if piece.col < board.col-1:
                if board.board[piece.row+1][piece.col+1][0] == "W":
                    successor_moves.append(Move(piece.label, piece.row+1, piece.col+1))
    return successor_moves

# Function to determine if a given board is in a terminal state, either player winning, or a stalemate
def terminal_board(board):
    # If white is out of pieces
    if len(board.white) == 0:
        return True
    # If black is out of pieces
    if len(board.black) == 0:
        return True
    # If a white piece reaches the top row
    for piece in board.white:
        if piece.row == 0:
            return True
    # If a black piece reaches the bottom row
    for piece in board.black:
        if piece.row == board.col:
            return True
    # If both players have no remaining moves
    white_moves = Successor(board, True)
    black_moves = Successor(board, False)
    if len(white_moves) == 0 and len(black_moves) == 0:
        return True
    # Else the board is not in a terminal state
    return False

# Determine value for a given terminal board
def terminal_val(board):
    # If white is out of pieces
    if len(board.white) == 0:
        return -100000
    # If black is out of pieces
    if len(board.black) == 0:
        return 100000
    # If a white piece reaches the top row
    for piece in board.white:
        if piece.row == 0:
            return 100000
    # If a black piece reaches the bottom row
    for piece in board.black:
        if piece.row == board.col:
            return -100000
    # If both players have no remaining moves
    white_moves = Successor(board, True)
    black_moves = Successor(board, False)
    if len(white_moves) == 0 and len(black_moves) == 0:
        return 0

# Helper function to determine if 2 moves are equal
def moves_equal(move1, move2):
    if move1.label == move2.label:
        if move1.col == move2.col:
            if move1.row == move2.row:
                return True
    return False

# Function MiniMax to determine best possible move
def minimax(state, maxing, depth = -1, h = None):
    if terminal_board(state):
        return (terminal_val(state), Move(""))
    if depth == 0:
        return (h(state), Move(""))
    if maxing:
        successor_moves = Successor(state, maxing)
        bestMax = (-1000, Move(""))
        if len(successor_moves) > 0:
            bestMax = (-1000, Move(successor_moves[0].label, successor_moves[0].row, successor_moves[0].col))
            for suc_move in successor_moves:
                newBoard = copy_board(state)
                newBoard.apply_move(suc_move)
                val = minimax(newBoard, False, depth-1, h)
                if val[0] > bestMax[0]:
                    bestMax = (val[0], suc_move)
        return bestMax
    else:
        successor_moves = Successor(state, maxing)
        bestMin = (1000, Move(""))
        if len(successor_moves) > 0:
            bestMin = (1000, Move(successor_moves[0].label, successor_moves[0].row, successor_moves[0].col))
            for suc_move in successor_moves:
                newBoard = copy_board(state)
                newBoard.apply_move(suc_move)
                val = minimax(newBoard, True, depth-1, h)
                if val[0] < bestMin[0]:
                    bestMin = (val[0], suc_move)
        return bestMin

# Function MiniMax to determine best possible move, with alph-beta pruning
def minimax_ab(state, maxing, depth, h, alpha, beta):
    if terminal_board(state):
        return (terminal_val(state), Move(""))
    if depth == 0:
        return (h(state), Move(""))
    if maxing:
        successor_moves = Successor(state, maxing)
        bestMax = (-1000, Move(""))
        if len(successor_moves) > 0:
            bestMax = (-1000, Move(successor_moves[0].label, successor_moves[0].row, successor_moves[0].col))
            for suc_move in successor_moves:
                newBoard = copy_board(state)
                newBoard.apply_move(suc_move)
                val = minimax_ab(newBoard, False, depth-1, h, alpha, beta)
                if val[0] > bestMax[0]:
                    bestMax = (val[0], suc_move)
                alpha = max(alpha, val[0])
                if beta <= alpha:
                    break
        return bestMax
    else:
        successor_moves = Successor(state, maxing)
        bestMin = (1000, Move(""))
        if len(successor_moves) > 0:
            bestMin = (1000, Move(successor_moves[0].label, successor_moves[0].row, successor_moves[0].col))
            for suc_move in successor_moves:
                newBoard = copy_board(state)
                newBoard.apply_move(suc_move)
                val = minimax_ab(newBoard, True, depth-1, h, alpha, beta)
                if val[0] < bestMin[0]:
                    bestMin = (val[0], suc_move)
                beta = min(beta, val[0])
                if beta <= alpha:
                    break
        return bestMin
   
# Estimated value for who is winning the current game
def eval_board(board): ## higher better for white, lower better for black
    h_cost = 0
    h_cost += (len(board.white) - len(board.black))
    return h_cost

# Gets input from player and makes the move if it's valid
def player_turn(board, white_turn):
    play_game = True
    inputs = raw_input("Enter a move, format \"piece row col\" Type 'help' for help: ").split()
    if len(inputs) == 1:
        if inputs[0] == 'q':
            play_game = False
        elif inputs[0] == 'p':
            board.print_board()
        elif inputs[0] == 'm':
            successor_moves = Successor(board, white_turn)
            print ""
            for move in successor_moves:
                print str(move.label) + " " + str(move.row) + " " + str(move.col)
            print ""
        elif inputs[0] == 'help':
            print "\nhelp - Displays Help"
            print "   q - Quit Program"
            print "   m - All possible moves for the player"
            print "   p - Prints the current board\n"
    elif len(inputs) == 3:
        successor_moves = Successor(board, white_turn)
        move = Move(inputs[0], int(inputs[1]), int(inputs[2]))
        for suc_move in successor_moves:
            if moves_equal(suc_move, move):
                board.apply_move(move)
                board.print_board()
                white_turn = not white_turn
                if terminal_board(board):
                    play_game = False
                if len(Successor(board, white_turn)) == 0:
                    print "No possible moves, skipped Turn"
                    white_turn = not white_turn
                break
    return (white_turn, play_game)

def comp_turn(board, white_turn, depth_limit):
    # move = minimax(board, white_turn, depth_limit, eval_board)
    move = minimax_ab(board, white_turn, depth_limit, eval_board, -100000, 100000)
    print move[1].label + " " + str(move[1].row) + " " + str(move[1].col)
    board.apply_move(move[1])
    board.print_board()

# Start of Main
board = Board()
board.print_board()

white_turn = True
play_game = True

p1_cpu = True
p2_cpu = True

depth_limit = 12

while play_game == True:
    if white_turn:
        print "White's Turn"
    else:
        print "Black's Turn"
    if white_turn:
        if p1_cpu:
            comp_turn(board, white_turn, depth_limit)
            white_turn = False
        else:
            turn = player_turn(board, white_turn)
            white_turn = turn[0]
            play_game = turn[1]
        if terminal_board(board):
            play_game = False
    else:
        if p2_cpu:
            comp_turn(board, white_turn, depth_limit)
            white_turn = True
        else:
            turn = player_turn(board, white_turn)
            white_turn = turn[0]
            play_game = turn[1]
        if terminal_board(board):
            play_game = False
quit = input("Game Over")