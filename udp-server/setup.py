import re
import copy

class Setup:
    amount_of_players = 0
    player_tags = []
    ball_tag = ""
    anchors = []
    teams = []

    # Dependent on the unit of measurement used. This is assumed to be millimeters
    ANCHOR_COORDINATE_LIMIT = 100000
    TEAM_NAMES = ["Blue", "Red"]

    def start(self):
        mock = self.prompt_mock_data()

        if not mock:
            self.prompt_amount_of_players()
            self.prompt_player_tags()
            self.assign_teams()
            self.prompt_anchors()
            self.prompt_ball_tag()

    def prompt_mock_data(self):
        use_mock_data = input("Use mock data? (y/n) ")
        if use_mock_data == "y":
            self.amount_of_players = 4
            self.ball_tag = 0x0
            self.anchors.append(Anchor(0x1, 1, 0, 0))
            self.anchors.append(Anchor(0x2, 1, 1, 0))
            self.anchors.append(Anchor(0x3, 1, 1, 0))
            self.anchors.append(Anchor(0x4, 0, 1, 0))
            self.player_tags.append(0x1)
            self.player_tags.append(0x2)
            self.player_tags.append(0x3)
            self.player_tags.append(0x4)
            return True
        return False

    def prompt_amount_of_players(self):
        """
		Function that prompts the user for the amount of players in the game.
		"""
        while True:
            amount_of_players = input("Amount of players? ")
            if self.is_int(amount_of_players):
                self.amount_of_players = int(amount_of_players)
                break
            else:
                print("The input must be an integer, please try again.")

    def prompt_ball_tag(self):
        """
		Function that prompts the user for the ball tag.
		"""
        while True:
            ball_tag = input("Ball tag: ")
            if self.is_hex(ball_tag):
                self.ball_tag = ball_tag
                break
            else:
                print("Ball tag must be hexadecimal, please try again.")

    def prompt_anchors(self):
        """
		Function that prompts the user for the anchors' coordinates.
		"""
        # assumes that there are 4 anchors
        for i in range(1, 5):
            while True:
                anchor_id = input("Id of anchor {}: ".format(i))
                string = input("Position of anchor {}: ".format(i))
                coordinates = string.split()
                if self.verify_anchor_coordinates(coordinates) and self.is_hex(anchor_id):
                    break
            self.anchors.append(Anchor(anchor_id, coordinates[0], coordinates[1], coordinates[2]))
        self.anchors = self.sort_anchors()

    def sort_anchors(self):
        """
		Function that sorts the anchors to ensure that they are in clockwise order
		"""
        center_x = 0

        sw_corner = None
        nw_corner = None
        ne_corner = None
        se_corner = None

        # Calculate the center x-coordinate of the playing field
        for anchor in self.anchors:
            center_x = center_x + int(anchor.x)
        center_x = center_x / len(self.anchors)

        # Find the lowest x value left of center
        for anchor in (anchor for anchor in self.anchors if int(anchor.x) <= int(center_x)):
            if sw_corner is None or int(anchor.y) < int(sw_corner.y):
                nw_corner = sw_corner
                sw_corner = anchor
            else:
                nw_corner = anchor

        # Find the lowest x value right of center
        for anchor in (anchor for anchor in self.anchors if int(anchor.x) >= int(center_x)):
            if ne_corner is None or int(anchor.y) > int(ne_corner.y):
                se_corner = ne_corner
                ne_corner = anchor
            else:
                se_corner = anchor

        return [sw_corner, nw_corner, ne_corner, se_corner]

    def prompt_player_tags(self):
        """
		Function that prompts the user the players' tags.
		"""
        for i in range(1, self.amount_of_players + 1):
            while True:
                if i < self.amount_of_players // 2 + 1:
                    player_tag = input("[{}] Player {}'s tag: ".format(self.TEAM_NAMES[0], i))
                else:
                    player_tag = input("[{}] Player {}'s tag: "
                                       .format(self.TEAM_NAMES[1], i - (self.amount_of_players // 2)))
                if self.is_hex(player_tag):
                    self.player_tags.append(player_tag)
                    break
                else:
                    print("Player tag must be hexadecimal, please try again.")

    def is_hex(self, x):
        """
		Function that checks if a string is a hexadecimal

		Parameters:
			x (string): input to be checked.
		"""
        if re.match("^(0[xX])?[a-fA-F0-9]+$", x):
            return True
        return False

    def is_int(self, x):
        """
		Function that checks if a string is an integer

		Parameters:
			x (string): input to be checked.
		"""
        try:
            x = int(x)
            return True
        except ValueError:
            return False

    def verify_anchor_coordinates(self, coordinates):
        """
		Function that verifies a list of strings by checking if it is three integer coordinates for an Anchor

		Parameters:
			coordinates [(string)]: list of strings.
		"""

        if len(coordinates) != 3:
            print("You must enter 3 coordinates, please try again.")
            return False

        for coordinate in coordinates:
            try:
                coordinate = int(coordinate)
                if abs(coordinate) > self.ANCHOR_COORDINATE_LIMIT:
                    print("Anchor coordinate value must be less than {}".format(
                        self.ANCHOR_COORDINATE_LIMIT))
                    return False
            except ValueError:
                print("Anchor coordinate value must be an integer, please try again.")
                return False

        return True

    def assign_teams(self):
        """
        Function that assigns players into teams by taking the first players inputed in player_tags and assigns them to
        the first team, and the rest to the following teams.

        """
        number_of_teams = len(self.TEAM_NAMES)
        players = copy.copy(self.player_tags)        # copy.copy copies the list into a new variable
        size_of_teams = int(self.amount_of_players / number_of_teams + self.amount_of_players % number_of_teams)
        if self.amount_of_players != 0:
            for i in range(0, number_of_teams):
                team = []
                for k in range(0, size_of_teams):
                    if len(players) == 0:
                        break
                    team.append(players[0])
                    players.remove(players[0])
                self.teams.append(Team(self.TEAM_NAMES[i], team, 0))    # The 0 appended into teams is the goal score.

class Anchor:
    def __init__(self, anchor_id, x, y, z):
        self.id = anchor_id
        self.x = x
        self.y = y
        self.z = z


class Team:
    def __init__(self, team_color, players, score):
        self.team_color = team_color
        self.players = players
        self.score = score


if __name__ == "__main__":
    setup = Setup()
    setup.start()
