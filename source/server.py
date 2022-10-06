import socket
import sys
from _thread import *

PORT = 64355
IP = ""

def parse_args():
    global IP
    if len(sys.argv) < 2:
        print("Debes especificar una IP.")
        exit(1)
    
    IP = sys.argv[1]

def game(conn1, conn2):
    conn1.send("w".encode())
    conn2.send("b".encode())

    while True:
        conn2.send(conn1.recv(5))
        conn1.send(conn2.recv(5))


if __name__ == "__main__":

    parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(5)

    print("Esperando a jugador 1...")
    conn1, addr1 = s.accept()
    print("Jugador 1: ", addr1)

    print("Esperando a jugador 2...")
    conn2, addr2 = s.accept()
    print("Jugador 2: ", addr2)

    print("\nEmpezando partida...")
    game(conn1, conn2)
    s.close()
    
