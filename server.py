import socket
from _thread import *
from game import Game
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.0.171"
port = 5550

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print(f'Waiting for a connection')

mouse_pos = [(0, 0), (0, 0)]


def handle_client(conn, playerID):
    conn.send(str.encode(str(playerID)))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print(f'Player {playerID}: {data}')
            if not data:
                conn.send(str.encode('Closing connection...'))
                break
            else:
                mouse_pos[playerID-1] = data
                if game.turn[0] % 2 == 1:
                    game.update_game(mouse_pos[0])
                else:
                    game.update_game(mouse_pos[1])
                conn.send(pickle.dumps(game))
        except:
            print(f'Error')
            break

    print(f'Connection closed')
    conn.close()


playerID = 1
game = Game()
game.wall.create_wall()

while True:
    conn, addr = s.accept()
    print(f'Connected to: {addr}')

    start_new_thread(handle_client, (conn, playerID))
    playerID += 1
