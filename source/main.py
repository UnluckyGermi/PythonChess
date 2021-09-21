from board import Board
from move import Move
import pygame as game
import sys

from pygame.constants import FULLSCREEN



class Interface:


    def getPos(self, coords):
        return int(coords[1]/self.squaresize), int(coords[0]/self.squaresize)


    def __init__(self, b):

        self.SPRITE_ORDER = ["K", "Q", "B", "N", "R", "P", "k", "q", "b", "n", "r", "p"]
        self.ICON = game.transform.smoothscale(game.image.load("assets/icon.ico"), (32, 32))
        game.init()
        game.display.set_icon(self.ICON)
        game.display.set_caption("Ajedrez")
        
        self.selectedSquare = None
        self.selectedpiece = None
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
                        if board.pieces[pos[0]][pos[1]] != '-':
                            self.selectedpiece = pos
                    elif event.button == 3:
                        if self.selectedSquare == pos : self.selectedSquare = None
                        else: self.selectedSquare = pos
                    
                elif event.type == game.MOUSEBUTTONUP and event.button == 1 and self.selectedpiece != None:
                    pos = self.getPos(game.mouse.get_pos())

                    for move in Move.kingMoves(self.selectedpiece):
                        if move.squareto != pos : continue

                        board.pieces[pos[0]][pos[1]] = board.pieces[self.selectedpiece[0]][self.selectedpiece[1]]
                        board.pieces[self.selectedpiece[0]][self.selectedpiece[1]] = '-'
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
                c = board.pieces[i][j]
                if c != '-':
                    imgpos = pos
                    if self.selectedpiece == (i,j):
                        imgpos = (game.mouse.get_pos()[0] - self.squaresize/2, game.mouse.get_pos()[1] - self.squaresize/2)

                    sprite = game.transform.smoothscale(self.sprites[self.SPRITE_ORDER.index(c)], (self.squaresize, self.squaresize))                    
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

interface = Interface(b)
interface(b)





