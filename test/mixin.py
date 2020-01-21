import os


class TestVerifierMixin:
    def create_verifier(self):
        raise NotImplementedError()

    def sample_file_relevant_path(self):
        raise NotImplementedError()

    def setUp(self):
        self.sample_path = os.path.join(os.path.split(__file__)[0],
                                        self.sample_file_relevant_path())
        self.bad_samples = []
        with open(self.sample_path, "rb") as f:
            sample = f.read()
            self.sample = sample
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
                self.bad_samples.append(b)
        self.verifier = self.create_verifier()

    def test_verifier(self):
        self.assertTrue(self.verifier.verify(self.sample))
        self.assertFalse(b"")
        self.assertFalse(self.verifier.verify(self.sample[:-1]))
        passed = [self.verifier.verify(s) for s in self.bad_samples]
        self.assertGreater(len([p for p in passed if p]), 0)
