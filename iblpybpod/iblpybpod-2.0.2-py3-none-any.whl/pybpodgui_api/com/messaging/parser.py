# !/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from pybpodapi.com.messaging.error import ErrorMessage
from pybpodapi.com.messaging.debug import DebugMessage
from pybpodapi.com.messaging.stderr import StderrMessage
from pybpodapi.com.messaging.stdout import StdoutMessage
from pybpodapi.com.messaging.warning import WarningMessage
from pybpodapi.com.messaging.end_trial import EndTrial
from pybpodapi.com.messaging.trial import Trial
from pybpodapi.com.messaging.event_occurrence import EventOccurrence
from pybpodapi.com.messaging.state_occurrence import StateOccurrence
from pybpodapi.com.messaging.softcode_occurrence import SoftcodeOccurrence
from pybpodapi.com.messaging.event_resume import EventResume
from pybpodapi.com.messaging.untagged_message import UntaggedMessage
from pybpodapi.com.messaging.session_info import SessionInfo


logger = logging.getLogger(__name__)


class BpodMessageParser(object):

    MESSAGES_TYPES_CLASSES = [
        Trial,
        EndTrial,
        ErrorMessage,
        DebugMessage,
        StderrMessage,
        StdoutMessage,
        WarningMessage,
        SoftcodeOccurrence,
        StateOccurrence,
        EventOccurrence,
        EventResume,
        SessionInfo,
        UntaggedMessage
    ]

    COLUMN_SEPARATOR = ';'

    @classmethod
    def fromlist(cls, row):
        """
        Parses messages saved on session history file

        .. seealso::

            :py:meth:`pybpodgui_plugin.api.models.session.session_io.SessionIO.load_contents`


        :param str txtline: file line entry
        :returns: list of history messages
        :rtype: list(BaseMessage)
        """
        if row is None or len(row) == 0:
            return ErrorMessage('Parse error: line is empty')

        msg = None
        try:
            msgtype = row[0]

            for msgtype_class in cls.MESSAGES_TYPES_CLASSES:
                if msgtype_class.check_type(msgtype):
                    msg = msgtype_class.fromlist(row)
                    break
        except Exception:
            logger.warning("Could not parse bpod message: {0}".format(str(row)), exc_info=True)
            return ErrorMessage(row)  # default case

        return msg
