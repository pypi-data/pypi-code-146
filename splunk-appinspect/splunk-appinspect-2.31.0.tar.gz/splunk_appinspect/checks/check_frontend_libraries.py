# Copyright 2019 Splunk Inc. All rights reserved.

"""
### Checking for Front-end Libraries

This check looks for various front-end libraries inside of apps. 
As of 03/23/2022, we are looking at Splunk UI and it's predecessor, SplunkJS. 
This is currently an INFORMATIONAL Check. 
"""

import logging
import re

import splunk_appinspect
from splunk_appinspect.regex_matcher import JSSplunkJSMatcher, JSSplunkReactUIMatcher, JSSplunkDashboardCoreMatcher, JSSplunkVisualizationsMatcher

logger = logging.getLogger(__name__)


@splunk_appinspect.tags(
    "splunk_appinspect", "cloud", "self-service", "private_app"
)
@splunk_appinspect.cert_version(min="1.6.0")
def check_for_splunkjs(app, reporter):
    """Check that SplunkJS is being used."""
    matcher = JSSplunkJSMatcher()
    for result, file_path, lineno in matcher.match_results_iterator(
        app.app_dir, app.iterate_files(types=[".js", ".html"]), regex_option=re.IGNORECASE
    ):
        reporter_output = (
            "Splunk has begun gathering telemetry on apps submitted to appinspect, that utilize SplunkJS. Please ignore this warning as it has no impact to your Splunk app."
            f" Match: {result}"
            f" File: {file_path}"
            f" Line: {lineno}"
        )
        reporter.warn(reporter_output, file_path, lineno)

    if not matcher.has_valid_files:
        reporter_output = "SplunkJS has not been detected inside of this app. Please ignore this message as it has no impact to your Splunk App."
        reporter.not_applicable(reporter_output)


@splunk_appinspect.tags(
    "splunk_appinspect", "cloud", "self-service", "private_app"
)
@splunk_appinspect.cert_version(min="1.6.0")
def check_for_splunkreactui(app, reporter):
    """Check that @splunk/react-ui is being used."""
    matcher = JSSplunkReactUIMatcher()
    for result, file_path, lineno in matcher.match_results_iterator(
        app.app_dir, app.iterate_files(types=[".js",".jsx",".html",".json"]), regex_option=re.IGNORECASE
    ):
        reporter_output = (
            "Splunk has begun gathering telemetry on apps submitted to appinspect, that utilize @splunk/react-ui. Please ignore this warning as it has no impact to your Splunk app."

            f" Match: {result}"
            f" File: {file_path}"
            f" Line: {lineno}"
        )
        reporter.warn(reporter_output, file_path, lineno)

    if not matcher.has_valid_files:
        reporter_output = "@splunk/react-ui has not been detected inside of this app. Please ignore this message as it has no impact to your Splunk App."
        reporter.not_applicable(reporter_output)


@splunk_appinspect.tags(
    "splunk_appinspect", "cloud", "self-service", "private_app"
)
@splunk_appinspect.cert_version(min="1.6.0")
def check_for_splunkvisualizations(app, reporter):
    """Check that @splunk/visualizations is being used."""
    matcher = JSSplunkVisualizationsMatcher()
    for result, file_path, lineno in matcher.match_results_iterator(
        app.app_dir, app.iterate_files(types=[".js",".jsx",".html",".json"]), regex_option=re.IGNORECASE
    ):
        reporter_output = (
            "Splunk has begun gathering telemetry on apps submitted to appinspect, that utilize @splunk/visualizations. Please ignore this warning as it has no impact to your Splunk app."
            f" Match: {result}"
            f" File: {file_path}"
            f" Line: {lineno}"
        )
        reporter.warn(reporter_output, file_path, lineno)

    if not matcher.has_valid_files:
        reporter_output = "@splunk/visualizations has not been detected inside of this app. Please ignore this message as it has no impact to your Splunk App."
        reporter.not_applicable(reporter_output)


@splunk_appinspect.tags(
    "splunk_appinspect", "cloud", "self-service", "private_app"
)
@splunk_appinspect.cert_version(min="1.6.0")
def check_for_splunkdashboardcore(app, reporter):
    """Check that @splunk/dashboard-core is being used."""
    matcher = JSSplunkDashboardCoreMatcher()
    for result, file_path, lineno in matcher.match_results_iterator(
        app.app_dir, app.iterate_files(types=[".js",".jsx",".html",".json"]), regex_option=re.IGNORECASE
    ):
        reporter_output = (
            "Splunk has begun gathering telemetry on apps submitted to appinspect, that utilize @splunk/dashboard-core. Please ignore this warning as it has no impact to your Splunk app."
            f" Match: {result}"
            f" File: {file_path}"
            f" Line: {lineno}"
        )
        
        reporter.warn(reporter_output, file_path, lineno)

    if not matcher.has_valid_files:
        reporter_output = "@splunk/dashboard-core has not been detected inside of this app. Please ignore this message as it has no impact to your Splunk App."
        reporter.not_applicable(reporter_output)

