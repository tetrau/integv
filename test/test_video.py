import os
from integv.video import MP4IntegrityVerifier
from mixin import TestVerifierMixin
from unittest import TestCase


class TestMP4Verifier(TestVerifierMixin, TestCase):
    @staticmethod
    def create_verifier():
        return MP4IntegrityVerifier()

    @staticmethod
    def sample_file_relevant_path():
        return os.path.join("sample", "video", "sample.mp4")
