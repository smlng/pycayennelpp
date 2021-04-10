import pytest

from cayennelpp.lpp_type import LppType


@pytest.fixture
def acc():
    return LppType.get_lpp_type(113)


def test_accelerometer(acc):
    val = (12.345, -12.345, 0.0)
    accel_buf = acc.encode(val)
    assert acc.decode(accel_buf) == val
    val = (-12.345, 0.0, -12.345)
    accel_buf = acc.encode(val)
    assert acc.decode(accel_buf) == val


def test_accelerometer_invalid_buf(acc):
    with pytest.raises(Exception):
        acc.decode(bytearray([0x00]))


def test_accelerometer_invalid_val_type(acc):
    with pytest.raises(Exception):
        acc.encode([0x00])


def test_accelerometer_invalid_val(acc):
    with pytest.raises(Exception):
        acc.encode((0, 0))
