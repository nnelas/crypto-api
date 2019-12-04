import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, message, from_addr, to_addr,
               smtp_host, smtp_port, smtp_user, smtp_pass,
               attachments=[], html=False):

    # Create a text/plain message
    msg = MIMEMultipart("mixed")

    msg["Subject"] = subject
    msg["To"] = ",".join(to_addr)
    msg.attach(MIMEText(message, "html" if html else "plain"))

    for f in attachments:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(fil.read(),
                                       Content_Disposition='attachment; filename="%s"' % f,
                                       Name=f))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    if smtp_user:
        server.login(smtp_user, smtp_pass)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
