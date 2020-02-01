from unittest import TestCase
import os
from integv.video import MKVIntegrityVerifier
from integv import UndecidableError
from integv.audio import OGGIntegrityVerifier


class TestLiveStreamMKV(TestCase):
    def test(self):
        file_path = os.path.join(os.path.split(__file__)[0],
                                 "special_sample",
                                 "live_stream.mkv")
        verifier = MKVIntegrityVerifier()
        self.assertRaises(UndecidableError,
                          lambda: verifier.verify(file_path))


class TestOggOneByte(TestCase):
    def test(self):
        file_path = os.path.join(os.path.split(__file__)[0],
                                 "sample", "audio",
                                 "sample.ogg")
        with open(file_path, "rb") as f:
            file = f.read()
        verifier = OGGIntegrityVerifier(slow=True)
        byte_change_pos = len(file) // 3
        bad_file = file[:byte_change_pos - 1] + b"\x00" + file[byte_change_pos:]
        self.assertFalse(verifier.verify(bad_file))
        verifier.slow = False
        self.assertTrue(verifier.verify(bad_file))
