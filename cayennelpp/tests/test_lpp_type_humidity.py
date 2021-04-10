import pytest

from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_type import LppType


@pytest.fixture
def hum():
    return LppType.get_lpp_type(104)


def test_humidity(hum):
    val = (50.00,)
    hum_buf = hum.encode(val)
    assert hum.decode(hum_buf) == val
    hum_buf = hum.encode(50.25)
    assert hum.decode(hum_buf) == val
    val = (50.50,)
    hum_buf = hum.encode(val)
    assert hum.decode(hum_buf) == val
    hum_buf = hum.encode(50.75)
    assert hum.decode(hum_buf) == val


def test_humidity_negative_val(hum):
    with pytest.raises(Exception):
        val = (-50.50,)
        hum.encode(val)


def test_humidity_invalid_buf(hum):
    with pytest.raises(Exception):
        hum.decode(bytearray([0x00, 0x00]))


def test_humidity_invalid_val_type(hum):
    with pytest.raises(Exception):
        hum.encode([0x00])


def test_humidity_invalid_val(hum):
    with pytest.raises(Exception):
        hum.encode((0, 0))