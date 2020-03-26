import socket
import struct
import sys

class SocketMulticastReceiver(socket.socket):
    def __init__(self, multicast_group, server_address):
        """ 
        The constructor for the SocketMulticastSender
  
        Parameters: 
            multicast_group (string): address of the multicast group
            server_address ((string, int)): tuple containing the address and port.
        """

        # Create the socket using ipv4 and UDP
        # AF_INET represent the address (and protocol) family ipv4. 
        # SOCK_DGRAM sets the socket to use UDP.
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the server address
        self.bind(server_address)

        # Tell the operating system to add the socket to
        # the multicast group on all interfaces.
        group = socket.inet_aton(multicast_group)

        # struct.pack() returns the object as bytes
        # 4sL is the format of the packing. 4s meaning the first is a string of 4 chars. L meaning it is follewed by an unsigned long
        # INADDR_ANY binds the socket to all available local interfaces
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)

        # Sets options for the socket.
        self.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            mreq)
    
    def receive(self):
        """ 
        Function to receive information from the multicast group.
        """
        print('\nwaiting to receive message')
        # receive message from sender with bufsize 1024. Also receive address
        data, address = self.recvfrom(1024)

        print('received {} bytes from {}'.format(
            len(data), address))
        print(data)

        print('sending acknowledgement to', address)
        self.sendto('ack'.encode('UTF-8'), address)


if __name__ == '__main__':
    sock = SocketMulticastReceiver(multicast_group='224.3.29.71', server_address=('', 10000))
    sock.receive()
