import pytest

from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_type import LppType


@pytest.fixture
def gen():
    return LppType.get_lpp_type(100)


def test_generic(gen):
    val = 4294967295
    vol_buf = gen.encode((val,))
    assert gen.decode(vol_buf) == (val,)


def test_generic_invalid_buf(gen):
    with pytest.raises(Exception):
        gen.decode(bytearray([0x00, 0x00, 0x00]))


def test_generic_invalid_val(gen):
    with pytest.raises(Exception):
        gen.encode((0, 1))
    with pytest.raises(ValueError):
        # val exceeds 4 bytes
        val = 4294967297
        gen.encode((val,))


def test_generic_negative_val(gen):
    with pytest.raises(Exception):
        gen.encode((-1,))