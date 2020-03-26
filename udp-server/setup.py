import re


class Setup():
    amountOfPlayers = 0
    playerTags = []
    ballTag = ""
    anchors = []
    # Dependent on the unit of measurement used. This is assumed to be millimeters
    ANCHOR_COORDINATE_LIMIT = 100000

    def start(self):
        self.promptAmountOfPlayers()
        self.promptPlayerTags()
        self.promptAnchors()
        self.promptBallTag()
    
    def promptAmountOfPlayers(self):
        """
        Function that prompts the user for the amount of players in the game.
        """
        while True:
            amountOfPlayers = input("Amount of players?")
            if self.isInt(amountOfPlayers):
                self.amountOfPlayers = int(amountOfPlayers)
                break
            else:
                print("The input must be an integer, please try again.")

    def promptBallTag(self):
        """
        Function that prompts the user for the ball tag.
        """
        while True:
            ballTag = input("Ball tag: ")
            if self.isHex(ballTag):
                self.ballTag = ballTag
                break
            else:
                print("Ball tag must be hexadecimal, please try again.")

    def promptAnchors(self):
        """
        Function that prompts the user for the anchors' coordinates.
        """
        # assumes that there are 4 anchors
        for i in range(1, 5):
            while True:
                anchorId = input("Id of anchor {}".format(i))
                string = input("Position of anchor {}: ".format(i))
                coordinates = string.split()
                if self.verifyAnchorCoordinates(coordinates) and self.isHex(anchorId):
                    break


		self.anchors.append(Anchor(coordinates[0], coordinates[1], coordinates[2]))
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

    def promptPlayerTags(self):
        """ 
        Function that prompts the user the players' tags.
        """
        for i in range(1, self.amountOfPlayers + 1):
            while True:
                playerTag = input("Player {}'s tag: ".format(i))
                if self.isHex(playerTag):
                    self.playerTags.append(playerTag)
                    break
                else:
                    print("Player tag must be hexadecimal, please try again.")

    def isHex(self, x):
        """ 
        Function that checks if a string is a hexadecimal

        Parameters:
            x (string): input to be checked.
        """
        if re.match("^(0[xX])?[a-fA-F0-9]+$", x):
            return True
        return False

    def isInt(self, x):
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

    def verifyAnchorCoordinates(self, coordinates):
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


class Anchor():
    def __init__(self,id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z


if __name__ == "__main__":
    setup = Setup()
    setup.promptAmountOfPlayers()
    setup.promptPlayerTags()
    setup.promptAnchors()
    setup.promptBallTag()
