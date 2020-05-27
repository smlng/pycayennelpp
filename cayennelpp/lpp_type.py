try:
    import logging
except ImportError:
    class logging:
        def debug(self, *args, **kwargs):
            pass


def __assert_data_tuple(data, num):
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == num:
        raise AssertionError()
    return data


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


def __to_bytes(val, buflen):
    logging.debug("  in:    value = %d", val)
    buf = bytearray(buflen)
    for i in range(buflen):
        shift = (buflen - i - 1) * 8
        buf[i] = (val >> shift) & 0xff
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def __to_signed(val, bits):
    """
    internal function to convert a unsigned integer to signed
    of given bits length
    """
    logging.debug("  in:    value = %d", val)
    mask = 0x00
    for i in range(int(bits / 8)):
        mask |= 0xff << (i * 8)
    if val >= (1 << (bits - 1)):
        val = -1 - (val ^ mask)
    logging.debug("  out:   value = %d", val)
    return val


def __to_s16(val):
    return __to_signed(val, 16)


def __to_s24(val):
    return __to_signed(val, 24)


def __to_unsigned(val):
    """
    convert signed (2 complement) value to unsigned
    """
    if val < 0:
        val = ~(-val - 1)
    return val


def lpp_digital_io_from_bytes(buf):
    """
    Decode digitial input/output from CyaenneLPP byte buffer,
    and return the value as a tupel.
    """
    logging.debug("lpp_digital_io_from_bytes")
    val = __from_bytes(buf, 1)
    return (val,)


def lpp_digital_io_to_bytes(data):
    """
    Encode digitial input/output into CayenneLPP,
    and return as a byte buffer
    """
    logging.debug("lpp_digital_io_to_bytes")
    data = __assert_data_tuple(data, 1)
    return __to_bytes(data[0], 1)


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
    data = __assert_data_tuple(data, 1)
    val = data[0]
    if val < 0:
        logging.error("Negative Voltage value is not allowed")
        raise AssertionError("Negative values are not allowed")
    logging.debug("  in:    value = %f", val)
    val_i = int(val * 100)
    return __to_bytes(val_i, 2)


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
    data = __assert_data_tuple(data, 1)
    val = data[0]
    logging.debug("  in:    value = %f", val)
    val_i = int(val * 100)
    logging.debug("  in:    value = %d", val_i)
    val_i = __to_unsigned(val_i)
    return __to_bytes(val_i, 2)


def lpp_generic_from_bytes(buf):
    """
    Convert a 4 byte unsigned integer from bytes.
    """
    logging.debug("lpp_generic_from_bytes")
    val_i = __from_bytes(buf, 4)
    return (val_i,)


def lpp_generic_to_bytes(data):
    """
    Convert an unsigned 4 byte integer to byte array.
    """
    logging.debug("lpp_generic_to_bytes")
    data = __assert_data_tuple(data, 1)
    val_i = int(data[0])
    logging.debug("  in:    value = %i", val_i)
    if val_i < 0:
        raise ValueError("Negative values are not allowed")
    if val_i >= (1 << 32):
        raise ValueError("Values larger than 4294967295 are not allowed")
    return __to_bytes(val_i, 4)


def lpp_unix_time_from_bytes(buf):
    """
    Convert a 4 byte unix timestamp (unsigned integer) from bytes.
    """
    logging.debug("lpp_unix_time_from_bytes")
    val_i = __from_bytes(buf, 4)
    if val_i >= (1 << 31):
        raise ValueError("Unix timestamp can not be negative.")
    return (val_i,)


def lpp_unix_time_to_bytes(data):
    """
    Convert an 4 byte unix timestamp (unsigned integer) to byte array.
    """
    logging.debug("lpp_unix_time_to_bytes")
    data = __assert_data_tuple(data, 1)
    val_i = int(data[0])
    logging.debug("  in:    value = %i", val_i)
    if val_i < 0:
        raise ValueError("Negative values are not allowed")
    return __to_bytes(val_i, 4)


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
    data = __assert_data_tuple(data, 1)
    val_i = int(data[0])
    if val_i < 0:
        raise ValueError("Illuminance sensor values must be positive!")
    return __to_bytes(val_i, 2)


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
    data = __assert_data_tuple(data, 1)
    val_i = int(data[0])
    if val_i < 0:
        raise ValueError("Presence sensor values must be positive!")
    return __to_bytes(val_i, 1)


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
    data = __assert_data_tuple(data, 1)
    val = data[0]
    logging.debug("  in:    value = %f", val)
    val_i = int(val * 10)
    logging.debug("  in:    value = %d", val_i)
    val_i = __to_unsigned(val_i)
    return __to_bytes(val_i, 2)


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
    data = __assert_data_tuple(data, 1)
    val = data[0]
    logging.debug("  in:    value = %f", val)
    val_i = int(val * 2)
    if val_i < 0:
        raise ValueError("Humidity sensor values must be positive!")
    return __to_bytes(val_i, 1)


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
    data = __assert_data_tuple(data, 3)
    val_x = data[0]
    val_y = data[1]
    val_z = data[2]
    logging.debug("  in:    x = %f, y = %f, z = %f", val_x, val_y, val_z)
    val_xi = int(val_x * 1000)
    val_yi = int(val_y * 1000)
    val_zi = int(val_z * 1000)
    logging.debug("  in:    x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    val_xi = __to_unsigned(val_xi)
    val_yi = __to_unsigned(val_yi)
    val_zi = __to_unsigned(val_zi)
    logging.debug("  in:    x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    buf = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    buf[0:2] = __to_bytes(val_xi, 2)
    buf[2:4] = __to_bytes(val_yi, 2)
    buf[4:6] = __to_bytes(val_zi, 2)
    logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
    return buf


def lpp_baro_from_bytes(buf):
    """
    Decode barometer sensor data from CyaenneLPP byte buffer,
    and return the value as a tupel.
    """
    logging.debug("lpp_baro_from_bytes")
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
    data = __assert_data_tuple(data, 1)
    val = data[0]
    logging.debug("  in:    value = %f", val)
    val_i = int(val * 10)
    if val_i < 0:
        raise ValueError("Barometer sensor values must be positive!")
    return __to_bytes(val_i, 2)


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
    data = __assert_data_tuple(data, 3)
    val_x = data[0]
    val_y = data[1]
    val_z = data[2]
    logging.debug("  in:    x = %f, y = %f, z = %f", val_x, val_y, val_z)
    val_xi = int(val_x * 100)
    val_yi = int(val_y * 100)
    val_zi = int(val_z * 100)
    logging.debug("  in:    x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    val_xi = __to_unsigned(val_xi)
    val_yi = __to_unsigned(val_yi)
    val_zi = __to_unsigned(val_zi)
    logging.debug("  in:    x = %d, y = %d, z = %d", val_xi, val_yi, val_zi)
    buf = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    buf[0:2] = __to_bytes(val_xi, 2)
    buf[2:4] = __to_bytes(val_yi, 2)
    buf[4:6] = __to_bytes(val_zi, 2)
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
    data = __assert_data_tuple(data, 3)
    lat = data[0]
    lon = data[1]
    alt = data[2]
    logging.debug("  in:    latitude = %f, longitude = %f, altitude = %f",
                  lat, lon, alt)

    lat_i = int(lat * 10000)
    lon_i = int(lon * 10000)
    alt_i = int(alt * 100)
    logging.debug("  in:    latitude = %d, longitude = %d, altitude = %d",
                  lat_i, lon_i, alt_i)
    lat_i = __to_unsigned(lat_i)
    lon_i = __to_unsigned(lon_i)
    alt_i = __to_unsigned(alt_i)
    logging.debug("  in:    latitude = %d, longitude = %d, altitude = %d",
                  lat_i, lon_i, alt_i)
    buf = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    buf[0:3] = __to_bytes(lat_i, 3)
    buf[3:6] = __to_bytes(lon_i, 3)
    buf[6:9] = __to_bytes(alt_i, 3)
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
    data = __assert_data_tuple(data, 1)
    val = data[0]
    logging.debug("  in:    value = %f", val)
    val_i = int(val * 1000)
    logging.debug("  in:    value = %d", val_i)
    val_i = __to_unsigned(val_i)
    logging.debug("  in:    value = %d", val_i)
    return __to_bytes(val_i, 3)


class LppType(object):
    """Cayenne LPP type representation

    Attributes:
        type (int): LPP type ID number
        name (str): human readable type description
        size (int): predefined/fixes byte size
        dim (int):  dimension of the data, i.e. number of values
        decode:     decode function name
        encode:     encode function name
    """

    def __init__(self, type_, name, size, dim, decode, encode):
        """Create a LppType object with given attributes"""
        if not isinstance(type_, int):
            raise AssertionError()
        if not isinstance(name, str):
            raise AssertionError()
        if not isinstance(size, int):
            raise AssertionError()
        if not isinstance(dim, int):
            raise AssertionError()
        self.type = type_
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
    LppType(133, 'Unix Timestamp', 4, 1,
            lpp_unix_time_from_bytes, lpp_unix_time_to_bytes),
    LppType(134, 'Gyrometer', 6, 3,
            lpp_gyro_from_bytes, lpp_gyro_to_bytes),
    LppType(136, 'GPS Location', 9, 3,
            lpp_gps_from_bytes, lpp_gps_to_bytes)
]


def get_lpp_type(type_):
    """Returns a LppType instance for a given `type` or `None` if not found"""
    if not isinstance(type_, int):
        raise AssertionError()
    # `next` on MicroPython does not support `default` parameter
    # use try/except construct instead
    # https://docs.micropython.org/en/latest/genrst/modules.html#second-argument-to-next-is-not-implemented
    try:
        return next(filter(lambda x: x.type == type_, LPP_TYPES))
    except StopIteration:
        return None
