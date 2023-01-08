def anonymize(email_address):
    parts = email_address.split('@', maxsplit=1)
    if len(parts) <= 1:
        return email_address
    return '{}***@{}'.format(email_address[0:1], parts[1])
