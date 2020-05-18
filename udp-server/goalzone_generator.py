from __future__ import division
import random


class GoalzoneGenerator:
    GOAL_LENGTH_PERCENTAGE_LIMIT = 30
    # When accumulating sequential goals this constant defines the length of the required sequence.
    ACCUMULATED_GOALS_NEEDED = 4

    def __init__(self, anchor_list, goal_length_percentage):
        """ 
        Constructor function for the goalzone generator
  
        Parameters: 
            anchor_list ([Anchor]): List of anchor objects
            goal_length_percentage (int): The percentage size
            of the edges of a goal. The percentage is based on the shortest edge.
        """
        self.anchor_list = anchor_list

        # Sets the goal length percentage
        self.set_goal_length_percentage(goal_length_percentage)
        
        # The x and y values of the anchors
        self.xs, self.ys = self.get_size_arrays()

        # The max and min x and y values of the anchors
        self.max_x = max(self.xs)
        self.min_x = min(self.xs)
        self.max_y = max(self.ys)
        self.min_y = min(self.ys)
        self.center_of_field = ((self.max_x + self.min_x) / 2, (self.max_y + self.min_y) / 2)

        # The difference between the largest and smallest x and y values
        self.x_difference = self.max_x - self.min_x
        self.y_difference = self.max_y - self.min_y

        # True if the field shape is vertical
        self.is_vertical = None

        # The length of the goal zone's edges
        self.goal_zone_edge_length = None

        # The distance between the center and an edge in a goal zone.
        self.goal_zone_middle_offset = None

        self.get_field_shape()
        self.calculate_goalzone_size()
        
        # Gets the initial goal zones
        self.center_of_blue_goal, self.center_of_red_goal = self.calculate_initial_goal_centers()

        # To avoid outliers several goals should be counted in a sequence. These are the accumulators for this.
        self.accumulated_goals_red = 0
        self.accumulated_goals_blue = 0


    def set_goal_length_percentage(self, goal_length_percentage):
        """ 
        Sets the goal length percentage value
        
        Parameters: 
            goal_length_percentage (int): # The difference between the largest and smallest x and y values
        """
        if 0 < goal_length_percentage < self.GOAL_LENGTH_PERCENTAGE_LIMIT:
            self.goal_length_percentage = goal_length_percentage
        else:
            raise ValueError("Not a valid goal length percentage")

    def calculate_initial_goal_centers(self):
        """ 
        Calculates the initial set of goalzones returning the two center coordinates
        """
        if self.is_vertical:
            center_of_blue_goal = (self.center_of_field[0], self.max_y - self.goal_zone_middle_offset)
            center_of_red_goal = (self.center_of_field[0], self.min_y + self.goal_zone_middle_offset)
            return center_of_blue_goal, center_of_red_goal
        else:
            center_of_blue_goal = (self.max_x - self.goal_zone_middle_offset, self.center_of_field[1])
            center_of_red_goal = (self.min_x + self.goal_zone_middle_offset, self.center_of_field[1])
            return center_of_blue_goal, center_of_red_goal

    def get_size_arrays(self):
        """ 
        Goes through the list of anchors and creates two lists with the x and y values
        """
        xs = []
        ys = []
        for anchor in self.anchor_list:
            xs.append(int(anchor.x))
            ys.append(int(anchor.y))
        return xs, ys

    def get_field_shape(self):
        """ 
        Gets the shape of the field
        """
        if self.x_difference < self.y_difference:
            self.is_vertical = True
        else:
            self.is_vertical = False

    def calculate_goalzone_size(self):
        """ 
        Calculates the size of the goalzones' edges
        """
        if self.is_vertical:
            self.goal_zone_edge_length = (self.goal_length_percentage / 100.0) * self.x_difference
        else:
            self.goal_zone_edge_length = (self.goal_length_percentage / 100.0) * self.y_difference

        self.goal_zone_middle_offset = self.goal_zone_edge_length / 2.0

    def generate_random_goalzones(self):
        """ 
        Generates new random goalzones for each team
        """
        random_y = 0.0
        random_x = 0.0

        if self.is_vertical:
            # For vertical field - if blue center is > than field center it means blue is on top. Random ranges are defined to ensure it swaps sides.
            if self.center_of_blue_goal[1] > self.center_of_field[1]:
                # Goal zone middle offset ensures the goal does not have anchors that cross the middle, goal zone edge length ensures goals spawn a bit away from the middle line, and not on top of it.
                random_x = random.uniform(self.min_x + self.goal_zone_middle_offset, self.max_x - self.goal_zone_middle_offset)
                random_y = random.uniform(self.center_of_field[1] + self.goal_zone_middle_offset + self.goal_zone_edge_length, 
                                            self.max_y - self.goal_zone_middle_offset)            
            else:
                random_x = random.uniform(self.min_x + self.goal_zone_middle_offset, self.max_x - self.goal_zone_middle_offset)
                random_y = random.uniform(self.min_y + self.goal_zone_middle_offset, 
                                            self.center_of_field[1] - self.goal_zone_middle_offset - self.goal_zone_edge_length)
        else:
            # For horizontal field - if blue center is > x then blue is on the right
            if self.center_of_blue_goal[0] > self.center_of_field[0]:
                random_x = random.uniform(self.center_of_field[0] + self.goal_zone_middle_offset + self.goal_zone_edge_length, 
                                            self.max_x - self.goal_zone_middle_offset)
                random_y = random.uniform(self.min_y + self.goal_zone_middle_offset, self.max_y - self.goal_zone_middle_offset)
            else:
                random_x = random.uniform(self.min_x + self.goal_zone_middle_offset, 
                                            self.center_of_field[0] - self.goal_zone_middle_offset - self.goal_zone_edge_length)
                random_y = random.uniform(self.min_y + self.goal_zone_middle_offset, self.max_y - self.goal_zone_middle_offset)

        self.center_of_blue_goal = (random_x, random_y)
        self.center_of_red_goal = (self.max_x + self.min_x - random_x, self.max_y + self.min_y - random_y)

    def goal_scored_red(self, ball_position):
        """
        Returns true if red team has scored
        
        Parameters: 
            ball_position ((int, int)): tuple with the x and y coordinate of the ball.
        """
        # check x position for blue goal
        if (self.center_of_blue_goal[0] - self.goal_zone_middle_offset) < ball_position[0] < (self.center_of_blue_goal[0] + self.goal_zone_middle_offset):
            # check y position for blue goal
            if (self.center_of_blue_goal[1] - self.goal_zone_middle_offset) < ball_position[1] < (self.center_of_blue_goal[1] + self.goal_zone_middle_offset):
                return True

        return False

    def goal_scored_blue(self, ball_position):
        """
            Returns true if blue team has scored

            Parameters:
                ball_position ((int, int)): tuple with the x and y coordinate of the ball.
            """
        # check x position for red goal
        if (self.center_of_red_goal[0] - self.goal_zone_middle_offset) < ball_position[0] < (self.center_of_red_goal[0] + self.goal_zone_middle_offset):
            # check y position for red goal
            if (self.center_of_red_goal[1] - self.goal_zone_middle_offset) < ball_position[1] < (self.center_of_red_goal[1] + self.goal_zone_middle_offset):
                return True

        return False

    def accumulate_goals_scored_red(self, ball_position):
        """
        Checks if red team has scored and accumulates a counter.
        Returns true if the team has scored several times in a row, to prevent an outlier point from being counted.

        Parameters:
            ball_position ((int, int)): tuple with the x and y coordinate of the ball.
        """
        if self.goal_scored_red(ball_position):
            if self.goal_accumulator("red"):
                return True
        else:
            if self.accumulated_goals_red != 0:
                self.accumulated_goals_red = 0

        return False

    def accumulate_goals_scored_blue(self, ball_position):
        """
        Checks if blue team has scored and accumulates a counter.
        Returns true if the team has scored several times in a row, to prevent an outlier point from being counted.

        Parameters:
            ball_position ((int, int)): tuple with the x and y coordinate of the ball.
        """
        if self.goal_scored_blue(ball_position):
            if self.goal_accumulator("blue"):
                return True
        else:
            if self.accumulated_goals_blue != 0:
                self.accumulated_goals_blue = 0

        return False

    def goal_accumulator(self, team_color):
        if team_color == "red":
            self.accumulated_goals_red += 1
            if self.accumulated_goals_red == self.ACCUMULATED_GOALS_NEEDED:
                self.accumulated_goals_red = 0
                return True
        else:
            if team_color == "blue":
                self.accumulated_goals_blue += 1
                if self.accumulated_goals_blue == self.ACCUMULATED_GOALS_NEEDED:
                    self.accumulated_goals_blue = 0
                    return True

        return False
