from setup import Setup
from find_location import MultitagPositioning 
from socket_multicast_sender import SocketMulticastSender
from package_formatter import PackageFormatter
from mock_find_location import MockMultiTagPositioning

class Server() :
    """Server class that handles all of the functionality on the system"""
    def __init__(self ,shouldMock=False):
        """
        Initializes the class and either uses mock class for multitag positioning or the real class
        """
        self.timeStamp = 0
        self.setup = Setup()
        self.setup.start()
        self.multicastSender = SocketMulticastSender(('224.3.29.71', 10000), 0.2)
        if shouldMock :
            self.multiTagPositioning = MockMultiTagPositioning([self.setup.ballTag] + self.setup.playerTags)
        else:
            self.multiTagPositioning = MultitagPositioning([self.setup.ballTag] + self.setup.playerTags, self.setup.anchors)
        self.formatter = PackageFormatter()


    def run(self):
        """Function that loops and continuously broadcasts the position of all tags"""
        while True:
            self.updateBallPosition()
            self.updatePlayerPositions()
            self.timeStamp = (self.timeStamp + 1) % 256

    def updateBallPosition(self):
        """Broadcasts the updated ball position"""
        ball_tag = self.setup.ballTag;
        position = self.multiTagPositioning.getPosition(ball_tag)
        message = self.formatter.formatPlayerPosition(self.timeStamp, 0, position.x, position.y)
        self.multicastSender.send(message)

    def updatePlayerPositions(self):
        """Broadcasts updated positions for all players"""
        for i in range(0, self.setup.amountOfPlayers):
            playerTag = self.setup.playerTags[i]
            position = self.multiTagPositioning.getPosition(playerTag)
            message = self.formatter.formatPlayerPosition(self.timeStamp, i+1, position.x, position.y)   
            self.multicastSender.send(message)

    def sendAnchorPositions(self):
        """broadcasts the anchor positions"""
        for i in range(0, 4):
            anchor = self.setup.anchors[i]
            message = self.formatter.formatAnchorPosition(self.timeStamp, i, anchor.x, anchor.y)
            self.multicastSender.send(message)

if __name__ == "__main__":
    server = Server(True)
    server.run()
