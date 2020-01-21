import os
from integv.image import WEBPIntegrityVerifier, JPEGIntegrityVerifier
from mixin import TestVerifierMixin
from unittest import TestCase


class TestWEBPVerifier(TestVerifierMixin, TestCase):
    @staticmethod
    def create_verifier():
        return WEBPIntegrityVerifier()

    @staticmethod
    def sample_file_relevant_path():
        return os.path.join("sample", "image", "sample.webp")


class TestJPEGVerifier(TestVerifierMixin, TestCase):
    @staticmethod
    def create_verifier():
        return JPEGIntegrityVerifier()

    @staticmethod
    def sample_file_relevant_path():
        return os.path.join("sample", "image", "sample.jpg")
