import pytest

from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_type import LppType


@pytest.fixture
def temp():
    return LppType.get_lpp_type(103)


def test_temperature(temp):
    val = (32.1,)
    temp_buf = temp.encode(val)
    assert temp.decode(temp_buf) == val
    val = (-4.1,)
    temp_buf = temp.encode(val)
    assert temp.decode(temp_buf) == val


def test_temperature_invalid_buf(temp):
    with pytest.raises(Exception):
        temp.decode(bytearray([0x00]))


def test_temperature_invalid_val_type(temp):
    with pytest.raises(Exception):
        temp.encode([0x00])


def test_temperature_invalid_val(temp):
    with pytest.raises(Exception):
        temp.encode((0, 0))