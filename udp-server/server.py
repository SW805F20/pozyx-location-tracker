from setup import Setup
from find_location import MultitagPositioning
from socket_multicast_sender import SocketMulticastSender
from package_formatter import PackageFormatter
from mock_find_location import MockMultiTagPositioning


class Server:
    """Server class that handles all of the functionality on the system"""

    def __init__(self, should_mock=False):
        """
        Initializes the class and either uses mock class for multitag positioning or the real class
        """
        self.time_stamp = 0
        self.setup = Setup()
        self.setup.start()
        self.multicast_sender = SocketMulticastSender(('224.3.29.71', 10000), 0.2)
        if should_mock:
            self.multi_tag_positioning = MockMultiTagPositioning([self.setup.ball_tag] + self.setup.player_tags)
        else:
            self.multi_tag_positioning = MultitagPositioning([self.setup.ball_tag] + self.setup.player_tags,
                                                             self.setup.anchors)
        self.formatter = PackageFormatter()

    def run(self):
        """Function that loops and continuously broadcasts the position of all tags"""
        while True:
            self.update_ball_position()
            self.update_player_positions()
            self.time_stamp = (self.time_stamp + 1) % 256

    def update_ball_position(self):
        """Broadcasts the updated ball position"""
        ball_tag = self.setup.ball_tag
        position = self.multi_tag_positioning.get_position(ball_tag)
        message = self.formatter.format_player_position(self.time_stamp, 0, position.x, position.y)
        self.multicast_sender.send(message)

    def update_player_positions(self):
        """Broadcasts updated positions for all players"""
        for i in range(0, self.setup.amount_of_players):
            player_tag = self.setup.player_tags[i]
            position = self.multi_tag_positioning.get_position(player_tag)
            message = self.formatter.format_player_position(self.time_stamp, i + 1, position.x, position.y)
            self.multicast_sender.send(message)

    def sendAnchorPositions(self):
        """broadcasts the anchor positions"""
        for i in range(0, 4):
            anchor = self.setup.anchors[i]
            message = self.formatter.format_anchor_position(self.time_stamp, i, anchor.x, anchor.y)
            self.multicast_sender.send(message)


if __name__ == "__main__":
    server = Server(True)
    server.run()
