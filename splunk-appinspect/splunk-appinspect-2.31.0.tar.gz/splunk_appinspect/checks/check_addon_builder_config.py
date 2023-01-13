# Copyright 2019 Splunk Inc. All rights reserved.

"""
### addon_builder.conf standards

The **addon_builder.conf** file located at **default/addon_builder.conf** provides the information about the add on builder associated with the Splunk App
"""
import logging
import os

from packaging import version

import splunk_appinspect
from splunk_appinspect.app_util import AppVersionNumberMatcher

report_display_order = 5
logger = logging.getLogger(__name__)


@splunk_appinspect.tags("cloud", "private_app", "private_victoria", "private_classic")
@splunk_appinspect.cert_version(min="2.18.0")
def check_for_addon_builder_version(app, reporter):
    """Check that the `addon_builder.conf` indicates the app was built using an up-to-date version of Splunk Add-on Builder."""
    if app.file_exists("default", "addon_builder.conf"):
        filename = os.path.join("default", "addon_builder.conf")
        config = app.get_config("addon_builder.conf")
        matcher = AppVersionNumberMatcher()

        try:
            config.has_option("base", "builder_version")
            builder_version = config.get("base", "builder_version")
            if not matcher.match(builder_version):
                lineno = config.get_section("base").get_option("builder_version").lineno
                reporter_output = (
                    "Major, minor, build version numbering "
                    f"is required. File: {filename}, Line: {lineno}."
                )
                reporter.fail(reporter_output, filename, lineno)

            if version.parse(builder_version) < version.parse("4.1.0"):
                lineno = config.get_section("base").get_option("builder_version").lineno
                reporter_output = (
                    "The Add-on Builder version used to create this app is below the minimum required version of 4.1.0."
                    f"Please re-generate your add-on using at least Add-on Builder 4.1.0. "
                    f"File: {filename}, Line: {lineno}."
                )
                reporter.fail(reporter_output, filename, lineno)

        except splunk_appinspect.configuration_file.NoOptionError:
            lineno = config.get_section("base").lineno
            reporter_output = (
                "No builder_version specified in base section "
                f"of addon_builder.conf. File: {filename}, Line: {lineno}."
            )
            reporter.fail(reporter_output, filename, lineno)

        except splunk_appinspect.configuration_file.NoSectionError:
            reporter_output = (
                f"No base section found in addon_builder.conf. File: {filename}"
            )
            reporter.fail(reporter_output, file_name=filename)
    else:
        reporter_output = "`default/addon_builder.conf` does not exist."
        reporter.not_applicable(reporter_output)
