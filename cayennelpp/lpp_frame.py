from .lpp_data import LppData


class LppFrame(object):
    """
    A LPP frame instance which can hold multiple LppData objects.

    Attributes:
        data (list): a list of LppData objects
        maxsize (int): (optional) byte size limit
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
        """Return sub list of data with items matching given type."""
        return [d for d in self.data if int(d.type) == type_]

    def get_by_name(self, name):
        """Return sub list of data with items matching given name."""
        name = name.strip().lower()
        return [d for d in self.data if str(d.type).lower().startswith(name)]

    def add_by_type(self, type_, channel, value_tuple):
        """Generic helper to add LppDate to this LppFrame."""
        if not isinstance(value_tuple, tuple):
            raise TypeError('Parameter (value_tuple) must be a tuple!')
        data = LppData(channel, type_, value_tuple)
        self.__add_data_item(data)

    def add_digital_input(self, channel, value):
        """Create and add a digital input LppData item."""
        self.add_by_type(0, channel, (value, ))

    def add_digital_output(self, channel, value):
        """Create and add a digital output LppData item."""
        self.add_by_type(1, channel, (value, ))

    def add_analog_input(self, channel, value):
        """Create and add an analog input LppData item."""
        self.add_by_type(2, channel, (value, ))

    def add_analog_output(self, channel, value):
        """Create and add an analog output LppData item."""
        self.add_by_type(3, channel, (value, ))

    def add_generic(self, channel, value):
        """Create and add a generic 4-byte unsigned integer LppData item."""
        self.add_by_type(100, channel, (value, ))

    def add_luminosity(self, channel, value):
        """Create and add an illuminance sensor LppData item."""
        self.add_by_type(101, channel, (value, ))

    def add_presence(self, channel, value):
        """Create and add a presence sensor LppData item."""
        self.add_by_type(102, channel, (value, ))

    def add_temperature(self, channel, value):
        """Create and add a temperature sensor LppData item."""
        self.add_by_type(103, channel, (value, ))

    def add_humidity(self, channel, value):
        """Create and add a humidity sensor LppData item."""
        self.add_by_type(104, channel, (value, ))

    def add_accelerometer(self, channel, x, y, z):
        """Create and add a accelerometer sensor LppData item."""
        self.add_by_type(113, channel, (x, y, z))

    def add_pressure(self, channel, value):
        """Alias method for add_barometer()."""
        self.add_barometer(channel, value)

    def add_barometer(self, channel, value):
        """Create and add a barometer sensor LppData item."""
        self.add_by_type(115, channel, (value, ))

    def add_voltage(self, channel, value):
        """Create and add a voltage sensor LppData item."""
        self.add_by_type(116, channel, (value, ))

    def add_current(self, channel, value):
        """Create and add a current sensor LppData item."""
        self.add_by_type(117, channel, (value, ))

    def add_frequency(self, channel, value):
        """Create and add a frequency sensor LppData item."""
        self.add_by_type(118, channel, (value, ))

    def add_percentage(self, channel, value):
        """Create and add a percentage LppData item."""
        self.add_by_type(120, channel, (value, ))

    def add_altitude(self, channel, value):
        """Create and add a altitude LppData item."""
        self.add_by_type(121, channel, (value, ))

    def add_load(self, channel, value):
        """Create and add a load sensor LppData item."""
        self.add_by_type(122, channel, (value, ))

    def add_concentration(self, channel, value):
        """Create and add a concentration LppData item."""
        self.add_by_type(125, channel, (value, ))

    def add_power(self, channel, value):
        """Create and add a power sensor LppData item."""
        self.add_by_type(128, channel, (value, ))

    def add_distance(self, channel, value):
        """Create and add a distance LppData item."""
        self.add_by_type(130, channel, (value, ))

    def add_energy(self, channel, value):
        """Create and add a energy sensor LppData item."""
        self.add_by_type(131, channel, (value, ))

    def add_direction(self, channel, value):
        """Create and add a direction LppData item."""
        self.add_by_type(132, channel, (value, ))

    def add_unix_time(self, channel, value):
        """Create and add a unix timestamp LppData item."""
        self.add_by_type(133, channel, (value, ))

    def add_gyrometer(self, channel, x, y, z):
        """Create and add a gyrometer sensor LppData item."""
        self.add_by_type(134, channel, (x, y, z))

    def add_colour(self, channel, red, green, blue):
        """Create and add a color sensor LppData item."""
        self.add_by_type(135, channel, (red, green, blue))

    def add_gps(self, channel, lat, lon, alt):
        """Alias method for add_location()."""
        self.add_location(channel, lat, lon, alt)

    def add_location(self, channel, lat, lon, alt):
        """Create and add a location LppData item."""
        self.add_by_type(136, channel, (lat, lon, alt))

    def add_switch(self, channel, value):
        """Create and add a switch LppData item."""
        self.add_by_type(142, channel, (value, ))
