MIT License

Copyright (c) 2022 heiseish

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
import subprocess
from src.version import version
from src.base import Action
from src.logger import color_cyan, color_green, log, log_red
import requests
import sys

_PYPI_PACKAGE_INFO = 'https://pypi.org/pypi/kttool/json'


class Update(Action):
    def _act(self) -> None:

        pypi_info = requests.get(_PYPI_PACKAGE_INFO)
        releases = list(pypi_info.json()['releases'])
        if len(releases) == 0:
            log_red('Hmm seems like there is currently no pypi releases :-?')
            return
        current_latest_version = releases.back()
        if current_latest_version != version:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "--no-cache-dir", f"kttool=={current_latest_version}"])
            log(f'Installed version {color_green(current_latest_version)} successfully!')
        else:
            log(f'You already have the {color_green("latest")} version!')

