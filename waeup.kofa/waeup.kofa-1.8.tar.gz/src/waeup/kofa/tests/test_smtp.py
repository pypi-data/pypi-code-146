# -*- coding: utf-8 -*-
## $Id: test_smtp.py 16428 2021-03-23 13:15:55Z henrik $
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
# Tests for email-related components
import base64
import logging
import tempfile
import shutil
import unittest
from StringIO import StringIO
from zope.component import getUtility
from zope.component.hooks import setSite
from zope.sendmail.interfaces import IMailDelivery
from waeup.kofa.app import University
from waeup.kofa.interfaces import IMailService
from waeup.kofa.smtp import (
    encode_header_item, encode_address, encode_body, FakeSMTPDelivery,
    send_mail)
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase

#
# SMTP test config
#

# Also run tests that send mail to external servers?
#   If you enable this, please make sure the external smtp hosts and receivers
#   do exist really and are not bothered by being spammed by a test programme.
EXTERNAL_MAIL_TESTS = False

# Maybe existing receiver of externally sent mail. If this mail account
# exists really, it might receive mail from the tests!
EXTERNAL_MAIL_RECEIVER = 'no-reply@waeup.org'

# Names of mail deliveries to use when external mail tests are enabled.
#   See local mail.zcml for names of available deliveries.
EXTERNAL_DIRECT_DELIVERY = 'Direct SMTP on localhost'
EXTERNAL_QUEUED_DELIVERY = 'Queued SMTP on localhost'

#
# end of SMTP test config
#


def external_mail_test(func):
    if not EXTERNAL_MAIL_TESTS:
        myself = __file__
        if myself.endswith('.pyc'):
            myself = myself[:-1]
        print "WARNING: external mail tests are skipped!"
        print "WARNING: edit %s to enable them." % myself
        return
    return func


class HelperTests(unittest.TestCase):

    def test_encode_header_item(self):
        # encoding header items works with strings and unicodes, as
        # long as we pass in utf-8 encoded stuff.
        result1 = encode_header_item(u'Plain Name'.encode('utf-8'))
        result2 = encode_header_item(u'Name with umläut'.encode('utf-8'))
        result3 = encode_header_item(u'Plain Name')
        result4 = encode_header_item(u'Name with umläut')
        result5 = encode_header_item(None)
        self.assertEqual(result1, u'Plain Name')
        self.assertEqual(result2, u'=?iso-8859-1?q?Name_with_uml=E4ut?=')
        self.assertEqual(result3, u'Plain Name')
        self.assertEqual(result4, u'=?iso-8859-1?q?Name_with_uml=E4ut?=')
        self.assertTrue(result5 is None)
        return

    def test_encode_address(self):
        # we can correctly encode address parts
        result1 = encode_address('foo@bar.baz')
        result2 = encode_address(u'foo@bar.baz', 'The Foo')
        result3 = encode_address('foo@bar.baz', u'The Foo')
        result4 = encode_address('foo@bar.baz', u'With Umläut')
        self.assertEqual(result1, 'foo@bar.baz')
        self.assertEqual(result2, 'The Foo <foo@bar.baz>')
        self.assertEqual(result3, 'The Foo <foo@bar.baz>')
        self.assertEqual(result4,
                         '=?iso-8859-1?q?With_Uml=E4ut?= <foo@bar.baz>')
        return

    def test_encode_body(self):
        result1 = encode_body(u'Simple Text')
        self.assertEqual(
            str(result1).split('\n')[1:],
            ['MIME-Version: 1.0',
             'Content-Type: text/plain; charset="us-ascii"',
             'Content-Transfer-Encoding: 7bit',
             '',
             'Simple Text'])
        return

    def test_encode_body_latin1_string(self):
        # utf-8 encoded byte streams are transferred correctly when
        # they contain chars unrepresentable in ascii but available in latin1
        text = u'Simple text with Ümläut'.encode('utf-8')
        result1 = encode_body(text)
        result1 = str(result1).split('\n')[1:]
        self.assertEqual(
            result1,
            ['MIME-Version: 1.0',
             'Content-Type: text/plain; charset="iso-8859-1"',
             'Content-Transfer-Encoding: quoted-printable',
             '',
             'Simple text with =DCml=E4ut'])
        return

    def test_encode_body_latin1_unicode(self):
        # unicode strings are transferred correctly when they contain
        # chars unrepresentable in ascii but available in latin1
        text = u'Simple text with Ümläut'
        result1 = encode_body(text)
        result1 = str(result1).split('\n')[1:]
        self.assertEqual(
            result1,
            ['MIME-Version: 1.0',
             'Content-Type: text/plain; charset="iso-8859-1"',
             'Content-Transfer-Encoding: quoted-printable',
             '',
             'Simple text with =DCml=E4ut'])
        return

    def test_encode_body_utf8_string(self):
        # utf-8 encoded byte streams are transferred correctly when
        # they contain chars unrepresentable in ascii but available in latin1
        text = u"Simple text with ü and capital pi: " + unichr(0x3a0)
        text = text.encode('utf-8')  # turn unicode into byte stream
        result1 = encode_body(text)
        result1 = str(result1).split('\n')[1:]
        self.assertEqual(
            result1,
            ['MIME-Version: 1.0',
             'Content-Type: text/plain; charset="utf-8"',
             'Content-Transfer-Encoding: base64',
             '',
             'U2ltcGxlIHRleHQgd2l0aCDDvCBhbmQgY2FwaXRhbCBwaTogzqA=', ''])
        self.assertEqual(
            base64.b64decode(result1[-2]).decode('utf-8'),
            u"Simple text with ü and capital pi: " + unichr(0x3a0))
        return

    def test_encode_body_utf8_unicode(self):
        # utf-8 encoded byte streams are transferred correctly when
        # they contain chars unrepresentable in latin1
        text = u"Simple text with ü and capital pi: " + unichr(0x3a0)
        result1 = encode_body(text)
        result1 = str(result1).split('\n')[1:]
        self.assertEqual(
            result1,
            ['MIME-Version: 1.0',
             'Content-Type: text/plain; charset="utf-8"',
             'Content-Transfer-Encoding: base64',
             '',
             'U2ltcGxlIHRleHQgd2l0aCDDvCBhbmQgY2FwaXRhbCBwaTogzqA=', ''])
        self.assertEqual(
            base64.b64decode(result1[-2]).decode('utf-8'),
            u"Simple text with ü and capital pi: " + unichr(0x3a0))
        return


class FunctionalMailerTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(FunctionalMailerTests, self).setUp()
        self.setup_logging()
        return

    def tearDown(self):
        super(FunctionalMailerTests, self).tearDown()
        self.teardown_logging()
        return

    def setup_logging(self):
        # setup a log-handler that catches all fake mailer output
        self.stream = StringIO()
        handler = logging.StreamHandler(self.stream)
        logger = logging.getLogger('test.smtp')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return

    def get_fake_smtp_output(self):
        # get output generated by fake mailer
        self.stream.flush()
        self.stream.seek(0)
        return self.stream.read()

    def teardown_logging(self):
        # remove the log handler for fake mailer output
        logger = logging.getLogger('test.smtp')
        handlers = [x for x in logger.handlers]
        for handler in handlers:
            logger.removeHandler(handler)
        return

    def test_get_fake_mailer(self):
        # we can get the fake mailer if we want
        mailer = getUtility(IMailDelivery, name='No email service')
        self.assertTrue(isinstance(mailer, FakeSMTPDelivery))
        return

    def test_get_default_mailer(self):
        # we can get a default mailer if we want
        mailer = getUtility(IMailService)
        self.assertTrue(isinstance(mailer(), FakeSMTPDelivery))
        return

    def test_send_mail(self):
        # we can really send mail.
        mail_id = send_mail(
            u'A sender', u'sender@example.com',
            u'A recipient', u'recpt@example.com',
            u'A subject',
            u'This is a test mail.')
        self.assertEqual(mail_id, 'fake-message-id@example.com')
        self.assertEqual(
            self.get_fake_smtp_output().split('\n'),
            [u'Sending email from no-reply@waeup.org to '
             u'recpt@example.com, sender@example.com:',
             u'Message:',
             u'msg: MIME-Version: 1.0',
             u'msg: Content-Type: text/plain; charset="us-ascii"',
             u'msg: Content-Transfer-Encoding: 7bit',
             u'msg: From: A sender <no-reply@waeup.org>',
             u'msg: To: A recipient <recpt@example.com>',
             # u'msg: Cc: A sender <sender@example.com>',
             u'msg: Reply-To: A sender <sender@example.com>',
             u'msg: Subject: A subject',
             u'msg: ',
             u'msg: This is a test mail.',
             u'']
            )
        return

    def test_send_mail_with_cc(self):
        # with cc=True the message will be CCed to the from address
        mail_id = send_mail(
            u'A sender', u'sender@example.com',
            u'A recipient', u'recpt@example.com',
            u'A subject',
            u'This is a test mail.',None,
            (('recpt1@example.com', 'A cc recipient'),),
            (('recpt2@example.com', 'A bcc recipient'),
             ('recpt3@example.com', 'A 2nd bcc recipient')),
            )
        self.assertEqual(mail_id, 'fake-message-id@example.com')
        self.assertEqual(
            self.get_fake_smtp_output().split('\n'),
            [u'Sending email from no-reply@waeup.org to '
             u'recpt@example.com, recpt1@example.com, recpt2@example.com, '
             u'recpt3@example.com, sender@example.com:',
             u'Message:',
             u'msg: MIME-Version: 1.0',
             u'msg: Content-Type: text/plain; charset="us-ascii"',
             u'msg: Content-Transfer-Encoding: 7bit',
             u'msg: From: A sender <no-reply@waeup.org>',
             u'msg: To: A recipient <recpt@example.com>',
             u'msg: Cc: A cc recipient <recpt1@example.com>',
             u'msg: Bcc: A bcc recipient <recpt2@example.com>',
             u'msg: Bcc: A 2nd bcc recipient <recpt3@example.com>',
             u'msg: Reply-To: A sender <sender@example.com>',
             u'msg: Subject: A subject',
             u'msg: ',
             u'msg: This is a test mail.',
             u'']


            )
        return

    def test_send_mail_utf8_strings(self):
        # we can send mail with utf-8 encoded strings as input
        mail_id = send_mail(
            u'A sender', u'sender@example.com',
            u'A recipient', u'recpt@example.com',
            u'A subject',
            u'This is a test mail with ümläut.'.encode('utf-8'))
        self.assertEqual(mail_id, 'fake-message-id@example.com')
        self.assertEqual(
            self.get_fake_smtp_output().split('\n'),
            [u'Sending email from no-reply@waeup.org '
             u'to recpt@example.com, sender@example.com:',
             u'Message:', u'msg: MIME-Version: 1.0',
             u'msg: Content-Type: text/plain; charset="iso-8859-1"',
             u'msg: Content-Transfer-Encoding: quoted-printable',
             u'msg: From: A sender <no-reply@waeup.org>',
             u'msg: To: A recipient <recpt@example.com>',
             # u'msg: Cc: A sender <sender@example.com>',
             u'msg: Reply-To: A sender <sender@example.com>',
             u'msg: Subject: A subject',
             u'msg: ',
             u'msg: This is a test mail with =FCml=E4ut.',
             u'']
            )
        return

    def test_send_mail_utf8_unicode(self):
        # we can send mail with utf-8 encoded unicode as input
        mail_id = send_mail(
            u'A sender', u'sender@example.com',
            u'A recipient', u'recpt@example.com',
            u'A subject',
            u'This is a test mail with ümläut.')
        self.assertEqual(mail_id, 'fake-message-id@example.com')
        self.assertEqual(
            self.get_fake_smtp_output().split('\n'),
            [u'Sending email from no-reply@waeup.org '
             u'to recpt@example.com, sender@example.com:',
             u'Message:', u'msg: MIME-Version: 1.0',
             u'msg: Content-Type: text/plain; charset="iso-8859-1"',
             u'msg: Content-Transfer-Encoding: quoted-printable',
             u'msg: From: A sender <no-reply@waeup.org>',
             u'msg: To: A recipient <recpt@example.com>',
             # u'msg: Cc: A sender <sender@example.com>',
             u'msg: Reply-To: A sender <sender@example.com>',
             u'msg: Subject: A subject',
             u'msg: ',
             u'msg: This is a test mail with =FCml=E4ut.',
             u'']
            )
        return


class ExternalMailerTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(ExternalMailerTests, self).setUp()
        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        return

    def tearDown(self):
        super(ExternalMailerTests, self).tearDown()
        shutil.rmtree(self.dc_root)
        return

    def test_config_default_mailer(self):
        # The default mailer set in config is 'no mailer'.
        self.assertEqual(
            getattr(self.app.get('configuration', None), 'smtp_mailer'),
            u'No email service')
        return

    @external_mail_test
    def test_send_direct_mail(self):
        # send mail using direct mail delivery
        self.app['configuration'].smtp_mailer = EXTERNAL_DIRECT_DELIVERY
        setSite(self.app)
        result = send_mail(
            'test program', 'no-reply@waeup.org',
            'test mail receiver', EXTERNAL_MAIL_RECEIVER,
            'Test Mail from WAeUP Kofa',
            'Hi from test mailer!\n\nRegards,\nTest Programme\n'
            )
        import transaction
        transaction.commit()  # The mail is really sent when transactions is
                              # committed
        self.assertTrue('@' in result)
        return

    @external_mail_test
    def test_send_direct_mails(self):
        # send several mails using direct mail delivery
        self.app['configuration'].smtp_mailer = EXTERNAL_DIRECT_DELIVERY
        setSite(self.app)
        result = send_mail(
            'test program', 'no-reply@waeup.org',
            'test mail receiver',
            '%s, %s' % (EXTERNAL_MAIL_RECEIVER, EXTERNAL_MAIL_RECEIVER),
            'Test Mail from WAeUP Kofa',
            'Hi from test mailer!\n\nRegards,\nTest Programme\n'
            )
        import transaction
        transaction.commit()  # The mail is really sent when transactions is
                              # committed
        self.assertTrue('@' in result)
        return

    @external_mail_test
    def test_send_queued_mail(self):
        # send mail using queued mail delivery
        self.app['configuration'].smtp_mailer = EXTERNAL_QUEUED_DELIVERY
        setSite(self.app)
        result = send_mail(
            'test program', 'no-reply@waeup.org',
            'test mail receiver', EXTERNAL_MAIL_RECEIVER,
            'Test Mail from WAeUP Kofa',
            'Hi from test mailer!\n\nRegards,\nTest Programme\n'
            )
        import transaction
        transaction.commit()  # The mail is really sent when transactions is
                              # committed
        self.assertTrue('@' in result)
        return
