from unittest import TestCase
from integv import _IntegrityVerifierBase


class TestBase(TestCase):
    def setUp(self):
        class TestVerifier(_IntegrityVerifierBase):
            MIME = "TEST"

        self.test_verifier = TestVerifier

    def test_register(self):
        self.assertIs(self.test_verifier,
                      _IntegrityVerifierBase._MIME_MAPPING["TEST"])
