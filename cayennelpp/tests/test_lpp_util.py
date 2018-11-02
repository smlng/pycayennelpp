from cayennelpp.lpp_util import (lpp_digital_io_to_bytes,
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
                                 lpp_gps_from_bytes)


def test_digital_io():
    val = (0,)
    dio_buf = lpp_digital_io_to_bytes(val)
    assert lpp_digital_io_from_bytes(dio_buf) == val
    val = (1,)
    dio_buf = lpp_digital_io_to_bytes(val)
    assert lpp_digital_io_from_bytes(dio_buf) == val


def test_analog_io():
    val = (123.45,)
    aio_buf = lpp_analog_io_to_bytes(val)
    assert lpp_analog_io_from_bytes(aio_buf) == val
    val = (123.45,)
    aio_buf = lpp_analog_io_to_bytes(val)
    assert lpp_analog_io_from_bytes(aio_buf) == val


def test_illuminance():
    val = (12345,)
    illu_buf = lpp_illuminance_to_bytes(val)
    assert lpp_illuminance_from_bytes(illu_buf) == val


def test_presence():
    val = (0,)
    pre_buf = lpp_presence_to_bytes(val)
    assert lpp_presence_from_bytes(pre_buf) == val
    val = (1,)
    pre_buf = lpp_presence_to_bytes(val)
    assert lpp_presence_from_bytes(pre_buf) == val


def test_temperature():
    val = (32.1,)
    temp_buf = lpp_temperature_to_bytes(val)
    assert lpp_temperature_from_bytes(temp_buf) == val
    val = (-4.1,)
    temp_buf = lpp_temperature_to_bytes(val)
    assert lpp_temperature_from_bytes(temp_buf) == val


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


def test_accelerometer():
    val = (12.345, -12.345, 0.0)
    accel_buf = lpp_accel_to_bytes(val)
    assert lpp_accel_from_bytes(accel_buf) == val


def test_barometer():
    val = (1234.5,)
    baro_buf = lpp_baro_to_bytes(val)
    assert lpp_baro_from_bytes(baro_buf) == val


def test_gyrometer():
    val = (123.45, -123.45, 0.0)
    gyro_buf = lpp_gyro_to_bytes(val)
    assert lpp_gyro_from_bytes(gyro_buf) == val


def test_gps():
    val = (42.3519, -87.9094, 10.00)
    gps_buf = lpp_gps_to_bytes(val)
    assert lpp_gps_from_bytes(gps_buf) == val
