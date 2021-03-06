from .lpp_type import LppType

try:
    import logging
except ImportError:
    class logging:
        def debug(self, *args, **kwargs):
            pass


class LppData(object):
    """
    A LPP data object.

    Attributes:
        chn (int):      data channel number
        type (LppType): data type
        value (tuple):  data value(s)
    """

    def __init__(self, chn, type_, value):
        """Create a LppData object with given attriubes."""
        logging.debug("LppData.__init__")
        self.channel = chn
        self.type = LppType.get_lpp_type(type_)
        if self.type is None:
            raise ValueError("Invalid LPP data type!")
        if value is None:
            raise ValueError("Empty value!")
        if not isinstance(value, tuple):
            value = (value,)
        if not len(value) == self.type.dimension:
            raise ValueError("Invalid number of data values!")
        self.value = value
        self._size = self.type.size + 2
        logging.debug("LppData(channel=%d, type=%d, len=%d)",
                      chn, type_, len(value))

    def __str__(self):
        """Return a pretty string representation of the LppData object."""
        logging.debug("LppData.__str__")
        return 'LppData(channel = {}, type = {}, value = {})'.format(
                self.channel, self.type.name, str(self.value))

    @classmethod
    def from_bytes(class_object, buf):
        """Parse a given byte string and return a LppData object."""
        logging.debug("LppData.from_bytes: buf=%s, length=%d",
                      buf, len(buf))
        if len(buf) < 3:
            raise BufferError("Invalid buffer size!")
        chn = buf[0]
        type_ = buf[1]
        lpp_type = LppType.get_lpp_type(type_)
        size = lpp_type.size
        logging.debug("LppData.from_bytes: date_size = %d", size)
        if len(buf) < size + 2:
            raise BufferError("Buffer too small!")
        value = lpp_type.decode(buf[2:(2 + size)])
        return class_object(chn, type_, value)

    def bytes(self):
        """Return a byte string representation of this LppData object."""
        logging.debug("LppData.bytes")
        hdr_buf = bytearray([self.channel, int(self.type)])
        dat_buf = self.type.encode(self.value)
        buf = hdr_buf + dat_buf
        logging.debug("  out:   bytes = %s, length = %d", buf, len(buf))
        return buf

    @property
    def size(self):
        """Return the length of the LppData byte string representation."""
        logging.debug("LppData.size")
        return self._size
