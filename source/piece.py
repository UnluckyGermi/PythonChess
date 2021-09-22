from enum import Enum

class Piece:
    
    NONE = 0
    KING = 1
    PAWN = 2
    KNIGHT = 3
    BISHOP = 4
    ROOK = 5
    QUEEN = 6

    WHITE = 8
    BLACK = 16

    pieceTypeFromChar = {'k' : KING, 'q': QUEEN, 'b': BISHOP, 'n': KNIGHT, 'r': ROOK, 'p': PAWN}


    def isTeam(piece, team):
        return piece & team > 7
        

    def isType(piece, type):
        return piece & type >= 7

