"""Provides FilenameScanner class."""

import copy
import logging

import fs

from ...importers import match_util
from .. import errors
from .. import schemas as s
from .abstract import AbstractScanner

log = logging.getLogger(__name__)


class FilenameScanner(AbstractScanner):
    """FilenameScanner groups files together by a common prefix.

    This works by looking at the first slash (or if there is no slash, the first dot) in
    each file path, and using that as the acquisition label.
    """

    def _scan(self, subdir):
        self.validate_opts(self.opts)
        template = match_util.compile_regex(self.opts["pattern"])

        for fileinfo in self.iter_files(subdir):
            filename = fs.path.basename(fileinfo.name)
            file_context = copy.deepcopy(self.context)
            dirpath = fs.path.relpath(fs.path.dirname(fileinfo.name))

            if not match_util.extract_metadata_attributes(
                filename, template, file_context
            ):
                msg = f"File {fileinfo.name} did not match the template {self.opts['pattern']}"
                log.debug(msg)
                self.file_errors.append(
                    s.Error(
                        code=errors.FilenameDoesNotMatchTemplate.code,
                        message=msg,
                        filepath=fileinfo.name,
                    )
                )
                continue

            yield s.Item(
                type="file",
                dir=fs.path.combine(subdir, dirpath),
                filename=filename,
                files=[filename],
                files_cnt=1,
                bytes_sum=fileinfo.size,
                context=file_context,
            )

    @staticmethod
    def validate_opts(opts):
        if opts is None or "pattern" not in opts:
            raise ValueError("Filename scanner requires pattern!")

        try:
            match_util.compile_regex(opts["pattern"])
        except Exception as ex:
            log.debug("Cannot compile filename pattern.", exc_info=True)
            raise ValueError(f"Invalid filename pattern: {ex}") from ex
