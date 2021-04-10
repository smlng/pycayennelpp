import pytest

from cayennelpp.lpp_type import LppType


@pytest.fixture
def cur():
    return LppType.get_lpp_type(117)


def test_current(cur):
    val = (2,)
    cur_buf = cur.encode(val)
    assert cur.decode(cur_buf) == val


def test_current_invalid_buf(cur):
    with pytest.raises(Exception):
        cur.decode(bytearray([0x00]))


def test_current_invalid_val(cur):
    with pytest.raises(Exception):
        cur.encode((0, 1))


def test_current_negative_val(cur):
    with pytest.raises(Exception):
        cur.encode((-42,))
