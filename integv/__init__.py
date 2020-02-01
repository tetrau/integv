import mimetypes as _mimetypes
from ._base import _IntegrityVerifierBase
import integv.video
import integv.image


class FileIntegrityVerifier(_IntegrityVerifierBase):
    def guess_type(self, filename):
        return _mimetypes.guess_type(filename)[0]

    def verify(self, file, file_type=None):
        if file_type is None:
            if not isinstance(file, str):
                raise ValueError("file_type is required for binary input")
            file_type = self.guess_type(file)
            if file_type is None:
                raise ValueError("Unknown file type for file {}".format(file))
        try:
            verifier = self._MIME_MAPPING[file_type]()
        except KeyError:
            raise NotImplementedError("File integrity verifier for {} is not "
                                      "implemented".format(repr(file_type)))
        return verifier.verify(file)
