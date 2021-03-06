import pytest

from cayennelpp.lpp_type import LppType


@pytest.fixture
def lum():
    return LppType.get_lpp_type(101)


def test_illuminance(lum):
    val = (0,)
    lum_buf = lum.encode(val)
    assert lum.decode(lum_buf) == val
    val = (12345,)
    lum_buf = lum.encode(val)
    assert lum.decode(lum_buf) == val


def test_illuminance_max_value(lum):
    val = (65535,)
    lum_buf = lum.encode(val)
    assert lum.decode(lum_buf) == val
    with pytest.raises(ValueError):
        val = (65536,)
        lum_buf = lum.encode(val)


def test_illuminance_invalid_buf(lum):
    with pytest.raises(Exception):
        lum.decode(bytearray([0x00]))


def test_illuminance_invalid_val_type(lum):
    with pytest.raises(Exception):
        lum.encode([0, 1])


def test_illuminance_invalid_val(lum):
    with pytest.raises(Exception):
        lum.encode((0, 1))


def test_illuminance_negative_val(lum):
    with pytest.raises(Exception):
        lum.encode((-1,))
