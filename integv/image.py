import struct as _struct
from ._base import _IntegrityVerifierBase
import integv._file as _file


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


class JPEGIntegrityVerifier(_IntegrityVerifierBase):
    MIME = "image/jpeg"

    def verify(self, file):
        start_of_image = file.read(3)
        file.seek(-2, _file.SEEK_END)
        end_of_image = file.read()
        return start_of_image == b"\xFF\xD8\xFF" and end_of_image == b"\xFF\xD9"
