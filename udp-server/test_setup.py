from setup import Setup, Anchor


# isInt tests
class SetupTest(Setup):
	def __init__(self):
		pass

def test_isInt_int_input():
    setup = Setup()
    result = setup.isInt("5")
    assert result is True

def test_isInt_negative_int_input():
    setup = SetupTest()
    result = setup.isInt("-5")
    assert result is True


def test_isInt_string_input():
    setup = SetupTest()
    result = setup.isInt("string")
    assert result is False


def test_isInt_float_input():
    setup = SetupTest()
    result = setup.isInt("1.43")
    assert result is False


# isHex tests
def test_isHex_correct_hex_input():
    setup = SetupTest()
    result = setup.isHex("0x23af")
    assert result is True


def test_isHex_wrong_hex_input_1():
    setup = SetupTest()
    result = setup.isHex("0x67mn")
    assert result is False


def test_isHex_wrong_hex_input_2():
    setup = SetupTest()
    result = setup.isHex("0x0X0x23af")
    assert result is False


def test_isHex_string_input():
    setup = SetupTest()
    result = setup.isHex("not a hexadecimal")
    assert result is False


def test_isHex_int_input():
    setup = SetupTest()
    result = setup.isHex("45")
    assert result is True


def test_isHex_float_input():
    setup = SetupTest()
    result = setup.isHex("0.45")
    assert result is False


# verifyAnchorCoordinates Tests
# This method takes a list of strings made from the split of the standard input string
def test_verifyAnchorCoordinates_correct_coordinates():
    setup = SetupTest()
    coordinates = ["500", "0", "300"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result is True


def test_verifyAnchorCoordinates_wrong_string_coordinates():
    setup = SetupTest()
    coordinates = ["string", "string", "string"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result is False


def test_verifyAnchorCoordinates_wrong_float_coordinates():
    setup = SetupTest()
    coordinates = ["2.3", "1.534", "0.00"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result is False


def test_verifyAnchorCoordinates_wrong_large_coordinates():
    setup = SetupTest()
    coordinates = ["1000000000", "4", "-20000"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result is False


def test_verifyAnchorCoordinates_too_few_coordinates():
    setup = SetupTest()
    coordinates = ["5", "0"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result is False


def test_verifyAnchorCoordinates_too_many_coordinates():
    setup = SetupTest()
    coordinates = ["5", "0", "10", "8"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result is False


# Prompt anchors Tests
def test_verify_anchors_being_corrected():
    setup = Setup()
    anchor0 = Anchor("0", "0", "200")
    anchor1 = Anchor("0", "10", "200")
    anchor2 = Anchor("10", "10", "200")
    anchor3 = Anchor("10", "0", "200")
    anchors = [anchor0, anchor2, anchor1, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_being_corrected_2():
    setup = Setup()
    anchor0 = Anchor("0", "0", "200")
    anchor1 = Anchor("0", "10", "200")
    anchor2 = Anchor("10", "10", "200")
    anchor3 = Anchor("10", "0", "200")
    anchors = [anchor0, anchor3, anchor1, anchor2]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_being_corrected_3():
    setup = Setup()
    anchor0 = Anchor("0", "0", "200")
    anchor1 = Anchor("0", "10", "200")
    anchor2 = Anchor("10", "10", "200")
    anchor3 = Anchor("10", "0", "200")
    anchors = [anchor3, anchor2, anchor1, anchor0]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_dont_change_if_correct():
    setup = Setup()
    anchor0 = Anchor("0", "0", "200")
    anchor1 = Anchor("0", "10", "200")
    anchor2 = Anchor("10", "10", "200")
    anchor3 = Anchor("10", "0", "200")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3


def test_verify_anchors_dont_care_about_z_coordinates():
    setup = Setup()
    anchor0 = Anchor("0", "0", "15")
    anchor1 = Anchor("0", "10", "10")
    anchor2 = Anchor("10", "10", "900")
    anchor3 = Anchor("10", "0", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_trapezoid():
    setup = Setup()
    anchor0 = Anchor("0", "0", "15")
    anchor1 = Anchor("0", "10", "10")
    anchor2 = Anchor("5", "4", "900")
    anchor3 = Anchor("10", "10", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor3
    assert result[3] == anchor2

def test_verify_anchors_trapezoid():
    setup = Setup()
    anchor0 = Anchor("0", "0", "15")
    anchor1 = Anchor("0", "10", "10")
    anchor2 = Anchor("10", "0", "900")
    anchor3 = Anchor("10", "-5", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_trapezoid_2():
    setup = Setup()
    anchor0 = Anchor("0", "0", "15")
    anchor1 = Anchor("0", "10", "10")
    anchor2 = Anchor("10", "0", "900")
    anchor3 = Anchor("10", "-50", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_trapezoid_2():
    setup = Setup()
    anchor0 = Anchor("0", "0", "15")
    anchor1 = Anchor("0", "10", "10")
    anchor2 = Anchor("10", "0", "900")
    anchor3 = Anchor("10", "-2", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3


def test_verify_anchors_trapezoid_3():
    setup = Setup()
    anchor0 = Anchor("0", "0", "15")
    anchor1 = Anchor("0", "10", "10")
    anchor2 = Anchor("10", "20", "900")
    anchor3 = Anchor("10", "0", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3
