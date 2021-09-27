from interface import Interface
from board import Board
from move import Move
from piece import Piece

STANDARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
TEST_FEN = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"

DEPTH = 3

b = Board.fromFen(TEST_FEN)

nodes = 0

outF = open("perft.txt", "w")


def generateMoves(depth, board):
    
    global outF, DEPTH, nodes
    counter = 0

    if depth == 0: return 1

    for move in Move.allLegalMovesForTeam(board.turn, board):
        
        newboard = board.newBoardAfterMove(move)
        counter += generateMoves(depth - 1, newboard)
        nodes += counter
        

        if depth == DEPTH:
            outF.write(move.toString() + ": " + str(counter) + "\n")
            
        counter = 0
        
        

    return counter

generateMoves(DEPTH, b)

print(nodes)

outF.close()

interface = Interface(b)
interface(b)