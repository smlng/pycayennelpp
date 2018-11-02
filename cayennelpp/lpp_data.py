from __future__ import absolute_import

from cayennelpp.lpp_util import (LPP_DATA_TYPE,
                                 LppDataTypeError,
                                 LppDataSizeError)

import logging


class LppData(object):

    def __init__(self, chn, tid, data):
        logging.debug("LppData(channel=%d, type=%d, len=%d)",
                      chn, tid, len(data))
        if tid not in LPP_DATA_TYPE:
            logging.error("LppData.from_buffer: invalid data type!")
            raise LppDataTypeError
        if not len(data) == LPP_DATA_TYPE[tid]['num']:
            logging.error("LppData: invalid number of data values!")
            raise LppDataSizeError
        self._chn = chn
        self._tid = tid
        self._dat = data

    def __str__(self):
        return 'LppData(channel = {}, type = {}, data = {})'.format(
                self._chn, LPP_DATA_TYPE[self._tid]['name'], str(self._dat))

    @classmethod
    def from_bytes(class_object, bytes):
        logging.debug("LppData.from_bytes: bytes=%s, length=%d",
                      bytes.hex(), len(bytes))
        if len(bytes) < 3:
            logging.error("LppData.from_bytes: invalid buffer size!")
            raise LppDataSizeError
        chn = bytes[0]
        tid = bytes[1]
        size = LPP_DATA_TYPE[tid]['size']
        logging.debug("LppData.from_bytes: date_size = %d", size)
        if len(bytes) < size + 2:
            logging.error("LppData.from_bytes: buffer too small!")
            raise LppDataSizeError
        dat = LPP_DATA_TYPE[tid]['decode'](bytes[2:(2 + size)])
        return class_object(chn, tid, dat)

    def data(self):
        logging.debug("LppData.get_data")
        logging.debug("  out:   values = %s, num = %d",
                      str(self._dat), len(self._dat))
        return self._dat

    def bytes(self):
        logging.debug("LppData.get_bytes")
        hdr_buf = bytearray([self._chn, self._tid])
        dat_buf = LPP_DATA_TYPE[self._tid]['encode'](self._dat)
        buf = hdr_buf + dat_buf
        logging.debug("  out:   bytes = %s, length = %d",
                      str(buf.hex()), len(buf))
        return buf

    def data_size(self):
        logging.debug("LppData.data_size")
        return len(self._dat)

    def bytes_size(self):
        logging.debug("LppData.bytes_size")
        return (LPP_DATA_TYPE[self._tid]['size'] + 2)


def main():
    # 01 67 FF D7 = -4.1C
    temp_buf = bytearray([0x01, 0x67, 0xFF, 0xD7])
    temp_dat = LppData.from_bytes(temp_buf)
    print("Temperature: data=%s, bytes=%s, data_size=%d, bytes_size=%d" %
          (temp_dat.data(), temp_dat.bytes().hex(),
           temp_dat.data_size(), temp_dat.bytes_size()))
    # 06 71 04 D2 FB 2E 00 00
    acc_buf = bytearray([0x06, 0x71, 0x04, 0xD2, 0xFB, 0x2E, 0x00, 0x00])
    acc_dat = LppData.from_bytes(acc_buf)
    print("Accelerometer: data=%s, bytes=%s, data_size=%d, bytes_size=%d" %
          (acc_dat.data(), acc_dat.bytes().hex(),
           acc_dat.data_size(), acc_dat.bytes_size()))
    # 01 88 06 76 5f f2 96 0a 00 03 e8
    gps_buf = bytearray([0x01, 0x88, 0x06, 0x76,
                         0x5f, 0xf2, 0x96, 0x0a,
                         0x00, 0x03, 0xe8])
    gps_dat = LppData.from_bytes(gps_buf)
    print("GPS: data=%s, bytes=%s, data_size=%d, bytes_size=%d" %
          (gps_dat.data(), gps_dat.bytes().hex(),
           gps_dat.data_size(), gps_dat.bytes_size()))


if __name__ == '__main__':
    # execute when run as program
    main()
