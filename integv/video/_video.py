from .._base import _IntegrityVerifierBase
from ..exception import UndecidableError
from .._common import _RIFFIntegrityVerifier
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


class MKVIntegrityVerifier(_IntegrityVerifierBase):
    MIME = "video/x-matroska"

    @staticmethod
    def _leading_zero_bit(x):
        return 10 - len(bin(x))

    def _read_vint(self, file):
        first_char = self._peek_unit8(file)
        if first_char == 0xFF:
            raise UndecidableError("Can't verify MKV/WEBM files contain "
                                   "elements with no known size")
        if first_char == 0:
            return None, None
        vint_length = self._leading_zero_bit(first_char) + 1
        vint_bytes = file.read(vint_length)
        if len(vint_bytes) != vint_length:
            return None, None
        vint = _struct.unpack(">Q", vint_bytes.rjust(8, b"\x00"))[0]
        first_1_bit = 8 * vint_length - vint_length
        max_unit64 = 0xFFFFFFFFFFFFFFFF
        vint = (vint << (64 - first_1_bit) & max_unit64) >> (64 - first_1_bit)
        return vint_length, vint

    def _verify_chunk(self, file):
        try:
            element_id_length, element_id = self._read_vint(file)
            data_size_length, data_size = self._read_vint(file)
        except _struct.error:
            return None
        if element_id_length is None or data_size_length is None:
            return None
        file.seek(data_size, _file.SEEK_CUR)
        return data_size + data_size_length + element_id_length

    def verify(self, file):
        file_size = 0
        while True:
            chunk_size = self._verify_chunk(file)
            if chunk_size is None:
                break
            else:
                file_size += chunk_size
        return file_size == len(file)


class WEBMIntegrityVerifier(MKVIntegrityVerifier):
    MIME = "video/webm"


class AVIIntegrityVerifier(_RIFFIntegrityVerifier):
    MIME = "video/vnd.avi"


class FLVIntegrityVerifier(_IntegrityVerifierBase):
    MIME = "video/x-flv"

    def _check_chunk(self, file):
        try:
            file.seek(1, _file.SEEK_CUR)
            payload_size = b"\x00" + file.read(3)
            payload_size = _struct.unpack(">L", payload_size)[0]
            file.seek(7 + payload_size, _file.SEEK_CUR)
            self_size = self._read_uint32_be(file)
            if self_size != payload_size + 11:
                return None
            return 15 + payload_size
        except _struct.error:
            return None

    def verify(self, file):
        header = file.read(5)
        if header[:4] != b"FLV\x01":
            return False
        try:
            header_size = self._read_uint32_be(file)
        except _struct.error:
            return False
        file.seek(0)
        file.seek(header_size)
        if file.read(4) != b"\x00" * 4:
            return False
        chunk_size_sum = 0
        while True:
            chunk_size = self._check_chunk(file)
            if chunk_size is None:
                break
            else:
                chunk_size_sum += chunk_size
        return chunk_size_sum + header_size + 4 == len(file)
