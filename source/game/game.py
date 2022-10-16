from pygame.color import Color
from game.board import Board
from game.move import Move
from game.piece import Piece
import pygame as game
import sys
import socket


from pygame.constants import FULLSCREEN


class Game:

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

        board_coords = int(coords[1]/self.squaresize), int(coords[0]/self.squaresize)
        if self.color != 0: board_coords = (7 - board_coords[0], 7 - board_coords[1])

        return board_coords


    def __init__(self, board, color, s):
        self.s = s
        self.board = board
        self.color = color
        self.ICON = game.transform.smoothscale(game.image.load("../assets/icon.ico"), (32, 32))
        game.init()
        game.mixer.init()
        game.display.set_icon(self.ICON)
        game.display.set_caption("Ajedrez")

        self.move_sound = game.mixer.Sound("../assets/sounds/piece_move.wav")
        self.check_sound = game.mixer.Sound("../assets/sounds/piece_check.wav")
        
        self.moves = []
        self.arrow = []
        self.arrowinit = None
        self.selectedpiece = Piece.NONE
        self.sprites = [None] * 12
        self.squaresize = 80
        self.surface = game.display.set_mode((self.squaresize*8, self.squaresize*8), vsync=1)
        self.loadSprites()
        

    
    def __call__(self):

        ### BUCLE PRINCIPAL ###

        while True:
            game.event.pump()

            self.surface.fill((0,0,0))
            self.drawBoard()
            for event in game.event.get():
                if event.type == game.QUIT: sys.exit()
                elif event.type == game.MOUSEBUTTONDOWN:
                    pos = self.getPos(game.mouse.get_pos())

                    if event.button == 1:
                        self.arrow = []
                        piece = self.board.pieces[pos[0]][pos[1]]

                        if piece != Piece.NONE:
                            self.selectedpiece = pos
                            if not ((Piece.isTeam(piece, Piece.WHITE) and self.color == 0) or (Piece.isTeam(piece, Piece.BLACK) and self.color == 1)):
                                continue
                            try:
                                if(Piece.isTeam(self.board.pieces[self.selectedpiece[0]][self.selectedpiece[1]], self.board.turn)):
                                    for move in Move.generateLegalMoves(self.selectedpiece, self.board):
                                        self.moves.append(move)
                            except: continue
                                    

                    elif event.button == 3:
                        self.arrowinit = pos
                    
                elif event.type == game.MOUSEBUTTONUP:
                    pos = self.getPos(game.mouse.get_pos())
                    if event.button == 1 and self.selectedpiece != None:
                        try:

                            if Piece.isTeam(self.board.pieces[self.selectedpiece[0]][self.selectedpiece[1]], self.board.turn):
                                for move in self.moves:
                                    if move.squareto == pos:
                                        self.board.makeMove(move)
                                        self.s.send(move.toString().encode())
                                        
                                        if self.board.inCheck(self.board.turn): game.mixer.Sound.play(self.check_sound)
                                        else: game.mixer.Sound.play(self.move_sound)
                        except: continue
                    elif event.button == 3 and self.arrowinit != None:
                        self.arrow.append((self.arrowinit, pos))

                    self.selectedpiece = None
                    self.moves = []
            
            game.display.flip()
            
    def loadSprites(self):
        for i in range(12):
            self.sprites[i] = game.image.load("../assets/pieces/" + str(i+1) + ".png")

    def drawPieces(self):
        for i in range(8):
            for j in range(8):
                piece = self.board.pieces[i][j]
                if self.color != 0:
                    piece = self.board.pieces[7-i][7-j]
                pos = (self.squaresize*j, self.squaresize*i)
            
                if piece != Piece.NONE:
                    spritepos = Game.SPRITE_FROM_PIECE[piece]
                    imgpos = pos
                    
                    if (self.selectedpiece == (i,j) and self.color == 0) or (self.selectedpiece == (7-i, 7-j) and self.color == 1):
                        imgpos = (game.mouse.get_pos()[0] - self.squaresize/2, game.mouse.get_pos()[1] - self.squaresize/2)

                    sprite = game.transform.smoothscale(self.sprites[spritepos], (self.squaresize, self.squaresize))                    
                    self.surface.blit(sprite, imgpos, area=None)

    
    def drawBoard(self):
        for i in range(8):
            for j in range(8):
                square = i,j

                if self.color != 0: square = (7 - i, 7 - j)

                pos = (self.squaresize*j, self.squaresize*i)
                color = (99, 83, 72)
                
                if (i+j) % 2 == 0:  color = (227, 192, 168)


                rect = game.Rect(pos[0], pos[1], self.squaresize, self.squaresize)
                game.draw.rect(self.surface, color, rect)


                for move in self.moves:
                    if move.squareto == square:
                        s = game.Surface((self.squaresize, self.squaresize))
                        s.set_alpha(70)
                        s.fill((255, 123, 123))
                        self.surface.blit(s, pos)

        

        for arr in self.arrow:
            start = arr[0]
            end = arr[1]

            if(start == end): continue

            startpos = self.squaresize*start[1] + self.squaresize/2, self.squaresize*start[0] + self.squaresize/2
            endpos = self.squaresize*end[1] + self.squaresize/2, self.squaresize*end[0] + self.squaresize/2

            dir = end[0] - start[0], end[1] - start[1]
            oppdir = dir[1], -dir[0]

            
            game.draw.circle(self.surface, (0,0,0), startpos, 5)
            game.draw.line(self.surface, (0,0,0), startpos, endpos, width=10)
            #game.draw.polygon(self.surface, (0,0,0), ((endpos[0] + oppdir[0], endpos[1] + oppdir[1]*100), (endpos[0] - oppdir[0], endpos[1] - oppdir[1]*100), (endpos[0] + dir[0]*100, endpos[1] + dir[1]*100)))
            #game.draw.polygon(self.surface, (0, 0, 0), ((start), (startpos[0] + 10*dir[0], startpos[1] - 10*dir[1]), (endpos), (endpos[0] + 10*dir[0], endpos[1] - 10*dir[1])))
            
        self.drawPieces()

