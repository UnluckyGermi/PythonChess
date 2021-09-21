

class Move:


    def checkValidMove(move):
        if move.squareto[0] > 7 or move.squareto[1] > 7 or move.squareto[0] < 0 or move.squareto[1] < 0: return False
        return True

    def diagonalMoves(squarefrom):
        moves = []

        for i in [-1, 1]:
            for j in [-1, 1]:
                to = squarefrom[0] + i, squarefrom[1] + j
                moves.append(Move(squarefrom, to))
        
        return moves

    def linearMoves(squarefrom): 
        moves = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if abs(i) == abs(j): continue

                to = squarefrom[0] + i, squarefrom[1] + j
                moves.append(Move(squarefrom, to))

        return moves

    def knightMoves(squarefrom):
        moves = []

        for i in [-2, -1, 1, 2]:
            for j in [-2, -1, 1, 2]:
                if abs(i) == abs(j) : continue

                to = squarefrom[0] + i, squarefrom[1] + j
                move = Move(squarefrom, to)
                if Move.checkValidMove(move) : moves.append(move)

        return moves

    def kingMoves(squarefrom):
        return Move.diagonalMoves(squarefrom) + Move.linearMoves(squarefrom)



    def __init__(self, squarefrom, squareto):
        self.squarefrom = squarefrom
        self.squareto = squareto

    