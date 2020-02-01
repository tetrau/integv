from unittest import TestCase
from integv import FileIntegrityVerifier


class TestInterface(TestCase):
    def setUp(self):
        self.verifier = FileIntegrityVerifier()

    def test_args_validation(self):
        self.assertRaises(NotImplementedError,
                          lambda: self.verifier.verify(b"", "NotImplemented"))
        self.assertRaises(ValueError, lambda: self.verifier.verify(""))
        self.assertRaises(ValueError, lambda: self.verifier.verify(b""))
