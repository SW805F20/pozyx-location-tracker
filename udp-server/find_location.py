
# !/usr/bin/env python
"""
The Pozyx ready to localize tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch:
https://www.pozyx.io/Documentation/Tutorials/ready_to_localize/Python

This tutorial requires at least the contents of the Pozyx Ready to
Localize kit. It demonstrates the positioning capabilities
of the Pozyx device both locally and remotely. Follow the steps to
correctly set up your environment in the link, change the
parameters and upload this sketch. Watch the coordinates change as
you move your device around!

"""
from time import sleep

from pypozyx import (PozyxConstants, Coordinates, POZYX_SUCCESS,
                     PozyxRegisters, version,
                     DeviceCoordinates, PozyxSerial,
                     get_first_pozyx_serial_port, SingleRegister)
from pythonosc.udp_client import SimpleUDPClient

from pypozyx.tools.version_check import perform_latest_version_check

from pypozyx.structures.device import Coordinates, DeviceCoordinates

from datetime import datetime


class MultitagPositioning(object):
    """Continuously performs multitag positioning"""

    def __init__(self, tag_ids, anchors):
        """Initializes posyz and adds tags and to the instance of the class"""
        self.tag_ids = tag_ids
        self.algorithm = PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY
        self.dimension = PozyxConstants.DIMENSION_3D
        self.height = 1000
        serial_port = get_first_pozyx_serial_port()
        if serial_port is None:
            print("No Pozyx connected. Check your USB cable or your driver!")
            quit()
        device_anchors = []

        for anchor in anchors:
            device_anchors.append(DeviceCoordinates(anchor.id), 0, Coordinates(anchor.x, anchor.y, anchor.z))
        
        self.anchors = device_anchors
        self.pozyx = PozyxSerial(serial_port)
        self.setup()

    def getPosition(self, tag_id):
        """
        Gets the position of a tag
        Parameters:
            tag_id (string): hexadecimal id of the tag.
        """
        position = Coordinates()
        status = self.pozyx.doPositioning(position, self.dimension, self.height, self.algorithm, tag_id)
        return position
        

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX MULTITAG POSITIONING V{} -------------".format(version))
        print("")
        print(" - System will manually calibrate the tags")
        print("")
        print(" - System will then auto start positioning")
        print("")
        if None in self.tag_ids:
            for device_id in self.tag_ids:
                self.pozyx.printDeviceInfo(device_id)
        else:
            for device_id in [None] + self.tag_ids:
                self.pozyx.printDeviceInfo(device_id)
        print("")
        print("------------POZYX MULTITAG POSITIONING V{} -------------".format(version))
        print("")

        self.set_anchors_manual(save_to_flash=False)

        self.print_publish_anchor_configuration()

    def loop(self):
        """Performs positioning and prints the results."""
        for tag_id in self.tag_ids:
            position = Coordinates()
            status = self.pozyx.doPositioning(
                position, self.dimension, self.height, self.algorithm, remote_id=tag_id)
            if status == POZYX_SUCCESS:
                self.print_publish_position(position, tag_id)
            else:
                self.print_publish_error_code("positioning", tag_id)

    def print_publish_position(self, position, network_id):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        if network_id is None:
            network_id = 0
        pozyx_location = "POS ID: {}, x(mm): {}, y(mm): {}, z(mm): {}, TimeStamp: {}".format("0x%0.4x" % network_id,
                                                                                            position.x, position.y, position.z, datetime.now().strftime("%H:%M:%S.%f"))
        print(pozyx_location)
        filename = str(network_id) + "data.txt"
        file = open(filename, "a")
        pozyx_location += "\n"
        file.write(pozyx_location)
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, position.x, position.y, position.z])

    def set_anchors_manual(self, save_to_flash=False):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for tag_id in self.tag_ids:
            status = self.pozyx.clearDevices(tag_id)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, tag_id)
            if len(self.anchors) > 3:
                status &= self.pozyx.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO, len(self.anchors),
                                                           remote_id=tag_id)
            # enable these if you want to save the configuration to the devices.
            if save_to_flash:
                self.pozyx.saveAnchorIds(tag_id)
                self.pozyx.saveRegisters(
                    [PozyxRegisters.POSITIONING_NUMBER_OF_ANCHORS], tag_id)

            self.print_publish_configuration_result(status, tag_id)

    def print_publish_configuration_result(self, status, tag_id):
        """Prints the configuration explicit result, prints and publishes error if one occurs"""
        if tag_id is None:
            tag_id = 0
        if status == POZYX_SUCCESS:
            print("Configuration of tag %s: success" % tag_id)
        else:
            self.print_publish_error_code("configuration", tag_id)

    def print_publish_error_code(self, operation, network_id):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        # is succes if it finds an errorcode
        status = self.pozyx.getErrorCode(error_code, network_id)
        if network_id is None:
            network_id = 0
        if status == POZYX_SUCCESS:
            print("Error %s on ID %s, %s" %
                  (operation, "0x%0.4x" % network_id, self.pozyx.getErrorMessage(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/error_%s" % operation, [network_id, error_code[0]])
        else:
            # should only happen when not being able to communicate with a remote Pozyx.
            self.pozyx.getErrorCode(error_code)
            print("Error % s, local error code %s" %
                  (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/error_%s" % operation, [0, error_code[0]])

    def print_publish_anchor_configuration(self):
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.pos)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [anchor.network_id, anchor.pos.x, anchor.pos.y, anchor.pos.z])
                sleep(0.025)


class PozyxStarter:
    """Class to set important values as well as setup and start the pozyx data gathering"""
    mtp = None
    # IDs of the tags to position, add None to position the local tag as well. There is no None because we are connected to a Anchor
    tag_ids = [0x690f, 0x6763, 0x602e, 0x6979, 0x6915]

    # necessary data for calibration
    anchors = [DeviceCoordinates(0x676e, 1, Coordinates(0, 0, 2100)),
               DeviceCoordinates(0x676c, 1, Coordinates(2400, 0, 1900)),
               DeviceCoordinates(0x6738, 1, Coordinates(2400, 2400, 2100)),
               DeviceCoordinates(0x6e2b, 1, Coordinates(0, 2400, 1900))]

    def setup(self):
        # Check for the latest PyPozyx version. Skip if this takes too long or is not needed by setting to False.
        check_pypozyx_version = True
        if check_pypozyx_version:
            perform_latest_version_check()

        # shortcut to not have to find out the port yourself.
        serial_port = get_first_pozyx_serial_port()
        if serial_port is None:
            print("No Pozyx connected. Check your USB cable or your driver!")
            quit()

        # enable to send position data through OSC
        use_processing = True

        # configure if you want to route OSC to outside your localhost. Networking knowledge is required.
        ip = "127.0.0.1"
        network_port = 8888
        # positioning algorithm to use, other is PozyxConstants.POSITIONING_ALGORITHM_TRACKING
        algorithm = PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY
        # positioning dimension. Others are PozyxConstants.DIMENSION_2D, PozyxConstants.DIMENSION_2_5D
        dimension = PozyxConstants.DIMENSION_3D
        # height of device, required in 2.5D positioning
        height = 1000

        osc_udp_client = None
        if use_processing:
            osc_udp_client = SimpleUDPClient(ip, network_port)

        pozyx = PozyxSerial(serial_port)

        self.mtp = MultitagPositioning(pozyx, osc_udp_client, self.tag_ids, self.anchors,
                                       algorithm, dimension, height)
        self.mtp.setup()

    def Start(self):
        while True:
            self.mtp.loop()


if __name__ == "__main__":
    ps = PozyxStarter()
    ps.setup()
    ps.Start()