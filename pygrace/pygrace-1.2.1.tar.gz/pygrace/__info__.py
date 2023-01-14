#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pygrace/blob/master/LICENSE
'''
------------------------------------
pygrace: Python bindings to xmgrace.
------------------------------------

About Pygrace
=============

``pygrace`` was designed to enable the construction and use of ``xmgrace`` projects from python.  ``pygrace`` provides a collection of classes that serve as editable templates for elements of a xmgrace project. The inheritance structure of ``pygrace`` mirrors the structure of ``xmgrace``.

``pygrace`` ``Project`` objects are used to construct and save ``xmgrace`` project files (.agr). ``Project`` files capture the state of a ``xmgrace`` session, including the figures, settings, and current variables.

.. image:: https://github.com/uqfoundation/pygrace/raw/master/docs/source/_static/crow_diagram.png
   :alt: pygrace project

A more detailed diagram of all the attributes of ``pygrace`` template objects can be found at https://github.com/uqfoundation/pygrace/blob/master/docs/diagrams/diagram.pdf, while a handy cheatsheet of the methods and attributes of each ``pygrace`` template class can be found at https://github.com/uqfoundation/pygrace/blob/master/docs/diagrams/cheatsheet.pdf. This cheatsheet can be dynamically generated through use of the ``write_cheatsheet`` method, available from the ``Project`` class.

``pygrace`` is in active development, so any user feedback, bug reports, comments, or suggestions are highly appreciated.  A list of issues is located at https://github.com/uqfoundation/pygrace/issues, with a legacy list maintained at https://github.com/pygrace/pygrace/issues.


Major Features
==============

``pygrace`` provides an object-oriented python interface for the efficient construction of ``xmgrace`` projects (e.g. highly-customizable publication-quality single and multi-figure plots). ``pygrace`` provides:

    - an object-relational mapping from python objects to a ``xmgrace`` project
    - an interactive python-based ``grace>`` prompt for ``xmgrace`` commands
    - a set of high-level python functions for drawing ``xmgrace`` ``Graphs``

Current Release
===============

The latest released version of ``pygrace`` is available from:

    https://pypi.org/project/pygrace

``pygrace`` is distributed under a 3-clause BSD license.

Development Version
===================

You can get the latest development version with all the shiny new features at:

    https://github.com/uqfoundation

If you have a new contribution, please submit a pull request.


Installation
============

``pygrace`` can be installed with ``pip``::

    $ pip install pygrace

It is assumed ``xmgrace`` is already installed and on the user's ``$PATH``.  ``xmgrace`` is available at:

    https://plasma-gate.weizmann.ac.il/pub/grace/src/

Alternately, ``xmgrace`` typically can be installed with most package managers. For example::

    $ apt-get install grace # on Linux
    $ brew install grace # on MacOS

Installing an Xserver from X.org (``xorg``, ``xorg-server``, ``xquartz``, or similar, depending on your operating system and package manager) is also required to open the ``xmgrace`` GUI.


Requirements
============

``pygrace`` requires:

    - ``python`` (or ``pypy``), **>=3.7**
    - ``setuptools``, **>=42**
    - ``cython``, **>=0.29.30**
    - ``numpy``, **>=1.0**
    - ``mpmath``, **>=0.19**

Additional requirements:

    - ``xmgrace``, **>=5.1.14**


Basic Usage
===========

start a ``pygrace`` project file::

    >>> from pygrace.project import Project
    >>> plot = Project()

add a ``Graph`` to the ``Project`` instance::

    >>> graph = plot.add_graph()
    >>> graph.title.text = 'Hello, world!'

add a ``DataSet`` to the graph::

    >>> data = [(0, 0), (0.5, 0.75), (1, 1)]
    >>> dataset = graph.add_dataset(data)

save the ``Project`` to a xmgrace project file (.agr format)::

    >>> plot.saveall('00_helloworld.agr')

then, open the project file with xmgrace::

    $ xmgrace 00_helloworld.agr

.. image:: https://github.com/uqfoundation/pygrace/raw/master/docs/source/_static/00_helloworld.png
   :alt: 00_helloworld

find out more about ``pygrace`` at http://pygrace.rtfd.io or browse some more of the examples at https://github.com/uqfoundation/pygrace/tree/master/examples.

for example::

    $ python 05_colorplot.py
    $ xmgrace 05_colorplot.agr

.. image:: https://github.com/uqfoundation/pygrace/raw/master/docs/source/_static/05_colorplot.png
   :alt: 05_colorplot

and::

    $ python 08_latexlabels.py
    $ xmgrace 08_latexlabels.agr

.. image:: https://github.com/uqfoundation/pygrace/raw/master/docs/source/_static/08_latexlabels.png
   :alt: 08_latexlabels


we can also work in an interactive xmgrace session::

    >>> from pygrace import grace
    >>> pg = grace()

use xmgrace methods directly from the python interpreter::

    >>> import numpy as np
    >>> x = np.arange(21) * np.pi/10
    >>> pg.plot(x, np.sin(x))

.. image:: https://github.com/uqfoundation/pygrace/raw/master/docs/source/_static/sin.png
   :alt: sin

push variables into xmgrace and interact with the xmgrace scripting language::

    >>> pg.put('x', x)
    >>> pg.put('y', np.cos(x))
    >>> pg.eval('s0 line color 2')
    >>> pg.eval('plot(x,y)')

.. image:: https://github.com/uqfoundation/pygrace/raw/master/docs/source/_static/cos.png
   :alt: cos

use the interactive xmgrace prompt::

    >>> pg.prompt()
    grace interface:
    vars=
         y
         x
    grace> histoPlot(y)
    grace> s0 fill color 3
    grace> redraw()
    grace> exit

.. image:: https://github.com/uqfoundation/pygrace/raw/master/docs/source/_static/histoPlot.png
   :alt: histoPlot

check variables in xmgrace session::

    >>> list(pg.who().keys())
    ['x', 'y']
    >>> pg.who('x')
    array([0.        , 0.31415927, 0.62831853, 0.9424778 , 1.25663706,
           1.57079633, 1.88495559, 2.19911486, 2.51327412, 2.82743339,
           3.14159265, 3.45575192, 3.76991118, 4.08407045, 4.39822972,
           4.71238898, 5.02654825, 5.34070751, 5.65486678, 5.96902604,
           6.28318531])

get variables back into python from xmgrace::

    >>> cosx = pg.get('y')

use shortcuts for put, eval, and get::

    >>> pg.z = 0.5
    >>> pg('print(z)')
    0.5
    >>> pg.z + cosx
    array([ 1.5       ,  1.45105652,  1.30901699,  1.08778525,  0.80901699,
            0.5       ,  0.19098301, -0.08778525, -0.30901699, -0.45105652,
           -0.5       , -0.45105652, -0.30901699, -0.08778525,  0.19098301,
            0.5       ,  0.80901699,  1.08778525,  1.30901699,  1.45105652,
            1.5       ])

delete variables from xmgrace::

    >>> pg.delete('x')
    >>> pg.delete('y')

save the current session to a project file, then exit::

    >>> pg.saveall('histoPlot.agr')
    >>> pg.exit()

start a new interactive xmgrace session from the saved project::

    >>> pg = grace(project='histoPlot.agr')


More Information
================

Probably the best way to get started is to look at the documentation at
http://pygrace.rtfd.io. Also see ``pygrace.tests`` for a set of scripts that
demonstrate several of the many features of ``pygrace``.
You can run the test suite with ``python -m pygrace.tests``. 
Also see ``pygrace.examples`` for examples that demonstrate the construction
of ``xmgrace`` project files (.agr). ``pygrace.examples.interactive`` includes
examples of using ``python`` to interact with a live ``xmgrace`` session.
The source code is relatively well documented, so some questions may be resolved by inspecting the code itself.  However, please feel free to submit a ticket on github, or ask a question on stackoverflow (**@Mike McKerns**).
If you would like to share how you use ``pygrace`` in your work, please send
an email (to **mmckerns at uqfoundation dot org**).


Citation 
========

If you use ``pygrace`` to do research that leads to publication, we ask that you
acknowledge use of ``pygrace`` by citing the following in your publication::

    Michael McKerns, Dean Malmgren, Mike Stringer, and Daniel Stouffer,
    "pygrace: python bindings to xmgrace", 2005- ;
    https://github.com/uqfoundation/pygrace

Please see https://pygrace.github.io/ for further information on an earlier version of ``pygrace`` developed by Dean Malmgren, Mike Stringer, and members of the Amaral Lab, and later maintained by Daniel Stouffer and members of the Stouffer Lab. This code has been merged into the original ``pygrace`` developed by Mike McKerns.
'''

__version__ = '1.2.1'
__author__ = 'Mike McKerns'

__license__ = '''
Copyright (c) 2004-2016 California Institute of Technology.
Copyright (c) 2013 Daniel Stouffer.
Copyright (c) 2023 The Uncertainty Quantification Foundation.
All rights reserved.

This software is available subject to the conditions and terms laid
out below. By downloading and using this software you are agreeing
to the following conditions.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met::

    - Redistribution of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    - Redistribution in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentations and/or other materials provided with the distribution.

    - Neither the names of the copyright holders nor the names of any of
      the contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
