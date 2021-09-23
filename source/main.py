from interface import Interface
from board import Board
from move import Move



b = Board.fromFen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -")


def generateMoves(depth, board):
    
    counter = 0

    if depth == 0: return 1

    for move in Move.allLegalMovesForTeam(board.turn, board):
        newboard = board.newBoardAfterMove(move)
        counter += generateMoves(depth - 1, newboard, castles)
        if move.castle: castles = castles+1

    return counter

print(generateMoves(3, b))

interface = Interface(b)
interface(b)