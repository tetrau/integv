# integv
[![pypi versions](https://img.shields.io/pypi/v/integv)](https://pypi.org/project/integv) [![python versions](https://img.shields.io/pypi/pyversions/integv)](https://pypi.org/project/integv) [![codecov](https://img.shields.io/codecov/c/github/tetrau/integv)](https://codecov.io/gh/tetrau/integv) [![unittest](https://github.com/tetrau/integv/workflows/unittest/badge.svg)](https://github.com/tetrau/integv)

 integv is a file integrity verifier based on the format of the file. It's 
 capable of checking the integrity of multiple types of files without any 
 additional information like Content-Length or checksum. The main goal of integv
 is to detect file corruption (mostly shortened) during file download caused by 
 network glitch. But integv still can be used for many other purposes as well.
 
# Installation

 ```bash
pip install integv
```
 
# Why integv

Sometimes when you download some media files using `requests`, a network glitch 
happens and your file downloaded is corrupted. If there's a `Content-Length` 
header, you can compare it to the downloaded file size. But the worst thing is 
most of the time, media files are served using HTTP chunked transfer encoding, 
and there's no `Content-Length` header. So you don't know if the download file 
is good or not. And that's the time integv comes to help, just feed the 
downloaded file to integv and it can verify the integrity of the file with zero 
other information like `Content-Length`. All integv needs are the type of the file.
 
integv has many advantages.

1. integv is light, integv is written in pure python with 0 dependencies. Which 
makes integv portable and easy to integrate into your project.

2. integv is fast, integv does not try to decode the file, it just checks all the 
key points in the file, so integv is much faster than other solutions that try
to decode the file.

Here's a comparison of verifying a 70 MB mp4 file using integv and FFmpeg.

 ```
python3 -m timeit "import integv;integv.FileIntegrityVerifier().verify('../test.mp4')"
5000 loops, best of 5: 61.4 usec per loop

python3 -m timeit "import subprocess;subprocess.run('ffmpeg -v error -i ../test.mp4 -f null -', shell=True)"
1 loop, best of 5: 11.2 sec per loop
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
* **flv\*:** `video/x-flv` 

\* not f4v. Basically, f4v is just mp4 with a different name.
For f4v files, use mp4 integrity verifier.

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

### Effectiveness of integv on different types of corruption
#### Types of corruption:
* **S**mall **D**eletion at the **E**nd of the file. (**SDE**)

A few bytes of data were deleted at the end of the file. The length of the file 
is reduced.
```
Original file:  ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ
Corrupted file: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXY
```

* **L**arge **D**eletion at the **E**nd of the file. (**LDE**)

A large chunk of data was deleted at the end of the file. The length of the 
file is reduced.
```
Original file:  ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ
Corrupted file: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNO
```

* **S**mall **S**ubstitution at the **E**nd of the file. (**SSE**)

A few bytes of data were substituted at the end of file. The length of the file 
remains the same.
```
Original file:  ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ
Corrupted file: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYA
```

* **L**arge **S**ubstitution at the **E**nd of the file. (**LSE**)

A large chunk of data was substituted at the end of file. The length of the 
file remains the same.
```
Original file:  ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ
Corrupted file: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNAAAAAAAAAAAA
```

* **S**mall **D**eletion at a **R**andom position of the file. (**SDR**)

A few bytes of data were deleted at a random position of the file. The length of 
the file is reduced.

```
Original file:  ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ
Corrupted file: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLNOPQRSTUVWXYZ
                                                      ^
```

* **L**arge **D**eletion at a **R**andom position of the file. (**LDR**)

A large chunk of data was deleted at a random position of the file. The length 
of the file is reduced.

```
Original file:  ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ
Corrupted file: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLYZ
                                                      ^
```

* **S**mall **S**ubstitution at a **R**andom position of the file. (**SSR**)

A few bytes of data were substituted at a random position of the file. The length
of the file remains the same.

```
Original file:  ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ
Corrupted file: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLANOPQRSTUVWXYZ
                                                      ^
```

* **L**arge **S**ubstitution at a **R**andom position of the file. (**LSR**)

A large chunk of data wass substituted at a random position of the file. The 
length of the file remains the same.

```
Original file:  ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ
Corrupted file: ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLAAAAAAAAAAWXYZ
                                                      ^
```

#### Effectiveness Table
From my personal experience, the most common types of corruption happen during
file downloading using `requests` or similar things are **SDE** and **LDE**.

|           |    SDE   |    LDE   |     SSE    |     LSE    |     SDR    |     LDR    |     SSR    |     LSR    |
|-----------|:--------:|:--------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
| mp4       | :smiley: | :smiley: | :frowning: |  :smiley:  |  :smiley:  |  :smiley:  | :frowning: |  :smiley:  |
| mkv       | :smiley: | :smiley: | :frowning: |  :smiley:  |  :smiley:  |  :smiley:  | :frowning: |  :smiley:  |
| webm      | :smiley: | :smiley: | :frowning: |  :smiley:  |  :smiley:  |  :smiley:  | :frowning: |  :smiley:  |
| avi       | :smiley: | :smiley: | :frowning: | :frowning: |  :smiley:  |  :smiley:  | :frowning: | :frowning: |
| flv       | :smiley: | :smiley: |  :smiley:  |  :smiley:  |  :smiley:  |  :smiley:  | :frowning: |  :smiley:  |
| jpeg      | :smiley: | :smiley: |  :smiley:  |  :smiley:  | :frowning: | :frowning: | :frowning: | :frowning: |
| png       | :smiley: | :smiley: |  :smiley:  |  :smiley:  |  :smiley:  |  :smiley:  |  :smiley:  |  :smiley:  |
| gif       | :smiley: | :smiley: |  :smiley:  |  :smiley:  | :frowning: | :frowning: | :frowning: | :frowning: |
| webp      | :smiley: | :smiley: | :frowning: | :frowning: |  :smiley:  |  :smiley:  | :frowning: | :frowning: |
| wav       | :smiley: | :smiley: | :frowning: | :frowning: |  :smiley:  |  :smiley:  | :frowning: | :frowning: |
| ogg       | :smiley: | :smiley: | :frowning: |  :smiley:  |  :smiley:  |  :smiley:  | :frowning: |  :smiley:  |
| ogg(slow) | :smiley: | :smiley: |  :smiley:  |  :smiley:  |  :smiley:  |  :smiley:  |  :smiley:  |  :smiley:  |

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
| test/sample/video/sample.flv        | U.S. Geological Survey (USGS) [Public domain], converted to flv by ffmpeg                                                                        |
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