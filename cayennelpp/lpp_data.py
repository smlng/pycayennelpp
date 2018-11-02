from __future__ import absolute_import

from .lpp_util import LPP_DATA_TYPE

import logging


class LppDataTypeError(Exception):
    pass


class LppDataSizeError(Exception):
    pass


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
                      bytes, len(bytes))
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
        logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
        return buf

    def data_size(self):
        logging.debug("LppData.data_size")
        return len(self._dat)

    def bytes_size(self):
        logging.debug("LppData.bytes_size")
        return (LPP_DATA_TYPE[self._tid]['size'] + 2)
