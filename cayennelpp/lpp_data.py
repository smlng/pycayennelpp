from .lpp_type import get_lpp_type

try:
    import logging
except ImportError:
    class logging:
        def debug(self, *args, **kwargs):
            pass


class LppData(object):
    """A single LPP data object representation

    Attributes:
        chn (int):     data channel number
        type (int):    data type ID
        value (tuple): data value(s)
    """

    def __init__(self, chn, type_, value):
        """Create a LppData object with given attriubes
        channel `chn`, type `type_`, and values `value`
        """
        logging.debug("LppData.__init__")
        if value is None:
            raise ValueError("Empty value!")
        if not isinstance(value, tuple):
            value = (value,)
        logging.debug("LppData(channel=%d, type=%d, len=%d)",
                      chn, type_, len(value))
        if get_lpp_type(type_) is None:
            raise ValueError("Invalid LPP data type!")
        if not len(value) == get_lpp_type(type_).dimension:
            raise ValueError("Invalid number of data values!")
        self.channel = chn
        self.type = type_
        self.value = value

    def __str__(self):
        """Return a pretty string representation of the LppData instance"""
        logging.debug("LppData.__str__")
        return 'LppData(channel = {}, type = {}, value = {})'.format(
                self.channel, get_lpp_type(self.type).name, str(self.value))

    @classmethod
    def from_bytes(class_object, buf):
        """Parse LppData from given a byte string"""
        logging.debug("LppData.from_bytes: buf=%s, length=%d",
                      buf, len(buf))
        if len(buf) < 3:
            raise BufferError("Invalid buffer size!")
        chn = buf[0]
        type_ = buf[1]
        size = get_lpp_type(type_).size
        logging.debug("LppData.from_bytes: date_size = %d", size)
        if len(buf) < size + 2:
            raise BufferError("Buffer too small!")
        value = get_lpp_type(type_).decode(buf[2:(2 + size)])
        return class_object(chn, type_, value)

    def bytes(self):
        """Convert LppData instance into a byte string"""
        logging.debug("LppData.bytes")
        hdr_buf = bytearray([self.channel, self.type])
        dat_buf = get_lpp_type(self.type).encode(self.value)
        buf = hdr_buf + dat_buf
        logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
        return buf

    def bytes_size(self):
        """Return the length of the LppData byte string representation"""
        logging.debug("LppData.bytes_size")
        return (get_lpp_type(self.type).size + 2)
