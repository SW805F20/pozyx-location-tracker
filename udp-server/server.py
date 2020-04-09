from setup import Setup
from find_location import MultitagPositioning
from socket_multicast_sender import SocketMulticastSender
from package_formatter import PackageFormatter
from mock_find_location import MockMultiTagPositioning
from goalzone_generator import GoalzoneGenerator
import asyncio


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

    async def run(self):
        """Function that loops and continuously broadcasts the position of all tags"""
        while True:
            update_ball_pos_task = asyncio.create_task(self.update_ball_position())
            update_player_pos_task = asyncio.create_task(self.update_player_positions())
            update_goal_zone_task = asyncio.create_task(self.update_goal_zone())

            await update_ball_pos_task
            await update_player_pos_task
            await update_goal_zone_task

            # %256 because max value for the time stamp is 255
            self.time_stamp = (self.time_stamp + 1) % 256

    async def update_goal_zone(self):
        """ Updates the goal zone if ball is inside goal zone """

        # Accumulate consecutive goals and then broadcast newly generated goalzones
        ball_pos = self.multi_tag_positioning.get_position(self.setup.ball_tag)
        if self.goalzone_generator.accumulate_goals_scored_blue((ball_pos.x, ball_pos.y)):
            self.setup.teams[0].score += 1
            goal_scored_task = await asyncio.create_task(self.goal_scored_procedure())
            await goal_scored_task

        if self.goalzone_generator.accumulate_goals_scored_red((ball_pos.x, ball_pos.y)):
            self.setup.teams[1].score += 1
            goal_scored_task = await asyncio.create_task(self.goal_scored_procedure())
            await goal_scored_task

    async def goal_scored_procedure(self):
        """Calls the necessary functions when a goal has been scored"""
        self.goalzone_generator.generate_random_goalzones()
        await asyncio.create_task(self.send_goalzone_positions())
        await asyncio.create_task(self.send_goal_scored())

    async def update_ball_position(self):
        """Broadcasts the updated ball position"""
        ball_tag = self.setup.ball_tag
        position = self.multi_tag_positioning.get_position(ball_tag)
        message = self.formatter.format_player_position(self.time_stamp, 0, position.x, position.y)
        self.multicast_sender.send(message)

    async def update_player_positions(self):
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

    async def send_goalzone_positions(self):
        """ Broadcasts the goalzone positions"""
        blue_team_message = self.formatter.format_goal_position(self.time_stamp, 0, int(self.goalzone_generator.center_of_blue_goal[0]), 
                                                                int(self.goalzone_generator.center_of_blue_goal[1]))
        red_team_message = self.formatter.format_goal_position(self.time_stamp, 1, int(self.goalzone_generator.center_of_red_goal[0]), 
                                                                int(self.goalzone_generator.center_of_red_goal[1]))
        self.multicast_sender.send(blue_team_message)
        self.multicast_sender.send(red_team_message)

    async def send_goal_scored(self):
        """Broadcasts that a goal was scored for either team"""
        goal_message = self.formatter.format_goal_scored(self.time_stamp, self.setup.teams[0].score, self.setup[1].score)
        self.multicast_sender.send(goal_message)


if __name__ == "__main__":
    server = Server(True)
    # Initial goalzones are broadcasted to the clients
    server.send_goalzone_positions()
    asyncio.run(server.run())
