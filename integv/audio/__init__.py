from ._audio import *
from ..video._video import MP4IntegrityVerifier as _MP4IntegrityVerifier, \
    WEBMIntegrityVerifier as _WEBMIntegrityVerifier


class MP4IntegrityVerifier(_MP4IntegrityVerifier):
    MIME = "audio/mp4"


class WEBMIntegrityVerifier(_WEBMIntegrityVerifier):
    MIME = "audio/webm"
