from interface import Interface
from board import Board
from move import Move



b = Board.fromFen(Interface.STANDARD_FEN)


def generateMoves(depth, board):
    
    counter = 0

    if depth == 0: return 1

    for move in Move.allLegalMovesForTeam(board.turn, board):
        newboard = board.newBoardAfterMove(move)
        counter += generateMoves(depth - 1, newboard)

    return counter

interface = Interface(b)
interface(b)