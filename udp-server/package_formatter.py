class PackageFormatter:
    """formats data to hexadecimal packages"""

    def format_anchor_position(self, time_stamp, tag_id, pos_x, pos_y):
        """
		formats inputs to : 0xYYYYXXXXAATTII
		Parameters:
            time_stamp (int): timestamp of the package (T)
			tag_id (int): id of the anchor (A)
			pos_x (int): x coordinate of the anchor (X)
			pos_y (int): y coordinate of the anchor (Y)
		"""
        package = self.format_position(pos_y, pos_x, tag_id, time_stamp, 0x0)
        return hex(package)

    def format_player_position(self, time_stamp, tag_id, pos_x, pos_y):
        """
		formats inputs to : 0xYYYYXXXXPPTTII
		Parameters:
            time_stamp (int): timestamp of the package (T)
			tag_id (int): id of the player (P)
			pos_x (int): x coordinate of the player tag (X)
			pos_y (int): y coordinate of the player tag (Y)
		"""
        package = self.format_position(pos_y, pos_x, tag_id, time_stamp, 0x1)
        return hex(package)

    def format_goal_position(self, time_stamp, team_id, pos_x, pos_y):
        """
		formats inputs to : 0xYYYYXXXXGGTTII
		Parameters:
            time_stamp (int): timestamp of the package (T)
			team_id (int): teamId that the goal belongs to (G)
			pos_x (int): x coordinate of the goal corner (X)
			pos_y (int): y coordinate of the goal corner (Y)
		"""
        package = self.format_position(pos_y, pos_x, team_id, time_stamp, 0x2)
        return hex(package)

    def format_goal_scored(self, time_stamp, team_0_score, team_1_score):
        """
		formats inputs to : 0x1100TTII
		Parameters:
            timestamp (int): timestamp of the package (T)
			team_0_score (int): score of team 0 (0)
			team_1_score (int): score of team 1 (1)
		"""
        package = team_1_score				# package = 0x11
        package = package << 8				# package = 0x1100	
        package = package | team_0_score	# package = 0x1100
        package = package << 8				# package = 0x110000
        package = package | time_stamp		# package = 0x1100TT
        package = package << 8				# package = 0x1100TT00
        package = package | 0x3				# package = 0x1100TTII
        return hex(package)

    def format_position(self, pos_y, pos_x, tag_id, time_stamp, package_type):
        """
		general purpouse function for formatting position packages
		Parameters:
			package_type (int): Type of the package that is being formatted (I)
            time_stamp (int): timestamp of the package (T)
			tag_id (int): teamId that the goal belongs to (G)
			pos_x (int): x coordinate of the goal corner (X)
			pos_y (int): y coordinate of the goal corner (Y)
		"""
        package = pos_y 					# package = 0xYYYY
        package = package << 16				# package = 0xYYYY0000
        package = package | pos_x			# package = 0xYYYYXXXX
        package = package << 8	    		# package = 0xYYYYXXXX00
        package = package | tag_id			# package = 0xYYYYXXXXPP
        package = package << 8				# package = 0xYYYYXXXXPP00
        package = package | time_stamp		# package = 0xYYYYXXXXPPTT
        package = package << 8				# package = 0xYYYYXXXXPPTT00
        package = package | package_type    # package = 0xYYYYXXXXPPTTII
        return package


if __name__ == "__main__":
    formatter = PackageFormatter()
    formatter.format_player_position(1, 1, 1000, 3999)
