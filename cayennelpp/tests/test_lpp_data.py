import pytest
from datetime import datetime
from datetime import timezone as tz

from cayennelpp.lpp_data import LppData


def test_temperature_from_bytes():
    # 01 67 FF D7 = -4.1C
    temp_buf = bytearray([0x01, 0x67, 0xFF, 0xD7])
    temp_dat = LppData.from_bytes(temp_buf)
    assert temp_buf == temp_dat.bytes()


def test_accelerometer_from_bytes():
    # 06 71 04 D2 FB 2E 00 00
    acc_buf = bytearray([0x06, 0x71, 0x04, 0xD2, 0xFB, 0x2E, 0x00, 0x00])
    acc_dat = LppData.from_bytes(acc_buf)
    assert acc_buf == acc_dat.bytes()


def test_generic_from_bytes():
    buff = bytearray([0x00, 0x64, 0xff, 0xff, 0xff, 0xfb])
    data = LppData.from_bytes(buff)
    assert buff == data.bytes()
    assert data.type == 100
    assert data.value == (4294967291,)


def test_generic_from_bytes_invalid_size():
    with pytest.raises(Exception):
        buf = bytearray([0x00, 0x64, 0x00, 0x00, 0x00])
        LppData.from_bytes(buf)


def test_gps_from_bytes():
    # 01 88 06 76 5f f2 96 0a 00 03 e8
    gps_buf = bytearray([0x01, 0x88, 0x06, 0x76,
                         0x5f, 0xf2, 0x96, 0x0a,
                         0x00, 0x03, 0xe8])
    gps_dat = LppData.from_bytes(gps_buf)
    assert gps_buf == gps_dat.bytes()


def test_voltage_from_bytes():
    # 25V on channel 1
    buff = bytearray([0x01, 0x74, 0x9, 0xc4])
    data = LppData.from_bytes(buff)
    assert buff == data.bytes()
    assert data.value == (25,)


def test_load_from_bytes():
    # 42.321kg on channel 0
    buff = bytearray([0x00, 0x7A, 0x00, 0xA5, 0x51])
    data = LppData.from_bytes(buff)
    assert buff == data.bytes()


def test_unix_time_from_bytes():
    # 1970-01-01T08:00Z (ie unix time 0)
    buff = bytearray([0x01, 0x85, 0x00, 0x00, 0x00, 0x00])
    data = LppData.from_bytes(buff)
    assert buff == data.bytes()
    assert data.value == (datetime.fromtimestamp(0, tz.utc),)


def test_init_invalid_type():
    with pytest.raises(Exception):
        LppData(0, 4242, 0)


def test_init_data_none():
    with pytest.raises(Exception):
        LppData(0, 0, None)


def test_init_invalid_dimension():
    with pytest.raises(Exception):
        LppData(0, 136, 0)


def test_any_from_bytes_invalid_size():
    with pytest.raises(Exception):
        buf = bytearray([0x00, 0x00])
        LppData.from_bytes(buf)


def test_gps_from_bytes_invalid_size():
    with pytest.raises(Exception):
        buf = bytearray([0x00, 0x88, 0x00])
        LppData.from_bytes(buf)


def test_lpp_data_str():
    print(LppData(0, 0, 0))
