from unittest import TestCase
from io import BytesIO
from tempfile import NamedTemporaryFile
from integv._file import NormalizedFile


class TestException(TestCase):
    def test_type_error(self):
        self.assertRaises(TypeError, lambda: NormalizedFile({}))


class TestFile(TestCase):
    def setUp(self):
        self.raw = b"0123456789" * 1234
        self.file = NormalizedFile(self.raw)

    def test_read(self):
        self.assertEqual(self.file.read(), self.raw)

    def test_seek(self):
        raw = self.raw[1000:1100]
        self.file.seek(1000)
        chunk = self.file.read(100)
        self.assertEqual(raw, chunk)

    def test_tell(self):
        self.file.seek(1000)
        self.file.read(100)
        self.assertEqual(self.file.tell(), 1100)

    def test_peek(self):
        raw = self.raw[1000:1100]
        self.file.seek(1000)
        self.assertEqual(self.file.peek(100), self.file.peek(100), raw)

    def test_len(self):
        self.assertEqual(len(self.file), len(self.file), len(self.raw))


class TestByteIOFile(TestFile):
    def setUp(self):
        self.raw = b"0123456789" * 1234
        self.file = NormalizedFile(BytesIO(self.raw))


class TestOnDiskFile(TestFile):
    def setUp(self):
        self.raw = b"0123456789" * 1234
        self.file_on_disk = NamedTemporaryFile()
        self.file_on_disk.write(self.raw)
        self.file_on_disk.flush()
        self.file = NormalizedFile(self.file_on_disk.name)

    def tearDown(self):
        self.file_on_disk.close()
        self.file.close()
