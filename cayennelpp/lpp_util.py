
from __future__ import absolute_import

import logging


def lpp_digital_io_from_bytes(buf):
    logging.debug("lpp_digital_io_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    assert(len(buf) == 1)
    val = buf[0]
    logging.debug("  out:   value = %d", val)
    return (val,)


def lpp_digital_io_to_bytes(data):
    logging.debug("lpp_digital_io_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    assert(len(data) == 1)
    val = data[0]
    logging.debug("  in:    value = %d", val)
    buf = bytearray([0x00])
    buf[0] = (val) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_analog_io_from_bytes(buf):
    logging.debug("lpp_analog_io_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    assert(len(buf) == 2)
    val_i = (buf[0] << 8 | buf[1])
    logging.debug("  out:   value = %d", val_i)
    if val_i >= (1 << 15):
        val_i = -1 - (val_i ^ 0xffff)
    logging.debug("  out:   value = %d", val_i)
    val = val_i / 100.0
    logging.debug("  out:   value = %f", val)
    return (val,)


def lpp_analog_io_to_bytes(data):
    logging.debug("lpp_analog_io_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    assert(len(data) == 1)
    val = data[0]
    logging.debug("  in:    value = %f", val)
    buf = bytearray([0x00, 0x00])
    val_i = int(val * 100)
    logging.debug("  in:    value = %d", val_i)
    if val_i < 0:
        val_i = ~(-val_i - 1)
    logging.debug("  in:    value = %d", val_i)
    buf[0] = (val_i >> 8) & 0xff
    buf[1] = (val_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_illuminance_from_bytes(buf):
    logging.debug("lpp_illuminance_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    assert(len(buf) == 2)
    val = int(buf[0] << 8 | buf[1])
    logging.debug("  out:   value = %d", val)
    return (val,)


def lpp_illuminance_to_bytes(data):
    logging.debug("lpp_illuminance_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    assert(len(data) == 1)
    val = data[0]
    logging.debug("  in:    value = %d", val)
    assert(val >= 0)
    buf = bytearray([0x00, 0x00])
    buf[0] = (val >> 8) & 0xff
    buf[1] = (val) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_presence_from_bytes(buf):
    logging.debug("lpp_presence_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    assert(len(buf) == 1)
    val = buf[0]
    logging.debug("  out:   value = %d", val)
    return (val,)


def lpp_presence_to_bytes(data):
    logging.debug("lpp_presence_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    assert(len(data) == 1)
    val = data[0]
    logging.debug("  in:    value = %d", val)
    assert(val >= 0)
    buf = bytearray([0x00])
    buf[0] = (val) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_temperature_from_bytes(buf):
    logging.debug("lpp_temperature_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    assert(len(buf) == 2)
    val_i = (buf[0] << 8 | buf[1])
    logging.debug("  out:   value = %d", val_i)
    if val_i >= (1 << 15):
        val_i = -1 - (val_i ^ 0xffff)
    logging.debug("  out:   value = %d", val_i)
    val = val_i / 10.0
    logging.debug("  out:   value = %f", val)
    return (val, )


def lpp_temperature_to_bytes(data):
    logging.debug("lpp_temperature_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    assert(len(data) == 1)
    val = data[0]
    logging.debug("  in:    value = %f", val)
    buf = bytearray([0x00, 0x00])
    val_i = int(val * 10)
    logging.debug("  in:    value = %d", val_i)
    if val_i < 0:
        val_i = ~(-val_i - 1)
    logging.debug("  in:    value = %d", val_i)
    buf[0] = (val_i >> 8) & 0xff
    buf[1] = (val_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_humidity_from_bytes(buf):
    logging.debug("lpp_humidity_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    assert(len(buf) == 1)
    val_i = buf[0]
    logging.debug("  out:   value = %d", val_i)
    val = val_i / 2.0
    logging.debug("  out:   value = %f", val)
    return (val, )


def lpp_humidity_to_bytes(data):
    logging.debug("lpp_humidity_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    assert(len(data) == 1)
    val = data[0]
    logging.debug("  in:    value = %f", val)
    assert(val >= 0)
    buf = bytearray([0x00])
    val_i = int(val * 2)
    logging.debug("  in:    value = %d", val_i)
    buf[0] = (val_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_accel_from_bytes(buf):
    logging.debug("lpp_accel_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    assert(len(buf) == 6)
    val_xi = int(buf[0] << 8 | buf[1])
    val_yi = int(buf[2] << 8 | buf[3])
    val_zi = int(buf[4] << 8 | buf[5])
    logging.debug("  out:   x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    if val_xi >= (1 << 15):
        val_xi = -1 - (val_xi ^ 0xffff)
    if val_yi >= (1 << 15):
        val_yi = -1 - (val_yi ^ 0xffff)
    if val_zi >= (1 << 15):
        val_zi = -1 - (val_zi ^ 0xffff)
    logging.debug("  out:   x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    val_x = val_xi / 1000.0
    val_y = val_yi / 1000.0
    val_z = val_zi / 1000.0
    logging.debug("  out:   x = %f, y = %f, z = %f", val_x, val_y, val_z)
    return (val_x, val_y, val_z,)


def lpp_accel_to_bytes(data):
    logging.debug("lpp_accel_to_bytes")
    assert(isinstance(data, tuple))
    assert(len(data) == 3)
    val_x = data[0]
    val_y = data[1]
    val_z = data[2]
    logging.debug("  in:    x = %f, y = %f, z = %f", val_x, val_y, val_z)
    buf = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    val_xi = int(val_x * 1000)
    val_yi = int(val_y * 1000)
    val_zi = int(val_z * 1000)
    logging.debug("  in:    x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    if val_xi < 0:
        val_xi = ~(-val_xi - 1)
    if val_yi < 0:
        val_yi = ~(-val_yi - 1)
    if val_zi < 0:
        val_zi = ~(-val_zi - 1)
    logging.debug("  in:    x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    buf[0] = (val_xi >> 8) & 0xff
    buf[1] = (val_xi) & 0xff
    buf[2] = (val_yi >> 8) & 0xff
    buf[3] = (val_yi) & 0xff
    buf[4] = (val_zi >> 8) & 0xff
    buf[5] = (val_zi) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_baro_from_bytes(buf):
    logging.debug("lpp_baro_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    assert(len(buf) == 2)
    val = (buf[0] << 8 | buf[1]) / 10.0
    logging.debug("  out:   value = %f", val)
    return (val,)


def lpp_baro_to_bytes(data):
    logging.debug("lpp_baro_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    assert(len(data) == 1)
    val = data[0]
    logging.debug("  in:    value = %f", val)
    assert(val >= 0)
    buf = bytearray([0x00, 0x00])
    val_i = int(val * 10)
    buf[0] = (val_i >> 8) & 0xff
    buf[1] = (val_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_gyro_from_bytes(buf):
    logging.debug("lpp_gyro_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    assert(len(buf) == 6)
    val_xi = int(buf[0] << 8 | buf[1])
    val_yi = int(buf[2] << 8 | buf[3])
    val_zi = int(buf[4] << 8 | buf[5])
    logging.debug("  out:   x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    if val_xi >= (1 << 15):
        val_xi = -1 - (val_xi ^ 0xffff)
    if val_yi >= (1 << 15):
        val_yi = -1 - (val_yi ^ 0xffff)
    if val_zi >= (1 << 15):
        val_zi = -1 - (val_zi ^ 0xffff)
    logging.debug("  out:   x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    val_x = val_xi / 100.0
    val_y = val_yi / 100.0
    val_z = val_zi / 100.0
    logging.debug("  out:   x = %f, y = %f, z = %f", val_x, val_y, val_z)
    return (val_x, val_y, val_z,)


def lpp_gyro_to_bytes(data):
    logging.debug("lpp_gyro_to_bytes")
    assert(isinstance(data, tuple))
    assert(len(data) == 3)
    val_x = data[0]
    val_y = data[1]
    val_z = data[2]
    logging.debug("  in:    x = %f, y = %f, z = %f", val_x, val_y, val_z)
    buf = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    val_xi = int(val_x * 100)
    val_yi = int(val_y * 100)
    val_zi = int(val_z * 100)
    logging.debug("  in:    x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    if val_xi < 0:
        val_xi = ~(-val_xi - 1)
    if val_yi < 0:
        val_yi = ~(-val_yi - 1)
    if val_zi < 0:
        val_zi = ~(-val_zi - 1)
    logging.debug("  in:    x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    buf[0] = (val_xi >> 8) & 0xff
    buf[1] = (val_xi) & 0xff
    buf[2] = (val_yi >> 8) & 0xff
    buf[3] = (val_yi) & 0xff
    buf[4] = (val_zi >> 8) & 0xff
    buf[5] = (val_zi) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_gps_from_bytes(buf):
    logging.debug("lpp_gps_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    assert(len(buf) == 9)
    lat_i = int(buf[0] << 16 | buf[1] << 8 | buf[2])
    lon_i = int(buf[3] << 16 | buf[4] << 8 | buf[5])
    alt_i = int(buf[6] << 16 | buf[7] << 8 | buf[8])
    logging.debug("  out:   latitude = %d, longitude = %d, altitude = %d",
                  lat_i, lon_i, alt_i)
    if lat_i >= (1 << 23):
        lat_i = -1 - (lat_i ^ 0xffffff)
    if lon_i >= (1 << 23):
        lon_i = -1 - (lon_i ^ 0xffffff)
    if alt_i >= (1 << 23):
        alt_i = -1 - (alt_i ^ 0xffffff)
    logging.debug("  out:   latitude = %d, longitude = %d, altitude = %d",
                  lat_i, lon_i, alt_i)
    lat = lat_i / 10000.0
    lon = lon_i / 10000.0
    alt = alt_i / 100.0
    logging.debug("  out:   latitude = %f, longitude = %f, altitude = %f",
                  lat, lon, alt)
    return (lat, lon, alt,)


def lpp_gps_to_bytes(data):
    logging.debug("lpp_gps_to_bytes")
    assert(isinstance(data, tuple))
    assert(len(data) == 3)
    lat = data[0]
    lon = data[1]
    alt = data[2]
    logging.debug("  in:    latitude = %f, longitude = %f, altitude = %f",
                  lat, lon, alt)
    buf = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    lat_i = int(lat * 10000)
    lon_i = int(lon * 10000)
    alt_i = int(alt * 100)
    logging.debug("  in:    latitude = %d, longitude = %d, altitude = %d",
                  lat_i, lon_i, alt_i)
    if lat_i < 0:
        lat_i = ~(-lat_i - 1)
    if lon_i < 0:
        lon_i = ~(-lon_i - 1)
    if alt_i < 0:
        alt_i = ~(-alt_i - 1)
    logging.debug("  in:    latitude = %d, longitude = %d, altitude = %d",
                  lat_i, lon_i, alt_i)
    buf[0] = (lat_i >> 16) & 0xff
    buf[1] = (lat_i >> 8) & 0xff
    buf[2] = (lat_i) & 0xff
    buf[3] = (lon_i >> 16) & 0xff
    buf[4] = (lon_i >> 8) & 0xff
    buf[5] = (lon_i) & 0xff
    buf[6] = (alt_i >> 16) & 0xff
    buf[7] = (alt_i >> 8) & 0xff
    buf[8] = (alt_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


LPP_DATA_TYPE = {
    0:      {'name': 'Digital Input', 'size': 1, 'num': 1,
             'decode': lpp_digital_io_from_bytes,
             'encode': lpp_digital_io_to_bytes},
    1:      {'name': 'Digital Output', 'size': 1, 'num': 1,
             'decode': lpp_digital_io_from_bytes,
             'encode': lpp_digital_io_to_bytes},
    2:      {'name': 'Analog Input', 'size': 2, 'num': 1,
             'decode': lpp_analog_io_from_bytes,
             'encode': lpp_analog_io_to_bytes},
    3:      {'name': 'Analog Output', 'size': 2, 'num': 1,
             'decode': lpp_analog_io_from_bytes,
             'encode': lpp_analog_io_to_bytes},
    101:    {'name': 'Illuminance Sensor', 'size': 2, 'num': 1,
             'decode': lpp_illuminance_from_bytes,
             'encode': lpp_illuminance_to_bytes},
    102:    {'name': 'Presence Sensor', 'size': 1, 'num': 1,
             'decode': lpp_presence_from_bytes,
             'encode': lpp_presence_to_bytes},
    103:    {'name': 'Temperature Sensor', 'size': 2, 'num': 1,
             'decode': lpp_temperature_from_bytes,
             'encode': lpp_temperature_to_bytes},
    104:    {'name': 'Humidity Sensor', 'size': 1, 'num': 1,
             'decode': lpp_humidity_from_bytes,
             'encode': lpp_humidity_to_bytes},
    113:    {'name': 'Accelerometer', 'size': 6, 'num': 3,
             'decode': lpp_accel_from_bytes,
             'encode': lpp_accel_to_bytes},
    115:    {'name': 'Barometer', 'size': 2, 'num': 1,
             'decode': lpp_baro_from_bytes,
             'encode': lpp_baro_to_bytes},
    134:    {'name': 'Gyrometer', 'size': 6, 'num': 3,
             'decode': lpp_gyro_from_bytes,
             'encode': lpp_gyro_to_bytes},
    136:    {'name': 'GPS Location', 'size': 9, 'num': 3,
             'decode': lpp_gps_from_bytes,
             'encode': lpp_gps_to_bytes}
}
