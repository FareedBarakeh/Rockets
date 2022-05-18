from errno import EILSEQ
from hashlib import new
from pickle import FALSE, TRUE
import re
from turtle import isdown
from numpy import ALLOW_THREADS
import pygame
from .constants import BLUE, HEIGHT, WHITE, BLUE, BLACK, SQUARE_SIZE, RED, ROWS,COLS,WIDTH
from Packages.board import Board
from .piece import Direction, Piece
pygame.init()
main_font = pygame.font.SysFont("comicsans", 28)

class Game:

    def __init__(self, win):
        self._init()
        self.win = win
        self.black_on_board = 8
        self.white_on_board = 8
        self.black_alive = 8
        self.white_alive = 8
        self.rotated = False
        self.new_piece = False
        self.click_black = 0
        self.click_white = 0

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        black_alive_label = main_font.render(f"Black Piece In Airport: {self.black_on_board}", 1 , (255,215,0))
        white_alive_label = main_font.render(f"White Piece In Airport: {self.white_on_board}", 1 , (255,215,0))

        if self.turn == BLACK:
            player_label = main_font.render(f"BLACK EAGLE", 1 , (255,215,0))
        else:
            player_label = main_font.render(f"WHITE SWAN", 1 , (255,215,0))

        self.win.blit(black_alive_label , (10, HEIGHT + 5))
        self.win.blit(white_alive_label, (WIDTH - white_alive_label.get_width() - 10, HEIGHT + 5))
        self.win.blit(player_label , (WIDTH - white_alive_label.get_width()- 225, HEIGHT + 5))
        pygame.display.update()
   
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.player = "BLACK BEGINS"

    def winner(self):
        return self.board.winner()
        
    def reset(self):
        self._init()

    def select(self, row, col, button):
        print("white", self.click_white)
        print(self.new_piece)

        #if we already selected something
        if self.selected and button == 1:
            #move returns boolean
            result = self._move(row, col)
            return
            #if our selection is not valid
            #if not result:
                #get rid of the current selection

                #select something new
                #call the method again
                #self.select(row, col, button)
        piece = self.board.get_piece(row, col)
        #if we are not selecting empty piece

        if button == 1 and piece == 0 and self.new_piece == False:
            if self.black_on_board > 0 and self.turn == BLACK:
                self.board.board[row][col] = Piece(row, col, self.turn, Direction.Top)
                self.new_piece = True
                self.black_on_board -=1
                self.click_black +=1
                return
            elif self.white_on_board > 0 and self.turn == WHITE:
                self.board.board[row][col] = Piece(row, col, self.turn, Direction.Bottom)
                self.new_piece = True
                self.white_on_board -=1
                self.click_white +=1
                return

        if button == 2 and piece != 0:
            if piece.rocketNr <2:
                piece.rocketNr +=1
                self.change_turn()
            return

        if button == 3 and piece !=0:
            self.move_rocket(row, col)
            return



        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)

            if self.new_piece or self.rotated :             
                self.valid_moves = self.valid_moves ={}
            print(self.valid_moves)

            # if self.turn == BLACK and self.new_piece == True:
            #     self.click_black +=1
            #     if self.click_black > 2:
            #         self.new_piece = False
            #         self.selected = None
            #         self.set_round_black()
            #     return 

            # if self.turn == WHITE and self.new_piece == True:
            #     self.click_white +=1
            #     if self.click_white > 2:
            #         self.new_piece = False
            #         self.selected = None
            #         self.set_round_white()
            #     return 

        return 

    def _move(self, row, col):
        if self.rotated:
            return

        piece = self.board.get_piece(row, col)
        #if we selected a place to move piece to which is 0 (empty space) and it's in the valid moves
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            #move piece to the row and col passed in function parameters
            self.board.move(self.selected, row, col)
            self.change_turn()


        elif self.selected and piece != 0 and piece.color != self.turn and (row, col) in self.valid_moves:
            self.board.board[row][col] = 0
            self.board.move(self.selected, row, col)
            self.change_turn()
 
    def move_rocket(self, row, col):
        if self.selected and (row,col) in self.valid_moves:
            self.board.move_rocket_instruct(self.selected, row, col)
        piece = self.selected

        if piece.color == BLACK:
            self.white_alive -=1
            self.change_turn()
        else:
            self.black_alive -=1

            self.change_turn()

    def set_round_black(self):
        self.click_black = 0 
        self.change_turn()

    def set_round_white(self):
        self.click_black = 0 
        self.change_turn()

    def change_dir(self, amount):
        #if self.allow_dir_change:
        #aktar mn mra
        
        #nonetype
        #self.selected == None
        if not self.selected:
            raise RuntimeError("SELECT A PIECE BITCH")

        if self.turn == self.selected.color:
            self.selected.moveDir(amount)
            self.rotated = True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, RED, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.rotated = False
        self.selected = None
        
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
            self.new_piece = False
            self.click_black = 0
            
        else:
            self.turn = BLACK
            self.valid_moves = {}
            self.new_piece = False
            self.click_white = 0

    def get_board(self):
        return self.board 

    def ai_move(self, board):
        self.board = board 
        self.change_turn()




            
