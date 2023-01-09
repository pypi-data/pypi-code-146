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

from importlib.util import module_from_spec, spec_from_file_location

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Idea:
      Define populator classes like

      class SomePopulator(Populator):
        def populate(self):
          ...
          self.previous_populator.items[...]

          self.next_populator.send(...)

      Pass constructed items to reuse the instances.
    """

    help = "Populate database using python scripts with ORM support."

    def handle(self, *unused_args, **unsed_options):
        basedir = settings.NEOM_POPULATION["DIR"]

        if not basedir.is_dir():
            raise CommandError(f"Invalid project directory: {basedir}")

        filenames = settings.NEOM_POPULATION["POPULATORS"]

        pairs = []
        for filename in filenames:
            path = basedir / (filename + ".py")

            spec = spec_from_file_location(filename, path)
            population_module = module_from_spec(spec)
            spec.loader.exec_module(population_module)

            populator = population_module.populate
            pairs.append((filename, populator))

        self.stdout.write(self.style.MIGRATE_HEADING("Populate data:"))
        for label, call in pairs:
            self.stdout.write(f"  Creating {label}...", ending="")
            call()
            self.stdout.write(self.style.SUCCESS(" OK"))
