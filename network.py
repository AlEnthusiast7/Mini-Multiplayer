import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server =  "192.168.1.66"
        self.port = 64340
        self.addr = (self.server, self.port)
        self.p = self.connect()



    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            x = pickle.loads(self.client.recv(2048))
            print(x)
            return x
        except Exception as e:
            print("Connection error:", e)
            return


    def send(self,data):
            try:
                self.client.send(pickle.dumps(data))
                return pickle.loads(self.client.recv(4096))
            except socket.error as e:
                print("Socket error: ", e)

