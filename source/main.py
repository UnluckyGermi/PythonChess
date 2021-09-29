from interface import Interface
from board import Board
from move import Move
from piece import Piece

STANDARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
TEST_FEN = "7k/8/8/8/8/8/8/KQ6"

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

#generateMoves(DEPTH, b)

print(nodes)

outF.close()

interface = Interface(b)
interface(b)