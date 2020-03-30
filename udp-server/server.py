from setup import Setup
from find_location import MultitagPositioning
from socket_multicast_sender import SocketMulticastSender
from package_formatter import PackageFormatter
from mock_find_location import MockMultiTagPositioning
from goalzone_generator import GoalzoneGenerator


class Server:
    """Server class that handles all of the functionality on the system"""

    def __init__(self, should_mock=False):
        """
        Initializes the class and either uses mock class for multitag positioning or the real class
		Parameters:
			should_mock(boolean): If the server shold use the MockMultiTagePositioning class
        """
        self.time_stamp = 0
        self.setup = Setup()
        self.setup.start()
        self.multicast_sender = SocketMulticastSender(('224.3.29.71', 10000), 0.2)
        self.goalzone_generator = GoalzoneGenerator(self.setup.anchors, 20)

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

            # check if a goal has been scored and then broadcast newly generated goalzones
            ball_pos = self.multi_tag_positioning.get_position(self.setup.ball_tag)
            if self.goalzone_generator.goal_scored((ball_pos.x, ball_pos.y)):
                self.goalzone_generator.generate_random_goalzones()
                self.send_goalzone_positions()
            
            self.time_stamp = (self.time_stamp + 1) % 256	# %256 because max value for the time stamp is 255

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
        for i in range(0, len(self.setup.anchors)):
            anchor = self.setup.anchors[i]
            message = self.formatter.format_anchor_position(self.time_stamp, i, anchor.x, anchor.y)
            self.multicast_sender.send(message)

    def send_goalzone_positions(self):
        """ Broadcasts the goalzone positions"""
        # TODO: Receive acknowledgement from clients that new goalzones have been received
        blue_team_message = self.formatter.format_goal_position(self.time_stamp, 0, int(self.goalzone_generator.center_of_blue_goal[0]), 
                                                                int(self.goalzone_generator.center_of_blue_goal[1]))
        red_team_message = self.formatter.format_goal_position(self.time_stamp, 1, int(self.goalzone_generator.center_of_red_goal[0]), 
                                                                int(self.goalzone_generator.center_of_red_goal[1]))
        self.multicast_sender.send(blue_team_message)
        self.multicast_sender.send(red_team_message)

if __name__ == "__main__":
    server = Server(True)
    # Initial goalzones are broadcasted to the clients
    server.send_goalzone_positions()
    server.run()
