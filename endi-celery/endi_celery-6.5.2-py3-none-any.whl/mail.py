# -*- coding: utf-8 -*-
import logging
from pyramid_mailer.message import (
    Attachment,
)

from endi_base.exception import (
    MailAlreadySent,
    UndeliveredMail,
)
from endi_base.mail import send_mail
from endi_celery.models import (
    store_sent_mail,
    check_if_mail_sent,
)


logger = logging.getLogger(__name__)


SALARYSHEET_MAIL_MESSAGE = """Bonjour,
Vous trouverez ci-joint votre bulletin de salaire.
"""

SALARYSHEET_MAIL_SUBJECT = "Votre bulletin de salaire"


def send_salary_sheet(
    request,
    email,
    company_id,
    filename,
    filepath,
    force=False,
    message=None,
    subject=None,
):
    """
    Send a salarysheet to the given company's e-mail

    :param obj request: A pyramid request object
    :param str company_mail: The mail to send it to
    :param int company_id: The id of the associated company
    :param str filepath: The path to the filename
    :param bool force: Whether to force sending this file again
    :param str message: The mail message
    :param str subject: The mail subject
    :returns: A MailHistory instance
    :TypeError UndeliveredMail: When the company has no mail
    :TypeError MailAlreadySent: if the file has
        already been sent and no force option was passed
    """
    filebuf = open(filepath, "rb")
    filedatas = filebuf.read()

    if not force and check_if_mail_sent(filedatas, company_id):
        logger.warn("Mail already sent : mail already sent")
        raise MailAlreadySent("Mail already sent")

    filebuf.seek(0)

    if email is None:
        logger.warn(
            "Undelivered email : no mail provided for company {0}".format(company_id)
        )
        raise UndeliveredMail("no mail provided for company {0}".format(company_id))
    else:
        logger.info("Sending the file %s" % filepath)
        logger.info("Sending it to %s" % email)
        attachment = Attachment(filename, "application/pdf", filebuf)

        subject = subject or SALARYSHEET_MAIL_SUBJECT
        message = message or SALARYSHEET_MAIL_MESSAGE

        send_mail(
            request,
            email,
            message,
            subject,
            attachment,
        )
        return store_sent_mail(filepath, filedatas, company_id)


INTERNAL_ORDER_CUSTOMER_MAIL_OBJECT = """Nouvelle commande founisseur générée \
dans votre espace"""

INTERNAL_ORDER_CUSTOMER_MAIL_TMPL = """
Bonjour {customer},

L'enseigne {supplier} vous a transmis un devis 'interne'.

Une commande fournisseur contenant le devis est accessible dans votre espace
dans la section "Commande fournisseur".
"""

INTERNAL_ORDER_SUPPLIER_MAIL_OBJECT = "Votre devis a été transmis à votre \
client"
INTERNAL_ORDER_SUPPLIER_MAIL_TMPL = """
Bonjour {supplier},

Votre devis 'interne' a été transmis à l'enseigne {customer}.

Une commande fournisseur contenant le devis est accessible dans son espace dans
la section "Commande fournisseur".
"""


def send_customer_new_order_mail(request, order):
    """
    Send an email to an internal customer
    """
    customer = order.company
    supplier = order.supplier
    message = INTERNAL_ORDER_CUSTOMER_MAIL_TMPL.format(
        customer=customer.name, supplier=supplier.label
    )
    if customer.email:
        recipients = [customer.email]
        send_mail(request, recipients, message, INTERNAL_ORDER_CUSTOMER_MAIL_OBJECT)
    else:
        logger.error("Company {} has no email set".format(customer.id))


def send_supplier_new_order_mail(request, order):
    """
    Send an email to an internal supplier
    """
    customer = order.company
    supplier = order.supplier
    message = INTERNAL_ORDER_SUPPLIER_MAIL_TMPL.format(
        customer=customer.name, supplier=supplier.label
    )
    if supplier:
        recipients = [supplier.email]
        send_mail(request, recipients, message, INTERNAL_ORDER_SUPPLIER_MAIL_OBJECT)
    else:
        logger.error("Company {} has no email set".format(supplier.id))


INTERNAL_INVOICE_CUSTOMER_MAIL_OBJECT = """Nouvelle facture founisseur \
générée dans votre espace"""

INTERNAL_INVOICE_CUSTOMER_MAIL_TMPL = """
Bonjour {customer},

L'enseigne {supplier} vous a transmis une facture 'interne'.

Une facture fournisseur contenant le devis est accessible dans votre espace
dans la section "Facture fournisseur".
"""

INTERNAL_INVOICE_SUPPLIER_MAIL_OBJECT = "Votre facture a été transmis à votre \
client"
INTERNAL_INVOICE_SUPPLIER_MAIL_TMPL = """
Bonjour {supplier},

Votre facture 'interne' a été transmis à l'enseigne {customer}.

Une facture fournisseur contenant la facture est accessible dans son espace
dans la section "Facture fournisseur".
"""


def send_customer_new_invoice_mail(request, supplier_invoice):
    """
    Send an email to an internal customer
    """
    customer = supplier_invoice.company
    supplier = supplier_invoice.supplier
    message = INTERNAL_INVOICE_CUSTOMER_MAIL_TMPL.format(
        customer=customer.name, supplier=supplier.label
    )
    if customer.email:
        recipients = [customer.email]
        send_mail(request, recipients, message, INTERNAL_INVOICE_CUSTOMER_MAIL_OBJECT)
    else:
        logger.error("Company {} has no email set".format(customer.id))


def send_supplier_new_invoice_mail(request, supplier_invoice):
    """
    Send an email to an internal supplier
    """
    customer = supplier_invoice.company
    supplier = supplier_invoice.supplier
    message = INTERNAL_INVOICE_SUPPLIER_MAIL_TMPL.format(
        customer=customer.name, supplier=supplier.label
    )
    if supplier:
        recipients = [supplier.email]
        send_mail(request, recipients, message, INTERNAL_INVOICE_SUPPLIER_MAIL_OBJECT)
    else:
        logger.error("Company {} has no email set".format(supplier.id))
