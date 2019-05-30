from socket import socket, AF_INET, SOCK_STREAM

class NetLogger:
    def __init__(self, host="localhost", port=8370):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.host = host
        self.port = port
        self.status = "disconnected"
    def connect(self):
        try:
            self.s.connect((self.host,self.port))
            self.status = "connected"
        except:
            pass
    def disconnect(self):
        self.s.close()
        self.status = "disconnected"
    def log(self,txt):
        if self.status == "connected":
            self.s.send(txt+"\n")
