from __future__ import annotations

from tcsoa.gen.Internal.DebugMonitor._2014_06.JournalBasedTesting import AuxiliaryInfo
from tcsoa.base import TcService
from tcsoa.gen.Internal.DebugMonitor._2015_10.JournalBasedTesting import TerminateJBTResponse


class JournalBasedTestingService(TcService):

    @classmethod
    def terminateJBT(cls, input: AuxiliaryInfo) -> TerminateJBTResponse:
        """
        terminateJBT marks the end of a journal based test and takes care of all the work that needs to be done when
        the test terminates, such as restoring the database to the initial state. It is called at the end of a test
        recording and test replaying. This operation is used internally by Journal Based Testing, which allows a user
        to record a test in Teamcenter and later on replay the test in a different session.
        
        Use cases:
        Case 1: Restore the database to its initial state
        
        Journal Based Testing is sensitive to database state. It requires the database state at the time of replaying a
        test be identical to the state when the test is recorded. To achieve this requirement, we utilize the
        Teamcenter mark point mechanism. During the test recording, the initializeJBT (an existing operation in the
        same service) is called at the beginning of the session to set the mark point. After the test recording is
        done, terminateJBT will be called to rollback the database to the mark point set by initializeJBT. This will
        ensure that whatever changes made during the test will be undone, and the next test recording will start from
        the same initial DB state.
        
        The database for Journal Based Testing is created using the Teamcenter tcdbinstaller utility. The utility has
        an option to export the DB to a dump file and later on, if the database is corrupted, the DB can be recovered
        from the dump. This dump file captures the initial DB state and so we can use it to recover the DB to the same
        initial state in cases where the client loses server connection or the terminateJBT operation fails to rollback
        the database for whatever reasons. Currently the command to restore the DB from dump is wrapped in a batch
        file, which is executed manually.
        """
        return cls.execute_soa_method(
            method_name='terminateJBT',
            library='Internal-DebugMonitor',
            service_date='2015_10',
            service_name='JournalBasedTesting',
            params={'input': input},
            response_cls=TerminateJBTResponse,
        )
