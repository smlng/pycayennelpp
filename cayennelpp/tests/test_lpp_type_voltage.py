import pytest

from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_type import LppType


@pytest.fixture
def vol():
    return LppType.get_lpp_type(116)


def test_voltage(vol):
    val = (2,)
    vol_buf = vol.encode(val)
    assert vol.decode(vol_buf) == val


def test_voltage_invalid_buf(vol):
    with pytest.raises(Exception):
        vol.decode(bytearray([0x00]))


def test_voltage_invalid_val(vol):
    with pytest.raises(Exception):
        vol.encode((0, 1))


def test_voltage_negative_val(vol):
    with pytest.raises(Exception):
        vol.encode((-42,))