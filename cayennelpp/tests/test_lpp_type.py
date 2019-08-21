import pytest
from cayennelpp.utils import datetime_as_utc
from datetime import datetime, timedelta
from datetime import timezone as tz

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
                                 get_lpp_type,
                                 LppType)


def test_digital_io():
    val = (0,)
    dio_buf = lpp_digital_io_to_bytes(val)
    assert lpp_digital_io_from_bytes(dio_buf) == val
    val = (1,)
    dio_buf = lpp_digital_io_to_bytes(val)
    assert lpp_digital_io_from_bytes(dio_buf) == val


def test_digital_io_invalid_buf():
    with pytest.raises(Exception):
        lpp_digital_io_from_bytes(bytearray([0x00, 0x00]))


def test_digital_io_invalid_val_type():
    with pytest.raises(Exception):
        lpp_digital_io_to_bytes([0, 1])


def test_digital_io_invalid_val():
    with pytest.raises(Exception):
        lpp_digital_io_to_bytes((0, 1))


def test_analog_io():
    val = (123.45,)
    aio_buf = lpp_analog_io_to_bytes(val)
    assert lpp_analog_io_from_bytes(aio_buf) == val
    val = (-123.45,)
    aio_buf = lpp_analog_io_to_bytes(val)
    assert lpp_analog_io_from_bytes(aio_buf) == val


def test_analog_io_invalid_buf():
    with pytest.raises(Exception):
        lpp_analog_io_from_bytes(bytearray([0x00]))


def test_analog_io_invalid_val_type():
    with pytest.raises(Exception):
        lpp_analog_io_to_bytes([0, 1])


def test_analog_io_invalid_val():
    with pytest.raises(Exception):
        lpp_analog_io_to_bytes((0, 1))


def test_illuminance():
    val = (12345,)
    illu_buf = lpp_illuminance_to_bytes(val)
    assert lpp_illuminance_from_bytes(illu_buf) == val


def test_illuminance_invalid_buf():
    with pytest.raises(Exception):
        lpp_illuminance_from_bytes(bytearray([0x00]))


def test_illuminance_invalid_val_type():
    with pytest.raises(Exception):
        lpp_illuminance_to_bytes([0, 1])


def test_illuminance_invalid_val():
    with pytest.raises(Exception):
        lpp_illuminance_to_bytes((0, 1))


def test_illuminance_negative_val():
    with pytest.raises(Exception):
        lpp_illuminance_to_bytes((-1,))


def test_voltage():
    val = (2,)
    vol_buf = lpp_voltage_to_bytes(val)
    assert lpp_voltage_from_bytes(vol_buf) == val


def test_voltage_invalid_buf():
    with pytest.raises(Exception):
        lpp_voltage_from_bytes(bytearray([0x00]))


def test_voltage_invalid_val():
    with pytest.raises(Exception):
        lpp_voltage_to_bytes((0, 1))


def test_voltage_negative_val():
    with pytest.raises(Exception):
        lpp_voltage_to_bytes((-1,))
    with pytest.raises(Exception):
        # -25.0V
        lpp_voltage_from_bytes(bytearray([0xf6, 0x3c]))


def test_load():
    val = (-5.432,)
    aio_buf = lpp_load_to_bytes(val)
    assert lpp_load_from_bytes(aio_buf) == val
    val = (160.987,)
    aio_buf = lpp_load_to_bytes(val)
    assert lpp_load_from_bytes(aio_buf) == val


def test_load_invalid_buf():
    with pytest.raises(Exception):
        lpp_load_from_bytes(bytearray([0x00]))


def test_load_invalid_val_type():
    with pytest.raises(Exception):
        lpp_load_to_bytes([0, 1])


def test_load_invalid_val():
    with pytest.raises(Exception):
        lpp_load_to_bytes((0, 1))


def test_generic():
    val = 4294967295
    vol_buf = lpp_generic_to_bytes((val,))
    assert lpp_generic_from_bytes(vol_buf) == (val,)


def test_generic_invalid_buf():
    with pytest.raises(Exception):
        lpp_generic_from_bytes(bytearray([0x00, 0x00, 0x00]))


def test_generic_invalid_val():
    with pytest.raises(Exception):
        lpp_generic_to_bytes((0, 1))
    with pytest.raises(ValueError):
        # val exceeds 4 bytes
        val = 4294967297
        lpp_generic_to_bytes((val,))


def test_generic_negative_val():
    with pytest.raises(Exception):
        lpp_generic_to_bytes((-1,))


def test_unix_time_datetime_without_tz():
    now = datetime.now()
    utcnow = datetime_as_utc(now.replace(microsecond=0))
    vol_buf = lpp_unix_time_to_bytes((now,))
    assert lpp_unix_time_from_bytes(vol_buf) == (utcnow,)


def test_unix_time_datetime_with_tz():
    now = datetime.now(tz=tz(timedelta(hours=-5)))
    utcnow = datetime_as_utc(now.replace(microsecond=0))
    vol_buf = lpp_unix_time_to_bytes((now,))
    assert lpp_unix_time_from_bytes(vol_buf) == (utcnow,)


def test_unix_time_int():
    val = datetime.fromtimestamp(5, tz.utc)
    vol_buf = lpp_unix_time_to_bytes((5,))
    assert lpp_unix_time_from_bytes(vol_buf) == (val,)


def test_unix_time_invalid_buf():
    with pytest.raises(Exception):
        lpp_unix_time_from_bytes(bytearray([0x00]))


def test_unix_time_invalid_val():
    with pytest.raises(Exception):
        lpp_unix_time_to_bytes((0, 1))
    val = datetime.fromtimestamp(-5, tz.utc)
    with pytest.raises(ValueError):
        # negative value
        lpp_unix_time_to_bytes((val,))


def test_unix_time_negative_val():
    with pytest.raises(Exception):
        lpp_unix_time_to_bytes((-1,))
    with pytest.raises(Exception):
        # -4 years (-4*365*24*3600 seconds)
        buff = bytearray([0xf8, 0x7b, 0x32, 0x0])
        lpp_unix_time_from_bytes(buff)


def test_presence():
    val = (0,)
    pre_buf = lpp_presence_to_bytes(val)
    assert lpp_presence_from_bytes(pre_buf) == val
    val = (1,)
    pre_buf = lpp_presence_to_bytes(val)
    assert lpp_presence_from_bytes(pre_buf) == val


def test_presence_invalid_buf():
    with pytest.raises(Exception):
        lpp_presence_from_bytes(bytearray([0x00, 0x00]))


def test_presence_invalid_val_type():
    with pytest.raises(Exception):
        lpp_presence_to_bytes([0, 1])


def test_presence_invalid_val():
    with pytest.raises(Exception):
        lpp_presence_to_bytes((0, 1))


def test_presence_negative_val():
    with pytest.raises(Exception):
        lpp_presence_to_bytes((-1,))


def test_temperature():
    val = (32.1,)
    temp_buf = lpp_temperature_to_bytes(val)
    assert lpp_temperature_from_bytes(temp_buf) == val
    val = (-4.1,)
    temp_buf = lpp_temperature_to_bytes(val)
    assert lpp_temperature_from_bytes(temp_buf) == val


def test_temperature_invalid_buf():
    with pytest.raises(Exception):
        lpp_temperature_from_bytes(bytearray([0x00]))


def test_temperature_invalid_val_type():
    with pytest.raises(Exception):
        lpp_temperature_to_bytes([0x00])


def test_temperature_invalid_val():
    with pytest.raises(Exception):
        lpp_temperature_to_bytes((0, 0))


def test_humidity():
    val = (50.00,)
    hum_buf = lpp_humidity_to_bytes(val)
    assert lpp_humidity_from_bytes(hum_buf) == val
    hum_buf = lpp_humidity_to_bytes(50.25)
    assert lpp_humidity_from_bytes(hum_buf) == val
    val = (50.50,)
    hum_buf = lpp_humidity_to_bytes(val)
    assert lpp_humidity_from_bytes(hum_buf) == val
    hum_buf = lpp_humidity_to_bytes(50.75)
    assert lpp_humidity_from_bytes(hum_buf) == val


def test_humidity_negative_val():
    with pytest.raises(Exception):
        val = (-50.50,)
        lpp_humidity_to_bytes(val)


def test_humidity_invalid_buf():
    with pytest.raises(Exception):
        lpp_humidity_from_bytes(bytearray([0x00, 0x00]))


def test_humidity_invalid_val_type():
    with pytest.raises(Exception):
        lpp_humidity_to_bytes([0x00])


def test_humidity_invalid_val():
    with pytest.raises(Exception):
        lpp_humidity_to_bytes((0, 0))


def test_accelerometer():
    val = (12.345, -12.345, 0.0)
    accel_buf = lpp_accel_to_bytes(val)
    assert lpp_accel_from_bytes(accel_buf) == val
    val = (-12.345, 0.0, -12.345)
    accel_buf = lpp_accel_to_bytes(val)
    assert lpp_accel_from_bytes(accel_buf) == val


def test_accelerometer_invalid_buf():
    with pytest.raises(Exception):
        lpp_accel_from_bytes(bytearray([0x00]))


def test_accelerometer_invalid_val_type():
    with pytest.raises(Exception):
        lpp_accel_to_bytes([0x00])


def test_accelerometer_invalid_val():
    with pytest.raises(Exception):
        lpp_accel_to_bytes((0, 0))


def test_barometer():
    val = (1234.5,)
    baro_buf = lpp_baro_to_bytes(val)
    assert lpp_baro_from_bytes(baro_buf) == val


def test_barometer_negative_val():
    with pytest.raises(Exception):
        val = (-1234.5,)
        lpp_baro_to_bytes(val)


def test_barometer_invalid_buf():
    with pytest.raises(Exception):
        lpp_baro_from_bytes(bytearray([0x00]))


def test_barometer_invalid_val_type():
    with pytest.raises(Exception):
        lpp_baro_to_bytes([0x00])


def test_barometer_invalid_val():
    with pytest.raises(Exception):
        lpp_baro_to_bytes((0, 0))


def test_gyrometer():
    val = (123.45, -123.45, 0.0)
    gyro_buf = lpp_gyro_to_bytes(val)
    assert lpp_gyro_from_bytes(gyro_buf) == val
    val = (-123.45, 0.0, -123.45)
    gyro_buf = lpp_gyro_to_bytes(val)
    assert lpp_gyro_from_bytes(gyro_buf) == val


def test_gyrometer_invalid_buf():
    with pytest.raises(Exception):
        lpp_gyro_from_bytes(bytearray([0x00]))


def test_gyrometer_invalid_val_type():
    with pytest.raises(Exception):
        lpp_gyro_to_bytes([0x00])


def test_gyrometer_invalid_val():
    with pytest.raises(Exception):
        lpp_gyro_to_bytes((0, 0))


def test_gps():
    val = (42.3519, -87.9094, 10.00)
    gps_buf = lpp_gps_to_bytes(val)
    assert lpp_gps_from_bytes(gps_buf) == val
    val = (-42.3519, 87.9094, -10.00)
    gps_buf = lpp_gps_to_bytes(val)
    assert lpp_gps_from_bytes(gps_buf) == val


def test_gps_invalid_buf():
    with pytest.raises(Exception):
        lpp_gps_from_bytes(bytearray([0x00]))


def test_gps_invalid_val_type():
    with pytest.raises(Exception):
        lpp_gps_to_bytes([0x00])


def test_gps_invalid_val():
    with pytest.raises(Exception):
        lpp_gps_to_bytes((0, 0))


def test_lpp_type_init_invalid_tid():
    with pytest.raises(Exception):
        LppType("foo", "bar", 42, 42, None, None)


def test_lpp_type_init_invalid_name():
    with pytest.raises(Exception):
        LppType(42, 42, 42, 42, None, None)


def test_lpp_type_init_invalid_size():
    with pytest.raises(Exception):
        LppType(42, "foo", "foo", 42, None, None)


def test_lpp_type_init_invalid_dim():
    with pytest.raises(Exception):
        LppType(42, "foo", 42, "foo", None, None)


def test_get_lpp_type_invalid():
    with pytest.raises(Exception):
        get_lpp_type("foo")
