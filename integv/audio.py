from ._common import _RIFFIntegrityVerifier


class WAVIntegrityVerifier(_RIFFIntegrityVerifier):
    MIME = "audio/x-wav"
