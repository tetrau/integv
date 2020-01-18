import integv._file
import weakref as _weakref


class _IntegrityVerifierBase:
    _MIME_MAPPING = _weakref.WeakValueDictionary()

    def __init_subclass__(cls, **kwargs):
        if hasattr(cls, "MIME"):
            cls._MIME_MAPPING[cls.MIME] = cls
