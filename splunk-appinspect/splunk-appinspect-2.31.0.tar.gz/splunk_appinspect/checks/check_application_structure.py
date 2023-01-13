# Copyright 2019 Splunk Inc. All rights reserved.

"""
### Directory structure standards

Ensure that the directories and files in the app adhere to hierarchy standards.
"""

import logging
import os
import re
import string

import splunk_appinspect
from splunk_appinspect.common.file_hash import md5
from splunk_appinspect.splunk import normalizeBoolean

report_display_order = 2
logger = logging.getLogger(__name__)


@splunk_appinspect.tags(
    "splunk_appinspect", "appapproval", "cloud", "self-service", "private_app", "private_victoria", "private_classic"
)
@splunk_appinspect.cert_version(min="1.0.0")
@splunk_appinspect.display(report_display_order=1)
def check_that_local_does_not_exist(app, reporter):
    """Check that the 'local' directory does not exist.  All configuration
    should be in the 'default' directory.
    """
    if app.directory_exists("local"):
        reporter_output = "A 'local' directory exists in the app."
        reporter.fail(reporter_output)


@splunk_appinspect.tags(
    "splunk_appinspect",
    "cloud",
    "self-service",
    "private_app",
    "private_victoria",
    "private_classic"
)
@splunk_appinspect.cert_version(min="1.1.9")
def check_for_local_meta(app, reporter):
    """Check that the file 'local.meta' does not exist.  All metadata
    permissions should be set in 'default.meta'.
    """
    if app.file_exists("metadata", "local.meta"):
        file_path = os.path.join("metadata", "local.meta")
        reporter_output = (
            "Do not supply a local.meta file- put all settings"
            f" in default.meta. File: {file_path}"
        )
        reporter.fail(reporter_output, file_path)


@splunk_appinspect.tags("cloud", "private_app", "private_victoria", "private_classic")
@splunk_appinspect.cert_version(min="1.1.16")
def check_that_local_passwords_conf_does_not_exist(app, reporter):
    """Check that `local/passwords.conf` does not exist.  Password files are not
    transferable between instances.
    """
    if app.directory_exists("local"):
        if app.file_exists("local", "passwords.conf"):
            file_path = os.path.join("local", "passwords.conf")
            reporter_output = (
                "A 'passwords.conf' file exists in the 'local'"
                f" directory of the app. File: {file_path}"
            )
            reporter.fail(reporter_output, file_path)
        else:
            pass  # No passwords.conf so it passes
    else:
        reporter_output = "The local directory does not exist."
        reporter.not_applicable(reporter_output)


@splunk_appinspect.tags(
    "splunk_appinspect",
    "appapproval",
    "cloud",
    "private_app",
    "private_victoria",
    "private_classic"
)
@splunk_appinspect.cert_version(min="1.3.2")
def check_that_directory_name_matches_package_id(app, reporter, included_tags):
    """Check that when decompressed the Splunk app directory name matches the `id` property
    in the [package] stanza in `app.conf`.
    For Cloud apps, the `id` property must exist and match the app directory name.
    For on-premise apps, if the `id` property exists, it must match the app directory name;
    if there is no `id` property, `check_for_updates` must be set to False in `app.conf` for the check to pass.
    """
    if app.file_exists("default", "app.conf"):
        filename = os.path.join("default", "app.conf")
        uncompressed_directory_name = app.name
        app_configuration_file = app.get_config("app.conf")
        if app_configuration_file.has_section("package"):  # with [package] stanza
            package_configuration_section = app_configuration_file.get_section(
                "package"
            )
            if package_configuration_section.has_option("id"):  # with package id
                package_stanza_id_property = package_configuration_section.get_option(
                    "id"
                ).value
                if package_stanza_id_property != uncompressed_directory_name:
                    # Fail, app id is present but id does not match directory name
                    lineno = package_configuration_section.get_option("id").lineno
                    reporter_output = (
                        "The `app.conf` [package] stanza has an `id` property"
                        " that does not match the uncompressed directory's name."
                        f" `app.conf` [package] id: {package_stanza_id_property}"
                        f" uncompressed directory name: {uncompressed_directory_name}."
                        f" File: {filename}, Line: {lineno}."
                    )
                    reporter.fail(reporter_output, filename, lineno)
            else:  # without package id
                # cloud fail if no package id
                # appinspect fail if 'check_for_updates = True' or no 'check_for_updates'
                if "cloud" in included_tags:
                    lineno = package_configuration_section.lineno
                    reporter_output = (
                        "No `id` property found in [package] stanza. "
                        "Please add a valid `id`. "
                        f"File: {filename}, Line: {lineno}."
                    )
                    reporter.fail(reporter_output, filename, lineno)

                elif not package_configuration_section.has_option(
                    "check_for_updates"
                ) or _is_update_enabled(
                    package_configuration_section.get_option("check_for_updates").value
                ):
                    # Fail, app id isn't present but updates are enabled
                    lineno = (
                        package_configuration_section.get_option(
                            "check_for_updates"
                        ).lineno
                        if package_configuration_section.has_option("check_for_updates")
                        else package_configuration_section.lineno
                    )
                    reporter_output = (
                        "The `check_for_updates` property is enabled, "
                        "but no `id` property is defined. Please disable "
                        "`check_for_updates` or set the `id` property "
                        "to the uncompressed directory name of the app. "
                        f"File: {filename}, Line: {lineno}."
                    )
                    reporter.fail(reporter_output, filename, lineno)
        else:  # without [package] stanza
            # Fail, the package stanza doesn't exist.
            # Different message for cloud check and others
            if "cloud" in included_tags:
                reporter_output = (
                    "The `app.conf` [package] stanza does not exist. "
                    "Please add [package] stanza with valid `id` property. "
                    f"File: {filename}"
                )
            else:
                reporter_output = (
                    "The `app.conf` [package] stanza does not "
                    "exist. Please disable `check_for_updates` "
                    "or set the `id` property in the [package] "
                    f"stanza. File: {filename}"
                )
            reporter.fail(reporter_output, filename)
    else:
        reporter_output = "No app.conf file was detected."
        reporter.fail(reporter_output)


def _is_update_enabled(check_for_updates_value):
    try:
        return normalizeBoolean(check_for_updates_value)
    except ValueError:
        return True


@splunk_appinspect.tags("splunk_appinspect", "cloud", "private_app", "private_victoria", "private_classic")
@splunk_appinspect.cert_version(min="1.5.0")
def check_filenames_for_spaces(app, reporter):
    """Check that app has no .conf or dashboard filenames that contain spaces.
    Splunk software does not support such files.
    """
    # <app_dir>/default contains configuration required by your app and dashboard files,
    # so set it as the base directory.
    for directory, file, _ in list(
        app.iterate_files(basedir="default", types=[".conf"])
    ) + list(app.iterate_files(basedir="default/data", types=[".xml"])):
        if re.search(r"\s", file):
            filename = os.path.join(directory, file)
            # The regex that extracts the filename would extract wrong file name due to the space,
            # so here I use `Filename: {}`.
            reporter_output = f"A conf or dashboard file contains a space in the filename. Filename: {filename}"
            reporter.fail(reporter_output)


@splunk_appinspect.tags("splunk_appinspect", "cloud", "private_app", "private_victoria", "private_classic")
@splunk_appinspect.cert_version(min="1.6.0")
def check_that_app_name_config_is_valid(app, reporter):
    """Check that the app name does not start with digits"""
    if app.package.app_cloud_name.startswith(tuple(string.digits)):
        reporter_output = "The app name (%s) cannot start with digits!" % app.name
        reporter.fail(reporter_output)
    else:
        pass
