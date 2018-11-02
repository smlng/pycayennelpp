from __future__ import absolute_import

from .lpp_data import LppData

import base64
import logging


class LppFrame(object):

    def __init__(self, data=list()):
        assert(isinstance(data, list))
        assert(isinstance(d, LppData) for d in data)
        self._data = data

    @classmethod
    def from_bytes(cls, bytes):
        logging.debug("LppFrame.from_bytes: bytes=%s, length=%d",
                      bytes, len(bytes))
        i = 0
        data = list()
        while i < len(bytes):
            logging.debug("  loop: index = %d", i)
            lppdata = LppData.from_bytes(bytes[i:])
            data.append(lppdata)
            i = i + lppdata.bytes_size()
        return cls(data)

    @classmethod
    def from_base64(cls, strb64):
        logging.debug("LppFrame.from_base64: base64=%d, length=%d",
                      strb64, len(strb64))
        return cls.from_bytes(base64.decodebytes(strb64.encode('ascii')))

    def data(self):
        return self._data

    def bytes(self):
        buf = bytearray()
        for d in self._data:
            buf = buf + d.bytes()
        return buf

    def reset(self):
        self._data.clear()

    def add_digital_input(self, channel, value):
        din = LppData(channel, 0, (value, ))
        self._data.append(din)

    def add_digital_output(self, channel, value):
        dout = LppData(channel, 1, (value, ))
        self._data.append(dout)

    def add_analog_input(self, channel, value):
        ain = LppData(channel, 2, (value, ))
        self._data.append(ain)

    def add_analog_output(self, channel, value):
        aout = LppData(channel, 3, (value, ))
        self._data.append(aout)

    def add_luminosity(self, channel, value):
        lux = LppData(channel, 101, (value, ))
        self._data.append(lux)

    def add_presence(self, channel, value):
        pre = LppData(channel, 102, (value, ))
        self._data.append(pre)

    def add_temperature(self, channel, value):
        temp = LppData(channel, 103, (value, ))
        self._data.append(temp)

    def add_humitidy(self, channel, value):
        hum = LppData(channel, 104, (value, ))
        self._data.append(hum)

    def add_accelerometer(self, channel, x, y, z):
        acc = LppData(channel, 113, (x, y, z, ))
        self._data.append(acc)

    def add_pressure(self, channel, value):
        press = LppData(channel, 115, (value, ))
        self._data.append(press)

    def add_gyrometer(self, channel, x, y, z):
        gyro = LppData(channel, 134, (x, y, z, ))
        self._data.append(gyro)

    def add_gps(self, channel, lat, lon, alt):
        gps = LppData(channel, 134, (lat, lon, alt, ))
        self._data.append(gps)
