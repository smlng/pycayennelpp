import pytest

from cayennelpp.lpp_type import LppType


@pytest.fixture
def pres():
    return LppType.get_lpp_type(102)


def test_presence(pres):
    val = (0,)
    pre_buf = pres.encode(val)
    assert pres.decode(pre_buf) == val
    val = (1,)
    pre_buf = pres.encode(val)
    assert pres.decode(pre_buf) == val


def test_presence_invalid_buf(pres):
    with pytest.raises(Exception):
        pres.decode(bytearray([0x00, 0x00]))


def test_presence_invalid_val_type(pres):
    with pytest.raises(Exception):
        pres.encode([0, 1])


def test_presence_invalid_val(pres):
    with pytest.raises(Exception):
        pres.encode((0, 1))


def test_presence_negative_val(pres):
    with pytest.raises(Exception):
        pres.encode((-1,))
