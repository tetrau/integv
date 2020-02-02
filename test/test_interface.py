from unittest import TestCase
from integv import FileIntegrityVerifier
from integv.video import WEBMIntegrityVerifier, MP4IntegrityVerifier


class TestInterface(TestCase):
    def setUp(self):
        self.verifier = FileIntegrityVerifier()

    def test_args_validation(self):
        self.assertRaises(NotImplementedError,
                          lambda: self.verifier.verify(b"", "NotImplemented"))
        self.assertRaises(ValueError, lambda: self.verifier.verify(""))
        self.assertRaises(ValueError, lambda: self.verifier.verify(b""))

    def test_verifier_lookup(self):
        self.assertIs(self.verifier._get_verifier_class("video/webm"),
                      WEBMIntegrityVerifier)
        self.assertIs(self.verifier._get_verifier_class("webm"),
                      WEBMIntegrityVerifier)
        self.assertIs(self.verifier._get_verifier_class("m4v"),
                      MP4IntegrityVerifier)
