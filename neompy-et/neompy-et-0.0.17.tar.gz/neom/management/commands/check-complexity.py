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

import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser

try:
    import radon
except ImportError as error:
    raise CommandError("radon package not installed") from error


class Command(BaseCommand):
    help = "Run analysis tool to compute Cyclomatic Complexity."

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("module", help="Source code base")
        parser.add_argument(
            "--min_score",
            default="B",
            choices=["A", "B", "C", "D", "E", "F"],
            help="Minimum score to show",
        )
        parser.add_argument(
            "--check",
            default=False,
            action="store_true",
            help="Raise an exception when complexity fails",
        )

    def handle(self, *args, **options):
        basedir = Path(settings.BASE_DIR)

        if not basedir.is_dir():
            raise CommandError(f"Invalid project directory: {basedir}")

        if not (basedir / "manage.py").exists():
            raise CommandError(f"No project directory: {basedir}")

        module = options["module"]
        min_score = options["min_score"]
        check = options["check"]

        try:
            result = subprocess.run(
                " ".join(
                    (
                        "radon",
                        "cc",
                        "--show-complexity",
                        "--order",
                        "SCORE",
                        "--min",
                        min_score,
                        module,
                    )
                ),
                shell=True,
                check=True,
                capture_output=check,
            )
        except subprocess.CalledProcessError:
            raise CommandError(f"Radon execution: {radon.__version__}")

        if check and result.stdout:
            raise CommandError(
                f"Check complexity error:\n{result.stdout.decode()}"
            )
