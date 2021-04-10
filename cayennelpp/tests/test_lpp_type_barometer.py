import pytest

from cayennelpp.lpp_type import LppType


@pytest.fixture
def baro():
    return LppType.get_lpp_type(115)


def test_barometer(baro):
    val = (1234.5,)
    baro_buf = baro.encode(val)
    assert baro.decode(baro_buf) == val


def test_barometer_negative_val(baro):
    with pytest.raises(Exception):
        val = (-1234.5,)
        baro.encode(val)


def test_barometer_invalid_buf(baro):
    with pytest.raises(Exception):
        baro.decode(bytearray([0x00]))


def test_barometer_invalid_val_type(baro):
    with pytest.raises(Exception):
        baro.encode([0x00])


def test_barometer_invalid_val(baro):
    with pytest.raises(Exception):
        baro.encode((0, 0))
