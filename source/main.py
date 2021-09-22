from board import Board
from move import Move
from piece import Piece
import pygame as game
import sys


from pygame.constants import FULLSCREEN



class Interface:

    SPRITE_FROM_PIECE = {
                        Piece.KING | Piece.WHITE : 0,
                        Piece.QUEEN | Piece.WHITE : 1,
                        Piece.BISHOP | Piece.WHITE : 2,
                        Piece.KNIGHT | Piece.WHITE : 3,
                        Piece.ROOK | Piece.WHITE : 4,
                        Piece.PAWN | Piece.WHITE : 5,
                        Piece.KING | Piece.BLACK : 6,
                        Piece.QUEEN | Piece.BLACK : 7,
                        Piece.BISHOP | Piece.BLACK : 8,
                        Piece.KNIGHT | Piece.BLACK : 9,
                        Piece.ROOK | Piece.BLACK : 10,
                        Piece.PAWN | Piece.BLACK : 11}
                        

    def getPos(self, coords):
        return int(coords[1]/self.squaresize), int(coords[0]/self.squaresize)


    def __init__(self, b):

        self.ICON = game.transform.smoothscale(game.image.load("assets/icon.ico"), (32, 32))
        game.init()
        game.display.set_icon(self.ICON)
        game.display.set_caption("Ajedrez")
        
        self.selectedSquare = None
        self.selectedpiece = Piece.NONE
        self.sprites = [None] * 12
        self.squaresize = 100
        self.surface = game.display.set_mode((self.squaresize*8, self.squaresize*8), vsync=1)
        self.loadSprites()
        

    
    def __call__(self, board):

        ### BUCLE PRINCIPAL ###

        while True:
            self.surface.fill((0,0,0))
            self.drawBoard(board)
            for event in game.event.get():
                if event.type == game.QUIT: sys.exit()
                elif event.type == game.MOUSEBUTTONDOWN:
                    pos = self.getPos(game.mouse.get_pos())
                    if event.button == 1:
                        if board.pieces[pos[0]][pos[1]] != Piece.NONE:
                            self.selectedpiece = pos
                    elif event.button == 3:
                        if self.selectedSquare == pos : self.selectedSquare = None
                        else: self.selectedSquare = pos
                    
                elif event.type == game.MOUSEBUTTONUP and event.button == 1 and self.selectedpiece != None:
                    pos = self.getPos(game.mouse.get_pos())

                    for move in Move.kingMoves(self.selectedpiece):
                        if move.squareto != pos : continue

                        board.pieces[pos[0]][pos[1]] = board.pieces[self.selectedpiece[0]][self.selectedpiece[1]]
                        board.pieces[self.selectedpiece[0]][self.selectedpiece[1]] = Piece.NONE
                        break


                    
                    self.selectedpiece = None


                    
            

            game.display.flip()
            
    def loadSprites(self):
        for i in range(12):
            self.sprites[i] = game.image.load("assets/pieces/" + str(i+1) + ".png")

    def drawPieces(self, board):
        for i in range(8):
            for j in range(8):
                pos = (self.squaresize*j, self.squaresize*i)
                piece = board.pieces[i][j]
                if piece != Piece.NONE:
                    spritepos = Interface.SPRITE_FROM_PIECE[piece]
                    imgpos = pos
                    if self.selectedpiece == (i,j):
                        imgpos = (game.mouse.get_pos()[0] - self.squaresize/2, game.mouse.get_pos()[1] - self.squaresize/2)

                    sprite = game.transform.smoothscale(self.sprites[spritepos], (self.squaresize, self.squaresize))                    
                    self.surface.blit(sprite, imgpos, area=None)

    
    def drawBoard(self, board):
        for i in range(8):
            for j in range(8):
                square = i,j
                pos = (self.squaresize*j, self.squaresize*i)
                color = (99, 83, 72)
                
                if (i+j) % 2 == 0:  color = (227, 192, 168)


                rect = game.Rect(pos[0], pos[1], self.squaresize, self.squaresize)
                game.draw.rect(self.surface, color, rect)


                if (i,j) == self.selectedSquare : game.draw.rect(self.surface, game.Color(255,255,255,a=10), rect)

        self.drawPieces(board)

                

b = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

for i in range(8):
    for j in range(8):
        print(b.pieces)
    print()
interface = Interface(b)
interface(b)





