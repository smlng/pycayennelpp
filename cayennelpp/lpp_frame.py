from __future__ import absolute_import

from cayennelpp.lpp_data import LppData

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
                      bytes.hex(), len(bytes))
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


def main():
    empty_frame = LppFrame()
    print("Frame without data:")
    print("  %s" % empty_frame.data())
    print("Frame with many data:")
    empty_frame.add_digital_input(0, 21)
    empty_frame.add_digital_output(1, 42)
    empty_frame.add_analog_input(0, 12.34)
    empty_frame.add_analog_input(1, -12.34)
    empty_frame.add_analog_output(0, 56.78)
    empty_frame.add_analog_output(1, -56.78)
    empty_frame.add_luminosity(2, 12345)
    empty_frame.add_presence(3, 1)
    empty_frame.add_temperature(2, 12.3)
    empty_frame.add_temperature(3, -32.1)
    empty_frame.add_humitidy(2, 12.3)
    empty_frame.add_humitidy(3, 45.6)
    empty_frame.add_humitidy(4, 78.9)
    empty_frame.add_accelerometer(5, 1.234, -1.234, 0.0)
    empty_frame.add_pressure(6, 1005.5)
    empty_frame.add_gyrometer(7, 1.234, -1.234, 0.0)
    empty_frame.add_gps(8, 1.234, -1.234, 0.0)
    for d in empty_frame.data():
        print("  %s" % d)
    print("  BYTES: %s" % empty_frame.bytes().hex())
    # 03 67 01 10 05 67 00 FF = 27.2C + 25.5C
    bytes = bytearray([0x03, 0x67, 0x01, 0x10, 0x05, 0x67, 0x00, 0xff])
    bytes_frame = LppFrame.from_bytes(bytes)
    print("Frame from bytes, data:")
    for d in bytes_frame.data():
        print("  %s" % d)
    print("  BYTES: %s" % bytes_frame.bytes().hex())
    base64 = "AYgILMMBiIMAAAACAAY="
    base64_frame = LppFrame.from_base64(base64)
    print("Frame from base64, data:")
    for d in base64_frame.data():
        print("  %s" % d)
    print("  BYTES: %s" % base64_frame.bytes().hex())


if __name__ == '__main__':
    # execute when run as program
    main()
