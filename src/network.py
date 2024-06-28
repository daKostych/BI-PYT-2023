"""
Module representing a network connection for multiplayer Breakout game.

Classes:
    Network: Represents a network connection.
"""

import socket
import pickle


class Network:
    """
    Class representing a network connection for multiplayer Breakout game.

    Attributes:
        client (socket.socket): Socket object representing the client's connection.
        host (str): IP address of the server.
        port (int): Port number for the connection.
        addr (tuple): Tuple representing the server address (host, port).
        id (str): ID assigned by the server.

    Methods:
        __init__: Initializes the Network object.
        connect: Connects to the server and receives an ID.
        send: Sends data to the server and receives a reply.
    """

    def __init__(self, ip, port):
        """
        Initializes the Network object.

        Args:
            ip (str): IP address of the server.
            port (int): Port number for the connection.
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ip
        self.port = port
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        """
        Connects to the server and receives an ID.

        Returns:
            str: ID assigned by the server.
        """
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        """
        Sends data to the server and receives a reply.

        Args:
            data: Data to be sent to the server.

        Returns:
            Any: Reply received from the server.
        """
        try:
            self.client.send(pickle.dumps(data))
            reply = pickle.loads(self.client.recv(2048*12))
            return reply
        except socket.error as e:
            print(str(e))
            return None
