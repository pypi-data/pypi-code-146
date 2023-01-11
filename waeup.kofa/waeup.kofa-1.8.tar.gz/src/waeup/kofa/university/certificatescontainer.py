## $Id: certificatescontainer.py 8367 2012-05-06 11:19:38Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
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
"""Containers for certificates.
"""
import grok
from zope.catalog.interfaces import ICatalog
from zope.component.interfaces import IFactory
from zope.component import queryUtility
from zope.interface import implementedBy
from waeup.kofa.interfaces import DuplicationError
from waeup.kofa.university.interfaces import (
    ICertificatesContainer, ICertificate)

class CertificatesContainer(grok.Container):
    """A storage for certificates.

    A :class:`CertificatesContainer` stores
    :class:`waeup.kofa.university.Certificate` instances.

    It is a :class:`grok.Container` basically acting like a standard
    Python dictionary. That means you can add certificates like items
    in a normal dictionary and also get certificates by using
    :meth:`values`, :meth:`keys`, and :meth:`items`.

    This container type is picky about its contents: only real
    certificates can be stored here and each new certificate must
    provide a unique `code`. See :meth:`addCertificate` for details.

    Each :class:`CertificatesContainer` provides
    :class:`ICertificatesContainer`.
    """
    grok.implements(ICertificatesContainer)

    def __setitem__(self, name, certificate):
        """Insert `certificate` with `name` as key into container.

        The `certificate` must be an object implementing
        :class:`waeup.kofa.university.interfaces.ICertificate`. If
        not, a :exc:`TypeError` is raised.

        If the certificate `code` does not equal `name` a
        :exc:`ValueError` is raised.

        If the `code` attribute of `certificate` is already in use by
        another certificate stored in the local site
        (:class:`waeup.kofa.app.University` instance), then a
        :exc:`waeup.kofa.interfaces.DuplicationError` will be raised.

        If `name` is already used as a key, a :exc:`KeyError` will be
        raised.
        """
        if not ICertificate.providedBy(certificate):
            raise TypeError('CertificatesContainers contain only '
                            'ICertificate instances')

        # Only accept certs with code == key.
        if certificate.code != name:
            raise ValueError('key must match certificate code: '
                             '%s, %s' % (name, certificate.code))

        # Lookup catalog. If we find none: no duplicates possible.
        cat = queryUtility(ICatalog, name='certificates_catalog', default=None)
        if cat is not None:
            entries = cat.searchResults(
                code=(certificate.code,certificate.code))
            if len(entries) > 0:
                raise DuplicationError(
                    'Certificate exists already elsewhere.', entries)
        else:
            # No catalog, then this addition won't do harm to anything.
            pass
        super(CertificatesContainer, self).__setitem__(name, certificate)

    def addCertificate(self, certificate):
        """Add `certificate` to the container.

        The certificate must be an object implementing
        :class:`waeup.kofa.university.interfaces.ICertificate`. If
        not, a :exc:`TypeError` is raised.

        The certificate will be stored in the container with its
        `code` attribute as key. If this key is already used for
        another certificate stored in the local site
        (:class:`waeup.kofa.app.University` instance), then a
        :exc:`waeup.kofa.interfaces.DuplicationError` will be raised.
        """
        self[getattr(certificate, 'code', None)] = certificate

    def clear(self):
        """Remove all contents from the certificate container.

        This methods is pretty fast and optimized. Use it instead of
        removing all items manually yourself.
        """
        # This internal function is implemented in C and thus much
        # faster as we could do it in pure Python.
        self._SampleContainer__data.clear()
        # The length attribute is 'lazy'. See `zope.container` for details.
        # This way we make sure, the next time len() is called, it returns
        # the real value and not a cached one.
        del self.__dict__['_BTreeContainer__len']

class CertificatesContainerFactory(grok.GlobalUtility):
    """A factory for certificate containers.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.CertificatesContainer')
    title = u"Create a new container for certificates.",
    description = u"This factory instantiates new containers for certificates."

    def __call__(self, *args, **kw):
        return CertificatesContainer(*args, **kw)

    def getInterfaces(self):
        return implementedBy(CertificatesContainer)
