from unittest import TestCase
from integv import FileIntegrityVerifier
import os


class TestVerifierAuto(TestCase):
    @staticmethod
    def read_sample(sample_file):
        with open(sample_file, "rb") as f:
            return f.read()

    def create_bad_samples(self, sample):
        bad_samples = []
        sample_len_1_3 = len(sample) // 3
        sample_parts = [
            sample[:sample_len_1_3],
            sample[sample_len_1_3:2 * sample_len_1_3],
            sample[2 * sample_len_1_3:]
        ]
        for i in range(3):
            b = b""
            for idx, part in enumerate(sample_parts):
                if idx == i:
                    b += b"\x00" * len(part)
                else:
                    b += part
            assert b != sample
            bad_samples.append(b)
        return bad_samples

    @staticmethod
    def gen_bad_fragment(b, n=4096):
        for i in range(n):
            yield b[:i]

    def setUp(self):
        self.sample_paths = []
        sample_folder = os.path.join(os.path.split(__file__)[0], "sample")
        for sample_sub_folder in os.listdir(sample_folder):
            if sample_sub_folder.startswith("."):
                continue
            abs_sample_sub_folder = os.path.join(sample_folder,
                                                 sample_sub_folder)
            for sample_file in os.listdir(abs_sample_sub_folder):
                if sample_file.startswith("."):
                    continue
                self.sample_paths.append(
                    os.path.join(abs_sample_sub_folder, sample_file))
        self.verifier = FileIntegrityVerifier()

    def _test_one_sample(self, sample_file, slow=False):
        self.verifier.slow = slow
        file_type = self.verifier.guess_type(sample_file)
        with open(sample_file, "rb") as f:
            sample = f.read()
        self.assertTrue(self.verifier.verify(sample_file))
        self.assertFalse(b"")
        self.assertFalse(self.verifier.verify(sample[:-1], file_type))
        bad_samples = self.create_bad_samples(sample)
        passed = [not self.verifier.verify(s, file_type) for s in bad_samples]
        self.assertGreater(len([p for p in passed if p]), 0)

    def test_verifier(self):
        for sample_file in self.sample_paths:
            self._test_one_sample(sample_file)
            self._test_one_sample(sample_file, slow=True)
            self._test_bad_fragment(sample_file)

    def test_verifier_artificial_sample(self):
        for verifier_cls in self.verifier._MIME_MAPPING.values():
            for slow in (True, False):
                verifier = verifier_cls(slow=slow)
                self.assertFalse(verifier.verify(b""))

    def _test_bad_fragment(self, sample_file):
        file_type = self.verifier.guess_type(sample_file)
        file = self.read_sample(sample_file)

        def error_count():
            result = [self.verifier.verify(f, file_type=file_type)
                      for f in self.gen_bad_fragment(file)]
            return result.count(lambda x: x)

        self.verifier.slow = False
        error = error_count()
        self.verifier.slow = True
        error_slow = error_count()
        self.assertLess(error, 4)
        self.assertLess(error_slow, 4)
        self.assertLessEqual(error_slow, error)
