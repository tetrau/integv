from ._base import _IntegrityVerifierBase
import integv._file as _file
import struct as _struct


class MP4IntegrityVerifier(_IntegrityVerifierBase):
    MIME = "video/mp4"

    def _check_chunk(self, f):
        try:
            chunk_size = self._peek_uint32_be(f)
        except _struct.error:
            return None
        f.seek(chunk_size, _file.SEEK_CUR)
        if chunk_size < 4:
            return None
        else:
            return chunk_size

    def verify(self, file):
        chunk_size_sum = 0
        while True:
            chunk_size = self._check_chunk(file)
            if chunk_size is None:
                break
            else:
                chunk_size_sum += chunk_size
        return chunk_size_sum == len(file)
