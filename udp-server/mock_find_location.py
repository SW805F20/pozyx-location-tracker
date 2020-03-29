class MockMultiTagPositioning:
	"""Class that mocks positioning data. Used for when the pozyx hardware is not available """
	def __init__(self, tag_ids):
		"""
		Initializes players with hardcoded positions
		Parameters:
			tag_ids(list): List of tag_ids
		"""
		self.player_dict = {
			tag_ids[0]: TagPosition(1, 1),
			tag_ids[1]: TagPosition(100, 100),
			tag_ids[2]: TagPosition(550, 200),
			tag_ids[3]: TagPosition(50, 50),
			tag_ids[4]: TagPosition(700, 200),
		}

	def getPosition(self, tag_id):
		"""
		Get the position of a tag and increments it's position with 1
		Parameters:
			tag_id(string): tag id of the player that we are getting the position for
		"""
		
		position = self.player_dict[tag_id]
		self.player_dict[tag_id].x = self.player_dict[tag_id].x + 1
		self.player_dict[tag_id].y = self.player_dict[tag_id].y + 1
		return position


class TagPosition:
	def __init__(self, x, y):
		self.x = x
		self.y = y
