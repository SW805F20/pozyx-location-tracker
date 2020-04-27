class PackageFormatter:
    """formats data to hexadecimal packages"""

    def format_anchor_position(self, tag_id, pos_x, pos_y):
        """
		formats inputs to : 0xYYYYXXXXAATTII
		Parameters:
			tag_id (int): id of the anchor (A)
			pos_x (int): x coordinate of the anchor (X)
			pos_y (int): y coordinate of the anchor (Y)
            package_type (int): Type of the package that is being formatted (I)
		"""
        package = pos_y 					# package = 0xYYYY
        package = package << 16				# package = 0xYYYY0000
        package = package | pos_x			# package = 0xYYYYXXXX
        package = package << 8	    		# package = 0xYYYYXXXX00
        package = package | tag_id			# package = 0xYYYYXXXXAA
        package = package << 8				# package = 0xYYYYXXXXPP00
        package = package | 0x1             # package = 0xYYYYXXXXPPII

        hex_package = hex(package)
        return str(len(hex_package)).encode('UTF-8').zfill(2) + hex_package.encode('UTF-8')

    def format_player_tag(self, player_id, tag_id):
        """ formats input to: 0xPPTTTTII 
            Parameters:
                player_id (int): id of the player (P)
                tag:id (int): id of the tag that the player will be using (T)
                package_type (int): Type of the package that is being formatted (I)
        """
        package = player_id 				# package = 0xPP
        package = package << 16				# package = 0xPP0000
        package = package | tag_id			# package = 0xPPTTTT
        package = package << 8    		    # package = 0xPPTTTT00
        package = package | 0x2             # package = 0xPPTTTTII
        
        hex_package = hex(package)

        return str(len(hex_package)).encode('UTF-8').zfill(2) + hex_package.encode('UTF-8')

    def format_player_position(self, time_stamp, tag_id, pos_x, pos_y):
        """
		formats inputs to : 0xYYYYXXXXPPTTII
		Parameters:
            time_stamp (int): timestamp of the package (T)
			tag_id (int): id of the player (P)
			pos_x (int): x coordinate of the player tag (X)
			pos_y (int): y coordinate of the player tag (Y)
		"""
        return self.format_position(pos_y, pos_x, tag_id, time_stamp, 0x0)


    def format_goal_position(self, team_id, pos_x, pos_y, goal_zone_center_offset):
        """
		formats inputs to : 0xYYYYXXXXGGTTII
		Parameters:
			team_id (int): teamId that the goal belongs to (G)
			pos_x (int): x coordinate of the goal corner (X)
			pos_y (int): y coordinate of the goal corner (Y)
            goal_zone_center_offset (int): the length of the offset from the center of the goal (L)
		"""
        package = goal_zone_center_offset   # package = 0xLL
        package = package << 16				# package = 0xLL0000
        package = package | pos_y			# package = 0xLLYYYY
        package = package << 16             # package = 0xLLYYYY0000
        package = package | pos_x			# package = 0xLLYYYYXXXX
        package = package << 8	    		# package = 0xLLYYYYXXXX00
        package = package | team_id			# package = 0xLLYYYYXXXXGG
        package = package << 8				# package = 0xLLYYYYXXXXGG00
        package = package | 0x5             # package = 0xLLYYYYXXXXGGII

        hex_package = hex(package)

        return str(len(hex_package)).encode('UTF-8').zfill(2) + hex_package.encode('UTF-8')

    def format_goal_scored(self, team_0_score, team_1_score):
        """
		formats inputs to : 0x1100TTII
		Parameters:
			team_0_score (int): score of team 0 (0)
			team_1_score (int): score of team 1 (1)
		"""
        package = team_1_score				# package = 0x11
        package = package << 8				# package = 0x1100	
        package = package | team_0_score	# package = 0x1100
        package = package << 8				# package = 0x110000
        package = package | 0x4				# package = 0x1100II

        hex_package = hex(package)

        return str(len(hex_package)).encode('UTF-8').zfill(2) + hex_package.encode('UTF-8')

    def format_position(self, pos_y, pos_x, tag_id, time_stamp, package_type):
        """
		general purpouse function for formatting position packages
		Parameters:
			package_type (int): Type of the package that is being formatted (I)
            time_stamp (int): timestamp of the package (T)
			tag_id (int): The id of the tag (G)
			pos_x (int): x coordinate of the goal corner (X)
			pos_y (int): y coordinate of the goal corner (Y)
		"""
        package = pos_y 					# package = 0xYYYY
        package = package << 16				# package = 0xYYYY0000
        package = package | pos_x			# package = 0xYYYYXXXX
        package = package << 8	    		# package = 0xYYYYXXXX00
        package = package | tag_id			# package = 0xYYYYXXXXGG
        package = package << 8				# package = 0xYYYYXXXXGG00
        package = package | time_stamp		# package = 0xYYYYXXXXGGTT
        package = package << 8				# package = 0xYYYYXXXXGGTT00
        package = package | package_type    # package = 0xYYYYXXXXGGTTII
        
        
        return hex(package).encode('UTF-8')



if __name__ == "__main__":
    formatter = PackageFormatter()
    formatter.format_player_position(1, 1, 1000, 3999)
