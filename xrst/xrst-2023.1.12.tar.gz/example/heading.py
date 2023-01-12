# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-22 Bradley M. Bell
# ----------------------------------------------------------------------------
"""
{xrst_begin heading_example}

Heading and Link Example
########################
Both the page name and page title are level zero headings for a page.
Using the *page_name* label displays the page name as its linking text;
e.g. for this page both the label and linking text are::

   heading_example

The *page_name*  name followed by ``-title`` displays the page title
as its linking text;
e.g. for this page the label is ``heading_example-title``
and linking text is::

   Heading and Link Example


Level One
*********
The label for this heading is ``heading_example@Level One``.

Level Two
=========
The label for this heading is ``heading_example@Level One@Level Two``.

Another Level One
*****************
The label for this heading is ``heading_example@Another Level One``.

Level Two\_
===========
The label for this heading is
``heading_example@Another Level One@Level Two_``.
Note that the backslash in the heading keeps ``Two_``
from being interpreted as a link.
Also note that the backslash does not appear in the
display of the heading or in the corresponding label.

x
=
A heading can have just one character.
The label for this heading is
``heading_example@Another Level One@x``.

Links
*****
These links would also work from any other page because the page name
(``heading_example`` in this case)
is included at the beginning of the target for the link:

#. :ref:`heading_example-name`
#. :ref:`heading_example-title`
#. :ref:`heading_example@Level One`
#. :ref:`heading_example@Level One@Level Two`
#. :ref:`heading_example@Another Level One`
#. :ref:`heading_example@Another Level One@Level Two_`
#. :ref:`heading_example@Another Level One@x`

Linking Headings Using :ref:
****************************
The file below demonstrates linking to headings using ``:ref:`` .

This Example File
*****************
{xrst_literal}

{xrst_end heading_example}
"""
