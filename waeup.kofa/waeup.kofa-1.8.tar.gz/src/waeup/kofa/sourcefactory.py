## $Id: sourcefactory.py 12110 2014-12-02 06:43:10Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""Smarter contextual sources, that can do faster containment checks.
"""
import zc.sourcefactory.policies
from zc.sourcefactory.factories import ContextualSourceFactory
from zc.sourcefactory.source import FactoredContextualSource

class SmartFactoredContextualSource(FactoredContextualSource):
    """A contextual source that can be faster.

    Regular ContextualSources from zc.sourcefactory suffer from very
    expensive and slow containment checks. __contains__ is executed as
    a lookup over the complete set of possible values.

    If, however, a source could do this lookup faster, it had no
    chance to do that with regular ContextualSources.

    This source instead looks for a `contains()` method of a
    contextual source first and if it has one, this method is called
    with `value` and `context` as arguments.

    If a source does not provide `contains()`, the expensive default
    lookup method is done instead.
    """
    def __contains__(self, value):
        """Check whether `value` is part of the source.

        If the factored source provides a `contains(value, context)`
        method, this method is called for faster containment
        checks. If not, then the getValues() method of a factored
        source is used to examine each single item contained in the
        source.
        """
        if hasattr(self.factory, 'contains'):
            return self.factory.contains(self.context, value)
        # This is potentially expensive!
        return super(SmartFactoredContextualSource, self).__contains__(
            value)

class SmartContextualSourceFactory(ContextualSourceFactory):
    source_class = SmartFactoredContextualSource

class SmartBasicContextualSourceFactory(
    SmartContextualSourceFactory,
    zc.sourcefactory.policies.BasicContextualSourcePolicy):
    """Abstract base implementation for a basic but smart contextual
    source factory.

    These factories use any `contains(value, context)` method of
    factored sources to speed up containment checks.

    Instances of this class can be used as replacement for
    `zc.sourcefactory.BasicContextualSourceFactory`. If your
    implementation derived from :class:`SmartBasicContextualFactory`
    additionally provides a smart `contains()` method, you only get
    benefits from using this class.

    The basic requirements for a working
    `SmartBasicContextualSourceFactory` are the same as for regular
    ones: you have to implement a `getValues(context)` method. You can
    (optionally) implements a `contains(value, context)` method.
    """
