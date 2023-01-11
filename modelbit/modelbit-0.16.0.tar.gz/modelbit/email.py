from .utils import inDeployment
from .helpers import isAuthenticated, getJsonOrPrintError
from typing import List, Dict, Any
import re

_EmailPat = re.compile(r'([A-Za-z0-9]+[.-_+])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

_email_queue: List[Dict[str, Any]] = []


def sendEmail(subject: str, to: List[str], msg: str):
  if type(subject) is not str or len(subject) == 0:
    raise Exception("The subject= parameter must be a non-empty string")
  if type(to) is not list or len(to) == 0:
    raise Exception("The to= parameter must be a list of email addresses")
  for t in to:
    if type(t) is not str or not re.fullmatch(_EmailPat, t):
      raise Exception(f"The to= parameter '{t}' does not appear to be an email address")
  if type(msg) is not str or len(msg) == 0:
    raise Exception("The msg= parameter must be a non-empty string")

  if inDeployment():
    _queueEmail(subject, to, msg)
  else:
    if isAuthenticated():
      _sendEmailViaWeb(subject, to, msg)
    else:
      raise Exception("This environment is not authenticated with Modelbit and cannot send emails")


def _queueEmail(subject: str, to: List[str], text: str):
  _email_queue.append({"subject": subject, "to": to, "text": text})


def getQueuedEmails():
  return _email_queue


def resetQueue():
  global _email_queue
  _email_queue = []


def _sendEmailViaWeb(subject: str, to: List[str], text: str):
  getJsonOrPrintError("jupyter/v1/email/send", {"subject": subject, "to": to, "text": text})
