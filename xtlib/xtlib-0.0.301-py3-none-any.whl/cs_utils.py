# cs_utils.py: flat functions for communication services (sending email and SMS texts)
from xtlib import utils
from xtlib import errors

def send_email_via_outlook(to_list, cc_list, subject, body):
    '''
    Pro's:
        - quick to send
        - recognized sender
        - shows up an internal (not flagged EXTERNAL)
        
    Con's:
        - requires user to have Outlook installed
        - user cannot launch XT from admin command window
    '''
    import win32com.client as win32

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)

    mail.To = ";".join(to_list)
    mail.Cc = ";".join(cc_list)
    mail.Subject = subject
    mail.Body = body
    mail.HTMLBody = body

    # To attach a file to the email (optional):
    # attachment  = "Path to the attachment"
    # mail.Attachments.Add(attachment)

    mail.Send()

def send_sms(sms_cs, sms_from, to, plain_body):
    '''
    Sometimes deliver takes > 5 minutes.
    '''
    from azure.communication.sms import SmsClient

    sms_client = SmsClient.from_connection_string(sms_cs)
    to = to.replace("-", "")

    sms_responses = sms_client.send(from_ = sms_from, to=to, message=plain_body, enable_delivery_report=True,
        tag="custom-tag")      # tag="custom-tag") # optional property    

    sr = sms_responses[0]
    #print("from: {}, to: {}, msg: {}, successful: {}".format(to, sms_from, plain_body, sr.successful))

    if not sr.successful:
        errors.general_error("Unable to send SMS message: {}".format(sr))

    return sms_responses

def send_to_contacts_from_config(config, to_list, cc_list, subject, rich_body, sms_msg=None):
    email_cs = config.get("external-services", "xt-email", "connection-string")
    email_from = config.get("external-services", "xt-email", "from")
    sms_cs = config.get("external-services", "xt-sms", "connection-string")
    sms_from = config.get("external-services", "xt-sms", "from")

    send_to_contacts(email_cs, email_from, sms_cs, sms_from, to_list, cc_list, subject, rich_body, sms_msg)

def send_to_contacts(email_cs, email_from, sms_cs, sms_from, to_list, cc_list, subject, rich_body, sms_msg=None):
    '''
    route message to EMAIL and SMS, as per contact format
    '''
    to_em = []
    cc_em = []
    to_sms = []

    for contact in to_list:
        if "@" in contact:
            to_em.append(contact)
        else:
            if not contact.startswith("+"):
                contact = "+" + contact
            to_sms.append(contact)

    if cc_list:
        for contact in cc_list:
            if "@" in contact:
                cc_em.append(contact)
            else:
                to_sms.append(contact)

    if to_em or cc_em:
        send_email(email_cs, email_from, to_em, cc_em, subject, rich_body)

    if to_sms:

        if not sms_msg:
            rich = rich_body.replace("<br>", "\n")

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(rich, features="html.parser")
            plain_text = soup.get_text()
            sms_msg = subject + "\n" + plain_text

        # remove duplicates in to_sms
        to_sms = list(set(to_sms))
        for sms_user in to_sms:
            send_sms(sms_cs, sms_from, sms_user, sms_msg)
    
def send_email(email_cs, email_from, to_list, cc_list, subject, body):
    '''
    Pro's:
        - no special client requirements
    Con's:
        - sender domain is ugly 
        - flagged as EXTERNAL by Outlook 
    '''    
    from azure.communication.email import EmailClient, EmailContent, EmailAddress, EmailMessage, EmailRecipients

    client = EmailClient.from_connection_string(email_cs)
    content = EmailContent(subject=subject, plain_text=body, html=body)

    to_addr_list = [EmailAddress(email=to) for to in to_list]
    cc_addr_list = [EmailAddress(email=cc) for cc in cc_list] if cc_list else []

    message = EmailMessage(sender=email_from, content=content,
        recipients=EmailRecipients(to=to_addr_list, cc=cc_addr_list))

    response = client.send(message)
    return response

def get_approvers(team_dict):

    approver_dict = {key: md for key, md in team_dict.items() if utils.safe_value(md, "approver")}
    approver_contacts = [md["contact"] for md in approver_dict.values()]

    approver_contacts = [item for sublist in approver_contacts for item in sublist]
    approver_usernames = list(approver_dict)

    return approver_contacts, approver_usernames

def get_contacts(team_dict, name):
    name_contacts = team_dict[name]["contact"]
    return name_contacts

def combine_contacts(contact1, contact2):
    contacts = contact1 + contact2

    # remove duplicates
    contacts = list(set(contacts))

    return contacts

