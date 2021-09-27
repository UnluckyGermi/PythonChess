from interface import Interface
from board import Board
from move import Move
from piece import Piece

STANDARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
TEST_FEN = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -"

DEPTH = 3

b = Board.fromFen(TEST_FEN)


outF = open("perft.txt", "w")


def generateMoves(depth, board):
    
    global outF, DEPTH
    counter = 0

    if depth == 0: return 1

    for move in Move.allLegalMovesForTeam(board.turn, board):
        
        newboard = board.newBoardAfterMove(move)
        counter += generateMoves(depth - 1, newboard)

        if depth == DEPTH:
            outF.write(move.toString() + ": " + str(counter) + "\n")
            counter = 0

    return counter

print(generateMoves(3, b))

outF.close()

interface = Interface(b)
interface(b)