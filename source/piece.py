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




    def __init__(self, type, team):
        self.type = type
        self.team = team
        