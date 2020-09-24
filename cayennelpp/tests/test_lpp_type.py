import pytest

from datetime import datetime
from datetime import timezone

from cayennelpp.lpp_type import (lpp_digital_io_to_bytes,
                                 lpp_digital_io_from_bytes,
                                 lpp_analog_io_to_bytes,
                                 lpp_analog_io_from_bytes,
                                 lpp_illuminance_to_bytes,
                                 lpp_illuminance_from_bytes,
                                 lpp_presence_to_bytes,
                                 lpp_presence_from_bytes,
                                 lpp_temperature_to_bytes,
                                 lpp_temperature_from_bytes,
                                 lpp_humidity_to_bytes,
                                 lpp_humidity_from_bytes,
                                 lpp_accel_to_bytes,
                                 lpp_accel_from_bytes,
                                 lpp_baro_to_bytes,
                                 lpp_baro_from_bytes,
                                 lpp_gyro_to_bytes,
                                 lpp_gyro_from_bytes,
                                 lpp_gps_to_bytes,
                                 lpp_gps_from_bytes,
                                 lpp_voltage_to_bytes,
                                 lpp_voltage_from_bytes,
                                 lpp_load_to_bytes,
                                 lpp_load_from_bytes,
                                 lpp_generic_to_bytes,
                                 lpp_generic_from_bytes,
                                 lpp_unix_time_to_bytes,
                                 lpp_unix_time_from_bytes,
                                 lpp_current_from_bytes,
                                 lpp_current_to_bytes,
                                 lpp_power_from_bytes,
                                 lpp_power_to_bytes,
                                 lpp_direction_from_bytes,
                                 lpp_direction_to_bytes,
                                 get_lpp_type,
                                 LppType)


@pytest.mark.parametrize(
    "converter, test_value", [
        (lpp_generic_to_bytes,      (-1,)),         # type 100
        (lpp_illuminance_to_bytes,  (-1,)),         # type 101
        (lpp_presence_to_bytes,     (-1,)),         # type 102
        (lpp_humidity_to_bytes,     (-50.50,)),     # type 104
        (lpp_baro_to_bytes,         (-1234.5,)),    # type 115    
        (lpp_voltage_to_bytes,      (-1,)),         # type 116
        (lpp_current_to_bytes,      (-1,)),         # type 117
        (lpp_power_to_bytes,        (-1,)),         # type 128
        (lpp_direction_to_bytes,    (-1,)),         # type 132
        (lpp_unix_time_to_bytes,    (-1,)),         # type 133
    ]
)
def test_should_raise_Exception_on_negative_to_bytes(converter, test_value):
    # Test unsigned data type conversion to bytes  
    with pytest.raises(ValueError):
        converter(test_value)


@pytest.mark.parametrize(
    "converter, test_value", [
    # (lpp_generic_from_bytes,    (0xff, 0xff, 0xcf, 0xc7,)) # val -12345    type 100
    (lpp_illuminance_from_bytes,(0xff, 0xce,)),            # val -50       type 101
    (lpp_presence_from_bytes,   (0xff,)),                  # val -1        type 102
    (lpp_humidity_from_bytes,   (0x9b,)),                  # val -101      type 104
    (lpp_baro_from_bytes,       (0xcf, 0xc,)),             # val -12345    type 115
    (lpp_voltage_from_bytes,    (0xff, 0x9c,)),            # val -100      type 116
    (lpp_current_from_bytes,    (0xff, 0xff,)),            # val -1        type 117
    (lpp_power_from_bytes,      (0xff, 0xff,)),            # val -1        type 128
    (lpp_direction_from_bytes,  (0xfe, 0x93,)),            # val -365      type 132
    (lpp_unix_time_from_bytes,  (0xf8, 0x7b, 0x32, 0x0,)), # val -126144000  type 133
    ]
)
def test_should_raise_ValueError_on_negative_from_bytes(converter, test_value):
    # Test unsigned data type conversion from bytes
    with pytest.raises(ValueError):
        converter(test_value)


@pytest.mark.parametrize(
    "converter, test_value", [
    (lpp_digital_io_to_bytes,   (0, 1)),    # type 0 / 1
    (lpp_analog_io_to_bytes,    (0, 1)),    # type 2 / 3 
    (lpp_generic_to_bytes,      (0, 1)),    # type 100
    (lpp_illuminance_to_bytes,  (0, 1)),    # type 101
    (lpp_presence_to_bytes,     (0, 1)),    # type 102
    (lpp_temperature_to_bytes,  (0, 1)),    # type 103
    (lpp_humidity_to_bytes,     (0, 1)),    # type 104
    (lpp_accel_to_bytes,        (0, 1)),    # type 113
    (lpp_baro_to_bytes,         (0, 1)),    # type 115
    (lpp_voltage_to_bytes,      (0, 1)),    # type 116
    (lpp_current_to_bytes,      (0, 1)),    # type 117
    (lpp_load_to_bytes,         (0, 1)),    # type 122
    (lpp_power_to_bytes,        (0, 1)),    # type 128
    (lpp_direction_to_bytes,    (0, 1)),    # type 132
    (lpp_unix_time_to_bytes,    (0, 1)),    # type 133
    (lpp_gyro_to_bytes,         (0, 1)),    # type 134
    (lpp_gps_to_bytes,          (0, 1)),    # type 136
    ]
)
def test_should_raise_AssertionError_on_invalid_val(converter, test_value):
    with pytest.raises(AssertionError):
        converter(test_value)

@pytest.mark.parametrize(
    "converter, test_value", [
    (lpp_digital_io_from_bytes,  [0x00, 0x00]),         # type 0 / 1
    (lpp_analog_io_from_bytes,   [0x00]),               # type 0 / 1
    (lpp_generic_from_bytes,     [0x00, 0x00, 0x00]),   # type 100
    (lpp_illuminance_from_bytes, [0x00]),               # type 101
    (lpp_presence_from_bytes,    [0x00, 0x00]),         # type 102
    (lpp_temperature_from_bytes, [0x00]),               # type 103
    (lpp_humidity_from_bytes,    [0x00, 0x00]),         # type 104
    (lpp_accel_from_bytes,       [0x00]),               # type 113
    (lpp_baro_from_bytes,        [0x00]),               # type 115
    (lpp_voltage_from_bytes,     [0x00]),               # type 116
    (lpp_current_from_bytes,     [0x00]),               # type 117
    (lpp_load_from_bytes,        [0x00]),               # type 122
    (lpp_power_from_bytes,       [0x00]),               # type 128
    (lpp_direction_from_bytes,   [0x00]),               # type 132
    (lpp_unix_time_from_bytes,   [0x00]),               # type 133
    (lpp_gyro_from_bytes,        [0x00]),               # type 134
    (lpp_gps_from_bytes,         [0x00]),               # type 136
    ]
)
def test_should_raise_AssertionError_on_invalid_buf(converter, test_value):
    with pytest.raises(AssertionError):
        converter(bytearray(test_value))


@pytest.mark.parametrize(
    "converter, test_value", [
    (lpp_digital_io_to_bytes,     [0x00, 0x00]),       # type 0 / 1
    (lpp_analog_io_to_bytes,      [0x00]),             # type 1 / 2
    (lpp_generic_to_bytes,        [0x00, 0x00, 0x00]), # type 100
    (lpp_illuminance_to_bytes,    [0x00]),             # type 101
    (lpp_presence_to_bytes,       [0x00, 0x00]),       # type 102
    (lpp_temperature_to_bytes,    [0x00]),             # type 103
    (lpp_humidity_to_bytes,       [0x00, 0x00]),       # type 104
    (lpp_accel_to_bytes,          [0x00]),             # type 113
    (lpp_baro_to_bytes,           [0x00]),             # type 115
    (lpp_voltage_to_bytes,        [0x00]),             # type 116
    (lpp_current_to_bytes,        [0x00]),             # type 117
    (lpp_load_to_bytes,           [0x00]),             # type 122
    (lpp_power_to_bytes,          [0x00]),             # type 128
    (lpp_direction_to_bytes,      [0x00]),             # type 132
    (lpp_unix_time_to_bytes,      [0x00]),             # type 133
    (lpp_gyro_to_bytes,           [0x00]),             # type 134
    (lpp_gps_to_bytes,            [0x00]),             # type 136
    ]
)
def test_should_raise_Exception_on_invalid_val_type(converter, test_value):    
    with pytest.raises(Exception):
        converter(test_value)

@pytest.mark.parametrize(
    "converter, test_cases", [
    ("lpp_analog_io",   [(123.45,), (-123.45,)]),                                       # type 0 / 1
    ("lpp_digital_io",  [(0,), (1,)]),                                                  # type 1 / 2
    ("lpp_generic",     [(4294967295,)]),                                               # type 100
    ("lpp_illuminance", [(12345,)]),                                                    # type 101
    ("lpp_presence",    [(0,), (1,)]),                                                  # type 102    
    ("lpp_temperature", [(32.1,), (-4.1,)]),                                            # type 103
    ("lpp_humidity",    [(50.00,), (50.50,),]),                                         # type 104
    ("lpp_accel",       [(12.345, -12.345, 0.0), (-12.345, 0.0, -12.345)]),             # type 113
    ("lpp_baro",        [(1234.5,)]),                                                   # type 115
    ("lpp_voltage",     [(2,)]),                                                        # type 116
    ("lpp_current",     [(2,), (1,), (10,)]),                                           # type 117
    ("lpp_load",        [(-5.432,), (160.987,)]),                                       # type 122
    ("lpp_power",       [(1,), (10,), (15,)]),                                          # type 128
    ("lpp_direction",   [(10,), (90,), (270,)]),                                        # type 132
    ("lpp_unix_time",   [(int(datetime.now(timezone.utc).timestamp()),), (5,)]),        # type 133
    ("lpp_gyro",        [(123.45, -123.45, 0.0), (-123.45, 0.0, -123.45)]),             # type 134
    ("lpp_gps",         [(42.3519, -87.9094, 10.00), (-42.3519, 87.9094, -10.00)]),     # type 136
    ]
)
def test_type_endode_should_equal_decode(converter, test_cases):
    print(test_cases)
    for case_val in test_cases:
        buf = eval(converter+"_to_bytes")(case_val)
        assert eval(converter+"_from_bytes")(buf) == case_val


def test_init_invalid_type():
    with pytest.raises(Exception):
        LppType("foo", "bar", 42, 42, None, None)


def test_init_invalid_name():
    with pytest.raises(Exception):
        LppType(42, 42, 42, 42, None, None)


def test_init_invalid_size():
    with pytest.raises(Exception):
        LppType(42, "foo", "foo", 42, None, None)


def test_init_invalid_dim():
    with pytest.raises(Exception):
        LppType(42, "foo", 42, "foo", None, None)


def test_get_lpp_type_invalid():
    with pytest.raises(Exception):
        get_lpp_type("foo")
