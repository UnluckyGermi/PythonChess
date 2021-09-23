
import plistlib
from piece import Piece
from move import Move

class Board:

    def __init__(self):

        self.turn = Piece.WHITE
        
        self.blackcastleright = [True, True]
        self.whitecastleright = [True, True]

        self.totalmoves = 0
        self.movesbeforedraw = 0

        self.enpassant = None
        self.pieces = [[Piece.NONE]*8 for i in range(8)]

    def fromBoard(board):
        newboard = Board()
        newboard.turn = board.turn
        newboard.blackcastleright = [[board.blackcastleright[0]], [board.blackcastleright[1]]]
        newboard.whitecastleright = [[board.whitecastleright[0]], [board.whitecastleright[1]]]
        newboard.totalmoves = board.totalmoves
        newboard.movesbeforedraw = board.movesbeforedraw
        newboard.enpassant = board.enpassant
        newboard.pieces = []

        for i in range(8):
            subpieces = []
            for j in range(8):
                subpieces.append(board.pieces[i][j])
            newboard.pieces.append(subpieces)
        return newboard
        

    def searchKing(self, team):
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j] == Piece.KING | team:
                    return (i,j)

    def inCheck(self, team):
        opponent = Piece.WHITE
        kingsquare = self.searchKing(team)

        if team == Piece.WHITE: opponent = Piece.BLACK

        for move in Move.allMovesForTeam(opponent, self):
            if move.squareto == kingsquare:
                return True
        
        return False


    def newBoardAfterMove(self, move):
        newboard = Board.fromBoard(self)
        newboard.makeMove(move)

        return newboard

    def fromFen(fen):
        board = Board()
        phase = 0
        pos = (0,0)

        for c in str(fen):
            team = 1

            if c == ' ':
                phase += 1
            elif phase == 1:
                board.turn = Piece.WHITE
                if c == 'b': board.turn = Piece.BLACK
            elif phase == 2:

                if c == '-':
                    board.whitecastleright = [False, False]
                    board.blackcastleright = [False, False]
                if c == 'K': board.whitecastleright[0] = True
                elif c == 'Q': board.whitecastleright[1] = True
                elif c == 'k': board.blackcastleright[0] = True
                elif c == 'q': board.blackcastleright[1] = True
            
            elif phase == 3:
                #TODO
                pass
            
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
                board.pieces[pos[0]][pos[1]] = pieceType | pieceTeam
                pos = pos[0], pos[1] + 1
            
            
        board.checkCastles()

        return board

    def nextTurn(self):
        if self.turn == Piece.WHITE: self.turn = Piece.BLACK
        else: self.turn = Piece.WHITE

    def makeMove(self, move):

        self.enpassant = None
        piece = self.pieces[move.squarefrom[0]][move.squarefrom[1]]
        if Piece.isType(piece, Piece.KING):
            if Piece.isTeam(piece, Piece.WHITE): self.whitecastleright = [False, False]
            else: self.blackcastleright = [False, False]


        # Enpassant
        if move.enpassant:
            dir = move.squareto[0] - move.squarefrom[0]
            self.pieces[move.squareto[0]-dir][move.squareto[1]] = Piece.NONE

        
        # Castle.
        if move.castle:
            if Piece.isTeam(piece, Piece.BLACK):
                if move.squareto[1] < move.squarefrom[1]:
                    self.pieces[0][3] = self.pieces[0][0]
                    self.pieces[0][0] = Piece.NONE
                else:
                    self.pieces[0][5] = self.pieces[0][7]
                    self.pieces[0][7] = Piece.NONE
            else:
                if move.squareto[1] < move.squarefrom[1]:
                    self.pieces[7][3] = self.pieces[7][0]
                    self.pieces[7][0] = Piece.NONE
                else:
                    self.pieces[7][5] = self.pieces[7][7]
                    self.pieces[7][7] = Piece.NONE



        if move.pawnmovedtwo != None : self.enpassant = move.pawnmovedtwo
        self.pieces[move.squareto[0]][move.squareto[1]] = self.pieces[move.squarefrom[0]][move.squarefrom[1]]
        self.pieces[move.squarefrom[0]][move.squarefrom[1]] = Piece.NONE

        # Promotion
        if move.promotion != Piece.NONE:
            self.pieces[move.squareto[0]][move.squareto[1]] = move.promotion | Piece.getTeam(piece)

        self.checkCastles()

        
        self.nextTurn()


        
    def checkCastles(self):

        if self.pieces[7][7] != Piece.ROOK | Piece.WHITE: self.whitecastleright[0] = False
        if self.pieces[7][0] != Piece.ROOK | Piece.WHITE: self.whitecastleright[1] = False
        if self.pieces[0][7] != Piece.ROOK | Piece.BLACK: self.blackcastleright[0] = False
        if self.pieces[0][0] != Piece.ROOK | Piece.BLACK: self.blackcastleright[1] = False

                
                
                
            
        

