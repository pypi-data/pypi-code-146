# -*- coding: utf-8 -*-
# :Project:   SoL -- Business objects
# :Created:   sab 27 set 2008 14:00:47 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2013, 2014, 2018, 2020 Lele Gaifax
#

"""The application's model objects"""

from datetime import datetime
import logging
from uuid import uuid1

from sqlalchemy import Column, Index, event, func
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import object_session

from ..i18n import translatable_string as _
from .domains import date_t, guid_t, timestamp_t


logger = logging.getLogger(__name__)


class AbstractBase(object):
    "Abstract base entity class."

    @classmethod
    def check_insert(klass, session, fields, user_id):
        """Perform any check before an new instance is inserted.

        :param session: the SA session
        :param fields: a dictionary with the fields values
        :param user_id: either the string "admin" or the ID of the user performing the
                        operation
        """

    def check_update(self, fields):
        """Perform any check before updating the instance.

        :param fields: a mapping containing ``fieldname -> value`` associations

        This implementation does nothing, but subclasses can override it at will,
        either to `adapt` incoming values or to check their validity, raising an
        exception if something is wrong.
        """

    def delete(self):
        "Delete this instance from the database."

        object_session(self).delete(self)

    def update(self, data, missing_only=False):
        """Update entity with given data.

        :param data: a mapping kind of container
        :param missing_only: a boolean flag, ``False`` by default
        :rtype: dict
        :returns: a mapping between field name and a tuple ``(oldvalue, newvalue)``,
                  for each modified field

        First call :py:meth:`check_update` to assert the validity of incoming data,
        then update the instance fields.

        If `missing_only` is ``True`` then only the fields that are currently `empty`
        (that is, their value is either ``None`` or an empty string) are updated.
        Note that in this case an exception is made for ``bool`` fields: since in SoL
        they always have a value (i.e. they are never `missing`), they are always
        updated.
        """

        try:
            self.check_update(data)
        except Exception as e:
            logger.error('Error trying to update %r with %r: %s', self, data, e)
            raise

        changes = {}

        for attr in data:
            if hasattr(self, attr):
                cvalue = getattr(self, attr)
                if missing_only:
                    if not (cvalue is None or cvalue == '' or
                            cvalue is True or cvalue is False):
                        continue
                nvalue = data[attr]
                if ((attr in self.__table__.c and self.__table__.c[attr].type is date_t
                     and isinstance(nvalue, datetime))):
                    nvalue = nvalue.date()
                if cvalue != nvalue:
                    setattr(self, attr, nvalue)

                    # Omit automatic changes
                    if attr != 'modified':
                        changes[attr] = (cvalue, nvalue)

        return changes

    def __str__(self):
        "Return a description of the entity."

        return self.caption(html=False)

    def __repr__(self):
        "Return a representation of the entity, mostly for debugging and log purposes."

        return '<%s "%s">' % (self.__class__.__name__,
                              self.caption(html=False, localized=False))

    def caption(self, html=None, localized=True):
        """Return a possibly HTML-decorated caption of the entity.

        :param html: either ``None`` (the default) or a boolean value
        :param localized: a boolean value, ``True`` by default
        :rtype: str

        If `html` is ``None`` or ``True`` then the result may be an
        HTML representation of the entity, otherwise it is plain text.

        If `localized` is ``False`` then the localization is turned off.
        """

        return self.description


class GloballyUnique(object):
    "Mixin class for globally unique identified entities."

    _guid = Column(
        guid_t, name="guid",
        nullable=False,
        default=lambda: uuid1().hex,
        info=dict(label=_('GUID'),
                  hint=_('The globally unique identifier of the record.'),
                  hidden=True,
                  sortable=False))
    """An UUID key."""

    modified = Column(
        timestamp_t,
        nullable=False,
        server_default=func.now(),
        info=dict(label=_('Modified'),
                  hint=_('Timestamp of the last change to the record.'),
                  hidden=True))
    """Last update timestamp."""

    @hybrid_property
    def guid(self):
        "A global unique identifier for this entity."
        return self._guid

    @guid.setter
    def guid(self, guid):
        if self._guid:
            if self._guid != guid:
                raise ValueError('Cannot update instance guid')
        else:
            self._guid = guid

    @staticmethod
    def __table_args__(cls):
        # Put these fields near the end of the table, when creating it
        # from scratch
        if cls._guid._creation_order < 1000:
            cls._guid._creation_order = 1000
            cls.modified._creation_order = 1001

        return (Index('%s_guid' % cls.__tablename__.lower(), 'guid',
                      unique=True),)


Base = declarative_base(cls=AbstractBase)
"The common parent class for all declarative mapped classed."


from .board import Board               # noqa
from .championship import Championship # noqa
from .club import Club                 # noqa
from .competitor import Competitor     # noqa
from .match import Match               # noqa
from .mergedplayer import MergedPlayer # noqa
from .player import Player             # noqa
from .rate import Rate                 # noqa
from .rating import Rating             # noqa
from .tourney import Tourney           # noqa
from .user import User                 # noqa


def wipe_database(session):
    """Delete all records in all tables."""

    import transaction
    from zope.sqlalchemy import mark_changed

    with transaction.manager:
        session.execute(MergedPlayer.__table__.delete())
        session.execute(Board.__table__.delete())
        session.execute(Match.__table__.delete())
        session.execute(Competitor.__table__.delete())
        session.execute(Rate.__table__.delete())
        session.execute(Player.__table__.delete())
        session.execute(Tourney.__table__.delete())
        session.execute(Championship.__table__.delete())
        session.execute(Club.__table__.delete())
        session.execute(Rating.__table__.delete())
        session.execute(User.__table__.delete())
        mark_changed(session)


# Activate FOREIGN KEYS

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
