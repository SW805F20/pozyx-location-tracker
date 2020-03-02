from pypozyx import (PozyxConstants, Coordinates, POZYX_SUCCESS, PozyxRegisters, version,
                     DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister)
from pythonosc.udp_client import SimpleUDPClient

from pypozyx.tools.version_check import perform_latest_version_check

from pypozyx.structures.device import NetworkID, UWBSettings, DeviceList, Coordinates, RXInfo, DeviceCoordinates, FilterData, AlgorithmData


anchors = [DeviceCoordinates(0x676e, 1, Coordinates(0, 0, 2100)),
               DeviceCoordinates(0x676c, 1, Coordinates(2400, 0, 1900)),
               DeviceCoordinates(0x6738, 1, Coordinates(2400, 2400, 2100)),
               DeviceCoordinates(0x6e2b, 1, Coordinates(0, 2400, 1900))]

tag_ids = [0x690f, 0x6763, 0x602e, 0x6979, 0x6915]


