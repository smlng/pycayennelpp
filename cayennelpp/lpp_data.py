from .lpp_type import LppType


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
        for i in range(self.type.dimension):
            if not self.type.signs[i] and value[i] < 0:
                raise ValueError("Invalid value, must be positive!")
        self.value = value

    def __bytes__(self):
        """Return a byte string representation of this LppData object."""
        hdr_buf = bytearray([self.channel, int(self.type)])
        dat_buf = self.type.encode(self.value)
        buf = hdr_buf + dat_buf
        return bytes(buf)

    def __len__(self):
        """Return the length of the LppData byte string representation."""
        return self.type.size + 2

    def __str__(self):
        """Return a pretty string representation of the LppData object."""
        return 'LppData(channel = {}, type = {}, value = {})'.format(
                self.channel, self.type.name, str(self.value))

    @classmethod
    def from_bytes(class_object, buf):
        """Parse a given byte string and return a LppData object."""
        if len(buf) < 3:
            raise BufferError("Invalid buffer size!")
        chn = buf[0]
        type_ = buf[1]
        lpp_type = LppType.get_lpp_type(type_)
        size = lpp_type.size
        if len(buf) < size + 2:
            raise BufferError("Buffer too small!")
        value = lpp_type.decode(buf[2:(2 + size)])
        return class_object(chn, type_, value)
