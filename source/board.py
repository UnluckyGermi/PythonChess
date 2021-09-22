
import plistlib
from piece import Piece


class Board:

    def __init__(self, fen):
        
        self.blackcastleright = [True, True]
        self.whitecastleright = [True, True]

        self.totalmoves = 0
        self.movesbeforedraw = 0

        self.enpassant = [-1, -1]
        self.pieces = [[Piece.NONE]*8 for i in range(8)]

        self.inputFen(fen)


    def inputFen(self, fen):

        phase = 0
        pos = (0,0)

        for c in str(fen):
            team = 1

            if c == ' ':
                phase += 1
            elif phase == 1:
                self.turn = 0
                if c == 'b': self.turn = 1
            elif phase == 2:

                if c == 'K': self.whitecastleright[0] = True
                elif c == 'Q': self.whitecastleright[1] = True
                elif c == 'k': self.blackcastleright[0] = True
                elif c == 'q': self.blackcastleright[1] = True
            
            elif phase == 3:
                if c.isnumeric():
                    self.enpassant[0] = 8-c
                else:
                    self.enpassant[1] = ord(c) - ord('a')
            
            elif phase == 4:
                #TODO
                pass

            elif c.isnumeric():
                pos = pos[0], pos[1] + int(c)
            elif c == '/':
                pos = pos[0] + 1, 0
            
            else:
                
                pieceTeam = Piece.BLACK
                if c.isupper() : pieceTeam = Piece.WHITE

                pieceType = Piece.pieceTypeFromChar[c.lower()]
                self.pieces[pos[0]][pos[1]] = pieceType | pieceTeam
                pos = pos[0], pos[1] + 1





                
                
                
            
        

