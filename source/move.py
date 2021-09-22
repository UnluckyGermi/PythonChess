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
                if abs(dir1) == abs(dir2): break
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

        # Capture move 1.
        cap1 = squarefrom[0] + dir, squarefrom[1] + 1
        if cap1[0] < 8 and cap1[0] >= 0 and cap1[1] < 8 and cap1[1] >= 0:
            piececap1 = board.pieces[cap1[0]][cap1[1]]
            if piececap1 != Piece.NONE and not Piece.isTeam(piececap1, Piece.getTeam(piece)): moves.append(Move(squarefrom, cap1))

        # Capture move 2.
        cap2 = squarefrom[0] + dir, squarefrom[1] - 1
        if cap2[0] < 8 and cap2[0] >= 0 and cap2[1] < 8 and cap2[1] >= 0:
            piececap2 = board.pieces[cap2[0]][cap2[1]]
            if piececap2 != Piece.NONE and not Piece.isTeam(piececap2, Piece.getTeam(piece)): moves.append(Move(squarefrom, cap2))

        return moves

    def generateMoves(squarefrom, board):

        piece = board.pieces[squarefrom[0]][squarefrom[1]]

        if Piece.isType(piece, Piece.KING): return Move.kingMoves(squarefrom, board)
        elif Piece.isType(piece, Piece.KNIGHT): return Move.knightMoves(squarefrom, board)
        elif Piece.isType(piece, Piece.BISHOP): return Move.bishopMoves(squarefrom, board)
        elif Piece.isType(piece, Piece.ROOK): return Move.rookMoves(squarefrom, board)
        elif Piece.isType(piece, Piece.QUEEN): return Move.queenMoves(squarefrom, board)
        elif Piece.isType(piece, Piece.PAWN): return Move.pawnMoves(squarefrom, board)

    def __init__(self, squarefrom, squareto):
        self.squarefrom = squarefrom
        self.squareto = squareto

    