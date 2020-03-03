import socket
import struct
import sys

class SocketMulticastReceiver(socket.socket):
    def __init__(self, multicast_group, server_address):
        # Create the socket using ipv4 and UDP
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the server address
        self.bind(server_address)

        # Tell the operating system to add the socket to
        # the multicast group on all interfaces.
        group = socket.inet_aton(multicast_group)
        # struct.pack() returns the object as bytes
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            mreq)
    
    def receive(self):
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)

        print('received {} bytes from {}'.format(
            len(data), address))
        print(data)

        print('sending acknowledgement to', address)
        sock.sendto(b'ack', address)

sock = SocketMulticastReceiver(multicast_group='224.3.29.71', server_address=('', 10000))
sock.receive()
