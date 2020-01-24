import struct as _struct
import functools as _functools
import weakref as _weakref
import integv._file as _file


class _IntegrityVerifierBase:
    _MIME_MAPPING = _weakref.WeakValueDictionary()

    def __init_subclass__(cls, **kwargs):
        if hasattr(cls, "MIME"):
            cls._MIME_MAPPING[cls.MIME] = cls
            if hasattr(cls, "verify"):
                original_verify = cls.verify

                @_functools.wraps(original_verify)
                def wrapper(self, file, *args, **kwargs):
                    file = _IntegrityVerifierBase._prepare_file(file)
                    return original_verify(self, file, *args, **kwargs)

                cls.verify = wrapper

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

    @staticmethod
    def __read_unpack_one(f, size, fmt):
        return _struct.unpack(fmt, f.read(size))[0]

    def _read_uint32_le(self, f):
        return self.__read_unpack_one(f, 4, "<L")

    def _read_uint32_be(self, f):
        return self.__read_unpack_one(f, 4, ">L")
