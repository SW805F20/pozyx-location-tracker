
from pypozyx import (PozyxConstants, Coordinates, POZYX_SUCCESS, PozyxRegisters, version,
                     DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister)

from pypozyx.tools.version_check import perform_latest_version_check


class MultitagPositioning(object):

    """Continuously performs multitag positioning"""
    def __init__(self, tag_ids, anchors):
        ANCHOR_TYPEID = 1
        perform_latest_version_check()
        self.tag_ids = tag_ids
        self.pozyx = PozyxSerial(get_first_pozyx_serial_port())
        self.anchors = []
        for anchor in anchors:
            self.anchors.append(DeviceCoordinates(anchor.id, ANCHOR_TYPEID, Coordinates(anchor.x, anchor.y, anchor.z)))
        self.algorithm = PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY
        self.dimension = PozyxConstants.DIMENSION_2D
        self.height = 1000
        self.setup()

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

        self.setAnchorsManual(save_to_flash=False)

        self.printPublishAnchorConfiguration()

    def get_position(self, tag_id):
        """Performs positioning and prints the results."""
        print(tag_id)
        position = Coordinates()
        status = self.pozyx.doPositioning(
            position, self.dimension, self.height, self.algorithm, remote_id=tag_id)
        if status == POZYX_SUCCESS:
            self.printPublishPosition(position, tag_id)
            return position
        else:
            self.printPublishErrorCode("positioning", tag_id)

    def printPublishPosition(self, position, network_id):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        if network_id is None:
            network_id = 0
        s = "POS ID: {}, x(mm): {}, y(mm): {}, z(mm): {}".format("0x%0.4x" % network_id,
                                                                 position.x, position.y, position.z)
        print(s)

    def setAnchorsManual(self, save_to_flash=False):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for tag_id in self.tag_ids:
            status = self.pozyx.clearDevices(tag_id)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, tag_id)
            if len(self.anchors) > 4:
                status &= self.pozyx.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO, len(self.anchors),
                                                           remote_id=tag_id)
            # enable these if you want to save the configuration to the devices.
            if save_to_flash:
                self.pozyx.saveAnchorIds(tag_id)
                self.pozyx.saveRegisters([PozyxRegisters.POSITIONING_NUMBER_OF_ANCHORS], tag_id)

            self.printPublishConfigurationResult(status, tag_id)

    def printPublishConfigurationResult(self, status, tag_id):
        """Prints the configuration explicit result, prints and publishes error if one occurs"""
        if tag_id is None:
            tag_id = 0
        if status == POZYX_SUCCESS:
            print("Configuration of tag %s: success" % tag_id)
        else:
            self.printPublishErrorCode("configuration", tag_id)

    def printPublishErrorCode(self, operation, network_id):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        status = self.pozyx.getErrorCode(error_code, network_id)
        if network_id is None:
            network_id = 0
        if status == POZYX_SUCCESS:
            print("Error %s on ID %s, %s" %
                  (operation, "0x%0.4x" % network_id, self.pozyx.getErrorMessage(error_code)))

        else:
            # should only happen when not being able to communicate with a remote Pozyx.
            self.pozyx.getErrorCode(error_code)
            print("Error % s, local error code %s" % (operation, str(error_code)))

    def printPublishAnchorConfiguration(self):
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.pos)))


class Anchor:
    def __init__(self, anchor_id, x, y, z):
        self.id = anchor_id
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)


if __name__ == "__main__":
    # Check for the latest PyPozyx version. Skip if this takes too long or is not needed by setting to False.

    # IDs of the tags to position, add None to position the local tag as well.
    tag_ids = [0x6915, 0x6763, 0x690f]

    # necessary data for calibration
    anchors = []
    anchors.append(Anchor(0x6738, 0, 0, 1480))
    anchors.append(Anchor(0x676e, 0, 2900, 1760))
    anchors.append(Anchor(0x6e2b, 2500, 2900, 1750))
    anchors.append(Anchor(0x676c, 2900, 0, 1530))

    r = MultitagPositioning(tag_ids, anchors)
    while True:
        for tag in tag_ids:
            r.get_position(tag)



