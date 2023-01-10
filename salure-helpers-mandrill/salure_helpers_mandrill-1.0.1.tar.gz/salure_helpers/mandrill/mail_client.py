import os
import mandrill
import codecs
import base64
from salure_helpers.salureconnect import SalureConnect
from typing import Union, List


class MailClient(SalureConnect):
    def __init__(self, label: Union[str, List] = None, debug=False):
        # This is built in so you can use this class as a query generator for the SalureConnect Agent
        super().__init__()
        self.debug = debug
        if label is not None:
            credentials = self.get_system_credential(system='mandrill', label=label)
            self.api_token = credentials['token']
            self.email_from = 'support@salureconnect.com' if credentials['email_from'] is None else credentials['email_from']
            self.name_from = 'SalureConnect' if credentials['name_from'] is None else credentials['name_from']
            if self.debug:
                print('Retrieved credentials from SalureConnect')
        elif os.getenv("MANDRILL_TOKEN") is not None:
            self.api_token = os.getenv("MANDRILL_TOKEN")
            self.email_from = 'connect@salure.nl' if os.getenv("MANDRILL_EMAIL_FROM") is None else os.getenv("MANDRILL_EMAIL_FROM")
            self.name_from = 'SalureConnect' if os.getenv("MANDRILL_NAME_FROM") is None else os.getenv("MANDRILL_NAME_FROM")
            if self.debug:
                print('Retrieved credentials from environment variables')
        else:
            raise ValueError('No credentials found for Mandrill. Either pass a SalureConnect credential label or set the environment variables MANDRILL_TOKEN, MANDRILL_EMAIL_FROM and MANDRILL_NAME_FROM')

    def send_mail(self, email_to: list, subject: str, language='NL', content=None, attachment=None):
        """
        Send a mail with the salureconnect layout and using mandrill
        :param email_to: a list with name and mailadress to who the mail must be send
        :param subject: The subject of the email
        :param language: Determines the salutation and greeting text. For example Beste or Dear
        :param content: The message of the email
        :param attachment: The attachment of an email loaded as binary file (NOT the location of the file)
        :return: If the sending of the mail is successful or not
        """

        mandrill_client = mandrill.Mandrill(self.api_token)
        # Load the html template for e-mails
        html_file_location = '{}/templates/mail_salureconnect.html'.format(os.path.dirname(os.path.abspath(__file__)))
        html_file = codecs.open(html_file_location, 'r')
        html = html_file.read()
        if language == 'NL':
            salutation = 'Beste '
            greeting_text = 'Met vriendelijke groet'
        else:
            salutation = 'Dear '
            greeting_text = 'Kind regards'

        # Set attachment. Do not in loop because of errors
        if attachment is not None:
            opened_attachment = attachment.read()
            encoded_attachment = base64.b64encode(opened_attachment).decode('utf-8')
        else:
            encoded_attachment = None

        # Pick the configurations from the config file and create the mail
        response = []
        for email_object in email_to:
            if self.debug:
                print(f"Sending mail to: {email_object['email']}")
            new_html = html.replace('{', '{{'). \
                replace('}', '}}'). \
                replace('{{subject}}', '{subject}'). \
                replace('{{title}}', '{title}'). \
                replace('{{salutation}}', '{salutation}'). \
                replace('{{name}}', '{name}'). \
                replace('{{content}}', '{content}'). \
                replace('{{greeting}}', '{greeting}').format(subject=subject, title=subject, salutation=salutation, name=email_object['name'], content=content, greeting=greeting_text)
            mail = {
                'from_email': self.email_from,
                'from_name': self.name_from,
                'subject': subject,
                'html': new_html,
                'to': [{'email': email_object['mail'],
                        'name': email_object['name'],
                        'type': 'to'}]
            }
            if encoded_attachment is not None:
                mail.update({
                    'attachments': [{'content': encoded_attachment,
                                     'name': attachment.name.split('/')[-1]
                                     }]
                })

            # Send the mail and return the result per mail address
            result = {
                'Send to': email_object,
                'result': mandrill_client.messages.send(mail, False, 'Main Pool')
            }
            response.append(result)

        return response
