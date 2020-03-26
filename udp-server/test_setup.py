from setup import Setup, Anchor


# is_int tests
def test_is_int_int_input():
    setup = Setup()
    result = setup.is_int("5")
    assert result is True

def test_is_int_negative_int_input():
    setup = Setup()
    result = setup.is_int("-5")
    assert result is True


def test_is_int_string_input():
    setup = Setup()
    result = setup.is_int("string")
    assert result is False


def test_is_int_float_input():
    setup = Setup()
    result = setup.is_int("1.43")
    assert result is False


# is_hex tests
def test_is_hex_correct_hex_input():
    setup = Setup()
    result = setup.is_hex("0x23af")
    assert result is True


def test_is_hex_wrong_hex_input_1():
    setup = Setup()
    result = setup.is_hex("0x67mn")
    assert result is False


def test_is_hex_wrong_hex_input_2():
    setup = Setup()
    result = setup.is_hex("0x0X0x23af")
    assert result is False


def test_is_hex_string_input():
    setup = Setup()
    result = setup.is_hex("not a hexadecimal")
    assert result is False


def test_is_hex_int_input():
    setup = Setup()
    result = setup.is_hex("45")
    assert result is True


def test_is_hex_float_input():
    setup = Setup()
    result = setup.is_hex("0.45")
    assert result is False


# verify_anchor_coordinates Tests
# This method takes a list of strings made from the split of the standard input string
def test_verify_anchor_coordinates_correct_coordinates():
    setup = Setup()
    coordinates = ["500", "0", "300"]
    result = setup.verify_anchor_coordinates(coordinates)
    assert result is True


def test_verify_anchor_coordinates_wrong_string_coordinates():
    setup = Setup()
    coordinates = ["string", "string", "string"]
    result = setup.verify_anchor_coordinates(coordinates)
    assert result is False


def test_verify_anchor_coordinates_wrong_float_coordinates():
    setup = Setup()
    coordinates = ["2.3", "1.534", "0.00"]
    result = setup.verify_anchor_coordinates(coordinates)
    assert result is False


def test_verify_anchor_coordinates_wrong_large_coordinates():
    setup = Setup()
    coordinates = ["1000000000", "4", "-20000"]
    result = setup.verify_anchor_coordinates(coordinates)
    assert result is False


def test_verify_anchor_coordinates_too_few_coordinates():
    setup = Setup()
    coordinates = ["5", "0"]
    result = setup.verify_anchor_coordinates(coordinates)
    assert result is False


def test_verify_anchor_coordinates_too_many_coordinates():
    setup = Setup()
    coordinates = ["5", "0", "10", "8"]
    result = setup.verify_anchor_coordinates(coordinates)
    assert result is False


# Prompt anchors Tests
def test_verify_anchors_being_corrected():
    setup = Setup()
    anchor0 = Anchor("0", "0", "0", "200")
    anchor1 = Anchor("1", "0", "10", "200")
    anchor2 = Anchor("2", "10", "10", "200")
    anchor3 = Anchor("3", "10", "0", "200")
    anchors = [anchor0, anchor2, anchor1, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_being_corrected_2():
    setup = Setup()
    anchor0 = Anchor("0", "0", "0", "200")
    anchor1 = Anchor("1", "0", "10", "200")
    anchor2 = Anchor("2", "10", "10", "200")
    anchor3 = Anchor("3", "10", "0", "200")
    anchors = [anchor0, anchor3, anchor1, anchor2]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_being_corrected_3():
    setup = Setup()
    anchor0 = Anchor("0", "0", "0", "200")
    anchor1 = Anchor("1", "0", "10", "200")
    anchor2 = Anchor("2", "10", "10", "200")
    anchor3 = Anchor("3", "10", "0", "200")
    anchors = [anchor3, anchor2, anchor1, anchor0]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_dont_change_if_correct():
    setup = Setup()
    anchor0 = Anchor("0", "0", "0", "200")
    anchor1 = Anchor("1", "0", "10", "200")
    anchor2 = Anchor("2", "10", "10", "200")
    anchor3 = Anchor("3", "10", "0", "200")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3


def test_verify_anchors_dont_care_about_z_coordinates():
    setup = Setup()
    anchor0 = Anchor("0", "0", "0", "15")
    anchor1 = Anchor("1", "0", "10", "10")
    anchor2 = Anchor("2", "10", "10", "900")
    anchor3 = Anchor("3", "10", "0", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_trapezoid():
    setup = Setup()
    anchor0 = Anchor("0", "0", "0", "15")
    anchor1 = Anchor("1", "0", "10", "10")
    anchor2 = Anchor("2", "5", "4", "900")
    anchor3 = Anchor("3", "10", "10", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor3
    assert result[3] == anchor2

def test_verify_anchors_trapezoid():
    setup = Setup()
    anchor0 = Anchor("0", "0", "0", "15")
    anchor1 = Anchor("1", "0", "10", "10")
    anchor2 = Anchor("2", "10", "0", "900")
    anchor3 = Anchor("3", "10", "-5", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_trapezoid_2():
    setup = Setup()
    anchor0 = Anchor("0", "0", "0", "15")
    anchor1 = Anchor("1", "0", "10", "10")
    anchor2 = Anchor("2", "10", "0", "900")
    anchor3 = Anchor("3", "10", "-50", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3

def test_verify_anchors_trapezoid_2():
    setup = Setup()
    anchor0 = Anchor("0", "0", "0", "15")
    anchor1 = Anchor("1", "0", "10", "10")
    anchor2 = Anchor("2", "10", "0", "900")
    anchor3 = Anchor("3", "10", "-2", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3


def test_verify_anchors_trapezoid_3():
    setup = Setup()
    anchor0 = Anchor("0", "0", "0", "15")
    anchor1 = Anchor("1", "0", "10", "10")
    anchor2 = Anchor("2", "10", "20", "900")
    anchor3 = Anchor("3", "10", "0", "3")
    anchors = [anchor0, anchor1, anchor2, anchor3]
    setup.anchors = anchors
    result = setup.sort_anchors()
    assert result[0] == anchor0
    assert result[1] == anchor1
    assert result[2] == anchor2
    assert result[3] == anchor3