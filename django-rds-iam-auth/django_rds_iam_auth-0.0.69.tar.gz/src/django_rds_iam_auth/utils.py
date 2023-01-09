from dns.exception import DNSException
import dns.resolver
import dns.rdatatype
import datetime


def resolve_cname(hostname):
    """Resolve a CNAME record to the original hostname.

    This is required for AWS where the hostname of the RDS instance is part of
    the signing request.

    """
    try:
        answers = dns.resolver.query(hostname, "CNAME")
        for answer in answers:
            if answer.rdtype == dns.rdatatype.CNAME:
                return answer.to_text().strip('.')
    except DNSException:
        return hostname


def set_cookie(response, domain, key, value, days_expire=7, secure=None):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=domain, secure=secure or None)