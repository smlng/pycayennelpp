import pytest

from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_type import LppType


@pytest.fixture
def load():
    return LppType.get_lpp_type(122)


def test_load(load):
    val = (-5.432,)
    aio_buf = load.encode(val)
    assert load.decode(aio_buf) == val
    val = (160.987,)
    aio_buf = load.encode(val)
    assert load.decode(aio_buf) == val


def test_load_invalid_buf(load):
    with pytest.raises(Exception):
        load.decode(bytearray([0x00]))


def test_load_invalid_val_type(load):
    with pytest.raises(Exception):
        load.encode([0, 1])


def test_load_invalid_val(load):
    with pytest.raises(Exception):
        load.encode((0, 1))