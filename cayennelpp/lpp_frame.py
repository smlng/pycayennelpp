from .lpp_data import LppData


class LppFrame(object):
    """
    A LPP frame instance which can hold multiple LppData objects.

    Attributes:
        data (list): a list of LppData objects
        maxsize (int): (otpional) byte size limit
    """

    def __init__(self, data=None, maxsize=0):
        """Create a LppFrame object with (optional) arguments."""
        self._maxsize = maxsize
        self._data = []
        if data:
            for d in data:
                self.__add_data_item(d)

    def __str__(self):
        """Return a pretty string representation of the LppFrame object."""
        out = "LppFrame(data = ["
        if self._data:
            out = out + "\n"
        for d in self._data:
            out = out + "  " + str(d) + "\n"
        out = out + "])"
        return out

    def __len__(self):
        """Return the number of LppData items in this LppFrame."""
        return len(self._data)

    def __iter__(self):
        """Return an iterator over all LppData items in this LppFrame."""
        count = 0
        while count < len(self._data):
            yield self._data[count]
            count += 1

    def __bytes__(self):
        """Return this LppFrame object as a byte string."""
        buf = bytearray()
        for d in self._data:
            buf = buf + bytes(d)
        return bytes(buf)

    @classmethod
    def from_bytes(cls, buf):
        """Parse a given byte string and return as a LppFrame object."""
        i = 0
        data = []
        while i < len(buf):
            lppdata = LppData.from_bytes(buf[i:])
            data.append(lppdata)
            i = i + len(lppdata)
        return cls(data)

    def __add_data_item(self, item):
        """Helper function to add an LppData item to this LppFrame."""
        if not isinstance(item, LppData):
            raise TypeError()
        if self.maxsize > 0:
            if self.size + len(item) > self.maxsize:
                raise BufferError()
        self._data.append(item)

    @property
    def data(self):
        """Return list of data items."""
        return self._data

    @property
    def maxsize(self):
        """Return max allowed byte size for this LppFrame."""
        return self._maxsize

    @maxsize.setter
    def maxsize(self, value):
        """Set the max byte size for this LppFrame."""
        if value < 0:
            raise ValueError("Maxsize must be positive integer.")
        if value > 0 and value < self.size:
            raise ValueError("Maxsize must be greater than current frame size")
        self._maxsize = value

    def reset(self):
        """Reset LppFrame by clearing the list of LppData items."""
        self._data.clear()

    @property
    def size(self):
        """Return the length of the LppFrame byte string representation."""
        size = 0
        for d in self._data:
            size += len(d)
        return size

    def get_by_type(self, type_):
        """Return sub list of LppFrame data with items matching given type."""
        return list(filter(lambda t: (int(t.type) == type_), self.data))

    def add_digital_input(self, channel, value):
        """Create and add a digital input LppData item."""
        din = LppData(channel, 0, (value, ))
        self.__add_data_item(din)

    def add_digital_output(self, channel, value):
        """Create and add a digital output LppData item."""
        dout = LppData(channel, 1, (value, ))
        self.__add_data_item(dout)

    def add_analog_input(self, channel, value):
        """Create and add an analog input LppData item."""
        ain = LppData(channel, 2, (value, ))
        self.__add_data_item(ain)

    def add_analog_output(self, channel, value):
        """Create and add an analog output LppData item."""
        aout = LppData(channel, 3, (value, ))
        self.__add_data_item(aout)

    def add_generic(self, channel, value):
        """Create and add a generic 4-byte unsigned integer LppData item."""
        din = LppData(channel, 100, (value, ))
        self.__add_data_item(din)

    def add_luminosity(self, channel, value):
        """Create and add an illuminance sensor LppData item."""
        lux = LppData(channel, 101, (value, ))
        self.__add_data_item(lux)

    def add_presence(self, channel, value):
        """Create and add a presence sensor LppData item."""
        pre = LppData(channel, 102, (value, ))
        self.__add_data_item(pre)

    def add_temperature(self, channel, value):
        """Create and add a temperature sensor LppData item."""
        temp = LppData(channel, 103, (value, ))
        self.__add_data_item(temp)

    def add_humidity(self, channel, value):
        """Create and add a humidity sensor LppData item."""
        hum = LppData(channel, 104, (value, ))
        self.__add_data_item(hum)

    def add_unix_time(self, channel, value):
        """Create and add a unix time sensor LppData item."""
        timestamp = LppData(channel, 133, (value, ))
        self.__add_data_item(timestamp)

    def add_accelerometer(self, channel, x, y, z):
        """Create and add a accelerometer sensor LppData item."""
        acc = LppData(channel, 113, (x, y, z, ))
        self.__add_data_item(acc)

    def add_pressure(self, channel, value):
        """Create and add a barometer sensor LppData item."""
        press = LppData(channel, 115, (value, ))
        self.__add_data_item(press)

    def add_barometer(self, channel, value):
        """Alias method to Create and add a barometer sensor LppData item."""
        self.add_pressure(channel, value)

    def add_gyrometer(self, channel, x, y, z):
        """Create and add a gyrometer sensor LppData item."""
        gyro = LppData(channel, 134, (x, y, z, ))
        self.__add_data_item(gyro)

    def add_gps(self, channel, lat, lon, alt):
        """Create and add a GPS sensor LppData item."""
        gps = LppData(channel, 136, (lat, lon, alt, ))
        self.__add_data_item(gps)

    def add_voltage(self, channel, value):
        """Create and add a voltage sensor LppData item."""
        voltage = LppData(channel, 116, (value, ))
        self.__add_data_item(voltage)

    def add_load(self, channel, value):
        """Create and add a load sensor LppData item."""
        load = LppData(channel, 122, (value, ))
        self.__add_data_item(load)
