"""
Module for the Breakout game server.

This module sets up a server to handle connections from two clients for a multiplayer Breakout game.

Classes:
    Game: Represents the game state.
    Wall: Represents the brick wall in the game.
    Paddle: Represents the player's paddle.
    Ball: Represents the game ball.
    Network: Manages network communication between the server and clients.

Functions:
    handle_client: Handles communication with a client.
    handle_third_client: Handles a third client attempting to connect.

Variables:
    s: Server socket for accepting incoming connections.
    server: Server address.
    port: Server port.
    mouse_pos: List to store mouse positions for two players.
    playerID: Current player ID.
    connections: List to store connection sockets for two players.
    game: Game object representing the game state.
"""

import socket
from _thread import start_new_thread
import pickle
import time
import sys
from game import Game

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get server address and port from command line arguments
server = sys.argv[1]
port = int(sys.argv[2])

try:
    # Bind the socket to the server address and port
    s.bind((server, port))

except socket.error as e:
    print(str(e))

# Listen for incoming connections (maximum 2)
s.listen(2)
print('Waiting for a connection')

# Initialize mouse positions for two players
mouse_pos = [(0, 0), (0, 0)]


def handle_client(connection, player):
    """
    Handles communication with a client.

    Args:
        connection (socket): Connection socket for the client.
        player (int): Player ID (0 or 1).
    """
    # Send player ID to the client
    connection.send(str.encode(str(player)))
    # Set the player as ready
    game.ready[player] = True
    run = True

    while run:
        try:
            if game.ready[player] is True:
                # Receive mouse position data from the client
                data = pickle.loads(connection.recv(2048))
                print(f'Player {player + 1}: {data}')
                if not data:
                    connection.send(str.encode('Closing connection...'))
                    run = False
                else:
                    # Update the mouse position for the corresponding player
                    mouse_pos[player] = data
                    # Update the game based on the turn
                    update()
                    # Send the updated game state back to the client
                    connection.send(pickle.dumps(game))
                # If the game is over, wait for a short duration and reset the game
                if game.game_over != 0 and run is True:
                    time.sleep(0.1)
                    game.reset()
            else:
                # If the player is not ready, receive a simple "Ready" message
                data = connection.recv(2024).decode()
                print(f'Player {player + 1}: {data}')
                if data == "Ready":
                    game.ready[player] = True
                # Send the game state back to the client
                connection.send(pickle.dumps(game))
        except ConnectionResetError:
            # Handle the case where the connection was reset by the other side
            print("Connection reset by peer")
            run = False
        except socket.error as err:
            print(f"Socket error: {err}")
            run = False
        except EOFError as err:
            print(f"Error: {err}")
            run = False

    print(f'Player {player + 1}: Connection closed')
    game.ready[player] = False
    connections[player] = None
    # If both connections are closed, reset the game
    if connections == [None, None]:
        game.reset()
    connection.close()


def handle_third_client(connection):
    """
    Handles a third client attempting to connect.

    Args:
        connection (socket): Connection socket for the third client.
    """
    # Send a rejection message to the third client and close the connection
    connection.send(str.encode("Rejected"))
    connection.close()


def update():
    """
    If both players are ready, update the game state based on the turn.
    """
    if game.ready[0] and game.ready[1]:
        if game.turn[0] % 2 == 0:
            game.update_game(mouse_pos[0])
        else:
            game.update_game(mouse_pos[1])


playerID = 0
connections = [None, None]
game = Game()
game.wall.create_wall()

while True:
    # Accept incoming connections
    conn, addr = s.accept()

    if connections[playerID] is None:
        # If the first slot is available, assign the connection to it
        connections[playerID] = conn
        print(f'Connected to: {addr}')
        # Start a new thread to handle communication with the client
        start_new_thread(handle_client, (conn, playerID))
        playerID = (playerID + 1) % 2
    elif connections[(playerID + 1) % 2] is None:
        # If the second slot is available, assign the connection to it
        connections[(playerID + 1) % 2] = conn
        print(f'Connected to: {addr}')
        # Start a new thread to handle communication with the client
        start_new_thread(handle_client, (conn, (playerID + 1) % 2))
        playerID = (playerID + 1) % 2
    else:
        # If both slots are occupied, reject the connection
        print('Rejected, the maximum number of connections has been reached')
        # Start a new thread to handle the rejection
        start_new_thread(handle_third_client, (conn, ))
