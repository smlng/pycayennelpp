import pytest
from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_frame import LppFrame


@pytest.fixture
def frame():
    empty_frame = LppFrame()
    return empty_frame


def test_frame_empty(frame):
    assert not frame.data
    assert len(frame) == 0
    assert not frame.bytes()


def test_init_invalid_data_nolist():
    with pytest.raises(Exception):
        LppFrame(42)


def test_init_invalid_data_item():
    with pytest.raises(Exception):
        LppFrame([0])


def test_frame_reset(frame):
    frame.add_digital_input(0, 1)
    assert len(frame) == 1
    frame.reset()
    assert len(frame) == 0


def test_frame_from_bytes():
    # 03 67 01 10 05 67 00 FF = 27.2C + 25.5C
    buf = bytearray([0x03, 0x67, 0x01, 0x10, 0x05, 0x67, 0x00, 0xff])
    frame = LppFrame.from_bytes(buf)
    assert buf == frame.bytes()
    assert len(frame) == 2


def test_frame_from_base64():
    base64 = "AYgILMMBiIMAAAACAAY="
    frame = LppFrame.from_base64(base64)
    assert len(frame) == 2


def test_add_digital_io(frame):
    frame.add_digital_input(0, 21)
    frame.add_digital_output(1, 42)
    assert len(frame) == 2
    assert frame.data[0].type == 0
    assert frame.data[1].type == 1


def test_add_analog_io(frame):
    frame.add_analog_input(0, 12.34)
    frame.add_analog_input(1, -12.34)
    frame.add_analog_output(0, 56.78)
    frame.add_analog_output(1, -56.78)
    assert len(frame) == 4
    assert frame.data[0].type == 2
    assert frame.data[1].type == 2
    assert frame.data[2].type == 3
    assert frame.data[3].type == 3


def test_add_sensors(frame):
    frame.add_luminosity(2, 12345)
    frame.add_presence(3, 1)
    frame.add_accelerometer(5, 1.234, -1.234, 0.0)
    frame.add_pressure(6, 1005.5)
    frame.add_barometer(6, 999.0)
    frame.add_gyrometer(7, 1.234, -1.234, 0.0)
    frame.add_gps(8, 1.234, -1.234, 0.0)
    assert len(frame) == 7
    assert frame.data[0].type == 101
    assert frame.data[1].type == 102
    assert frame.data[2].type == 113
    assert frame.data[3].type == 115
    assert frame.data[4].type == 115
    assert frame.data[5].type == 134
    assert frame.data[6].type == 136


def test_add_voltage(frame):
    frame.add_voltage(0, 25.2)
    frame.add_voltage(1, 120.2)
    assert len(frame) == 2
    assert frame.data[0].type == 116
    assert frame.data[1].type == 116
    frame.add_voltage(2, -25)
    with pytest.raises(Exception):
        frame.bytes()


def test_add_load(frame):
    frame.add_load(0, -5.432)
    frame.add_load(1, 160.987)
    assert len(frame) == 2
    assert frame.data[0].type == 122
    assert frame.data[1].type == 122


def test_add_generic(frame):
    frame.add_generic(0, 4294967295)
    frame.add_generic(1, 1)
    assert len(frame) == 2
    assert frame.data[0].type == 100
    assert frame.data[1].type == 100


def test_add_unix_time(frame):
    frame.add_unix_time(0, datetime.now(timezone.utc).timestamp())
    frame.add_unix_time(1, 0)
    assert len(frame) == 2
    assert frame.data[0].type == 133
    assert frame.data[1].type == 133
    frame.bytes()


def test_add_temperature(frame):
    frame.add_temperature(2, 12.3)
    frame.add_temperature(3, -32.1)
    assert len(frame) == 2
    assert frame.data[0].type == 103
    assert frame.data[1].type == 103


def test_add_humidity(frame):
    frame.add_humidity(2, 12.3)
    frame.add_humidity(3, 45.6)
    frame.add_humidity(4, 78.9)
    assert len(frame) == 3
    assert frame.data[0].type == 104
    assert frame.data[1].type == 104
    assert frame.data[2].type == 104


def test_lpp_frame_str_empty(frame):
    print(frame)


def test_lpp_frame_str_data(frame):
    frame.add_temperature(2, 12.3)
    frame.add_temperature(3, -32.1)
    print(frame)


def test_lpp_frame_iterator(frame):
    frame.add_temperature(2, 12.3)
    frame.add_humidity(3, 45.6)
    frame.add_load(1, 160.987)
    counter = 0
    for val in frame:
        print(val)
        counter += 1
    assert counter == len(frame)
