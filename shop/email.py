import smtplib
import ssl
from email.message import EmailMessage


# email service - sending emails from Gmail account using SSL
class Email:

    def __init__(self):

        # variables init
        self.body = None
        self.subject = None
        self.to_email = None

        # sender
        self.from_email = 'ecommerce.shop.cz@gmail.com'

        # smtp account
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 465
        self.smtp_username = 'ecommerce.shop.cz@gmail.com'
        self.smtp_password = 'fudf geyb etmi gptj'

    # send email
    def send(self, to_email, subject, body):

        # parameters
        self.to_email = to_email
        self.subject = subject
        self.body = body

        # email message settings
        em = EmailMessage()
        em['From'] = self.from_email
        em['To'] = self.to_email
        em['Subject'] = self.subject
        em.set_content(self.body)

        # ssl settings
        context = ssl.create_default_context()

        try:
            smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context)

        except ConnectionError:
            print('Connection to SMTP server error.')

        else:
            # send email
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as smtp:
                smtp.login(self.smtp_username, self.smtp_password)
                smtp.sendmail(self.from_email, self.to_email, em.as_string())
