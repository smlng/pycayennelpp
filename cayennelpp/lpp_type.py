try:
    import logging
except ImportError:
    class logging:
        def debug(self, *args, **kwargs):
            pass


def __from_bytes(buf, buflen):
    """
    internal function to parse number from buffer
    """
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    if not len(buf) == buflen:
        raise AssertionError()
    val = 0
    for i in range(buflen):
        shift = (buflen - i - 1) * 8
        val |= buf[i] << shift
    logging.debug("  out:   value = %d", val)
    return val


def __to_s16(val):
    """
    internal function to convert a 16bit number to signed
    """
    logging.debug("  in:    value = %d", val)
    if val >= (1 << 15):
        val = -1 - (val ^ 0xffff)
    logging.debug("  out:   value = %d", val)
    return val


def __to_s24(val):
    """
    internal function to convert a 24bit number to signed
    """
    logging.debug("  in:    value = %d", val)
    if val >= (1 << 23):
        val = -1 - (val ^ 0xffffff)
    logging.debug("  out:   value = %d", val)
    return val


def lpp_digital_io_from_bytes(buf):
    """
    Decode digitial input/output from CyaenneLPP byte buffer,
    and return the value as a tupel.
    """
    logging.debug("lpp_digital_io_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    if not len(buf) == 1:
        raise AssertionError()
    val = buf[0]
    logging.debug("  out:   value = %d", val)
    return (val,)


def lpp_digital_io_to_bytes(data):
    """
    Encode digitial input/output into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_digital_io_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise AssertionError()
    val = data[0]
    logging.debug("  in:    value = %d", val)
    buf = bytearray([0x00])
    buf[0] = (val) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_voltage_from_bytes(buf):
    """
    Decode voltage from CyaenneLPP byte buffer,
    and return the value as a tuple.
    """
    logging.debug("lpp_voltage_from_bytes")
    val_i = __from_bytes(buf, 2)
    if val_i >= (1 << 15):
        logging.error("Negative Voltage value is not allowed")
        raise AssertionError("Negative values are not allowed.")
    val = val_i / 100.0
    logging.debug("  out:   value = %f", val)
    return (val,)


def lpp_voltage_to_bytes(data):
    """
    Encode voltage into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_voltage_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise AssertionError()
    val = data[0]
    if val < 0:
        logging.error("Negative Voltage value is not allowed")
        raise AssertionError("Negative values are not allowed")
    logging.debug("  in:    value = %f", val)
    buf = bytearray([0x00, 0x00])
    val_i = int(val * 100)
    logging.debug("  in:    value = %d", val_i)
    buf[0] = (val_i >> 8) & 0xff
    buf[1] = (val_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_analog_io_from_bytes(buf):
    """
    Decode analog input/output from CyaenneLPP byte buffer,
    and return the value as a tupel.
    """
    logging.debug("lpp_analog_io_from_bytes")
    val_i = __from_bytes(buf, 2)
    val_i = __to_s16(val_i)
    val = val_i / 100.0
    logging.debug("  out:   value = %f", val)
    return (val,)


def lpp_analog_io_to_bytes(data):
    """
    Encode analog input/output into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_analog_io_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise AssertionError()
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


def lpp_generic_from_bytes(buf):
    """
    Convert a 4 byte unsigned integer from bytes.
    """
    logging.debug("lpp_generic_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    if not len(buf) == 4:
        raise AssertionError()
    val_i = ((buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3])
    logging.debug("  out:   value = %d", val_i)
    return (val_i,)


def lpp_generic_to_bytes(data):
    """
    Convert an unsigned 4 byte integer to byte array.
    """
    logging.debug("lpp_generic_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise ValueError("Only one value allowed.")
    buf = bytearray([0x00, 0x00, 0x00, 0x00])
    val = data[0]
    logging.debug("  in:    value = %s", val)
    val_i = int(val)
    logging.debug("  in:    value = %i", val_i)
    if val_i < 0:
        raise ValueError("Negative values are not allowed")
    if val_i > 4294967295:
        raise ValueError("Values larger than 4294967295 are not allowed")
    logging.debug("  in:    value = %d", val_i)
    buf[0] = (val_i >> 24) & 0xff
    buf[1] = (val_i >> 16) & 0xff
    buf[2] = (val_i >> 8) & 0xff
    buf[3] = (val_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_unix_time_from_bytes(buf):
    """
    Convert a 4 byte unsigned integer (unix timestamp) to datetime object.
    Assume timezone is utc.
    """
    from datetime import datetime
    from datetime import timezone as tz
    logging.debug("lpp_unix_time_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    if not len(buf) == 4:
        raise AssertionError()
    val_i = ((buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3])
    logging.debug("  out:   value = %d", val_i)
    if val_i >= (1 << 31):
        raise ValueError("Unix timestamp can not be negative.")
    logging.debug("  out:   value = %d", val_i)
    val = datetime.fromtimestamp(val_i, tz.utc)
    return (val,)


def lpp_unix_time_to_bytes(data):
    """
    Convert a datetime object or integer to unsigned 4 byte unix timestamp.
    integer. Convert the datetime to utc first.
    If it is an integer, assume it already is in utc timezone.
    If it is a naive datetime object, assume it is in the system timezone.
    """
    from datetime import datetime
    from datetime import timezone as tz
    logging.debug("lpp_untix_time_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise ValueError("Only one value allowed.")
    val = data[0]
    logging.debug("  in:    value = %s", val)
    buf = bytearray([0x00, 0x00, 0x00, 0x00])
    epoch = datetime.fromtimestamp(0, tz.utc)
    if isinstance(val, datetime):
        from .utils import datetime_as_utc
        val = datetime_as_utc(val.replace(microsecond=0))
        # val = val.replace(microsecond=0).astimezone(tz.utc)
        if val < epoch:
            raise ValueError("Date/times before 1970-01-01 08:00 UTC"
                             "are not allowed")
        val = val.timestamp()
    logging.debug("  in:    value = %f", val)
    val_i = int(val)
    logging.debug("  in:    value = %i", val_i)
    if val_i < 0:
        raise ValueError("Negative values are not allowed")
    logging.debug("  in:    value = %d", val_i)
    buf[0] = (val_i >> 24) & 0xff
    buf[1] = (val_i >> 16) & 0xff
    buf[2] = (val_i >> 8) & 0xff
    buf[3] = (val_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_illuminance_from_bytes(buf):
    """
    Decode illuminance sensor data from CyaenneLPP byte buffer,
    and return the value as a tupel.
    """
    logging.debug("lpp_illuminance_from_bytes")
    val = int(__from_bytes(buf, 2))
    return (val,)


def lpp_illuminance_to_bytes(data):
    """
    Encode illuminance sensor data into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_illuminance_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise AssertionError()
    val = data[0]
    logging.debug("  in:    value = %d", val)
    if not val >= 0:
        raise AssertionError()
    buf = bytearray([0x00, 0x00])
    buf[0] = (val >> 8) & 0xff
    buf[1] = (val) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_presence_from_bytes(buf):
    """
    Decode presence sensor data from CyaenneLPP byte buffer,
    and return the value as a tupel.
    """
    logging.debug("lpp_presence_from_bytes")
    val = __from_bytes(buf, 1)
    return (val,)


def lpp_presence_to_bytes(data):
    """
    Encode presence sensor data into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_presence_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise AssertionError()
    val = data[0]
    logging.debug("  in:    value = %d", val)
    if not val >= 0:
        raise AssertionError()
    buf = bytearray([0x00])
    buf[0] = (val) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_temperature_from_bytes(buf):
    """
    Decode temperature sensor data from CyaenneLPP byte buffer,
    and return the value as a tupel.
    """
    logging.debug("lpp_temperature_from_bytes")
    val_i = __from_bytes(buf, 2)
    val_i = __to_s16(val_i)
    val = val_i / 10.0
    logging.debug("  out:   value = %f", val)
    return (val, )


def lpp_temperature_to_bytes(data):
    """
    Encode temperature sensor data into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_temperature_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise AssertionError()
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
    """
    Decode himidity sensor data from CyaenneLPP byte buffer,
    and return the value as a tupel.
    """
    logging.debug("lpp_humidity_from_bytes")
    val_i = __from_bytes(buf, 1)
    val = val_i / 2.0
    logging.debug("  out:   value = %f", val)
    return (val, )


def lpp_humidity_to_bytes(data):
    """
    Encode humidity sensor data into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_humidity_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise AssertionError()
    val = data[0]
    logging.debug("  in:    value = %f", val)
    if not val >= 0:
        raise AssertionError()
    buf = bytearray([0x00])
    val_i = int(val * 2)
    logging.debug("  in:    value = %d", val_i)
    buf[0] = (val_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_accel_from_bytes(buf):
    """
    Decode accelerometer sensor data from CyaenneLPP byte buffer,
    and return the values as a tupel.
    """
    logging.debug("lpp_accel_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    if not len(buf) == 6:
        raise AssertionError()
    val_xi = __from_bytes(buf[0:2], 2)
    val_yi = __from_bytes(buf[2:4], 2)
    val_zi = __from_bytes(buf[4:6], 2)
    logging.debug("  out:   x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    val_xi = __to_s16(val_xi)
    val_yi = __to_s16(val_yi)
    val_zi = __to_s16(val_zi)
    logging.debug("  out:   x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    val_x = val_xi / 1000.0
    val_y = val_yi / 1000.0
    val_z = val_zi / 1000.0
    logging.debug("  out:   x = %f, y = %f, z = %f", val_x, val_y, val_z)
    return (val_x, val_y, val_z,)


def lpp_accel_to_bytes(data):
    """
    Encode accelerometer sensor data into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_accel_to_bytes")
    if not isinstance(data, tuple):
        raise AssertionError()
    if not len(data) == 3:
        raise AssertionError()
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
    """
    Decode barometer sensor data from CyaenneLPP byte buffer,
    and return the value as a tupel.
    """
    logging.debug("lpp_baro_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    if not len(buf) == 2:
        raise AssertionError()
    val = __from_bytes(buf, 2)
    val = val / 10.0
    logging.debug("  out:   value = %f", val)
    return (val,)


def lpp_baro_to_bytes(data):
    """
    Encode barometer sensor data into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_baro_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise AssertionError()
    val = data[0]
    logging.debug("  in:    value = %f", val)
    if not val >= 0:
        raise AssertionError()
    buf = bytearray([0x00, 0x00])
    val_i = int(val * 10)
    buf[0] = (val_i >> 8) & 0xff
    buf[1] = (val_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_gyro_from_bytes(buf):
    """
    Decode gyrometer sensor data from CyaenneLPP byte buffer,
    and return the values as a tupel.
    """
    logging.debug("lpp_gyro_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    if not len(buf) == 6:
        raise AssertionError()
    val_xi = __from_bytes(buf[0:2], 2)
    val_yi = __from_bytes(buf[2:4], 2)
    val_zi = __from_bytes(buf[4:6], 2)
    logging.debug("  out:   x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    val_xi = __to_s16(val_xi)
    val_yi = __to_s16(val_yi)
    val_zi = __to_s16(val_zi)
    logging.debug("  out:   x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    val_x = val_xi / 100.0
    val_y = val_yi / 100.0
    val_z = val_zi / 100.0
    logging.debug("  out:   x = %f, y = %f, z = %f", val_x, val_y, val_z)
    return (val_x, val_y, val_z,)


def lpp_gyro_to_bytes(data):
    """
    Encode gyrometer sensor data into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_gyro_to_bytes")
    if not isinstance(data, tuple):
        raise AssertionError()
    if not len(data) == 3:
        raise AssertionError()
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
    """
    Decode GPS data from CyaenneLPP byte buffer,
    and return the values as a tupel.
    """
    logging.debug("lpp_gps_from_bytes")
    logging.debug("  in:    bytes = %s, length = %d", buf, len(buf))
    if not len(buf) == 9:
        raise AssertionError()
    lat_i = __from_bytes(buf[0:3], 3)
    lon_i = __from_bytes(buf[3:6], 3)
    alt_i = __from_bytes(buf[6:9], 3)
    logging.debug("  out:   latitude = %d, longitude = %d, altitude = %d",
                  lat_i, lon_i, alt_i)
    lat_i = __to_s24(lat_i)
    lon_i = __to_s24(lon_i)
    alt_i = __to_s24(alt_i)
    logging.debug("  out:   latitude = %d, longitude = %d, altitude = %d",
                  lat_i, lon_i, alt_i)
    lat = lat_i / 10000.0
    lon = lon_i / 10000.0
    alt = alt_i / 100.0
    logging.debug("  out:   latitude = %f, longitude = %f, altitude = %f",
                  lat, lon, alt)
    return (lat, lon, alt,)


def lpp_gps_to_bytes(data):
    """
    Encode GPS data into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_gps_to_bytes")
    if not isinstance(data, tuple):
        raise AssertionError()
    if not len(data) == 3:
        raise AssertionError()
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


def lpp_load_from_bytes(buf):
    """
    Decode load from CyaenneLPP byte buffer,
    and return the value as a tuple.
    """
    logging.debug("lpp_load_from_bytes")
    val_i = __from_bytes(buf, 3)
    val_i = __to_s24(val_i)
    val = val_i / 1000.0
    logging.debug("  out:   value = %f", val)
    return (val,)


def lpp_load_to_bytes(data):
    """
    Encode load into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_load_to_bytes")
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == 1:
        raise AssertionError()
    val = data[0]
    logging.debug("  in:    value = %f", val)
    buf = bytearray([0x00, 0x00, 0x00])
    val_i = int(val * 1000)
    logging.debug("  in:    value = %d", val_i)
    if val_i < 0:
        val_i = ~(-val_i - 1)
    logging.debug("  in:    value = %d", val_i)
    buf[0] = (val_i >> 16) & 0xff
    buf[1] = (val_i >> 8) & 0xff
    buf[2] = (val_i) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


class LppType(object):
    """Cayenne LPP type representation

    Attributes:
        tid (int):  LPP type ID number
        name (str): human readable type description
        size (int): predefined/fixes byte size
        dim (int):  dimension of the data, i.e. number of values
        decode:     decode function name
        encode:     encode function name
    """
    def __init__(self, tid, name, size, dim, decode, encode):
        if not isinstance(tid, int):
            raise AssertionError()
        if not isinstance(name, str):
            raise AssertionError()
        if not isinstance(size, int):
            raise AssertionError()
        if not isinstance(dim, int):
            raise AssertionError()
        self.tid = tid
        self.name = name
        self.size = size
        self.dimension = dim
        self.decode = decode
        self.encode = encode


LPP_TYPES = [
    LppType(0, 'Digital Input', 1, 1,
            lpp_digital_io_from_bytes, lpp_digital_io_to_bytes),
    LppType(1, 'Digital Output', 1, 1,
            lpp_digital_io_from_bytes, lpp_digital_io_to_bytes),
    LppType(2, 'Analog Input', 2, 1,
            lpp_analog_io_from_bytes, lpp_analog_io_to_bytes),
    LppType(3, 'Analog Output', 2, 1,
            lpp_analog_io_from_bytes, lpp_analog_io_to_bytes),
    LppType(100, 'Generic', 4, 1,
            lpp_generic_from_bytes, lpp_generic_to_bytes),
    LppType(101, 'Illuminance Sensor', 2, 1,
            lpp_illuminance_from_bytes, lpp_illuminance_to_bytes),
    LppType(102, 'Presence Sensor', 1, 1,
            lpp_presence_from_bytes, lpp_presence_to_bytes),
    LppType(103, 'Temperature Sensor', 2, 1,
            lpp_temperature_from_bytes, lpp_temperature_to_bytes),
    LppType(104, 'Humidity Sensor', 1, 1,
            lpp_humidity_from_bytes, lpp_humidity_to_bytes),
    LppType(113, 'Accelerometer', 6, 3,
            lpp_accel_from_bytes, lpp_accel_to_bytes),
    LppType(115, 'Barometer', 2, 1,
            lpp_baro_from_bytes, lpp_baro_to_bytes),
    LppType(116, 'Voltage', 2, 1,
            lpp_voltage_from_bytes, lpp_voltage_to_bytes),
    LppType(122, 'Load', 3, 1,
            lpp_load_from_bytes, lpp_load_to_bytes),
    LppType(133, 'Unix Time', 4, 1,
            lpp_unix_time_from_bytes, lpp_unix_time_to_bytes),
    LppType(134, 'Gyrometer', 6, 3,
            lpp_gyro_from_bytes, lpp_gyro_to_bytes),
    LppType(136, 'GPS Location', 9, 3,
            lpp_gps_from_bytes, lpp_gps_to_bytes)
]


def get_lpp_type(tid):
    """Returns the LppType instance for a given `tid` or `None` if not found"""
    if not isinstance(tid, int):
        raise AssertionError()
    # `next` on MicroPython does not support `default` parameter
    # use try/except construct instead
    # https://docs.micropython.org/en/latest/genrst/modules.html#second-argument-to-next-is-not-implemented
    try:
        return next(filter(lambda x: x.tid == tid, LPP_TYPES))
    except StopIteration:
        return None
