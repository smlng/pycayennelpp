def __assert_data_tuple(data, num):
    """Internal helper to ensure data is a tuple of given `num` length."""
    if not isinstance(data, tuple):
        data = (data,)
    if not len(data) == num:
        raise AssertionError()
    return data


def __from_bytes(buf, buflen):
    """Internal helper to parse a number from buffer."""
    if not len(buf) == buflen:
        raise AssertionError()
    val = 0
    for i in range(buflen):
        shift = (buflen - i - 1) * 8
        val |= buf[i] << shift
    return val


def __to_bytes(val, buflen):
    """Internal helper to write a value to a buffer."""
    buf = bytearray(buflen)
    for i in range(buflen):
        shift = (buflen - i - 1) * 8
        buf[i] = (val >> shift) & 0xff
    return buf


def __to_signed(val, bits):
    """Internal helper to convert unsigned int to signed of `bits` length."""
    mask = 0x00
    for i in range(int(bits / 8)):
        mask |= 0xff << (i * 8)
    if val >= (1 << (bits - 1)):
        val = -1 - (val ^ mask)
    return val


def __to_s16(val):
    return __to_signed(val, 16)


def __to_s24(val):
    return __to_signed(val, 24)


def __to_unsigned(val):
    """Convert signed (2 complement) value to unsigned."""
    if val < 0:
        val = ~(-val - 1)
    return val


def __from_bytes_s16(buf, scale):
    """Decode 3D sensor data from byte buffer and return values tupel."""
    if not len(buf) == 6:
        raise AssertionError()
    val_xi = __from_bytes(buf[0:2], 2)
    val_yi = __from_bytes(buf[2:4], 2)
    val_zi = __from_bytes(buf[4:6], 2)
    val_xi = __to_s16(val_xi)
    val_yi = __to_s16(val_yi)
    val_zi = __to_s16(val_zi)
    val_x = val_xi / scale
    val_y = val_yi / scale
    val_z = val_zi / scale
    return (val_x, val_y, val_z,)


def __to_bytes_s16(data, scale):
    """Encode 3D Sensor data into CayenneLPP and return byte buffer."""
    data = __assert_data_tuple(data, 3)
    val_x = data[0]
    val_y = data[1]
    val_z = data[2]
    val_xi = int(val_x * scale)
    val_yi = int(val_y * scale)
    val_zi = int(val_z * scale)
    val_xi = __to_unsigned(val_xi)
    val_yi = __to_unsigned(val_yi)
    val_zi = __to_unsigned(val_zi)
    buf = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    buf[0:2] = __to_bytes(val_xi, 2)
    buf[2:4] = __to_bytes(val_yi, 2)
    buf[4:6] = __to_bytes(val_zi, 2)
    return buf


def lpp_digital_io_from_bytes(buf):
    """Decode digitial input/output from byte buffer and return value tuple."""
    val = __from_bytes(buf, 1)
    return (val,)


def lpp_digital_io_to_bytes(data):
    """Encode digitial in/output into CayenneLPP and return byte buffer."""
    data = __assert_data_tuple(data, 1)
    return __to_bytes(data[0], 1)


def lpp_voltage_from_bytes(buf):
    """Decode voltage from byte buffer and return value tuple."""
    val_i = __from_bytes(buf, 2)
    if val_i >= (1 << 15):
        raise AssertionError("Negative values are not allowed.")
    val = val_i / 100.0
    return (val,)


def lpp_voltage_to_bytes(data):
    """Encode voltage into CayenneLPP and return byte buffer."""
    data = __assert_data_tuple(data, 1)
    val = data[0]
    if val < 0:
        raise AssertionError("Negative values are not allowed")
    val_i = int(val * 100)
    return __to_bytes(val_i, 2)


def lpp_analog_io_from_bytes(buf):
    """Decode analog in/output from byte buffer and return value tupel."""
    val_i = __from_bytes(buf, 2)
    val_i = __to_s16(val_i)
    val = val_i / 100.0
    return (val,)


def lpp_analog_io_to_bytes(data):
    """Encode analog in/output into CayenneLPP and return byte buffer."""
    data = __assert_data_tuple(data, 1)
    val = data[0]
    val_i = int(val * 100)
    val_i = __to_unsigned(val_i)
    return __to_bytes(val_i, 2)


def lpp_generic_from_bytes(buf):
    """Decode 4 byte unsigned int from byte buffer and return value tuple."""
    val_i = __from_bytes(buf, 4)
    return (val_i,)


def lpp_generic_to_bytes(data):
    """Encode unsigned 4 byte int into CayenneLpp and return byte buffer."""
    data = __assert_data_tuple(data, 1)
    val_i = int(data[0])
    if val_i < 0:
        raise ValueError("Negative values are not allowed")
    if val_i >= (1 << 32):
        raise ValueError("Values larger than 4294967295 are not allowed")
    return __to_bytes(val_i, 4)


def lpp_unix_time_from_bytes(buf):
    """Decode 4 byte unix timestamp from byte buffer and return value tuple."""
    val_i = __from_bytes(buf, 4)
    if val_i >= (1 << 31):
        raise ValueError("Unix timestamp can not be negative.")
    return (val_i,)


def lpp_unix_time_to_bytes(data):
    """Encode 4 byte unix timestamp into CayenneLpp and return byte buffer."""
    data = __assert_data_tuple(data, 1)
    val_i = int(data[0])
    if val_i < 0:
        raise ValueError("Negative values are not allowed")
    return __to_bytes(val_i, 4)


def lpp_illuminance_from_bytes(buf):
    """Decode illuminance data from byte buffer and return value tupel."""
    val = int(__from_bytes(buf, 2))
    return (val,)


def lpp_illuminance_to_bytes(data):
    """Encode illuminance data into CayenneLPP and return byte buffer."""
    data = __assert_data_tuple(data, 1)
    val_i = int(data[0])
    if val_i < 0:
        raise ValueError("Illuminance sensor values must be positive!")
    return __to_bytes(val_i, 2)


def lpp_presence_from_bytes(buf):
    """Decode presence data byte buffer and return value tupel."""
    val = __from_bytes(buf, 1)
    return (val,)


def lpp_presence_to_bytes(data):
    """Encode presence data into CayenneLPP and return byte buffer."""
    data = __assert_data_tuple(data, 1)
    val_i = int(data[0])
    if val_i < 0:
        raise ValueError("Presence sensor values must be positive!")
    return __to_bytes(val_i, 1)


def lpp_temperature_from_bytes(buf):
    """Decode temperature data byte buffer and return value tupel."""
    val_i = __from_bytes(buf, 2)
    val_i = __to_s16(val_i)
    val = val_i / 10.0
    return (val, )


def lpp_temperature_to_bytes(data):
    """Encode temperature data into CayenneLPP and return byte buffer."""
    data = __assert_data_tuple(data, 1)
    val = data[0]
    val_i = int(val * 10)
    val_i = __to_unsigned(val_i)
    return __to_bytes(val_i, 2)


def lpp_humidity_from_bytes(buf):
    """Decode humidity data from byte buffer and return value tupel."""
    val_i = __from_bytes(buf, 1)
    val = val_i / 2.0
    return (val, )


def lpp_humidity_to_bytes(data):
    """Encode humidity  data into CayenneLPP and return as a byte buffer."""
    data = __assert_data_tuple(data, 1)
    val = data[0]
    val_i = int(val * 2)
    if val_i < 0:
        raise ValueError("Humidity sensor values must be positive!")
    return __to_bytes(val_i, 1)


def lpp_accel_from_bytes(buf):
    """Decode accelerometer data byte buffer and return values tupel."""
    return __from_bytes_s16(buf, 1000.0)


def lpp_accel_to_bytes(data):
    """Encode accelerometer data into CayenneLPP and return byte buffer."""
    return __to_bytes_s16(data, 1000.0)


def lpp_baro_from_bytes(buf):
    """Decode barometer data byte buffer and return value tupel."""
    val = __from_bytes(buf, 2)
    val = val / 10.0
    return (val,)


def lpp_baro_to_bytes(data):
    """Encode barometer data into CayenneLPP and return byte buffer."""
    data = __assert_data_tuple(data, 1)
    val = data[0]
    val_i = int(val * 10)
    if val_i < 0:
        raise ValueError("Barometer sensor values must be positive!")
    return __to_bytes(val_i, 2)


def lpp_gyro_from_bytes(buf):
    """Decode gyrometer data byte buffer and return value tupel."""
    return __from_bytes_s16(buf, 100.0)


def lpp_gyro_to_bytes(data):
    """Encode gyrometer data into CayenneLPP and return byte buffer."""
    return __to_bytes_s16(data, 100.0)


def lpp_gps_from_bytes(buf):
    """Decode GPS data from byte buffer and return value tupel."""
    if not len(buf) == 9:
        raise AssertionError()
    lat_i = __from_bytes(buf[0:3], 3)
    lon_i = __from_bytes(buf[3:6], 3)
    alt_i = __from_bytes(buf[6:9], 3)
    lat_i = __to_s24(lat_i)
    lon_i = __to_s24(lon_i)
    alt_i = __to_s24(alt_i)
    lat = lat_i / 10000.0
    lon = lon_i / 10000.0
    alt = alt_i / 100.0
    return (lat, lon, alt,)


def lpp_gps_to_bytes(data):
    """Encode GPS data into CayenneLPP and return byte buffer."""
    data = __assert_data_tuple(data, 3)
    lat = data[0]
    lon = data[1]
    alt = data[2]
    lat_i = int(lat * 10000)
    lon_i = int(lon * 10000)
    alt_i = int(alt * 100)
    lat_i = __to_unsigned(lat_i)
    lon_i = __to_unsigned(lon_i)
    alt_i = __to_unsigned(alt_i)
    buf = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    buf[0:3] = __to_bytes(lat_i, 3)
    buf[3:6] = __to_bytes(lon_i, 3)
    buf[6:9] = __to_bytes(alt_i, 3)
    return buf


def lpp_load_from_bytes(buf):
    """Decode load from byte buffer and return value tuple."""
    val_i = __from_bytes(buf, 3)
    val_i = __to_s24(val_i)
    val = val_i / 1000.0
    return (val,)


def lpp_load_to_bytes(data):
    """Encode load into CayenneLPP and return byte buffer."""
    data = __assert_data_tuple(data, 1)
    val = data[0]
    val_i = int(val * 1000)
    val_i = __to_unsigned(val_i)
    return __to_bytes(val_i, 3)


class LppType(object):
    """
    Cayenne LPP type object.

    Attributes:
        type (int): LPP type ID number
        name (str): human readable type description
        sizes (list): byte size of values
        scales (list): scaling of values
        signs (list): signess of values
    """

    __lpp_types = {
        0:      ('Digital Input', [1], [1], [False]),
        1:      ('Digital Output', [1], [1], [False]),
        2:      ('Analog Input', [2], [100], [True]),
        3:      ('Analog Output', [2], [100], [True]),
        100:    ('Generic', [4], [1], [False]),
        101:    ('Illuminance Sensor', [2], [1], [False]),
        102:    ('Presence Sensor', [1], [1], [False]),
        103:    ('Temperature Sensor', [2], [10], [True]),
        104:    ('Humidity Sensor', [1], [2], [False]),
        113:    ('Accelerometer', [2,2,2], [1000,1000,1000], [True, True, True]),
        115:    ('Barometer', [2], [10], [False]),
        116:    ('Voltage', [2], [100], [False]),
        122:    ('Load', [3], [1000], [True]),
        133:    ('Unix Timestamp', [4], [1], [False]),
        134:    ('Gyrometer', [2,2,2], [100,100,100], [True,True,True]),
        136:    ('GPS Location', [3,3,3], [10000,10000,100], [True,True,True])
    }

    def __init__(self, type_, name, sizes, scales, signs):
        """Create a LppType object with given attributes."""
        if not isinstance(type_, int):
            raise TypeError('Parameter (type_) must be an integer!')
        if not isinstance(name, str):
            raise TypeError('Parameter (name) must be a string!')
        if not isinstance(sizes, list):
            raise TypeError('Parameter (sizes) must be a list of integers!')
        if not isinstance(scales, list):
            raise TypeError('Parameter (scales) must be a list of integers!')
        if not isinstance(signs, list):
            raise TypeError('Parameter (signs) must be a list of integers!')
        if type_ not in self.__lpp_types:
            raise ValueError('Invalid parameter: unknown type!')
        if len(sizes) != len(scales) or len(scales) != len(signs):
            raise ValueError('Invalid parameters: (sizes, scales, signs) must be of equal length!')
        self.type = type_
        self.name = name
        self.sizes = sizes
        self.scales = scales
        self.signs = signs

    def __int__(self):
        """Return LppType attribute as integer."""
        return self.type

    def __assert_data_tuple(self, data, num):
        """Internal helper to ensure data is a tuple of given `num` length."""
        if not isinstance(data, tuple):
            data = (data,)
        if not len(data) == num:
            raise AssertionError()
        return data

    def __from_bytes(self, buf):
        """Internal helper to parse a number from buffer."""
        buflen = len(buf)
        val = 0
        for i in range(buflen):
            shift = (buflen - i - 1) * 8
            val |= buf[i] << shift
        return val

    def __to_bytes(self, val, buflen):
        """Internal helper to write a value to a buffer."""
        buf = bytearray(buflen)
        val = int(val)
        for i in range(buflen):
            shift = (buflen - i - 1) * 8
            buf[i] = (val >> shift) & 0xff
        return buf

    def __to_signed(self, val, size):
        """Internal helper to convert unsigned int to signed."""
        mask = 0x00
        for i in range(size):
            mask |= 0xff << (i * 8)
        if val >= (1 << ((size * 8) - 1)):
            val = -1 - (val ^ mask)
        return val

    def __to_unsigned(self, val):
        """Convert signed (2 complement) value to unsigned."""
        if val < 0:
            val = ~(-val - 1)
        return val

    @classmethod
    def get_lpp_type(cls, type_):
        """Returns LppType object for given type or `None` if not found."""
        if not isinstance(type_, int):
            raise TypeError('Parameter (type_) must be an integer!')

        if type_ in cls.__lpp_types:
            return cls(type_, *cls.__lpp_types[type_])
        return None

    @property
    def dimension(self):
        return len(self.sizes)

    @property
    def size(self):
        return sum(self.sizes)

    def decode(self, buf):
        if len(buf) != sum(self.sizes):
            raise BufferError('Invalid buffer length, does not match data sizes!')
        data = []
        pos = 0
        for i in range(len(self.sizes)):
            size = self.sizes[i]
            value = self.__from_bytes(buf[pos:(pos + size)])
            if self.signs[i]:
                value = self.__to_signed(value, size)
            value = value / self.scales[i]
            data.append(value)
            pos += size
        return tuple(data)

    def encode(self, data):
        data = self.__assert_data_tuple(data, len(self.sizes))
        buf = bytearray(sum(self.sizes))
        pos = 0
        for i in range(len(self.sizes)):
            size = self.sizes[i]
            value = data[i]
            value *= self.scales[i]
            if not self.signs[i]:
                if value < 0:
                    raise ValueError('Invalid data, must be non negative!')
                maxval = 1 << (size * 8)
                if value >= maxval:
                    raise ValueError('Invalid data, exceed value range!')
                value = self.__to_unsigned(value)
            buf[pos:(pos + size)] = self.__to_bytes(value, size)
            pos += size
        return buf
