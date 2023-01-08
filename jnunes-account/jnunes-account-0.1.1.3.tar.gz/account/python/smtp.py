from django.core.mail import send_mail, EmailMultiAlternatives
from core.settings import EMAIL_HOST_USER


def send_email(subject, message, to):
    recipient_list = get_recipient_list(to)
    if message is not None:
        send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=recipient_list,
                  fail_silently=False)


def send_html_email(subject, text_content, to, html_content):
    email = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=EMAIL_HOST_USER, to=get_recipient_list(to))
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=False)


def get_recipient_list(to):
    return to if isinstance(to, (tuple, list)) else [to]
