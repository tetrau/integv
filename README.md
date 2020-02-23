# integv
[![python versions](https://img.shields.io/pypi/v/integv)](https://pypi.org/project/integv) [![python versions](https://img.shields.io/pypi/pyversions/integv)](https://pypi.org/project/integv) [![codecov](https://img.shields.io/codecov/c/github/tetrau/integv)](https://codecov.io/gh/tetrau/integv) [![unittest](https://github.com/tetrau/integv/workflows/unittest/badge.svg)](https://github.com/tetrau/integv)

 integv is a file integrity verifier based on the format of the file. It's 
 capable of checking the integrity of multiple types of files without any 
 additional information like Content-Length or checksum. The main goal of integv
 is to detect file corruption (mostly shortened) during file download caused by 
 network glitch. But integv still can be used for many other purposes as well.
 
 # Installation
 ```bash
pip install integv
```
 
 # Quick Start
 ```python
import integv

# load a test mp4 file
file_path = "./test/sample/video/sample.mp4"
with open(file_path, "rb") as f:
    file = f.read()

# initiate a verifier
verifier = integv.FileIntegrityVerifier()

# verify using the file and file_type
# file_type can be a simple filename extension like "mp4" or "jpg"
# or you can provide a full MIME type like "video/mp4" or "image/jpeg"
verifier.verify(file, file_type="mp4") # True

# a corrupted file (in this case, shortened by one byte) will not pass the verification
verifier.verify(file[:-1], file_type="mp4") # False

# the file input for the verifier can be bytes or a binary file like object
verifier.verify(open(file_path, "rb"), file_type="mp4") # True

# it can also be a string representing a file path
# if the file path contains a proper filename extension, the file_type is not needed.
verifier.verify(file_path) # True
```

# Supported types

### Video

* **mp4:** `video/mp4`
* **mkv:** `video/x-matroska`
* **webm:** `video/webm`
* **avi:** `video/vnd.avi`

### Image

* **jpeg:** `image/jpeg`
* **png:** `image/png`
* **gif:** `image/gif`
* **webp** `image/webp`

### Audio

* **wav:** `audio/x-wav`
* **ogg:** `audio/ogg`

# Limitation of integv
The integv verifier only checks the file by the format information embedded in 
file like file size in header, chuck size in chuck header, end of file markers,
etc. It does not try to decode the file which makes integv fast and simple.
But that also means the possibility of false negative (corrupted files can't be 
detected). The baseline of all integv file integrity verifiers must be extremely 
sensitive to shortened files, which is very common in file downloaded from the
network. Some types of files like png contain checksum inside, which is less
error-prone. By all means, do not use integv for any kind of security 
verification. As a bad file which passes the verification can be simply forged.


# Advanced Usage
## Specialized File Integrity Verifier
There are some specialized file integrity verifier for different types of files.
You can find them in `integv.video`, `integv.image` and `integv.audio`. They are
used exactly like the `FileIntegrityVerifier` except `file_type` are not needed.

```python
from integv.video import MP4IntegrityVerifier

verifier = MP4IntegrityVerifier()
verifier.verify("./test/sample/video/sample.mp4") # True
```

## Optional `slow` argument in verifier initialization
A boolean argument `slow` can be provided in verifier initialization. It will 
enable some sophisticated verification to eliminate false negatives. And that 
will consume more time. The default value of `slow` is `False`. For now, only 
one verifier, `OGGIntegrityVerifier` has a `slow` method of verification. 

```python
from integv import FileIntegrityVerifier

verifier = FileIntegrityVerifier()
slow_verifier = FileIntegrityVerifier(slow=True)

file_path = "./test/sample/audio/sample.ogg"
verifier.verify(file_path) # True
slow_verifier.verify(file_path) # also True, but slower

```

# Acknowledgment
| File                                | Attribution                                                                                                                                      |
|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| test/sample/video/sample.mp4        | (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org                                                                                    |
| test/sample/video/sample.webm       | U.S. Geological Survey (USGS) [Public domain]                                                                                                    |
| test/sample/video/sample.mkv        | (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org, converted by [Matroska-Org](https://github.com/Matroska-Org/matroska-test-files)  |
| test/sample/video/sample.avi        | U.S. Geological Survey (USGS) [Public domain], converted to avi by ffmpeg                                                                        |
| test/sample/image/sample.webp       | Benjamin Gimmel, BenHur [CC BY-SA](http://creativecommons.org/licenses/by-sa/3.0/), converted to webp by Google                                  |
| test/sample/image/sample.jpg        | Benjamin Gimmel, BenHur [CC BY-SA](http://creativecommons.org/licenses/by-sa/3.0/)                                                               |
| test/sample/image/sample.png        | Benjamin Gimmel, BenHur [CC BY-SA](http://creativecommons.org/licenses/by-sa/3.0/)                                                               |
| test/sample/image/sample.gif        | DemonDeLuxe (Dominique Toussaint) [CC BY-SA](http://creativecommons.org/licenses/by-sa/3.0/)                                                     |
| test/sample/audio/sample.wav        | Shishirdasika [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0)                                                                         |
| test/sample/audio/sample.ogg        | Wolfgang Amadeus Mozart [EEF OAL-1](https://commons.wikimedia.org/wiki/File:Wolfgang_Amadeus_Mozart_-_Symphony_40_g-moll_-_1._Molto_allegro.ogg) |
| test/special_sample/live_stream.mkv | (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org, converted by [Matroska-Org](https://github.com/Matroska-Org/matroska-test-files)  |

# Contribution
Pull requests, issues for bugs or feature requests, all kind of contributions 
are all welcome.