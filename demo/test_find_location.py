
from find_location import PozyxStarter

from pypozyx import Coordinates

from pypozyx.structures.device import  DeviceCoordinates


_anchors = [DeviceCoordinates(0x676e, 1, Coordinates(0, 0, 2100)),
               DeviceCoordinates(0x676c, 1, Coordinates(2400, 0, 1900)),
               DeviceCoordinates(0x6738, 1, Coordinates(2400, 2400, 2100)),
               DeviceCoordinates(0x6e2b, 1, Coordinates(0, 2400, 1900))]

_tag_ids = [0x690f, 0x6763, 0x602e, 0x6979, 0x6915]

def test_tags():
    """Compares the ids of the tags, since we only have the 5 tags these should never change"""
    a = PozyxStarter()
    assert _tag_ids == a.tag_ids

def test_anchors():
    """Compares the ids of the anchors, since we only have the 4 anchors these should never change"""
    a = PozyxStarter()
    _anchor_ids = []
    for id in _anchors:
        _anchor_ids.append(id)

    class_anchor_ids = []
    for id in a.anchors:
        class_anchor_ids.append(id)
    assert _anchor_ids == class_anchor_ids


