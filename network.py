import socket
import pickle


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.0.171"
        self.port = 5550
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            reply = pickle.loads(self.client.recv(2048*12))
            return reply
        except socket.error as e:
            print(str(e))
