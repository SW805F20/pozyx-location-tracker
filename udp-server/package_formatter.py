class PackageFormatter:
    """formats data to hexadecimal packages"""

    def format_anchor_position(self, time_stamp, tag_id, pos_x, pos_y):
        """
		formats inputs to : 0xyyyyxxxxaattii
		Parameters:
            time_stamp (int): timestamp of the package (t)
			tag_id (int): id of the anchor (a)
			pos_x (int): x coordinate of the anchor (x)
			pos_y (int): y coordinate of the anchor (y)
		"""
        package = self.format_position(pos_y, pos_x, tag_id, time_stamp, 0x0)
        return hex(package)

    def format_player_position(self, time_stamp, tag_id, pos_x, pos_y):
        """
		formats inputs to : 0xyyyyxxxxppttii
		Parameters:
            time_stamp (int): timestamp of the package (t)
			tag_id (int): id of the player (p)
			pos_x (int): x coordinate of the player tag (x)
			pos_y (int): y coordinate of the player tag (y)
		"""
        package = self.format_position(pos_y, pos_x, tag_id, time_stamp, 0x1)
        return hex(package)

    def format_goal_position(self, time_stamp, team_id, pos_x, pos_y):
        """
		formats inputs to : 0xyyyyxxxxggttii
		Parameters:
            time_stamp (int): timestamp of the package (t)
			team_id (int): teamId that the goal belongs to (g)
			pos_x (int): x coordinate of the goal corner (x)
			pos_y (int): y coordinate of the goal corner (y)
		"""
        package = self.format_position(pos_y, pos_x, team_id, time_stamp, 0x2)
        return hex(package)

    def format_goal_scored(self, time_stamp, team_0_score, team_1_score):
        """
		formats inputs to : 0x1100ttii
		Parameters:
            timestamp (int): timestamp of the package (t)
			team_0_score (int): score of team 0 (0)
			team_1_score (int): score of team 1 (1)
		"""
        package = team_1_score
        package = package << 8
        package = package | team_0_score
        package = package << 8
        package = package | time_stamp
        package = package << 8
        package = package | 0x3
        return hex(package)

    def format_position(self, pos_y, pos_x, tag_id, time_stamp, package_type):
        """
		general purpouse function for formatting position packages
		"""
        package = pos_y
        package = package << 16
        package = package | pos_x
        package = package << 8
        package = package | tag_id
        package = package << 8
        package = package | time_stamp
        package = package << 8
        package = package | package_type
        return package


if __name__ == "__main__":
    formatter = PackageFormatter()
    formatter.format_player_position(1, 1, 1000, 3999)
