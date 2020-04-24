from package_formatter import PackageFormatter


def test_formatPosition_maxvalue():
    formatter = PackageFormatter()
    package = formatter.format_position(65535, 65535, 255, 255, 255)
    assert package == b'0xffffffffffffff'


def test_formatPosition_minvalue():
    formatter = PackageFormatter()
    package = formatter.format_position(0, 0, 0, 0, 0)
    assert package == b'0x0'


def test_formatPosition_posY_zero():
    formatter = PackageFormatter()
    package = formatter.format_position(0, 10000, 1, 1, 1)
    assert package == b'0x2710010101'


def test_formatPosition_posX_zero():
    formatter = PackageFormatter()
    package = formatter.format_position(10000, 0, 1, 1, 1)
    assert package == b'0x27100000010101'


def test_formatPosition_id_zero():
    formatter = PackageFormatter()
    package = formatter.format_position(10000, 10000, 0, 1, 1)
    assert package == b'0x27102710000101'


def test_formatPosition_timestamp_zero():
    formatter = PackageFormatter()
    package = formatter.format_position(10000, 10000, 1, 0, 1)
    assert package == b'0x27102710010001'


def test_formatPosition_packageType_zero():
    formatter = PackageFormatter()
    package = formatter.format_position(10000, 10000, 1, 1, 0)
    assert package == b'0x27102710010100'


def test_formatAnchorPoisition_sets_correct_packageId():
    formatter = PackageFormatter()
    package = formatter.format_anchor_position(1, 10000, 10000)
    assert package == b'140x271027100101'


def test_formatPlayerPosition_sets_correct_packageId():
    formatter = PackageFormatter()
    package = formatter.format_player_position(1, 1, 10000, 10000)
    assert package == b'0x27102710010100'


def test_formatGoalPosition_sets_correct_packageId():
    formatter = PackageFormatter()
    package = formatter.format_goal_position(1, 10000, 10000)
    assert package == b'140x271027100105'


def test_formatGoalScored_sets_correct_packageId():
    formatter = PackageFormatter()
    package = formatter.format_goal_scored(100, 100)
    assert package == b'080x646404'
