import pytest

from cayennelpp.lpp_type import LppType


@pytest.fixture
def aio():
    return LppType.get_lpp_type(2)


def test_analog_io(aio):
    val = (123.45,)
    aio_buf = aio.encode(val)
    assert aio.decode(aio_buf) == val
    val = (-123.45,)
    aio_buf = aio.encode(val)
    assert aio.decode(aio_buf) == val


def test_analog_io_invalid_buf(aio):
    with pytest.raises(Exception):
        aio.decode(bytearray([0x00]))


def test_analog_io_invalid_val_type(aio):
    with pytest.raises(Exception):
        aio.encode([0, 1])


def test_analog_io_invalid_val(aio):
    with pytest.raises(Exception):
        aio.encode((0, 1))
