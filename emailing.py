'''Please Note in order to use this script, you need to enable your Gmail,
allow less secure applications use the Gmail services. You can also use other
APIs which are freely available.
'''

import ssl
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText


def send_email(sender, password, receivers, subject, cc=[], bcc=[], text='', attachments=None):
    # Create the container email message.
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)
    msg['Cc'] = ', '.join(cc)
    msg['Bcc'] = ', '.join(bcc)
    msg['Subject'] = subject

    # Add in the message body
    msg.attach(MIMEText(text, 'plain'))

    # Add attachments, if any
    if attachments is not None:
        for file in attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % file)
            msg.attach(part)

    # Convert to string
    message = msg.as_string()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465,  context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receivers+cc+bcc, message)
        smtp.close()
