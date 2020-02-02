import mimetypes as _mimetypes
import os as _os
from ._base import _IntegrityVerifierBase
from .exception import *
import integv.video
import integv.image
import integv.audio

_mimetypes.init([_os.path.join(_os.path.split(__file__)[0], "mime.types")])


class FileIntegrityVerifier(_IntegrityVerifierBase):
    @staticmethod
    def guess_type(filename):
        return _mimetypes.guess_type(filename)[0]

    def _get_verifier_class(self, file_type):
        try:
            if file_type not in self._MIME_MAPPING:
                file_type = self.guess_type("_.{}".format(file_type))
            verifier = self._MIME_MAPPING[file_type]
        except KeyError:
            raise NotImplementedError("File integrity verifier for {} is not "
                                      "implemented".format(repr(file_type)))
        return verifier

    def verify(self, file, file_type=None):
        if file_type is None:
            if not isinstance(file, str):
                raise ValueError("file_type is required for binary input")
            file_type = self.guess_type(file)
        if file_type is None:
            raise ValueError("Unknown file type for file {}".format(file))
        verifier_cls = self._get_verifier_class(file_type)
        return verifier_cls(slow=self.slow).verify(file)
