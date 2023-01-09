# Copyright 2022 neomadas-dev
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser

try:
    import autopep8
except ImportError as error:
    raise CommandError("autopep8 package not installed") from error

try:
    import isort
except ImportError as error:
    raise CommandError("isort package not installed") from error


class Command(BaseCommand):
    help = "Apply pep8 format each python file."

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "--file",
            "-f",
            help="Use when you want to apply format this file",
        )

    def handle(self, *args, **options):
        basedir = Path(settings.BASE_DIR)

        if not basedir.is_dir():
            raise CommandError(f"Invalid project directory: {basedir}")

        autopep8.DEFAULT_INDENT_SIZE = 2

        paths = (
            [options["file"]] if options["file"] else basedir.glob("**/*.py")
        )

        for path in paths:
            name = str(path)
            autopep8.main(("autopep8", "-i", "-a", "-a", name))
            isort.file(name, quiet=True)
