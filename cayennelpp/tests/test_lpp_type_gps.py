import pytest

from cayennelpp.lpp_type import LppType


@pytest.fixture
def gps():
    return LppType.get_lpp_type(136)


def test_gps(gps):
    val = (42.3519, -87.9094, 10.00)
    gps_buf = gps.encode(val)
    assert gps.decode(gps_buf) == val
    val = (-42.3519, 87.9094, -10.00)
    gps_buf = gps.encode(val)
    assert gps.decode(gps_buf) == val


def test_gps_invalid_buf(gps):
    with pytest.raises(Exception):
        gps.decode(bytearray([0x00]))


def test_gps_invalid_val_type(gps):
    with pytest.raises(Exception):
        gps.encode([0x00])


def test_gps_invalid_val(gps):
    with pytest.raises(Exception):
        gps.encode((0, 0))
