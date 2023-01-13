from pyqalx.core.adapters.adapter import QalxAdapter
from pyqalx.core.entities import Notification


class QalxNotification(QalxAdapter):
    """
    Provides an interface for accessing the API for
    :class:`~pyqalx.core.entities.notification.Notification` entities
    """

    _entity_class = Notification

    def add(self, subject, message, to, cc=None, bcc=None, **kwargs):
        """
        Posts a notification request to the API, to send an email with the
        provided subject, message and recipient list. Optionally, lists for CC
        and BCC recipients can be provided

        :param subject: The subject of the message
        :type subject: str
        :param message: The message to send
        :type message: str
        :param to: A list with the addresses of the recipients of the message
        :type to: list
        :param cc:  An optional list with the addresses of th recipients of a
                    carbon copy(CC) of the message
        :type cc: list
        :param bcc:  An optional list with the addresses of th recipients of a
                    blind carbon copy(BCC) of the message
        :type bcc: list
        """
        if cc is None:
            cc = []
        if bcc is None:
            bcc = []
        return super(QalxNotification, self).add(
            subject=subject, message=message, to=to, cc=cc, bcc=bcc, **kwargs
        )
