from setup import Setup

# isInt tests
class SetupTest(Setup):
	def __init__(self):
		pass

def test_isInt_int_input():
	setup = SetupTest()
	result = setup.isInt("5")
	assert result == True

def test_isInt_negative_int_input():
    setup = SetupTest()
    result = setup.isInt("-5")
    assert result == True

def test_isInt_string_input():
    setup = SetupTest()
    result = setup.isInt("string")
    assert result == False

def test_isInt_float_input():
    setup = SetupTest()
    result = setup.isInt("1.43")
    assert result == False

# isHex tests
def test_isHex_correct_hex_input():
    setup = SetupTest()
    result = setup.isHex("0x23af")
    assert result == True

def test_isHex_wrong_hex_input_1():
    setup = SetupTest()
    result = setup.isHex("0x67mn")
    assert result == False

def test_isHex_wrong_hex_input_2():
    setup = SetupTest()
    result = setup.isHex("0x0X0x23af")
    assert result == False

def test_isHex_string_input():
    setup = SetupTest()
    result = setup.isHex("not a hexadecimal")
    assert result == False

def test_isHex_int_input():
    setup = SetupTest()
    result = setup.isHex("45")
    assert result == True

def test_isHex_float_input():
    setup = SetupTest()
    result = setup.isHex("0.45")
    assert result == False

# verifyAnchorCoordinates Tests
# This method takes a list of strings made from the split of the standard input string
def test_verifyAnchorCoordinates_correct_coordinates():
    setup = SetupTest()
    coordinates = ["500", "0", "300"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == True

def test_verifyAnchorCoordinates_wrong_string_coordinates():
    setup = SetupTest()
    coordinates = ["string", "string", "string"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == False

def test_verifyAnchorCoordinates_wrong_float_coordinates():
    setup = SetupTest()
    coordinates = ["2.3", "1.534", "0.00"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == False

def test_verifyAnchorCoordinates_wrong_large_coordinates():
    setup = SetupTest()
    coordinates = ["1000000000", "4", "-20000"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == False

def test_verifyAnchorCoordinates_too_few_coordinates():
    setup = SetupTest()
    coordinates = ["5", "0"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == False

def test_verifyAnchorCoordinates_too_many_coordinates():
    setup = SetupTest()
    coordinates = ["5", "0", "10", "8"]
    result = setup.verifyAnchorCoordinates(coordinates)
    assert result == False
