from unittest import TestCase
import os
from integv.video import MP4IntegrityVerifier


class TestMP4Verifier(TestCase):
    def setUp(self):
        self.sample_path = os.path.join(os.path.split(__file__)[0],
                                        "sample", "video", "sample.mp4")
        with open(self.sample_path, "rb") as f:
            self.sample_bad = f.read()[:-1]
        self.verifier = MP4IntegrityVerifier()

    def test_verify(self):
        self.assertTrue(self.verifier.verify(self.sample_path))
        self.assertFalse(self.verifier.verify(self.sample_bad))
