from interface import Interface
from board import Board
from move import Move

STANDARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def main():
    b = Board.fromFen(STANDARD_FEN)

    interface = Interface(b)
    interface()


if __name__ == "__main__":
    main()
