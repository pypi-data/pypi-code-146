# Copyright 2019 Splunk Inc. All rights reserved.

"""
### Meta file standards

Ensure that all meta files located in the **/metadata** folder are well formed and valid.
"""
import collections
import logging
import os
import re

import splunk_appinspect

report_display_order = 2
logger = logging.getLogger(__name__)

RE_META_ACCESS = re.compile(
    r"read:\[(?P<read>[\w\,\*]+)\],write:\[(?P<write>[\w\,\*]+)\]"
)


@splunk_appinspect.cert_version(min="1.6.1")
@splunk_appinspect.tags("splunk_appinspect")
def check_validate_no_duplicate_stanzas_in_meta_files(app, reporter):
    """Check that `.meta` files do not have duplicate
    [stanzas](https://docs.splunk.com/Splexicon:Stanza).
    """
    stanzas_regex = r"^\[(.*)\]"
    stanzas = app.search_for_pattern(stanzas_regex, types=[".meta"])
    stanzas_found = collections.defaultdict(list)

    for fileref_output, match in stanzas:
        filepath, line_number = fileref_output.rsplit(":", 1)
        file_stanza = (filepath, match.group())
        stanzas_found[file_stanza].append(line_number)

    for key, linenos in iter(stanzas_found.items()):
        if len(linenos) > 1:
            for lineno in linenos:
                reporter_output = f"Duplicate {key[1]} stanzas were found. File: {key[0]}, Line: {lineno}."
                reporter.fail(reporter_output, key[0], lineno)


@splunk_appinspect.tags("splunk_appinspect")
@splunk_appinspect.cert_version(min="1.1.12")
def check_meta_file_parsing(app, reporter):
    """Check that all `.meta` files parse with no trailing whitespace after
    continuations with no duplicate stanzas or options.
    """
    for directory, file, _ in app.iterate_files(types=[".meta"]):
        file_path = os.path.join(directory, file)
        meta = app.get_meta(file, directory=directory)
        for err, line, section in meta.errors:
            reporter_output = (
                f"{err} at line {line} in [{section}] of {file}."
                " File: {file_path}, Line: {line}."
            )
            reporter.fail(reporter_output, file_path, line)


@splunk_appinspect.tags("cloud", "private_app", "private_victoria", "private_classic", "future")
def check_kos_are_accessible(app, reporter):
    """Check that knowledge objects with access control restrictions defined in
     *.meta files are accessible to customers in Splunk Cloud."""
    meta_files = []
    if app.file_exists("metadata", "default.meta"):
        meta_files.append(app.get_meta("default.meta"))
    if app.file_exists("metadata", "local.meta"):
        meta_files.append(app.get_meta("local.meta"))

    for meta_file in meta_files:
        for section in meta_file.sections():
            if not section.has_option("access"):
                continue

            access_option = section.get_option("access")
            match = RE_META_ACCESS.match(access_option.value.replace(" ", ""))
            if not match:
                continue

            read = match.group("read")
            write = match.group("write")
            if read == "admin" or write == "admin":
                # Will promote to a failure later on.
                reporter.warn(
                    "In Splunk Cloud, customers have access to the sc_admin role instead of the admin role. "
                    "Your customers will not be able to access knowledge objects where the only assigned role is admin. "
                    "Please consider also including the sc_admin role for compatibility with Splunk Cloud.",
                    file_name=meta_file.name,
                    line_number=access_option.lineno,
                )
            elif (("admin" in read.split(",") and not "sc_admin" in read.split(",")) or
                  "admin" in write.split(",") and not "sc_admin" in write.split(",")):
                reporter.warn(
                    "The 'admin' role is not available to Splunk Cloud customers. "
                    "Please consider also including the 'sc_admin' role if you want "
                    "Splunk Cloud customer administrators to be able to access this knowledge object",
                    file_name=meta_file.name,
                    line_number=access_option.lineno,
                )
