class MockMultiTagPositioning():
    def __init__(self, tag_ids):
        """Initializes players with hardcoded positions"""
        self.playerDict = {
            tag_ids[0]: TagPosition(1, 1),
            tag_ids[1]: TagPosition(100, 100),
            tag_ids[2]: TagPosition(550, 200),
            tag_ids[3]: TagPosition(50, 50),
            tag_ids[4]: TagPosition(700, 200),
        }
    
    def getPosition(self, tag_id):
        """Get the position of a tag and increments it's position with 2"""
        position = self.playerDict[tag_id]
        self.playerDict[tag_id].x = self.playerDict[tag_id].x + 2
        self.playerDict[tag_id].y = self.playerDict[tag_id].y + 2
        return position

class TagPosition():
    def __init__(self, x, y):
        self.x = x
        self.y = y
