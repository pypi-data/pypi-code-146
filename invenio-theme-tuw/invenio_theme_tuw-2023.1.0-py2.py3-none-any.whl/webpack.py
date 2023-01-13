# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS Webpack bundles for TU Wien theme."""

from flask_webpackext import WebpackBundleProject
from invenio_assets.webpack import WebpackThemeBundle
from pywebpack import bundles_from_entry_point

# our override for the frontend build project:
# we override the build configuration (based on the one provided in `invenio-assets`)
# in order to customize its behaviour, e.g. allowing the collection of '*.webp' images.
#
# implementation note, in case you'll need to touch this:
# `project.path` is overridden by the `_PathStorageMixin` in `flask_webpackext` and
# will point to the directory specified by `app.config['WEBPACKEXT_PROJECT_BUILDDIR']`,
# which # will be used as the working directory for `npm`, and also specifies where
# the assets from each module should be copied to.
#
# rough explanation of the arguments:
# * import_name:    the import name of the current module, will be used to determine
#                   the base path where to look for the provided assets/configs
# * project_folder: the sub-directory in which to look for the `package.json`
# * config_path:    where to put npm's `config.json` (inside the `project_folder`)
# * bundles:        the bundles that should be used for building the frontend
project = WebpackBundleProject(
    import_name=__name__,
    project_folder="build_project",
    config_path="build/config.json",
    bundles=bundles_from_entry_point("invenio_assets.webpack"),
)

# the definition of our own bundle of frontend assets, which will be collected and
# built by `pywebpack`/`flask_webpackext`/`invenio_assets`.
#
# rough explanation of the arguments:
# * import_name: similar to above
# * folder:      similar to the `project_folder` above
# * default:     default theme to use if `APP_THEME` isn't set
# * themes:      dictionary with available themes and their definitions
theme = WebpackThemeBundle(
    import_name=__name__,
    folder="theme/assets",
    default="semantic-ui",
    themes={
        "semantic-ui": {
            "entry": {
                "invenio-theme-tuw-tracking": "./js/invenio_theme_tuw/tracking/index.js",
                "invenio-theme-tuw-mobilemenu": "./js/invenio_theme_tuw/mobilemenu/index.js",
                "invenio-theme-tuw-pdf-preview": "./js/invenio_theme_tuw/pdf-preview/index.js",
                "invenio-theme-tuw-tuwstones": "./less/invenio_theme_tuw/tuwstone.less",
            },
            "dependencies": {
                "jquery": "^3.2.1",
            },
            "aliases": {
                # the 'themes/tuw' alias registers our theme (*.{override,variables})
                # as 'tuw' theme for semantic-ui
                "themes/tuw": "less/invenio_theme_tuw/theme",
                # aliases in case you would like to reference js/less files from
                # somewhere else (e.g. other modules)
                "@less/invenio_theme_tuw": "less/invenio_theme_tuw",
                "@js/invenio_theme_tuw": "js/invenio_theme_tuw",
            },
        },
    },
)
