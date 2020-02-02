from ._video import *
from ..audio._audio import OGGIntegrityVerifier as _OGGIntegrityVerifier


class OGGIntegrityVerifier(_OGGIntegrityVerifier):
    MIME = "video/ogg"
