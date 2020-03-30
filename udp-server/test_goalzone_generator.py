from goalzone_generator import GoalzoneGenerator
from setup import Anchor
import unittest

anchor_list = [Anchor(1, 0, 0, 0), Anchor(2, 20, 0, 0), Anchor(3, 20, 10, 0), Anchor(4, 0, 10, 0)]
goal_length_percentage = 20


class TestGoalGenerator(unittest.TestCase):
    def test_correct_center_of_field(self):
        goalzone_gen = GoalzoneGenerator(anchor_list, goal_length_percentage)
        assert goalzone_gen.center_of_field == (10, 5)

    def test_x_difference_is_correct(self):
        goalzone_gen = GoalzoneGenerator(anchor_list, goal_length_percentage)
        assert goalzone_gen.x_difference == 20

    def test_y_difference_is_correct(self):
        goalzone_gen = GoalzoneGenerator(anchor_list, goal_length_percentage)
        assert goalzone_gen.y_difference == 10

    def test_field_shape_is_horizontal(self):
        goalzone_gen = GoalzoneGenerator(anchor_list, goal_length_percentage)
        assert goalzone_gen.is_vertical is False

    def test_field_shape_is_vertical(self):
        vertical_anchor_list = [Anchor(1, 0, 0, 0), Anchor(2, 10, 0, 0), Anchor(3, 10, 20, 0), Anchor(4, 0, 20, 0)]
        goalzone_gen = GoalzoneGenerator(vertical_anchor_list, goal_length_percentage)
        assert goalzone_gen.is_vertical is True

    def test_goal_zone_middle_offset_is_correct(self):
        goalzone_gen = GoalzoneGenerator(anchor_list, goal_length_percentage)
        assert goalzone_gen.goal_zone_middle_offset == 1.0

    def test_wrong_goal_length_percentage_exception_raised(self):
        wrong_goal_length_percentage = -30
        with self.assertRaises(ValueError) as context:
            GoalzoneGenerator(anchor_list, wrong_goal_length_percentage)
        self.assertTrue("Not a valid goal length percentage", context.exception)

    def test_correct_goalzone_centers_calculated(self):
        goalzone_gen = GoalzoneGenerator(anchor_list, goal_length_percentage)
        assert goalzone_gen.center_of_blue_goal == (19, 5)
        assert goalzone_gen.center_of_red_goal == (1, 5)
    
    def test_goal_scored_should_return_true(self):
        goalzone_gen = GoalzoneGenerator(anchor_list, goal_length_percentage)
        ball_position = (19.5, 5.5)
        assert goalzone_gen.goal_scored(ball_position) is True

    def test_goal_scored_should_return_false(self):
        goalzone_gen = GoalzoneGenerator(anchor_list, goal_length_percentage)
        ball_position = (10, 10)
        assert goalzone_gen.goal_scored(ball_position) is False
