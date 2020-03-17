import re

class Setup():
    amountOfPlayers = 0
    playerTags = []
    ballTag = ""
    anchors = []
    # Dependent on the unit of measurement used. This is assumed to be millimeters
    ANCHOR_COORDINATE_LIMIT = 100000

    def promptAmountOfPlayers(self):
        """
        Function that prompts the user for the amount of players in the game.
        """
        while True:
            amountOfPlayers = input("Amount of players? ")
            if self.isInt(amountOfPlayers):
                self.amountOfPlayers = amountOfPlayers
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
        for i in range(1,5):
            while True:
                string = input("Position of anchor {}: ".format(i))
                coordinates = string.split()
                if self.verifyAnchorCoordinates(coordinates):
                    break
                
            self.anchors.append(Anchor(coordinates[0], coordinates[1], coordinates[2]))

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
                    print("Anchor coordinate value must be less than {}".format(self.ANCHOR_COORDINATE_LIMIT))
                    return False
            except ValueError:
                print("Anchor coordinate value must be an integer, please try again.")
                return False
        
        return True

            

class Anchor():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


if __name__ == "__main__":
    setup = Setup()
    setup.promptAmountOfPlayers()
    setup.promptPlayerTags()
    setup.promptAnchors()
    setup.promptBallTag()
