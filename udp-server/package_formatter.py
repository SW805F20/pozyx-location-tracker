class PackageFormatter():
	"""formats data to hexadecimal packages"""

	def formatAnchorPosition(self, timeStamp, id, posX, posY):
		"""
		formats inputs to : 0xyyyyxxxxaattii
		Parameters:
            timestamp (int): timestamp of the package (t)
			id (int): id of the anchor (a)
			posX (int): x coordinate of the anchor (x)
			posY (int): y coordinate of the anchor (y)
		"""
		package = self.formatPosition(posY, posX, id, timeStamp, 0x0)
		return hex(package)

	def formatPlayerPosition(self, timeStamp, id, posX, posY):
		"""
		formats inputs to : 0xyyyyxxxxppttii
		Parameters:
            timestamp (int): timestamp of the package (t)
			id (int): id of the player (p)
			posX (int): x coordinate of the player tag (x)
			posY (int): y coordinate of the player tag (y)
		"""
		package = self.formatPosition(posY, posX, id, timeStamp, 0x1)
		return hex(package) 

	def formatGoalPosition(self, timeStamp, teamId, posX, posY):
		"""
		formats inputs to : 0xyyyyxxxxggttii
		Parameters:
            timestamp (int): timestamp of the package (t)
			id (int): teamId that the goal belongs to (g)
			posX (int): x coordinate of the goal corner (x)
			posY (int): y coordinate of the goal corner (y)
		"""
		package = self.formatPosition(posY, posX, teamId, timeStamp, 0x2)
		return hex(package)

	def formatGoalScored(self, timeStamp, team0Score, team1Score):
		"""
		formats inputs to : 0x1100ttii
		Parameters:
            timestamp (int): timestamp of the package (t)
			team0Score (int): score of team 0 (0)
			team1Score (int): score of team 1 (1)
		"""
		package = team1Score
		package = package << 8
		package = package | team0Score
		package = package << 8
		package = package | timeStamp
		package = package << 8
		package = package | 0x3
		return hex(package)

	def formatPosition(self, posY, posX, id, timeStamp, packageType):
		"""
		general purpouse function for formatting position packages
		"""
		package = posY
		package = package << 16
		package = package | posX
		package = package << 8
		package = package | id
		package = package << 8
		package = package | timeStamp
		package = package << 8
		package = package | packageType
		return package

if __name__ == "__main__":
	formatter = PackageFormatter()
	formatter.formatPlayerPosition(1, 1, 1000, 3999)

