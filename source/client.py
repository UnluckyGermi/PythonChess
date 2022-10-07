import socket
import sys
from _thread import *
from game.game import Game
from game.board import Board
from game.move import Move

STANDARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

SERVER_IP = "192.168.0.131"
SERVER_PORT = 64355

def parse_args():
    global SERVER_IP
    if "-s" in sys.argv:
        idx = sys.argv.index("-s")
        if len(sys.argv) < idx+2:
            print("Se usó la opción -s pero no se especificó ninguna IP.")         
            exit(1)

        SERVER_IP = sys.argv[idx+1]
        
if __name__ == "__main__":
    print("-- PYTHON CHESS --")
    print("Conectando al servidor...")

    b = Board.fromFen(STANDARD_FEN)

    parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = (SERVER_IP, SERVER_PORT)
    conn = s.connect(server)


    team = s.recv(1).decode()

    if team == 'w':
        game = Game(b, 0, s)
    else:
        game = Game(b, 1, s)

    start_new_thread(game, ())

    while True:
        move_str = s.recv(6).decode()
        move = Move.fromString(move_str)
        b.makeMove(move)


