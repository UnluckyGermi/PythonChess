

class Move:

    def checkValidMove(move):
        if move.squareto[0] > 7 or move.squareto[1] > 7 or move.squareto[0] < 0 or move.squareto[1] < 0: return False
        return True


    """def slidingMove(squarefrom, dir, board):
        moves = []
        i = 0

        while True:
            to = squarefrom[0] + dir[0], squarefrom[1] + dir[1]
            move = Move(squarefrom, to)

            if not Move.checkValidMove(move): break
            i += 1

            if(board.pieces[to] != '-'):
                pass


"""

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
        moves = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0: continue

                to = squarefrom[0] + i, squarefrom[1] + j
                move = Move(squarefrom, to)
                if Move.checkValidMove(move) : moves.append(move)

        return moves



    def __init__(self, squarefrom, squareto):
        self.squarefrom = squarefrom
        self.squareto = squareto

    