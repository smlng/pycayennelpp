from .lpp_data import LppData

import base64
import logging


class LppFrame(object):
    """A LPP frame representation which can hold multiple LppData objects

    Attributes:
        data (list): a list of LppData objects
    """
    def __init__(self, data=None):
        self.data = data or []
        if not isinstance(self.data, list):
            raise AssertionError()
        for d in self.data:
            if not isinstance(d, LppData):
                raise AssertionError()

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

    @classmethod
    def from_base64(cls, strb64):
        """Parse LppFrame from a given base64 encoded string"""
        logging.debug("LppFrame.from_base64: base64=%s, length=%d",
                      strb64, len(strb64))
        return cls.from_bytes(base64.decodebytes(strb64.encode('ascii')))

    def bytes(self):
        """Convert LppFrame instance into a byte string"""
        buf = bytearray()
        for d in self.data:
            buf = buf + d.bytes()
        return buf

    def reset(self):
        """Reset LppFrame by clearing the list of LppData instances"""
        self.data.clear()

    def add_digital_input(self, channel, value):
        """Create and add a digital input LppData"""
        din = LppData(channel, 0, (value, ))
        self.data.append(din)

    def add_digital_output(self, channel, value):
        """Create and add a digital output LppData"""
        dout = LppData(channel, 1, (value, ))
        self.data.append(dout)

    def add_analog_input(self, channel, value):
        """Create and add an analog input LppData"""
        ain = LppData(channel, 2, (value, ))
        self.data.append(ain)

    def add_analog_output(self, channel, value):
        """Create and add an analog output LppData"""
        aout = LppData(channel, 3, (value, ))
        self.data.append(aout)

    def add_luminosity(self, channel, value):
        """Create and add an illuminance sensor LppData"""
        lux = LppData(channel, 101, (value, ))
        self.data.append(lux)

    def add_presence(self, channel, value):
        """Create and add a presence sensor LppData"""
        pre = LppData(channel, 102, (value, ))
        self.data.append(pre)

    def add_temperature(self, channel, value):
        """Create and add a temperature sensor LppData"""
        temp = LppData(channel, 103, (value, ))
        self.data.append(temp)

    def add_humitidy(self, channel, value):
        """Create and add a humidity sensor LppData"""
        hum = LppData(channel, 104, (value, ))
        self.data.append(hum)

    def add_accelerometer(self, channel, x, y, z):
        """Create and add a accelerometer sensor LppData"""
        acc = LppData(channel, 113, (x, y, z, ))
        self.data.append(acc)

    def add_pressure(self, channel, value):
        """Create and add a barometer sensor LppData"""
        press = LppData(channel, 115, (value, ))
        self.data.append(press)

    def add_barometer(self, channel, value):
        """Alias method to Create and add a barometer sensor LppData"""
        self.add_pressure(channel, value)

    def add_gyrometer(self, channel, x, y, z):
        """Create and add a gyrometer sensor LppData"""
        gyro = LppData(channel, 134, (x, y, z, ))
        self.data.append(gyro)

    def add_gps(self, channel, lat, lon, alt):
        """Create and add a GPS LppData"""
        gps = LppData(channel, 134, (lat, lon, alt, ))
        self.data.append(gps)
