# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-22 Bradley M. Bell
# ----------------------------------------------------------------------------
# setup
xrst_version = "21.09.07"
package_name  = "xrst"
setup_result = setup(
   name         = 'xrst',
   version      = xrst_version,
   license      = 'GPL3',
   description  = 'Exract Sphinx RST Files',
   author       = 'Bradley M. Bell',
   author_email = 'bradbell@seanet.com',
   url          = 'https://github.com/bradbell/xrst',
   scripts      = [ 'xrst/run_xrst.py' ],
)
