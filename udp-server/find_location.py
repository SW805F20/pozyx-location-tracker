
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
from pypozyx import (PozyxConstants,
                     PozyxRegisters, version, PozyxSerial,
                     get_first_pozyx_serial_port)
from pypozyx.structures.device import Coordinates, DeviceCoordinates

class MultitagPositioning(object):
    """Continuously performs multitag positioning"""

    def __init__(self, tag_ids, anchors):
        """
		Initializes pozyx and adds tags to the instance of the class
		Parameters:
			tag_ids (list): List containing the player tags and the ball tag
			anchors (list): List containing all of the anchors
		"""
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

    def get_position(self, tag_id):
        """
        Gets the position of a tag
        Parameters:
            tag_id (string): hexadecimal id of the tag.
        """
        position = Coordinates()
        status = self.pozyx.doPositioning(position, self.dimension, self.height, self.algorithm, tag_id)

        position.x = position.x / 10	# divided with 10 to convert it from mm to cm
        position.y = position.y / 10	# divided with 10 to convert it from mm to cm
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


    def set_anchors_manual(self, save_to_flash=False):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for tag_id in self.tag_ids:
            status = self.pozyx.clearDevices(tag_id)
            for anchor in self.anchors:
                # Convert to millimeters before adding to pozyx
                mm_device = DeviceCoordinates(anchor.network_id, 0,
                                              Coordinates(anchor.x * 10, anchor.y * 10, anchor.z * 10))
                status &= self.pozyx.addDevice(mm_device, tag_id)
            if len(self.anchors) > 3:
                status &= self.pozyx.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO, len(self.anchors),
                                                           remote_id=tag_id)
            # enable these if you want to save the configuration to the devices.
            if save_to_flash:
                self.pozyx.saveAnchorIds(tag_id)
                self.pozyx.saveRegisters(
                    [PozyxRegisters.POSITIONING_NUMBER_OF_ANCHORS], tag_id)
