from unittest import TestCase
from integv import _IntegrityVerifierBase
from integv._file import NormalizedFile


class TestBase(TestCase):
    def setUp(self):
        class TestVerifier(_IntegrityVerifierBase):
            MIME = "TEST"

            def verify(self, file):
                return file

        self.test_verifier = TestVerifier()

    def test_prepare_file(self):
        file_bytes = b"1234567890"
        file = NormalizedFile(file_bytes)
        self.assertIs(self.test_verifier.verify(file), file)
        self.assertTrue(
            isinstance(self.test_verifier.verify(file_bytes), NormalizedFile)
        )

    def test_register(self):
        self.assertIs(self.test_verifier.__class__,
                      _IntegrityVerifierBase._MIME_MAPPING["TEST"])
