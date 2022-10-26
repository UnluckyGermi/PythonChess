from game.game import Game
from game.board import Board
from game.move import Move
from game.piece import Piece

STANDARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
TEST_FEN = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"

def generateMoves(depth, board):

    if depth == 0: return 1
    counter = 0

    for move in Move.allLegalMovesForTeam(board.turn, board):
        newboard = board.newBoardAfterMove(move)
        counter += generateMoves(depth - 1, newboard)

    return counter

if __name__ == "__main__":

    b = Board.fromFen(STANDARD_FEN)
    print(generateMoves(5, b))


    
    # game = Game(b, 0, None)
    # game()
    