import pytest
import base64
from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_frame import LppFrame


@pytest.fixture
def frame():
    empty_frame = LppFrame()
    return empty_frame


@pytest.fixture
def frame_hlt():
    hlt = LppFrame()
    hlt.add_humidity(3, 45.6)
    hlt.add_load(1, 160.987)
    hlt.add_temperature(2, 12.3)
    return hlt


def test_empty_frame(frame):
    assert not frame.data
    assert len(frame) == 0
    assert not bytes(frame)


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


def test_frame_size(frame):
    assert frame.size == 0
    frame.add_digital_input(0, 1)
    assert frame.size == 3
    frame.add_digital_output(1, 42)
    assert frame.size == 6


def test_frame_maxsize(frame):
    frame.add_digital_input(0, 1)
    assert frame.maxsize == 0
    frame.maxsize = 6
    assert frame.maxsize == 6


def test_frame_maxsize_invalid(frame):
    frame.add_digital_input(0, 1)
    assert frame.maxsize == 0
    with pytest.raises(Exception):
        frame.maxsize = 1


def test_frame_maxsize_negative(frame):
    with pytest.raises(Exception):
        frame.maxsize = -42


def test_frame_maxsize_exceeded(frame):
    frame.maxsize = 3
    with pytest.raises(Exception):
        frame.add_generic(0, 42)


def test_frame_from_bytes():
    # 03 67 01 10 05 67 00 FF = 27.2C + 25.5C
    buf = bytes([0x03, 0x67, 0x01, 0x10, 0x05, 0x67, 0x00, 0xff])
    frame = LppFrame.from_bytes(buf)
    assert buf == bytes(frame)
    assert len(frame) == 2
    # 01 67 FF D7
    buf = bytes([0x01, 0x67, 0xFF, 0xD7])
    frame = LppFrame.from_bytes(buf)
    assert buf == bytes(frame)
    assert len(frame) == 1
    # 06 71 04 D2 FB 2E 00 00
    buf = bytes([0x06, 0x71, 0x04, 0xD2, 0xFB, 0x2E, 0x00, 0x00])
    frame = LppFrame.from_bytes(buf)
    assert buf == bytes(frame)
    assert len(frame) == 1
    # 01 88 06 76 5f f2 96 0a 00 03 e8
    buf = bytes([0x01, 0x88, 0x06, 0x76, 0x5f, 0xf2,
                 0x96, 0x0a, 0x00, 0x03, 0xe8])
    frame = LppFrame.from_bytes(buf)
    assert buf == bytes(frame)
    assert len(frame) == 1


def test_frame_from_bytes_base64():
    base64_str = "AYgILMMBiIMAAAACAAY="
    frame = LppFrame.from_bytes(base64.decodebytes(base64_str.encode('ascii')))
    assert len(frame) == 2


def test_add_digital_io(frame):
    frame.add_digital_input(0, 21)
    frame.add_digital_output(1, 42)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 0
    assert int(frame.data[1].type) == 1


def test_add_analog_io(frame):
    frame.add_analog_input(0, 12.34)
    frame.add_analog_input(1, -12.34)
    frame.add_analog_output(0, 56.78)
    frame.add_analog_output(1, -56.78)
    assert len(frame) == 4
    assert int(frame.data[0].type) == 2
    assert int(frame.data[1].type) == 2
    assert int(frame.data[2].type) == 3
    assert int(frame.data[3].type) == 3


def test_add_sensors(frame):
    frame.add_luminosity(2, 12345)
    frame.add_presence(3, 1)
    frame.add_accelerometer(5, 1.234, -1.234, 0.0)
    frame.add_pressure(6, 1005.5)
    frame.add_barometer(6, 999.0)
    frame.add_gyrometer(7, 1.234, -1.234, 0.0)
    frame.add_gps(8, 1.234, -1.234, 0.0)
    assert len(frame) == 7
    assert int(frame.data[0].type) == 101
    assert int(frame.data[1].type) == 102
    assert int(frame.data[2].type) == 113
    assert int(frame.data[3].type) == 115
    assert int(frame.data[4].type) == 115
    assert int(frame.data[5].type) == 134
    assert int(frame.data[6].type) == 136


def test_add_voltage(frame):
    frame.add_voltage(0, 25.2)
    frame.add_voltage(1, 120.2)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 116
    assert int(frame.data[1].type) == 116
    with pytest.raises(Exception):
        frame.add_voltage(2, -25)


def test_add_current(frame):
    frame.add_current(0, 16.2)
    frame.add_current(1, 32.3)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 117
    assert int(frame.data[1].type) == 117
    with pytest.raises(Exception):
        frame.add_current(2, -25)


def test_add_frequency(frame):
    frame.add_frequency(0, 4294967295)
    frame.add_frequency(1, 1)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 118
    assert int(frame.data[1].type) == 118


def test_add_load(frame):
    frame.add_load(0, -5.432)
    frame.add_load(1, 160.987)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 122
    assert int(frame.data[1].type) == 122


def test_add_generic(frame):
    frame.add_generic(0, 4294967295)
    frame.add_generic(1, 1)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 100
    assert int(frame.data[1].type) == 100


def test_add_unix_time(frame):
    frame.add_unix_time(0, datetime.now(timezone.utc).timestamp())
    frame.add_unix_time(1, 0)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 133
    assert int(frame.data[1].type) == 133


def test_add_temperature(frame):
    frame.add_temperature(2, 12.3)
    frame.add_temperature(3, -32.1)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 103
    assert int(frame.data[1].type) == 103


def test_add_percentage(frame):
    frame.add_percentage(2, 10)
    frame.add_percentage(3, 100)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 120
    assert int(frame.data[1].type) == 120


def test_add_altitude(frame):
    frame.add_altitude(2, 4242)
    frame.add_altitude(3, -4242)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 121
    assert int(frame.data[1].type) == 121


def test_add_concentration(frame):
    frame.add_concentration(2, 10)
    frame.add_concentration(3, 10000)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 125
    assert int(frame.data[1].type) == 125


def test_add_power(frame):
    frame.add_power(2, 10)
    frame.add_power(3, 10000)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 128
    assert int(frame.data[1].type) == 128


def test_add_distance(frame):
    frame.add_distance(2, 1.2345)
    frame.add_distance(3, 1234.5)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 130
    assert int(frame.data[1].type) == 130


def test_add_energy(frame):
    frame.add_energy(2, 1.2345)
    frame.add_energy(3, 1234.5)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 131
    assert int(frame.data[1].type) == 131


def test_add_direction(frame):
    frame.add_direction(2, 30)
    frame.add_direction(2, 120)
    frame.add_direction(3, 210)
    frame.add_direction(3, 300)
    assert len(frame) == 4
    assert int(frame.data[0].type) == 132
    assert int(frame.data[1].type) == 132
    assert int(frame.data[2].type) == 132
    assert int(frame.data[3].type) == 132


def test_add_humidity(frame):
    frame.add_humidity(2, 12.3)
    frame.add_humidity(3, 45.6)
    frame.add_humidity(4, 78.9)
    assert len(frame) == 3
    assert int(frame.data[0].type) == 104
    assert int(frame.data[1].type) == 104
    assert int(frame.data[2].type) == 104


def test_add_colour(frame):
    frame.add_colour(2, 42, 42, 42)
    assert len(frame) == 1
    assert int(frame.data[0].type) == 135


def test_add_switch(frame):
    frame.add_switch(2, 0)
    frame.add_switch(2, 1)
    assert len(frame) == 2
    assert int(frame.data[0].type) == 142
    assert int(frame.data[1].type) == 142


def test_print_empty_frame(frame):
    print(frame)


def test_print_data_frame(frame_hlt):
    print(frame_hlt)


def test_iterator(frame_hlt):
    counter = 0
    for val in frame_hlt:
        print(val)
        counter += 1
    assert counter == len(frame_hlt)


def test_add_by_type(frame):
    with pytest.raises(TypeError):
        frame.add_by_type(0, 1, 42)


def test_get_by_type(frame_hlt):
    h_list = frame_hlt.get_by_type(104)
    assert len(h_list) == 1
    assert int(h_list[0].type) == 104
    l_list = frame_hlt.get_by_type(122)
    assert len(l_list) == 1
    assert int(l_list[0].type) == 122
    t_list = frame_hlt.get_by_type(103)
    assert len(t_list) == 1
    assert int(t_list[0].type) == 103
    b_list = frame_hlt.get_by_type(102)
    assert len(b_list) == 0


def test_get_by_name(frame_hlt):
    h_list = frame_hlt.get_by_name("Humidity")
    assert len(h_list) == 1
    assert int(h_list[0].type) == 104
    l_list = frame_hlt.get_by_name("Load")
    assert len(l_list) == 1
    assert int(l_list[0].type) == 122
    t_list = frame_hlt.get_by_name("Temperature")
    assert len(t_list) == 1
    assert int(t_list[0].type) == 103
    b_list = frame_hlt.get_by_name("Barometer")
    assert len(b_list) == 0


def test_get_by_type_invalid(frame_hlt):
    p_list = frame_hlt.get_by_type(102)
    assert len(p_list) == 0
    i_list = frame_hlt.get_by_type(666)
    assert len(i_list) == 0
