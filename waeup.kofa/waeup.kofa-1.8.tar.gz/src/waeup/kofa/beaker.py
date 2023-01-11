"""Configure dolmen.beaker.

One main advantage of using dolmen.beaker is that session data for a
certain user can be stored almost automatically in a cookie, thus
reducing the number of needed ZODB operations.

Security Advisory
-----------------

To prevent users from playing around with their session data, these
data is encrypted by some keys stored in a dict registered as a global
utility.

These keys are set each time the Zope instance starts. If they change,
all existing cookies will become unreadable and therefore the stored
sessions will be lost. Already logged-in users will have to login
again and all other session based operations might have to be
restarted.

Changing the keys might therefore have sideeffects.

On the other hand static keys stored in SVN might become known to
users and enable them to manipulate their session data.

For better security the keys (or one of the keys) could therefore be
gathered from 'outside' (a file in filesystem, some environment var,
or whatever).
"""
import grok
from zope.app.appsetup.interfaces import IDatabaseOpenedWithRootEvent
from zope.component import getUtility

#: Our configuration for dolmen.beaker sessions.
#:
#: See http://gitweb.dolmen-project.org/dolmen.beaker.git?a=blob;f=src/dolmen/beaker/utilities.py
#:
#: for default configuration.
BEAKER_CONFIG = dict(
    data_dir=None,
    invalidate_corrupt=True,
    key='waeup.kofa.session.id',
    log_file=None,
    secret="KofaRocks",
    timeout=3600,
    type="cookie",
    validate_key="thisMightBeChanged",
    )

@grok.subscribe(IDatabaseOpenedWithRootEvent)
def set_beaker_conf(event):
    # Set beaker conf once when ZODB was opened
    try:
        from dolmen.beaker.interfaces import ISessionConfig
    except ImportError:
        # we seem to work without dolmen.beaker
        return

    config = getUtility(ISessionConfig)
    config.update(BEAKER_CONFIG)
    return
