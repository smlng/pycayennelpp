from .lpp_data import LppData
from .lpp_frame import LppFrame
from .lpp_type import LppType


class LppUtil():
    """Cayenne LPP utility functions.

    This class provides helper functions and wrapper, e.g. for encoding and
    decoding LppType, LppData, and LppFrame into various data formats.
    """

    @staticmethod
    def json_encode(obj, type2str=False):
        """Encode LppType, LppData, and LppFrame to JSON."""
        if isinstance(obj, LppType):
            if type2str:
                return obj.name
            return obj.type
        if isinstance(obj, LppData):
            return obj.__dict__
        if isinstance(obj, LppFrame):
            return obj.data
        raise TypeError(repr(obj) + " is not JSON serialized")

    @classmethod
    def json_encode_type_int(cls, obj):
        """Wrapper function encode type as int in JSON."""
        return cls.json_encode(obj, False)

    @classmethod
    def json_encode_type_str(cls, obj):
        """Wrapper function encode type as string in JSON."""
        return cls.json_encode(obj, True)
