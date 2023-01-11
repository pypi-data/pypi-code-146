# coding=utf-8
"""
run the test from the sr/invesytoolbox directory:
python ../tests/test_data.py
"""

import sys
import unittest

from itb_email_phone import create_email_message, process_phonenumber
import email

sys.path.append(".")

phonenumbers = {
    '(699) 123 456 789': {
        'international': '+43 699 123456789',
        'national': '0699 123456789',
        'E164': '+43699123456789'
    },
    '01 456 789': {
        'international': '+43 1 456789',
        'national': '01 456789',
        'E164': '+431456789'
    },
    '+12124567890': {
        'international': '+1 212-456-7890',
        'national': '(212) 456-7890',
        'E164': '+12124567890'
    },
    '+32 460224965': {
        'international': '+32 460 22 49 65',
        'national': '0460 22 49 65',
        'E164': '+32460224965'
    }
}

email_data = {
    'mail_from': 'test@invesy.work',
    'subject': 'Testing email message',
    'text': 'Ein Text mit Umlauten öäüß',
    'mail_to': 'georg.tester@test.at',
    'html': '<html><body><p>Ein Text mit Umlauten öäüß</p></body></html>',
}

email_msg_boundary = '===============0423875057181292250=='
email_msg_str = f'Content-Type: multipart/alternative; boundary="{email_msg_boundary}"\nMIME-Version: 1.0\nSubject: Testing email message\nFrom: test@invesy.work\nTo: georg.tester@test.at\n\n--===============0423875057181292250==\nContent-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\n\nRWluIFRleHQgbWl0IFVtbGF1dGVuIMO2w6TDvMOf\n\n--===============0423875057181292250==\nContent-Type: text/html; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\n\nPGh0bWw+PGJvZHk+PHA+RWluIFRleHQgbWl0IFVtbGF1dGVuIMO2w6TDvMOfPC9wPjwvYm9keT48\nL2h0bWw+\n\n--===============0423875057181292250==--\n'


class TestEmailPhone(unittest.TestCase):
    def test_create_email_message(self):
        email_msg = create_email_message(**email_data)
        if not isinstance(email_msg, email.mime.multipart.MIMEMultipart):
            raise AssertionError('Email message is not email.mime.multipart.MIMEMultipart')
        email_msg.set_boundary(email_msg_boundary)
        self.assertEqual(
            email_msg_str,
            str(email_msg)
        )

    def test_process_phonenumber(self):
        for pn, data in phonenumbers.items():
            for fmt in (
                'international',
                'national',
                'E164'
            ):
                self.assertEqual(
                    data[fmt],
                    process_phonenumber(
                        pn,
                        numberfmt=fmt,
                        country='AT'
                    )
                )


if __name__ == '__main__':
    unittest.main()

    # print('finished format tests.')
