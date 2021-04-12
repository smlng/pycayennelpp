import pytest

from cayennelpp.lpp_type import LppType


@pytest.fixture
def freq():
    return LppType.get_lpp_type(118)


def test_generic(freq):
    val = 4294967295
    freq_buf = freq.encode((val,))
    assert freq.decode(freq_buf) == (val,)


def test_generic_invalid_buf(freq):
    with pytest.raises(BufferError):
        freq.decode(bytearray([0x00, 0x00, 0x00]))


def test_generic_invalid_val(freq):
    with pytest.raises(ValueError):
        freq.encode((0, 1))
    with pytest.raises(ValueError):
        # val exceeds 4 bytes
        val = 4294967297
        freq.encode((val,))


def test_generic_negative_val(freq):
    with pytest.raises(ValueError):
        freq.encode((-1,))
