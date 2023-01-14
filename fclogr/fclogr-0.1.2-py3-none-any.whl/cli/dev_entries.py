# SPDX-FileCopyrightText: 2023 Maxwell G <gotmax@e.email>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import logging
import shutil
import subprocess
import sys
import tarfile
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING

import pygit2
import specfile as sfile

from .base import Command

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath

LOG = logging.getLogger(__name__)


@dataclasses.dataclass
class GitLogEntry:
    commit: pygit2.Commit
    baseversion: str
    index: str | int = 1

    @property
    def message(self) -> list[str]:
        message = self.commit.message.splitlines()
        # --allow-empty-message
        if not message:
            message = ["bump"]
        return ["- " + message[0]]

    @property
    def author(self) -> str:
        return f"{self.commit.author.name} <{self.commit.author.email}>"

    @property
    def date(self) -> dt.date:
        # Use UTC date
        timestamp = dt.datetime.fromtimestamp(
            self.commit.commit_time, tz=dt.timezone.utc
        )
        return dt.date(timestamp.year, timestamp.month, timestamp.day)

    @property
    def version(self) -> str:
        return "{ref}^{num}.{date:%Y%m%d}.{hash}".format(
            ref=self.baseversion,
            num=self.index,
            date=self.date,
            hash=self.commit.short_id,
        )

    @property
    def evr(self) -> str:
        return self.version + "-1"

    @property
    def entry(self) -> sfile.changelog.ChangelogEntry:
        return sfile.changelog.ChangelogEntry.assemble(
            self.date, self.author, self.message, self.evr
        )

    def add_to_clog(self, clog: sfile.changelog.Changelog) -> None:
        if self.entry not in clog:
            clog.append(self.entry)


class DevEntries(Command):
    def __init__(
        self,
        *,
        specpath: Path | None,
        outdir: Path,
        stdout: bool = False,
        archive: bool,
        last_ref: str,
    ) -> None:
        try:
            self.specpath = self._v_specpath(specpath)
        except ValueError as err:
            sys.exit(str(err))

        self.outdir: Path = outdir or self.specpath
        if not self.outdir.is_dir():
            sys.exit(f"--outdir '{self.outdir}' is not a directory")

        self.stdout: bool = stdout

        self.archive: bool = archive

        self.git_path: Path = Path.cwd()

        try:
            self.spec = sfile.Specfile(self.specpath)
        except sfile.exceptions.SpecfileException as err:
            sys.exit(f"Failed to load specfile: {err}")

        try:
            self.repository = pygit2.Repository(str(self.git_path))
        except pygit2.GitError:
            sys.exit(f"{self.git_path} is not in a git repository")

        try:
            self.last_ref: str = last_ref
        except KeyError as exc:
            LOG.debug("", exc_info=exc)
            sys.exit(f"{last_ref} is not a valid commit reference")

        self.glog_entries: list[GitLogEntry] = []

    @classmethod
    def make_parser(
        cls, parser_func: Callable = argparse.ArgumentParser, standalone=False, **kwargs
    ) -> argparse.ArgumentParser:
        del standalone
        parser = parser_func(**kwargs)
        parser.add_argument("specpath", nargs="?", type=Path)
        parser.add_argument("-r", "--last-ref", required=True)
        parser.add_argument("-o", "--outdir", default=Path.cwd(), type=Path)
        parser.add_argument("--stdout", action="store_true")
        parser.add_argument("-A", "--archive", action="store_true")
        return parser

    def _v_specpath(self, path: Path | None = None) -> Path:
        if not path:
            pwd = Path.cwd()
            path = pwd.joinpath(pwd.name + ".spec")
        if not path.is_file() or path.suffix != ".spec":
            raise ValueError(f"{path} must exist an end with '.spec'")
        return path

    @property
    def last_ref(self) -> str:
        return self._last_ref

    @last_ref.setter
    def last_ref(self, value: str) -> None:
        self._last_ref = value.lstrip("v")
        ref = self.repository.revparse_single(value)
        if isinstance(ref, pygit2.Tag):
            self._last_ref = self._last_ref.lstrip("v")
            self.last_ref_hash = ref.target
            return
        self.last_ref_hash = ref.target if hasattr(ref, "target") else ref.id

    def write_spec(self) -> None:
        content = str(self.spec)
        if self.stdout:
            sys.stdout.write(content)
            return None
        out = self.outdir.joinpath(self.specpath.name)
        try:
            out.write_text(content)
        except OSError as err:
            sys.exit(f"Failed to output specfile to {out}: {err}")

    def add_entries(self) -> None:
        walker = self.repository.walk(
            self.repository.head.target, pygit2.GIT_SORT_REVERSE
        )
        walker.hide(self.last_ref_hash)
        with self.spec.changelog() as changelog:
            for index, commit in enumerate(walker):
                self.last_entry = GitLogEntry(
                    commit=commit, index=index + 1, baseversion=self.last_ref
                )
                self.last_entry.add_to_clog(changelog)

    def create_archive(self, nv: str):
        with tarfile.open(self.outdir / f"{nv}.tar.gz", "w") as tf:
            self.repository.write_archive(
                self.repository.head.target, tf, prefix=f"{nv}/"
            )

    def run(self) -> None:
        self.add_entries()
        self.spec.set_version_and_release(self.last_entry.version, "1")
        nv = f"{self.spec.expanded_name}-{self.spec.expanded_version}"
        self.write_spec()
        if self.archive:
            self.create_archive(nv)


class DevSRPM(DevEntries):
    def __init__(
        self, *, specpath: Path | None, last_ref: str, srpm_outdir: Path, keep: bool
    ) -> None:
        self.keep: bool = keep
        self.srpm_outdir = srpm_outdir
        outdir = self.srpm_outdir if keep else Path(tempfile.mkdtemp())
        self.cleanup: StrOrBytesPath | None = None if self.keep else outdir
        super().__init__(
            specpath=specpath,
            last_ref=last_ref,
            outdir=outdir,
            archive=True,
            stdout=False,
        )

    def run(self) -> None:
        super().run()
        try:
            self.build_srpm()
        finally:
            if self.cleanup:
                shutil.rmtree(self.cleanup)

    def build_srpm(self) -> None:
        defines = {
            "_topdir": self.outdir,
            "_sourcedir": self.outdir,
            "_specdir": self.outdir,
            "_srpmdir": self.srpm_outdir,
        }
        cmd: list[StrOrBytesPath] = [
            "rpmbuild",
            "-bs",
            self.outdir / self.specpath.name,
        ]
        for name, value in defines.items():
            cmd.extend(("-D", f"{name} {value}"))
        LOG.info("Building SRPM: %s", cmd)
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as err:
            LOG.error("Failed to run: %s", cmd)
            sys.exit(err.returncode)

    @classmethod
    def make_parser(
        cls, parser_func: Callable = argparse.ArgumentParser, standalone=False, **kwargs
    ) -> argparse.ArgumentParser:
        del standalone
        parser = parser_func(**kwargs)
        parser.add_argument("specpath", nargs="?", type=Path)
        parser.add_argument("-r", "--last-ref", required=True)
        parser.add_argument(
            "-o",
            "--outdir",
            default=Path.cwd(),
            type=Path,
            dest="srpm_outdir",
            metavar="OUTDIR",
        )
        parser.add_argument("-k", "--keep", action="store_true")
        return parser
