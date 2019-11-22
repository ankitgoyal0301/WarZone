import socket


class network:

    """
    FUNCTION DESCRIPTION:
    Initialises the client. Add the host ipv4 address.
    """
    def __init__(self):
        self.host = '172.31.70.162'#socket.gethostbyname(socket.gethostname())  # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
        # ipv4 address. This feild will be the same for all your clients.
        self.port = 8888
        self.addr = (self.host, self.port)
        self.id = self.connect()

    """
    FUNCTION DESCRIPTION:
    Client Connects to the server.
    """
    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    """
    FUNCTION DESCRIPTION:
    Sends the required data to the server.
    """
    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            # if len(data)!=0:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
            # else:
            # reply = self.client.recv(2048).decode()
            #   return ""
        except socket.error as e:
            return str(e)
