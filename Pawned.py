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
        print "Black Wins!"
        return True
    # If black is out of pieces
    if len(board.black) == 0:
        print "White Wins!"
        return True
    # If a white piece reaches the top row
    for piece in board.white:
        if piece.row == 0:
            print "White Wins!"
            return True
    # If a black piece reaches the bottom row
    for piece in board.black:
        if piece.row == board.col:
            print "Black Wins!"
            return True
    # If both players have no remaining moves
    white_moves = Successor(board, True)
    black_moves = Successor(board, False)
    if len(white_moves) == 0 and len(black_moves) == 0:
        print "It's a draw!"
        return True
    # Else the board is not in a terminal state
    return False

# Helper function to determine if 2 moves are equal
def moves_equal(move1, move2):
    if move1.label == move2.label:
        if move1.col == move2.col:
            if move1.row == move2.row:
                return True
    return False

# Start of Main
board = Board()
board.print_board()

white_turn = True
play_game = True

while play_game == True:
    if white_turn:
        print "White's Turn"
    else:
        print "Black's Turn"
    inputs = raw_input("Enter a move, format \"piece row col\" Type 'help' for help: ").split()
    if len(inputs) == 1:
        if inputs[0] == 'q':
            break
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
quit = input("Game Over")