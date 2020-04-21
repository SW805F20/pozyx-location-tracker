import socket

class TCPSocket(socket.socket):
    
    def __init__(self, tcp_port):
        self.tcp_ip = self.get_local_ip()
        self.tcp_port = tcp_port
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        self.bind((self.tcp_ip, self.tcp_port))


    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        local_ip_address = s.getsockname()[0]
        s.close()
        return local_ip_address
        
