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
        100:    ('Generic Sensor', [4], [1], [False]),
        101:    ('Illuminance', [2], [1], [False]),
        102:    ('Presence', [1], [1], [False]),
        103:    ('Temperature', [2], [10], [True]),
        104:    ('Humidity', [1], [2], [False]),
        113:    ('Accelerometer', [2, 2, 2], [1000, 1000, 1000],
                 [True, True, True]),
        115:    ('Barometer', [2], [10], [False]),
        116:    ('Voltage', [2], [100], [False]),
        117:    ('Current', [2], [1000], [False]),
        118:    ('Frequency', [4], [1], [False]),
        120:    ('Percentage', [1], [1], [False]),
        121:    ('Altitude', [2], [1], [True]),
        122:    ('Load', [3], [1000], [True]),
        125:    ('Concentration', [2], [1], [False]),
        128:    ('Power', [2], [1], [False]),
        130:    ('Distance', [4], [1000], [False]),
        131:    ('Energy', [4], [1000], [False]),
        132:    ('Direction', [2], [1], [False]),
        133:    ('Time', [4], [1], [False]),
        134:    ('Gyrometer', [2, 2, 2], [100, 100, 100],
                 [True, True, True]),
        135:    ('Colour', [1, 1, 1], [1, 1, 1],
                 [False, False, False]),
        136:    ('Location', [3, 3, 3], [10000, 10000, 100],
                 [True, True, True]),
        142:    ('Switch', [1], [1], [False])
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
        if len(sizes) != len(scales) or len(scales) != len(signs):
            raise ValueError('Invalid parameter length: sizes, scales, signs!')
        self.type = type_
        self.name = name
        self.sizes = sizes
        self.scales = scales
        self.signs = signs

    def __int__(self):
        """Return LppType as integer, i.e. its numeric type."""
        return self.type

    def __str__(self):
        """Return LppType as string, i.e. its name."""
        return self.name

    @staticmethod
    def __assert_data_tuple(data, num):
        """Internal helper to ensure data is a tuple of given `num` length."""
        if not isinstance(data, tuple):
            data = (data,)
        if not len(data) == num:
            raise ValueError()
        return data

    @staticmethod
    def __from_bytes(buf):
        """Internal helper to parse a number from buffer."""
        buflen = len(buf)
        val = 0
        for i in range(buflen):
            shift = (buflen - i - 1) * 8
            val |= buf[i] << shift
        return val

    @staticmethod
    def __to_bytes(val, buflen):
        """Internal helper to write a value to a buffer."""
        buf = bytearray(buflen)
        val = int(val)
        for i in range(buflen):
            shift = (buflen - i - 1) * 8
            buf[i] = (val >> shift) & 0xff
        return buf

    @staticmethod
    def __to_signed(val, size):
        """Internal helper to convert unsigned int to signed."""
        mask = 0x00
        for i in range(size):
            mask |= 0xff << (i * 8)
        if val >= (1 << ((size * 8) - 1)):
            val = -1 - (val ^ mask)
        return val

    @staticmethod
    def __to_unsigned(val):
        """Convert signed (2 complement) value to unsigned."""
        if val < 0:
            val = ~(-val - 1)
        return val

    @classmethod
    def get_lpp_type(cls, type_):
        """Return LppType object for given type or `None` if not found."""
        if not isinstance(type_, int):
            raise TypeError('Parameter (type_) must be an integer!')

        if type_ in cls.__lpp_types:
            return cls(type_, *cls.__lpp_types[type_])
        return None

    @property
    def dimension(self):
        """Return number of value dimensions."""
        return len(self.sizes)

    @property
    def size(self):
        """Return size of byte string representation."""
        return sum(self.sizes)

    def decode(self, buf):
        """Parse LppType from a byte string."""
        if len(buf) != sum(self.sizes):
            raise BufferError('Invalid buffer length!')
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
        """Convert LppType into a byte string."""
        data = self.__assert_data_tuple(data, len(self.sizes))
        buf = bytearray(sum(self.sizes))
        pos = 0
        for i in range(len(self.sizes)):
            size = self.sizes[i]
            value = data[i]
            if not self.signs[i] and value < 0:
                raise ValueError('Invalid data, must be non negative!')
            value = int(value * self.scales[i])
            maxval = 1 << (size * 8)
            if value >= maxval:
                raise ValueError('Invalid data, exceed value range!')
            if self.signs[i]:
                value = self.__to_unsigned(value)
            buf[pos:(pos + size)] = self.__to_bytes(value, size)
            pos += size
        return buf
