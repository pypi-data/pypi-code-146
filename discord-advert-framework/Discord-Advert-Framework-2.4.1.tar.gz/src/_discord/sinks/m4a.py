"""
The MIT License (MIT)

Copyright (c) 2021-present Pycord Development

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import io
import os
import subprocess
import time

from .core import CREATE_NO_WINDOW, Filters, Sink, default_filters
from .errors import M4ASinkError


class M4ASink(Sink):
    """A special sink for .m4a files.

    .. versionadded:: 2.0
    """

    def __init__(self, *, filters=None):
        if filters is None:
            filters = default_filters
        self.filters = filters
        Filters.__init__(self, **self.filters)

        self.encoding = "m4a"
        self.vc = None
        self.audio_data = {}

    def format_audio(self, audio):
        """Formats the recorded audio.

        Raises
        ------
        M4ASinkError
            Audio may only be formatted after recording is finished.
        M4ASinkError
            Formatting the audio failed.
        """
        if self.vc.recording:
            raise M4ASinkError(
                "Audio may only be formatted after recording is finished."
            )
        m4a_file = f"{time.time()}.tmp"
        args = [
            "ffmpeg",
            "-f",
            "s16le",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-i",
            "-",
            "-f",
            "ipod",
            m4a_file,
        ]
        if os.path.exists(m4a_file):
            os.remove(
                m4a_file
            )  # process will get stuck asking whether to overwrite, if file already exists.
        try:
            process = subprocess.Popen(
                args, creationflags=CREATE_NO_WINDOW, stdin=subprocess.PIPE
            )
        except FileNotFoundError:
            raise M4ASinkError("ffmpeg was not found.") from None
        except subprocess.SubprocessError as exc:
            raise M4ASinkError(
                "Popen failed: {0.__class__.__name__}: {0}".format(exc)
            ) from exc

        process.communicate(audio.file.read())

        with open(m4a_file, "rb") as f:
            audio.file = io.BytesIO(f.read())
            audio.file.seek(0)
        os.remove(m4a_file)

        audio.on_format(self.encoding)
