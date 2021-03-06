import time
from setup import Setup
from find_location import MultitagPositioning
from socket_multicast_sender import SocketMulticastSender
from tcp_socket import TCPSocket
from package_formatter import PackageFormatter
from mock_find_location import MockMultiTagPositioning
from goalzone_generator import GoalzoneGenerator
from player_connection import PlayerConnection
import asyncio
import threading
import socket
import copy


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
        self.multicast_sender = SocketMulticastSender(('224.3.29.71', 10000), 1)
        self.tcp_socket = TCPSocket(tcp_port=10000)
        self.player_connections = []
        self.player_id_counter = 1
        print('Server running on IP', self.tcp_socket.tcp_ip)
        self.goalzone_generator = GoalzoneGenerator(self.setup.anchors, 20)

        if should_mock:
            self.multi_tag_positioning = MockMultiTagPositioning([self.setup.ball_tag] + self.setup.player_tags)
        else:
            self.multi_tag_positioning = MultitagPositioning([self.setup.ball_tag] + self.setup.player_tags,
                                                             self.setup.anchors)
        self.formatter = PackageFormatter()


    def setup_game(self):
        """Function that handles the setup for the game by sending player tags and anchor positions"""
        self.tcp_socket.listen(self.setup.amount_of_players)
        player_tags_copy = copy.copy(self.setup.player_tags)

        self.tcp_socket.settimeout(2.0)
        while len(self.player_connections) < self.setup.amount_of_players:
            if self.setup.debug_mode:
                print('Waiting for connections')
            try:
                conn, addr = self.tcp_socket.accept()
            except socket.timeout:
                print('Received no incoming connection')
                continue
            
            
            if self.setup.debug_mode:
                print('connection from', addr)

            # The thread to handle the client connection is created
            client_handler = threading.Thread(
                # The function to execute on the thread
                target=self.send_setup_data,
                # The arguments passed to the function
                args=(conn, addr, player_tags_copy)
            )
            # The client is handled on a thread to allow the server to go 
            # back and wait for connection as data is sent to the first client
            client_handler.start()
        
        self.prompt_game_start()

    def prompt_game_start(self):
        """ Function that awaits a confirmation from host client before it starts sending positions
            On the UDP client socket. """
        print('All players have connected to the game.')
        start_game = ""

        while start_game != "y":
            start_game = input("Start game? (y/n): ")

        for player_con in self.player_connections:
            self.send_start_game(player_con.client_socket)

    def send_start_game(self, client_socket):
        """ Function that sends the formatted package to players """
        message = self.formatter.format_game_start()
        if self.setup.debug_mode:
            print('sending game start signal')
        self.tcp_send(client_socket, message)

    def send_end_game(self, client_socket):
        """ Function that sends the formatted end game package to players
            Parameters:
                client_socket (socket): The socket with connection to the client
        """
        message = self.formatter.format_game_end()
        if self.setup.debug_mode:
            print('sending game start signal')
        self.tcp_send(client_socket, message)

    def send_end_all_players(self):
        """ Function to send an endgame message to all connected players """
        for player_con in self.player_connections:
            self.send_end_game(player_con.client_socket)

    async def run(self):
        """ Function that loops and continuously broadcasts the position of all tags """
        game_running = True
        while game_running:
            update_ball_pos_task = asyncio.create_task(self.update_ball_position())
            update_player_pos_task = asyncio.create_task(self.update_player_positions())
            update_goal_zone_task = asyncio.create_task(self.update_goal_zone())

            await update_ball_pos_task
            await update_player_pos_task
            await update_goal_zone_task

            # %256 because max value for the time stamp is 255
            self.time_stamp = (self.time_stamp + 1) % 256

            if (self.setup.amount_of_goals == self.setup.teams[0].score or
                    self.setup.amount_of_goals == self.setup.teams[1].score):
                game_running = False
                self.setup.teams[0].score = 0
                self.setup.teams[1].score = 0

        if not game_running:
            self.send_end_all_players()
            # Unity waits for 3 seconds when the game ends, so doing it here as well prevents host from 
            # sending new game before players are ready.
            time.sleep(3)
            self.prompt_game_start()
            await self.run()


    async def update_goal_zone(self):
        """ Updates the goal zone if ball is inside goal zone """

        # Accumulate consecutive goals and then broadcast newly generated goalzones
        ball_pos = self.multi_tag_positioning.get_position(self.setup.ball_tag)
        if self.goalzone_generator.accumulate_goals_scored_blue((ball_pos.x, ball_pos.y)):
            self.setup.teams[0].score += 1
            self.goal_scored_procedure()

        if self.goalzone_generator.accumulate_goals_scored_red((ball_pos.x, ball_pos.y)):
            self.setup.teams[1].score += 1
            self.goal_scored_procedure()

    def goal_scored_procedure(self):
        """Calls the necessary functions when a goal has been scored"""
        self.goalzone_generator.generate_random_goalzones()
        for player_con in self.player_connections:
            self.send_goalzone_positions(player_con.client_socket)
            self.send_goal_scored(player_con.client_socket)

    async def update_ball_position(self):
        """Broadcasts the updated ball position"""
        ball_tag = self.setup.ball_tag
        position = self.multi_tag_positioning.get_position(ball_tag)
        message = self.formatter.format_player_position(self.time_stamp, 0, position.x, position.y)
        self.multicast_sender.send(message)

    async def update_player_positions(self):
        """Broadcasts updated positions for all players"""
        for player_connection in self.player_connections:
            position = self.multi_tag_positioning.get_position(player_connection.player_id - 1)
            message = self.formatter.format_player_position(self.time_stamp, player_connection.player_id, position.x, position.y)
            self.multicast_sender.send(message)

    def send_setup_data(self, client_socket, addr, player_tags_copy):
        """ Sends the initial information to a client before the game starts
            Parameters:
                client_socket (socket): The socket with connection to the client
                addr (tuple): tuple with the connected players ip and port
                player_tags_copy (list): list of the player tags
        """
        # If the PlayerConnection should be appended to the list of players connected
        should_append = False

        # Look up the a player connection from the addr
        player_connection = next((x for x in self.player_connections if x.addr[0] == addr[0]), None)
        if player_connection is None:
            # if none is found a new is created
            player_connection = PlayerConnection(addr, player_tags_copy.pop(), self.player_id_counter, client_socket)
            self.player_id_counter += 1
            should_append = True
        else:
            if self.setup.debug_mode:
                print('This address has already connected to the game')

        self.send_anchor_positions_to_client(client_socket, player_connection)
        self.send_player_goal_amount(client_socket, player_connection)
        self.send_player_tag(client_socket, player_connection)
        self.send_goalzone_positions(client_socket)

        # We only want to append to the list if its a new connection
        # This is done after sending, to avoid the main program from continuing before data is sent
        if should_append:
            self.player_connections.append(player_connection)

    def send_player_goal_amount(self, client_socket, player_connection):
        """ Sends the number of players and the required goal amount
                    Parameters:
                        client_socket (socket): The socket with connection to the client
                        player_connection (PlayerConnection): object with data about the player connected such as ip and port, player_tag and player_id
                """
        message = self.formatter.format_player_goal_amount(self.setup.amount_of_players, self.setup.amount_of_goals)
        if self.setup.debug_mode:
            print('sending', message, 'to', player_connection.addr)
        self.tcp_send(client_socket, message)

    def send_player_tag(self, client_socket, player_connection):
        """ Sends the player tag that the client will be using in the game 
            Parameters:
                client_socket (socket): The socket with connection to the client
                player_connection (PlayerConnection): object with data about the player connected such as ip and port, player_tag and player_id
        """
        message = self.formatter.format_player_tag(player_connection.player_id, player_connection.tag_id)
        if self.setup.debug_mode:
            print('sending', message, 'to', player_connection.addr)
        self.tcp_send(client_socket, message)

    def send_anchor_positions_to_client(self, client_socket, player_connection):
        """ Broadcasts the anchor positions
            Parameters:
                client_socket (socket): The socket with connection to the client
                player_connection (PlayerConnection): object with data about the player connected such as ip, player_tag and player_id
        """
        for i in range(0, len(self.setup.anchors)):
            anchor = self.setup.anchors[i]
            message = self.formatter.format_anchor_position(i, int(anchor.x), int(anchor.y))
            if self.setup.debug_mode:
                print('sending', message, 'to', player_connection.addr)
            self.tcp_send(client_socket, message)

    def send_goalzone_positions(self, client_socket):
        """ Broadcasts the goalzone positions
            Parameters:
                client_socket (socket): The socket with connection to the client
        """
        blue_team_message = self.formatter.format_goal_position(0, int(self.goalzone_generator.center_of_blue_goal[0]), 
                                                                int(self.goalzone_generator.center_of_blue_goal[1]), int(self.goalzone_generator.goal_zone_middle_offset))
        red_team_message = self.formatter.format_goal_position(1, int(self.goalzone_generator.center_of_red_goal[0]), 
                                                                int(self.goalzone_generator.center_of_red_goal[1]), int(self.goalzone_generator.goal_zone_middle_offset))
        self.tcp_send(client_socket, blue_team_message)
        self.tcp_send(client_socket, red_team_message)

    def send_goal_scored(self, client_socket):
        """Broadcasts that a goal was scored for either team
            Parameters:
                client_socket (socket): The socket with connection to the client
        """
        goal_message = self.formatter.format_goal_scored(self.setup.teams[0].score, self.setup.teams[1].score)
        self.tcp_send(client_socket, goal_message)


    def tcp_send(self, client_socket, message):
        """
        Sends a message on the tcp socket and handles any aborted connection errors that might have occured.
        Parameters: 
            player_connection (object): The player connection object containing information on the player that lost connection.
            message (bytes): the message as bytes.
        """
        try:
            client_socket.sendall(message)
        except ConnectionAbortedError:
            disconnected_player_con = next((x for x in self.player_connections if x.client_socket is client_socket), None)
            if disconnected_player_con is not None:
                print('Lost connection to client', disconnected_player_con.addr, 'with tag', disconnected_player_con.tag_id)
                self.player_connections.remove(disconnected_player_con)
                client_reconnection_thread = threading.Thread(
                    # The function to execute on the thread
                    target=self.reconnect_player,
                    # The arguments passed to the function
                    args=[disconnected_player_con]
                )
                # The client is handled on a thread to allow the server to go on
                client_reconnection_thread.start()

    def reconnect_player(self, player_connection):
        """
        Function to handle a player that is reconnectiong, should be called on its own thread.
        Parameters:
            player_connection (object): The player connection object containing information on the player that lost connection.
        """
        self.tcp_socket.listen()
        self.tcp_socket.settimeout(60)

        if self.setup.debug_mode:
            print('Waiting for reconnection')
        try:
            conn, addr = self.tcp_socket.accept()
        except socket.timeout:
            print('Received no incoming connection')
            self.tcp_socket.settimeout(2)
            return
        
        # Check if it is the same IP that has reconnected
        if player_connection.addr[0] == addr[0]:
            player_connection.client_socket = conn
            self.player_connections.append(player_connection)
            self.send_anchor_positions_to_client(conn, player_connection)
            self.send_player_goal_amount(conn, player_connection)
            self.send_player_tag(conn, player_connection)
            self.send_goalzone_positions(conn)
            self.send_goal_scored(conn)
            self.send_start_game(conn)

            if self.setup.debug_mode:
                print('Player reconnected from IP', addr)

if __name__ == "__main__":
    server = Server(True)
    server.setup_game()
    asyncio.run(server.run())
