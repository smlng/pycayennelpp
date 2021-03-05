from .lpp_data import LppData

try:
    import logging
except ImportError:
    class logging:
        def debug(self, *args, **kwargs):
            pass


class LppFrame(object):
    """A LPP frame representation which can hold multiple LppData objects

    Attributes:
        data (list): a list of LppData objects
    """

    def __init__(self, data=None, maxsize=0):
        """Create a LppFrame object with (optional)
        a list of LppData elements `data`
        """
        self._maxsize = maxsize
        self.data = []
        if data:
            if not isinstance(self.data, list):
                raise AssertionError()
            for d in data:
                self.__add_data_item(d)

    def __str__(self):
        """Return a pretty string representation of the LppFrame instance"""
        logging.debug("LppFrame.__str__")
        out = "LppFrame(data = ["
        if self.data:
            out = out + "\n"
        for d in self.data:
            out = out + "  " + str(d) + "\n"
        out = out + "])"
        return out

    def __len__(self):
        """Return number of data elements in a LppFrame"""
        return len(self.data)

    def __iter__(self):
        """Return an iterator over all data elements in a LppFrame"""
        count = 0
        while count < len(self.data):
            yield self.data[count]
            count += 1

    @classmethod
    def from_bytes(cls, buf):
        """Parse LppFrame from a given byte string"""
        logging.debug("LppFrame.from_bytes: buf=%s, length=%d", buf, len(buf))
        i = 0
        data = []
        while i < len(buf):
            logging.debug("  loop: index = %d", i)
            lppdata = LppData.from_bytes(buf[i:])
            data.append(lppdata)
            i = i + lppdata.bytes_size()
        return cls(data)

    def __add_data_item(self, item):
        if not isinstance(item, LppData):
            raise TypeError()
        if self.maxsize > 0:
            if self.size + item.size > self.maxsize:
                raise BufferError()
        self.data.append(item)

    def bytes(self):
        """Convert LppFrame instance into a byte string"""
        buf = bytearray()
        for d in self.data:
            buf = buf + d.bytes()
        return buf

    @property
    def maxsize(self):
        """Return max allowed byte size for this frame"""
        return self._maxsize

    @maxsize.setter
    def maxsize(self, value):
        if value < 0:
            raise ValueError("Maxsize must be positive integer.")
        if value > 0 and value < self.size:
            raise ValueError("Maxsize must be greater than current frame size")
        self._maxsize = value

    def reset(self):
        """Reset LppFrame by clearing the list of LppData instances"""
        self.data.clear()

    @property
    def size(self):
        """Return the length of the LppFrame byte string representation"""
        logging.debug("LppFrame.size")
        size = 0
        for d in self.data:
            size += d.size
        return size

    def get_by_type(self, type):
        """Return a sub list of LppFrame data with items matching given type"""
        return list(filter(lambda t: (int(t.type) == type), self.data))

    def add_digital_input(self, channel, value):
        """Create and add a digital input LppData"""
        din = LppData(channel, 0, (value, ))
        self.__add_data_item(din)

    def add_digital_output(self, channel, value):
        """Create and add a digital output LppData"""
        dout = LppData(channel, 1, (value, ))
        self.__add_data_item(dout)

    def add_analog_input(self, channel, value):
        """Create and add an analog input LppData"""
        ain = LppData(channel, 2, (value, ))
        self.__add_data_item(ain)

    def add_analog_output(self, channel, value):
        """Create and add an analog output LppData"""
        aout = LppData(channel, 3, (value, ))
        self.__add_data_item(aout)

    def add_generic(self, channel, value):
        """Create and add a generic 4-byte unsigned integer LppData"""
        din = LppData(channel, 100, (value, ))
        self.__add_data_item(din)

    def add_luminosity(self, channel, value):
        """Create and add an illuminance sensor LppData"""
        lux = LppData(channel, 101, (value, ))
        self.__add_data_item(lux)

    def add_presence(self, channel, value):
        """Create and add a presence sensor LppData"""
        pre = LppData(channel, 102, (value, ))
        self.__add_data_item(pre)

    def add_temperature(self, channel, value):
        """Create and add a temperature sensor LppData"""
        temp = LppData(channel, 103, (value, ))
        self.__add_data_item(temp)

    def add_humidity(self, channel, value):
        """Create and add a humidity sensor LppData"""
        hum = LppData(channel, 104, (value, ))
        self.__add_data_item(hum)

    def add_unix_time(self, channel, value):
        """Create and add a unix time sensor LppData"""
        timestamp = LppData(channel, 133, (value, ))
        self.__add_data_item(timestamp)

    def add_accelerometer(self, channel, x, y, z):
        """Create and add a accelerometer sensor LppData"""
        acc = LppData(channel, 113, (x, y, z, ))
        self.__add_data_item(acc)

    def add_pressure(self, channel, value):
        """Create and add a barometer sensor LppData"""
        press = LppData(channel, 115, (value, ))
        self.__add_data_item(press)

    def add_barometer(self, channel, value):
        """Alias method to Create and add a barometer sensor LppData"""
        self.add_pressure(channel, value)

    def add_gyrometer(self, channel, x, y, z):
        """Create and add a gyrometer sensor LppData"""
        gyro = LppData(channel, 134, (x, y, z, ))
        self.__add_data_item(gyro)

    def add_gps(self, channel, lat, lon, alt):
        """Create and add a GPS LppData"""
        gps = LppData(channel, 136, (lat, lon, alt, ))
        self.__add_data_item(gps)

    def add_voltage(self, channel, value):
        """Create and add a voltage LppData"""
        voltage = LppData(channel, 116, (value, ))
        self.__add_data_item(voltage)

    def add_load(self, channel, value):
        """Create and add a load LppData"""
        load = LppData(channel, 122, (value, ))
        self.__add_data_item(load)
