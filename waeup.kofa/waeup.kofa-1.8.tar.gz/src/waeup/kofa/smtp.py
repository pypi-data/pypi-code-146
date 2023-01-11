## $Id: smtp.py 16300 2020-11-04 22:25:27Z henrik $
##
## Copyright (C) 2014 Uli Fouquet & Henrik Bettermann
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
"""
Email (SMTP) services for Kofa.

Note About Encodings
--------------------

All functions in this module expect any raw strings passed in to be
encoded 'utf-8' (if you pass in unicode objects instead, this is not a
problem).

This is because we cannot easily tell from a raw string (it is in fact
only a byte stream) what encoding it has. In latin-1 and utf-8, for
instance, there exist some chars (byte values) that have different
meanings in both encodings. If we see such a char in a byte stream:
what is it meant to represent? The respective character from latin1 or
the one from utf-8?

We therefore interpret all internally used raw strings to be encoded as
utf-8.

The functions in here nevertheless try hard to produce output (mail
parts, headers, etc.) encoded in the least complex manner. For
instance if you pass in some address or mail body that is
representable (correctly) as ASCII or latin-1, we will turn the text
into that encoding (given, you passed it in as utf-8) to stay as
compatible as possible with old mailers that do not understand utf-8.

"""
import grok
import logging
from email.Header import Header
from email.Utils import formataddr
from email.mime.text import MIMEText
from zope.component import getUtility
from zope.sendmail.interfaces import IMailDelivery
from waeup.kofa.interfaces import IMailService


#: The hardcoded from address. Must not by yahoo.com.
FROM_ADDRESS = 'no-reply@waeup.org'


class DefaultMailService(grok.GlobalUtility):
    """Returns a :class:`zope.sendmail.IMailDelivery`.

    Searches a site from current request (if applicable) and returns
    the mail delivery set for this site or a fake mailer that does not
    really send mail (for testing, evaluating, etc.).
    """
    grok.implements(IMailService)

    def __call__(self):
        name = 'No email service'
        site = grok.getSite()
        if site is not None:
            config = site['configuration']
            name = getattr(config, 'smtp_mailer', name)
        return getUtility(IMailDelivery, name=name)


class FakeSMTPDelivery(grok.GlobalUtility):
    """A fake mail delivery for testing etc.

    Instead of sending real mails, this mailer only logs received
    messages to the ``test.smtp`` logger.
    """
    grok.implements(IMailDelivery)
    grok.name('No email service')

    def send(self, fromaddr, toaddrs, message):
        logger = logging.getLogger('test.smtp')
        rcpts = ', '.join([x.decode('utf-8') for x in toaddrs])
        logger.info(
            u"Sending email from %s to %s:" % (
                fromaddr.decode('utf-8'), rcpts))
        logger.info(u"Message:")
        for line in message.split('\n'):
            logger.info(u"msg: " + line.decode('utf-8'))
        return 'fake-message-id@example.com'

CHARSETS = ('US-ASCII', 'ISO-8859-1', 'UTF-8')


def encode_header_item(item):
    """Turns `item`, a string into an SMTP header part string.

    Encodings are checked carefully (we try to encode as ASCII,
    Latin-1 and UTF-8 in that order).

    If `item` is not a basestring, `None` is returned.
    """
    if not isinstance(item, basestring):
        return None
    if not isinstance(item, unicode):
        item = unicode(item, 'utf-8')
    return str(Header(item, 'iso-8859-1'))  # try ascii, then latin1, utf-8


def encode_address(addr, name=u''):
    """Turn email address parts into a single valid email string.

    The given email address and the name are turned into a single
    (byte stream) string, suitable for use with ``To:`` or ``From:``
    headers in emails.

    Any encodings to a mailer-readable format are performed.

    Preferred input format is unicode, although also raw strings (byte
    streams) work as long as they are decodable from UTF-8.

    That means: if you pass in non-unicode string, take care to
    deliver utf-8 encoded strings (or plain ASCII).

    Returns a single (raw) string like "My Name <my@sample.com>".
    """
    addr = encode_header_item(addr)
    name = encode_header_item(name)
    return formataddr((name, addr))


def encode_body(text):
    """Build MIME message part from text.

    You can pass unicode objects or simple strings as text.

    If the input is a simple string, this string is expected
    to be encoded 'utf-8'!

    Returns a MIMEText object.
    """
    if not isinstance(text, unicode):
        text = unicode(text, 'utf-8')
    charset = CHARSETS[-1]  # fallback
    for charset in CHARSETS:
        try:
            text = text.encode(charset)
        except UnicodeError:
            pass  # try next encoding
        else:
            break
    return MIMEText(text, 'plain', charset)


def send_mail(from_name, from_addr, rcpt_name, rcpt_addrs,
              subject, body, config=None, cc=None, bcc=None):
    """Send mail.

    Use `IMailService` to send a mail with the parameters
    delivered.

    Please note: the `from_addr` given will be used for the reply-to
    (and cc) field only. It will _not_ be used for the `from` field,
    as yahoo does not allow non-yahoo servers to deliver mail with
    ``@yahoo.com`` in the from-field.

    The from-address set here will be: `FROM_ADDRESS` as set above.

    XXX: The hard-coded from-address should be changable or be
         determined smarter by looking up a FQDN or similar.

    """
    # format message
    rcpt_addrs = rcpt_addrs.replace(' ', '').split(',')
    body_to = ''
    from_addr = from_addr.split(',')[0]
    for email in rcpt_addrs:
        body_to += '%s, ' % encode_address(email, rcpt_name)
    body = encode_body(body)
    sender_addr = encode_address(FROM_ADDRESS, from_name)
    reply_addr = encode_address(from_addr, from_name)
    body["From"] = sender_addr
    body["To"] = body_to.strip(', ')
    if cc:
        for item in cc:
            body["Cc"] = '%s' % encode_address(item[0], item[1])
            rcpt_addrs.append(item[0])
    if bcc:
        for item in bcc:
            body["Bcc"] = '%s' % encode_address(item[0], item[1])
            rcpt_addrs.append(item[0])
    body["Reply-To"] = reply_addr
    body["Subject"] = encode_header_item(subject)

    mailer = getUtility(IMailService)
    try:
        email_admin = grok.getSite()['configuration'].email_admin
        if from_addr != email_admin:
            rcpt_addrs += [from_addr]
    except TypeError:
        # In tests we might not have a site object
        rcpt_addrs += [from_addr]
        pass
    result = mailer().send(FROM_ADDRESS, rcpt_addrs, body.as_string())
    return result
