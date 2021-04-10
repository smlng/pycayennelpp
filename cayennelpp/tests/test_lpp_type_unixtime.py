import pytest

from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_type import LppType


@pytest.fixture
def ts():
    return LppType.get_lpp_type(133)


def test_unix_time_datetime(ts):
    now = datetime.now(timezone.utc).timestamp()
    ts_buf = ts.encode((now,))
    assert ts.decode(ts_buf) == (int(now),)


def test_unix_time_int(ts):
    val = 5
    ts_buf = ts.encode((val,))
    assert ts.decode(ts_buf) == (val,)


def test_unix_time_invalid_buf(ts):
    with pytest.raises(Exception):
        ts.decode(bytearray([0x00]))


def test_unix_time_invalid_val(ts):
    with pytest.raises(Exception):
        ts.encode((0, 1))


def test_unix_time_negative_val(ts):
    with pytest.raises(Exception):
        ts.encode((-1,))