import socket
import struct
import sys

class SocketMulticastSender(socket.socket):
    multicast_group = tuple()
    def __init__(self, multicast_group):
        self.multicast_group = multicast_group

        # Create the datagram socket
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block
        # indefinitely when trying to receive data.
        self.settimeout(0.2)

        # Set the time-to-live for messages to 1 so they do not
        # go past the local network segment (3rd argument).
        self.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))
    def send(self, message):
        try:
            # Send data to the multicast group
            print('sending {!r}'.format(message))
            sock.sendto(message, self.multicast_group)

            # Look for responses from all recipients
            while True:
                print('waiting to receive')
                try:
                    data, server = sock.recvfrom(16)
                except socket.timeout:
                    print('timed out, no more responses')
                    break
                else:
                    print('received {!r} from {}'.format(
                        data, server))

        finally:
            print('closing socket')
            sock.close()

sock = SocketMulticastSender(multicast_group=('224.3.29.71', 10000))
sock.send(b'test')
