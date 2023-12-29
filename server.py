import socket
from _thread import *
from game import Game
import pickle
import time
import sys

MAX_CONNECTIONS = 2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = sys.argv[1]
port = int(sys.argv[2])

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print(f'Waiting for a connection')

mouse_pos = [(0, 0), (0, 0)]


def handle_client(conn, playerID):
    conn.send(str.encode(str(playerID)))
    game.ready[playerID] = True

    while True:
        try:
            if game.ready[playerID] is True:
                data = pickle.loads(conn.recv(2048))
                print(f'Player {playerID + 1}: {data}')
                if not data:
                    conn.send(str.encode('Closing connection...'))
                    break
                else:
                    mouse_pos[playerID] = data
                    if game.ready[0] and game.ready[1]:
                        if game.turn[0] % 2 == 0:
                            game.update_game(mouse_pos[0])
                        else:
                            game.update_game(mouse_pos[1])
                    conn.send(pickle.dumps(game))
                if game.game_over != 0:
                    time.sleep(0.1)
                    game.reset()
            else:
                data = conn.recv(2024).decode()
                print(f'Player {playerID + 1}: {data}')
                if data == "Ready":
                    game.ready[playerID] = True
                conn.send(pickle.dumps(game))
        except:
            print(f'Error')
            break

    print(f'Player {playerID + 1}: Connection closed')
    game.ready[playerID] = False
    connections[playerID] = None
    if connections == [None, None]:
        game.reset()
    conn.close()


def handle_third_client(conn):
    conn.send(str.encode("Rejected"))
    conn.close()


playerID = 0
connections = [None, None]
game = Game()
game.wall.create_wall()

while True:
    conn, addr = s.accept()

    if connections[playerID] is None:
        connections[playerID] = conn
        print(f'Connected to: {addr}')
        start_new_thread(handle_client, (conn, playerID))
        playerID = (playerID + 1) % 2
    elif connections[(playerID + 1) % 2] is None:
        connections[(playerID + 1) % 2] = conn
        print(f'Connected to: {addr}')
        start_new_thread(handle_client, (conn, (playerID + 1) % 2))
        playerID = (playerID + 1) % 2
    else:
        print(f'Rejected, the maximum number of connections has been reached')
        start_new_thread(handle_third_client, (conn, ))
