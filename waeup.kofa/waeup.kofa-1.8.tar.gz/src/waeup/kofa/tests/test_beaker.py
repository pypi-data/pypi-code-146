from zope.component.hooks import setSite
from zope.publisher.browser import TestRequest
from zope.session.interfaces import ISession
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase

class BeakerTests(FunctionalTestCase):
    # Beaker-related tests.

    layer = FunctionalLayer

    def test_beaker_session(self):
        # Make sure we get a beaker session when asking for ISession.
        try:
            import dolmen.beaker
        except ImportError:
            # no beaker installed, no test
            return
        setSite(self.getRootFolder()) # needed to start transaction
        request = TestRequest()
        session = ISession(request)
        self.assertTrue(session.__module__.startswith('dolmen.beaker'))
        return
