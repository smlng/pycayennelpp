from .lpp_type import LPP_DATA_TYPE

import logging


class LppDataTypeError(Exception):
    pass


class LppDataSizeError(Exception):
    pass


class LppData(object):

    def __init__(self, chn, tid, data):
        logging.debug("LppData.__init__")
        if not isinstance(data, tuple):
            data = (data,)
        logging.debug("LppData(channel=%d, type=%d, len=%d)",
                      chn, tid, len(data))
        if tid not in LPP_DATA_TYPE:
            logging.error("LppData.from_buffer: invalid data type!")
            raise LppDataTypeError
        if not len(data) == LPP_DATA_TYPE[tid].dimension:
            logging.error("LppData: invalid number of data values!")
            raise LppDataSizeError
        self.channel = chn
        self.type = tid
        self.data = data

    def __str__(self):
        logging.debug("LppData.__str__")
        return 'LppData(channel = {}, type = {}, data = {})'.format(
                self.channel, LPP_DATA_TYPE[self.type].name, str(self.data))

    @classmethod
    def from_bytes(class_object, bytes):
        logging.debug("LppData.from_bytes: bytes=%s, length=%d",
                      bytes, len(bytes))
        if len(bytes) < 3:
            logging.error("LppData.from_bytes: invalid buffer size!")
            raise LppDataSizeError
        chn = bytes[0]
        tid = bytes[1]
        size = LPP_DATA_TYPE[tid].size
        logging.debug("LppData.from_bytes: date_size = %d", size)
        if len(bytes) < size + 2:
            logging.error("LppData.from_bytes: buffer too small!")
            raise LppDataSizeError
        dat = LPP_DATA_TYPE[tid].decode(bytes[2:(2 + size)])
        return class_object(chn, tid, dat)

    def bytes(self):
        logging.debug("LppData.bytes")
        hdr_buf = bytearray([self.channel, self.type])
        dat_buf = LPP_DATA_TYPE[self.type].encode(self.data)
        buf = hdr_buf + dat_buf
        logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
        return buf

    def bytes_size(self):
        logging.debug("LppData.bytes_size")
        return (LPP_DATA_TYPE[self.type].size + 2)
