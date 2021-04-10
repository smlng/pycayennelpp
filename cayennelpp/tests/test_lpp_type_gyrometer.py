import pytest

from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_type import LppType


@pytest.fixture
def gyro():
    return LppType.get_lpp_type(134)


def test_gyrometer(gyro):
    val = (123.45, -123.45, 0.0)
    gyro_buf = gyro.encode(val)
    assert gyro.decode(gyro_buf) == val
    val = (-123.45, 0.0, -123.45)
    gyro_buf = gyro.encode(val)
    assert gyro.decode(gyro_buf) == val


def test_gyrometer_invalid_buf(gyro):
    with pytest.raises(Exception):
        gyro.decode(bytearray([0x00]))


def test_gyrometer_invalid_val_type(gyro):
    with pytest.raises(Exception):
        gyro.encode([0x00])


def test_gyrometer_invalid_val(gyro):
    with pytest.raises(Exception):
        gyro.encode((0, 0))

