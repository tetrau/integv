import struct as _struct
from . import _IntegrityVerifierBase


class WEBPIntegrityVerifier(_IntegrityVerifierBase):
    MIME = "image/webp"

    def verify(self, file):
        riff = file.read(4)
        if riff != b"RIFF":
            return False
        try:
            size = self._read_uint32_le(file)
        except _struct.error:
            return False
        if size + 8 != len(file):
            return False
        return True
