import struct as _struct
import functools as _functools
import weakref as _weakref
import zlib as _zlib
import integv._file as _file


class _RegisterMeta(type):
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        if hasattr(cls, "MIME") and hasattr(cls, "_MIME_MAPPING"):
            cls._MIME_MAPPING[cls.MIME] = cls
            if hasattr(cls, "verify"):
                original_verify = cls.verify
                cls_name = cls.__name__

                @_functools.wraps(original_verify)
                def verify(self, file=None):
                    if not isinstance(self, _IntegrityVerifierBase):
                        raise TypeError(
                            "{0}.verify is not a class method, create a {0} "
                            "instance to verify the file.".format(cls_name))

                    file = _IntegrityVerifierBase._prepare_file(file)
                    if len(file) == 0:
                        return False
                    return original_verify(self, file)

                cls.verify = verify
        return cls


class _IntegrityVerifierBase(metaclass=_RegisterMeta):
    _MIME_MAPPING = _weakref.WeakValueDictionary()

    def __init__(self, slow=False):
        """
        :param slow: Enable some sophisticated methods of verification. Will
                     reduce the false negative rate but consume more time.
        """
        self.slow = slow

    @staticmethod
    def _prepare_file(file):
        if isinstance(file, _file.NormalizedFile):
            return file
        else:
            return _file.NormalizedFile(file)

    @staticmethod
    def __peek_unpack_one(f, size, fmt):
        return _struct.unpack(fmt, f.peek(size))[0]

    def _peek_uint32_be(self, f):
        return self.__peek_unpack_one(f, 4, ">L")

    def _peek_unit8(self, f):
        return self.__peek_unpack_one(f, 1, "B")

    @staticmethod
    def __read_unpack_one(f, size, fmt):
        return _struct.unpack(fmt, f.read(size))[0]

    def _read_uint32_le(self, f):
        return self.__read_unpack_one(f, 4, "<L")

    def _read_uint32_be(self, f):
        return self.__read_unpack_one(f, 4, ">L")

    def _read_unit8(self, f):
        return self.__read_unpack_one(f, 1, "B")

    @staticmethod
    def _crc32(*args, **kwargs):
        return _zlib.crc32(*args, **kwargs)
