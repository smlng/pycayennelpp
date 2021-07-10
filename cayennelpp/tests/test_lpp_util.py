import pytest
import json

from cayennelpp.lpp_frame import LppFrame
from cayennelpp.lpp_util import LppUtil


@pytest.fixture
def frame():
    lf = LppFrame()
    lf.add_humidity(3, 45.6)
    lf.add_temperature(2, 12.3)
    return lf


def test_json_encode_type_int(frame):
    dump_int = json.dumps(frame, default=LppUtil.json_encode_type_int)
    assert len(dump_int) > 0
    load_int = json.loads(dump_int)
    for o in load_int:
        assert isinstance(o['type'], int)


def test_json_encode_type_str(frame):
    dump_str = json.dumps(frame, default=LppUtil.json_encode_type_str)
    assert len(dump_str) > 0
    load_str = json.loads(dump_str)
    for o in load_str:
        assert isinstance(o['type'], str)


def test_json_encode_invalid():
    with pytest.raises(TypeError):
        json.dumps(type("foobar", (object,), {}), default=LppUtil.json_encode)
