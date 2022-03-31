import logging
import smtplib
from socket import error as socket_error
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64

import werkzeug.datastructures as ds

from ckan.common import config, asbool
from ckan.lib.mailer import MailerException


log = logging.getLogger(__name__)


def send_email(content, to, subject, file=None):
    '''Sends email
       :param content: The body content for the mail.
       :type string:
       :param to: To whom will be mail sent
       :type string:
       :param subject: The subject of mail.
       :type string:


       :rtype: string

       '''
    smtp_server = config.get('smtp.server')
    smtp_user = config.get('smtp.user')
    smtp_password = config.get('smtp.password')
    smtp_from = config.get('smtp.mail_from')
    smtp_starttls = asbool(config.get('smtp.starttls'))

    msg = MIMEMultipart()

    from_ = smtp_from

    if isinstance(to, str):
        to = [to]

    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = ','.join(to)

    content = """\
        <html>
          <head></head>
          <body>
            <p>""" + content + """</p>
          </body>
        </html>
    """

    msg.attach(MIMEText(content, 'html', _charset='utf-8'))

    if isinstance(file, ds.FileStorage):
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.stream.read())
        encode_base64(part)

        extension = file.filename.split('.')[-1]

        part.add_header('Content-Disposition',
                        'attachment; filename=attachment.{0}'.format(extension))

        msg.attach(part)

    try:
        smtp_connection = smtplib.SMTP(smtp_server)
    except socket_error as e:
        log.critical(
            'Could not connect to email server. \
            Have you configured the SMTP settings?')
        log.exception(e)
        error_dict = {
            'success': False,
            'message': 'An error occured while sending the email. Try again.'
        }
        return error_dict
    try:
        # Identify ourselves and prompt the server for supported features.
        smtp_connection.ehlo()

        if smtp_starttls:
            if smtp_connection.has_extn('STARTTLS'):
                smtp_connection.starttls()
                # Re-identify ourselves over TLS connection.
                smtp_connection.ehlo()
            else:
                raise MailerException("SMTP server does not support STARTTLS")

        # If 'smtp.user' is in CKAN config, try to login to SMTP server.
        if smtp_user:
            assert smtp_password, ("If smtp.user is configured then "
                                   "smtp.password must be configured as well.")
            smtp_connection.login(smtp_user, smtp_password)

        smtp_connection.sendmail(from_, to, msg.as_string())
        log.info("Sent email to {0}".format(msg['To']))

    except smtplib.SMTPException as e:
        msg = '%r' % e
        log.exception(msg)
        raise MailerException(msg)
    finally:
        smtp_connection.quit()
        response_dict = {
            'success': True,
            'message': 'Email message was successfully sent.'
        }
        return response_dict
