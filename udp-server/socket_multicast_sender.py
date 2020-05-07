import socket
import struct
import time


class SocketMulticastSender(socket.socket):
    """ 
    This class is for creating a multicast udp socket
      
    Attributes: 
        multicast_group ((string, int)): address and port of the multicast group as a tuple
        timeout (number): used to set the timeout for the socket.
    """


    def __init__(self, multicast_group, timeout):
        """ 
        The constructor for the SocketMulticastSender
  
        Parameters: 
            multicast_group ((string, int)): address and port of the multicast group as a tuple
            timeout (number): used to set the timeout for the socket.
        """
        # our messages are 7 bytes and we want a max update speed of 70 Hz
        # Our version of Poxyz is onlt capable of sending about 60 Hz according to the documentation
        self.maxSendRateBytesPerSecond = (70*7)
        self.bytesAheadOfSchedule = 0
        self.time_now = None
        self.time_prev = None

        self.multicast_group = multicast_group

        # Create the datagram socket
        # AF_INET represent the address (and protocol) family ipv4. 
        # SOCK_DGRAM sets the socket to use UDP.
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout so the socket does not block
        # indefinitely when trying to receive data.
        self.settimeout(timeout)

        # Set the time-to-live for messages to 1 so they do not
        # go past the local network segment (3rd argument).
        # IPPROTO_IP and IP_MULTICAST_TTL are constants used for the options to make the socket multicast aware.
        self.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))

    def send(self, message):
        """ 
        Function for sending a message to the multicast group
        Parameters: 
            message (bytes): the bytes to send to the multicast group
        """
        # Send data to the multicast group
        print('sending {!r}'.format(message))

        self.time_now = time.time()
        if(self.time_prev != None):
            self.bytesAheadOfSchedule -= self.ConvertSecondsToBytes(self.time_now - self.time_prev)
        self.time_prev = self.time_now

        self.bytesAheadOfSchedule += 7
        if(self.bytesAheadOfSchedule > 0):
            time.sleep(self.ConvertBytesToSeconds(self.bytesAheadOfSchedule))

        # Send message to all clients listening on the multicast_group
        self.sendto(message, self.multicast_group)

    def ConvertSecondsToBytes(self, numSeconds):
        return numSeconds*self.maxSendRateBytesPerSecond

    def ConvertBytesToSeconds(self, numBytes):
        return float(numBytes)/self.maxSendRateBytesPerSecond

if __name__ == '__main__':
    sock = SocketMulticastSender(multicast_group=('224.3.29.71', 10000), timeout=0.2)
    while True:
        sock.send('test')
