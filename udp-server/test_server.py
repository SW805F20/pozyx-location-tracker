from server import Server
from setup import Setup
from setup import Setup
from socket_multicast_sender import SocketMulticastSender
from package_formatter import PackageFormatter
from mock_find_location import MockMultiTagPositioning
from mock import patch, Mock

class TestServer(Server):
	def __init__(self):
		self.setup = Setup()
		self.setup.ballTag = '0x0'
		self.setup.playerTags=['0x1', '0x2', '0x3', '0x4']
		self.multicastSender = TestMulticastSender()
		self.multiTagPositioning = MockMultiTagPositioning([self.setup.ballTag] + self.setup.playerTags)
		self.formatter = TestFormatter()
		self.timeStamp = 0

class TestFormatter():
	def formatPlayerPosition(self, *arv):
		return CoordinateMock()

class TestMulticastSender():
	def send(self, message):
		return
class CoordinateMock():
	def __init__(self):
		self.x = 100
		self.y = 100

@patch('mock_find_location.MockMultiTagPositioning.getPosition')
def test_updateBallPosition_getPosition_called(getPosition_mock):
	coordinates = CoordinateMock()
	getPosition_mock.return_value = coordinates
	server = TestServer()
	server.updateBallPosition()
	assert	server.multiTagPositioning.getPosition.assert_called_with('0x0')
