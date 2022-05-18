import imp
import pygame
from .constants import BLACK, BLUE, ROWS, RED, SQUARE_SIZE, COLS, WHITE,WIDTH,HEIGHT
from .piece import Piece, Direction
import Packages.game
pygame.init()
main_font = pygame.font.SysFont("comicsans", 18)

class Board:
    def __init__(self):     
        #list contains the items 
        self.board = []
        self.black_left = 8
        self.white_left = 8
        self.create_board()

    def move(self, piece, move_to_row, move_to_col):
        #change the rows and cols in the board object
        self.board[piece.row][piece.col], self.board[move_to_row][move_to_col] = self.board[move_to_row][move_to_col], self.board[piece.row][piece.col]
        #change the rows and cols in the piece objects
        piece.move(move_to_row, move_to_col)

    def get_piece(self, row, col):
        return self.board[row][col]
        
    def move_rocket_instruct(self, piece, target_row, target_row_col):
        if piece.rocketNr < 1:
            return
        target = self.get_piece(target_row,target_row_col)
        if target !=0:
            self.board[target_row][target_row_col] = 0
            piece.rocketNr -= 1
            if piece.color == BLACK:
                self.black_left -= 1
            else:
                self.white_left -= 1 
                   
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(0)
         
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def draw_squares(self, win):
        win_squares = pygame.display.set_mode((WIDTH , HEIGHT + 35))
        win.fill(BLUE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2): 
                pygame.draw.rect(win_squares, WHITE, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.blue_left + (self.white_kings * 0.5 - self.blue_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLUE
        
        #no one won
        return None 
    
    def get_valid_moves(self, piece): 
        # moves = {}
        moves = {}

        left = piece.col - 1
        right = piece.col + 1
        straight = piece.col

        if piece.dir == Direction.Top:
            moves = self._traverse_vertical(piece.row - 1, -1, -1, piece.color, straight)
        if piece.dir == Direction.Bottom:
            moves = self._traverse_vertical(piece.row + 1, ROWS, 1, piece.color, straight)
        if piece.dir == Direction.Right:
            moves = self._traverse_horizontal(piece.col + 1, COLS, 1, piece.color, piece.row)
        if piece.dir == Direction.Left:
            moves = self._traverse_horizontal(piece.col -1, -1, -1, piece.color, piece.row)
        if piece.dir == Direction.BottomLeft:
            moves = self._traverse_diagonal(piece.col -1, -1, piece.row + 1, COLS, -1, 1,  piece.color)
        if piece.dir == Direction.TopRight:
            moves = self._traverse_diagonal(piece.col +1, COLS, piece.row - 1, -1, 1, -1,  piece.color)
        if piece.dir == Direction.BottomRight:
            moves = self._traverse_diagonal(piece.col + 1, COLS, piece.row + 1, COLS, 1, 1,  piece.color)
        if piece.dir == Direction.TopLeft:
            moves = self._traverse_diagonal(piece.col -1, -1, piece.row - 1, -1, -1, -1,  piece.color)

        return moves
        
    def _traverse_vertical(self, start, stop, step, color, straight):
        moves = {}
        for r in range(start, stop, step):
            current = self.board[r][straight]
            moves[(r, straight)] = current
            if self.board[r][straight] != 0:
                print(moves)
                
                break
        return moves

    def _traverse_horizontal(self, start, stop, step, color, row):
        moves = {}
        for r in range(start, stop, step):
            current = self.board[row][r]
            moves[(row, r)] = current
            if self.board[row][r] != 0:
             
                break
        print(moves)
        return moves

    def _traverse_diagonal(self, start_col, stop_col, start_row, stop_row, step_col, step_row, color):
        moves = {}

        i= 0
        while(True):
            y = start_col + i * step_col
            x = start_row + i * step_row
            if y == stop_col:
                break
            if x == stop_row:
                break
            current = self.board[x][y]
            moves[(x, y)] = current
            i += 1
            if self.board[x][y] != 0:
                break
        return moves
