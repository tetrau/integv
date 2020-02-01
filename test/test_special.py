from unittest import TestCase
import os
from integv.video import MKVIntegrityVerifier
from integv import UndecidableError


class TestLiveStreamMKV(TestCase):
    def test(self):
        file_path = os.path.join(os.path.split(__file__)[0],
                                 "special_sample",
                                 "live_stream.mkv")
        verifier = MKVIntegrityVerifier()
        self.assertRaises(UndecidableError,
                          lambda: verifier.verify(file_path))
