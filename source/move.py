from piece import Piece

class Move:
    
    # 0 - Invalid move
    # 1 - Blocked by friendly
    # 2 - Blocked by enemy
    # 3 - Valid move
    def checkValidMove(move, board):
        if move.squareto[0] > 7 or move.squareto[1] > 7 or move.squareto[0] < 0 or move.squareto[1] < 0: return 0
        piecefrom = board.pieces[move.squarefrom[0]][move.squarefrom[1]]
        pieceto = board.pieces[move.squareto[0]][move.squareto[1]]

        if pieceto != Piece.NONE:
            if Piece.isTeam(piecefrom, Piece.getTeam(pieceto)): return 1
            return 2

        return 3
        
    def slidingMove(squarefrom, dir, board):
        moves = []

        origin = squarefrom

        while True:
            to = squarefrom[0] + dir[0], squarefrom[1] + dir[1]
            move = Move(origin, to)

            validate = Move.checkValidMove(move, board)

            # Either invalid or blocked by friendly. In both cases the piece can't move there.
            if validate == 0 or validate == 1: break
        
            moves.append(move)

            # Blocked by enemy piece. Piece can move there to capture it but cannot go through.
            if validate == 2: break
            squarefrom = to

        return moves


    def bishopMoves(squarefrom, board):
        moves = []
        for dir1 in [-1, 1]:
            for dir2 in [-1, 1]:
                moves += Move.slidingMove(squarefrom, (dir1, dir2), board)
        return moves

    def rookMoves(squarefrom, board):
        moves = []
        for dir1 in [-1, 0, 1]:
            for dir2 in [-1, 0, 1]:
                if abs(dir1) == abs(dir2): continue
                moves += Move.slidingMove(squarefrom, (dir1, dir2), board)
        return moves

    def knightMoves(squarefrom, board):
        moves = []

        for i in [-2, -1, 1, 2]:
            for j in [-2, -1, 1, 2]:
                if abs(i) == abs(j) : continue

                to = squarefrom[0] + i, squarefrom[1] + j
                move = Move(squarefrom, to)
                if Move.checkValidMove(move, board) > 1: moves.append(move)

        return moves

    def kingMoves(squarefrom, board):
        moves = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0: continue

                to = squarefrom[0] + i, squarefrom[1] + j
                move = Move(squarefrom, to)
                if Move.checkValidMove(move, board) > 1: moves.append(move)

        team = Piece.getTeam(board.pieces[squarefrom[0]][squarefrom[1]])
        
        # White castle.
        if team == Piece.WHITE:
            # Short castle
            if board.whitecastleright[0] and squarefrom[1] + 2 < 8:
                if board.pieces[squarefrom[0]][squarefrom[1]+1] == Piece.NONE and board.pieces[squarefrom[0]][squarefrom[1]+2] == Piece.NONE:
                    to = squarefrom[0], squarefrom[1] + 2
                    move = Move(squarefrom, to)
                    move.castle = True
                    moves.append(move)
            # Long castle
            if board.whitecastleright[1] and squarefrom[1] - 2 > 0:
                if board.pieces[squarefrom[0]][squarefrom[1]-1] == Piece.NONE and board.pieces[squarefrom[0]][squarefrom[1]-2] == Piece.NONE:
                    to = squarefrom[0], squarefrom[1] - 2
                    move = Move(squarefrom, to)
                    move.castle = True
                    moves.append(move)
        else:
            # Short castle
            if board.blackcastleright[0] and squarefrom[1] + 2 < 8:
                if board.pieces[squarefrom[0]][squarefrom[1]+1] == Piece.NONE and board.pieces[squarefrom[0]][squarefrom[1]+2] == Piece.NONE:
                    to = squarefrom[0], squarefrom[1] + 2
                    move = Move(squarefrom, to)
                    move.castle = True
                    moves.append(move)
            # Long castle
            if board.blackcastleright[1] and squarefrom[1] - 2 > 0:
                if board.pieces[squarefrom[0]][squarefrom[1]-1] == Piece.NONE and board.pieces[squarefrom[0]][squarefrom[1]-2] == Piece.NONE:
                    to = squarefrom[0], squarefrom[1] - 2
                    move = Move(squarefrom, to)
                    move.castle = True
                    moves.append(move)

        return moves

    def queenMoves(squarefrom, board):
        moves = []

        for dir1 in [-1, 0, 1]:
            for dir2 in [-1, 0, 1]:
                if dir1 == 0 and dir2 == 0: continue
                
                moves += Move.slidingMove(squarefrom, (dir1, dir2), board)

        return moves

    def pawnMoves(squarefrom, board):
        moves = []
        piece = board.pieces[squarefrom[0]][squarefrom[1]]

        dir = 1
        if Piece.isTeam(piece, Piece.WHITE): dir = -1

        # Forward move.
        to = squarefrom[0] + dir, squarefrom[1]
        if to[0] < 8 and to[0] >= 0 and to[1] < 8 and to[1] >= 0:
            pieceto = board.pieces[to[0]][to[1]]
            if pieceto == Piece.NONE: moves.append(Move(squarefrom, to))
        
        #Forward move 2.
        if dir == 1 and squarefrom[0] == 1 or dir == -1 and squarefrom[0] == 6:
            to = squarefrom[0] + dir*2, squarefrom[1]
            if to[0] < 8 and to[0] >= 0 and to[1] < 8 and to[1] >= 0:
                pieceto = board.pieces[to[0]][to[1]]
                piecebefore = board.pieces[to[0]-dir][to[1]]
                if pieceto == Piece.NONE and piecebefore == Piece.NONE:
                    move = Move(squarefrom, to)
                    move.pawnmovedtwo = to[0]-dir, to[1]
                    moves.append(move)
                    


        # Capture moves.
        for i in [-1, 1]:
            cap = squarefrom[0] + dir, squarefrom[1] + i
            if cap[0] < 8 and cap[0] >= 0 and cap[1] < 8 and cap[1] >= 0:
                piececap2 = board.pieces[cap[0]][cap[1]]
                if piececap2 != Piece.NONE and not Piece.isTeam(piececap2, Piece.getTeam(piece)): moves.append(Move(squarefrom, cap))
                elif board.enpassant != None and board.enpassant == cap:
                    move = Move(squarefrom, cap)
                    move.enpassant = True
                    moves.append(move)

        # Promotion
        for move in moves:
            if move.squareto[0] == 0 and dir == -1:
                move.promotion = Piece.QUEEN | Piece.WHITE
                moven = Move(move.squarefrom, move.squareto)
                moven.promotion = Piece.KNIGHT | Piece.WHITE
                moveb = Move(move.squarefrom, move.squareto)
                moveb.promotion = Piece.BISHOP | Piece.WHITE
                mover = Move(move.squarefrom, move.squareto)
                mover.promotion = Piece.ROOK | Piece.WHITE

            elif move.squareto[0] == 7 and dir == 1:
                move.promotion = Piece.QUEEN | Piece.BLACK
                moven = Move(move.squarefrom, move.squareto)
                moven.promotion = Piece.KNIGHT | Piece.BLACK
                moveb = Move(move.squarefrom, move.squareto)
                moveb.promotion = Piece.BISHOP | Piece.BLACK
                mover = Move(move.squarefrom, move.squareto)
                mover.promotion = Piece.ROOK | Piece.BLACK
        

        return moves

    def generateMoves(squarefrom, board):

        piece = board.pieces[squarefrom[0]][squarefrom[1]]

        if Piece.isType(piece, Piece.KING): return Move.kingMoves(squarefrom, board)
        elif Piece.isType(piece, Piece.KNIGHT): return Move.knightMoves(squarefrom, board)
        elif Piece.isType(piece, Piece.BISHOP): return Move.bishopMoves(squarefrom, board)
        elif Piece.isType(piece, Piece.ROOK): return Move.rookMoves(squarefrom, board)
        elif Piece.isType(piece, Piece.QUEEN): return Move.queenMoves(squarefrom, board)
        elif Piece.isType(piece, Piece.PAWN): return Move.pawnMoves(squarefrom, board)
    
    def generateLegalMoves(squarefrom, board):
        moves = []
        for move in Move.generateMoves(squarefrom, board):
            if move.isLegal(board): moves.append(move)

        return moves


    def isLegal(self, board):
        piece = board.pieces[self.squarefrom[0]][self.squarefrom[1]]
        team = Piece.getTeam(piece)
        newboard = board.newBoardAfterMove(self)

        if self.castle:

            if board.inCheck(team): return False
            move = Move(self.squarefrom, (self.squareto[0], int((self.squareto[1] + self.squarefrom[1]) / 2)))
            newboard1 = board.newBoardAfterMove(move)
            if newboard1.inCheck(team):
                return False

        if newboard.inCheck(team):
            return False

        return True
        
    def allMovesForTeam(team, board):
        moves = []
        for i in range(8):
            for j in range(8):
                piece = board.pieces[i][j]
                if piece != Piece.NONE and Piece.isTeam(piece, team): moves += Move.generateMoves((i,j), board)

        return moves

    def allLegalMovesForTeam(team, board):
        moves = []

        for move in Move.allMovesForTeam(team, board):
            if move.isLegal(board): moves.append(move)

        return moves

    def squareName(square):
        squarefile = square[1]
        squarerank = square[0]

        rank = str(8 - squarerank)
        file = str(chr(ord('a') + squarefile))

        return file + rank

    def toString(self):
        return Move.squareName(self.squarefrom) + Move.squareName(self.squareto)
        

    def __init__(self, squarefrom, squareto):
        self.squarefrom = squarefrom
        self.squareto = squareto
        self.castle = False
        self.pawnmovedtwo = None
        self.enpassant = False
        self.promotion = Piece.NONE

    
    