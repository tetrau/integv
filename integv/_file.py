import io
import os

SEEK_SET = io.SEEK_SET
SEEK_CUR = io.SEEK_CUR
SEEK_END = io.SEEK_END


class NormalizedFile:
    def __init__(self, file):
        self._close_on_del = False
        if isinstance(file, bytes):
            self._file = io.BytesIO(file)
        elif isinstance(file, str) or isinstance(file, os.PathLike):
            self._file = open(file, "rb")
            self._close_on_del = True
        elif hasattr(file, "read"):
            self._file = file
        else:
            msg = ("expected str, os.PathLike object, bytes or file-like object"
                   ", not {}".format(type(file)))
            raise TypeError(msg)
        self._length = None

    def __len__(self):
        if self._length is None:
            position = self.tell()
            self.seek(0, SEEK_END)
            self._length = self.tell()
            self.seek(position)
            return self._length
        else:
            return self._length

    def __del__(self):
        if self._close_on_del:
            self.close()

    def read(self, size=-1):
        return self._file.read(size)

    def close(self):
        return self._file.close()

    def seek(self, offset, whence=SEEK_SET):
        return self._file.seek(offset, whence)

    def tell(self):
        return self._file.tell()

    def peek(self, size=-1):
        position = self.tell()
        b = self.read(size)
        self.seek(position)
        return b
