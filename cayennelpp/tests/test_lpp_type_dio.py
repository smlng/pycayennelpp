import pytest

from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_type import LppType

@pytest.fixture
def dio():
    return LppType.get_lpp_type(0)

def test_digital_io(dio):
    val = (0,)
    dio_buf = dio.encode(val)
    assert dio.decode(dio_buf) == val
    val = (1,)
    dio_buf = dio.encode(val)
    assert dio.decode(dio_buf) == val


def test_digital_io_invalid_buf(dio):
    with pytest.raises(Exception):
        dio.decode(bytearray([0x00, 0x00]))


def test_digital_io_invalid_val_type(dio):
    with pytest.raises(Exception):
        dio.encode([0, 1])


def test_digital_io_invalid_val(dio):
    with pytest.raises(Exception):
        dio.encode((0, 1))
