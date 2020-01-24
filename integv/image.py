import struct as _struct
import zlib as _zlib
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


class PNGIntegrityVerifier(_IntegrityVerifierBase):
    MIME = "image/png"

    def _verify_chunk(self, file):
        try:
            chunk_length = self._read_uint32_be(file)
        except _struct.error:
            return None
        chunk_type = file.read(4)
        chunk_data = file.read(chunk_length)
        try:
            chunk_crc = self._read_uint32_be(file)
        except _struct.error:
            return None
        if _zlib.crc32(chunk_type + chunk_data) != chunk_crc:
            return None
        return chunk_length + 12

    def verify(self, file):
        magic_number = file.read(8)
        if magic_number != b"\x89PNG\r\n\x1a\n":
            return False
        total_size = 8
        while True:
            chunk_length = self._verify_chunk(file)
            if chunk_length is None:
                break
            else:
                total_size += chunk_length
        return total_size == len(file)


class GIFIntegrityVerifier(_IntegrityVerifierBase):
    MIME = "image/gif"

    def verify(self, file):
        header = file.read(6)
        if header not in (b"GIF87a", b"GIF89a"):
            return False
        file.seek(-1, _file.SEEK_END)
        trailer = file.read()
        if trailer != b";":
            return False
        return True
