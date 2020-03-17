from setup import Setup

# isInt tests
def test_isInt_int_input():
    setup = Setup()
    result = setup.isInt("5")
    assert result == True

def test_isInt_negative_int_input():
    setup = Setup()
    result = setup.isInt("-5")
    assert result == True

def test_isInt_string_input():
    setup = Setup()
    result = setup.isInt("string")
    assert result == False

def test_isInt_float_input():
    setup = Setup()
    result = setup.isInt("1.43")
    assert result == False

# isHex tests
def test_isHex_correct_hex_input():
    setup = Setup()
    result = setup.isHex("0x23af")
    assert result == True

def test_isHex_wrong_hex_input_1():
    setup = Setup()
    result = setup.isHex("0x67mn")
    assert result == False

def test_isHex_wrong_hex_input_2():
    setup = Setup()
    result = setup.isHex("0x0X0x23af")
    assert result == False

def test_isHex_string_input():
    setup = Setup()
    result = setup.isHex("not a hexadecimal")
    assert result == False

def test_isHex_int_input():
    setup = Setup()
    result = setup.isHex("45")
    assert result == True

def test_isHex_float_input():
    setup = Setup()
    result = setup.isHex("0.45")
    assert result == False

# verifyAnchorCoordinates Tests
# This method takes a list of strings made from the split of the standard input string
def test_verifyAnchorCoordinates_correct_coordinates():
    setup = Setup()
    coordinates = ["500", "0", "300"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == True

def test_verifyAnchorCoordinates_wrong_string_coordinates():
    setup = Setup()
    coordinates = ["string", "string", "string"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == False

def test_verifyAnchorCoordinates_wrong_float_coordinates():
    setup = Setup()
    coordinates = ["2.3", "1.534", "0.00"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == False

def test_verifyAnchorCoordinates_wrong_large_coordinates():
    setup = Setup()
    coordinates = ["1000000000", "4", "-20000"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == False

def test_verifyAnchorCoordinates_too_few_coordinates():
    setup = Setup()
    coordinates = ["5", "0"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == False

def test_verifyAnchorCoordinates_too_many_coordinates():
    setup = Setup()
    coordinates = ["5", "0", "10", "8"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == False