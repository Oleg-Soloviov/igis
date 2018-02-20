import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from django.core.mail.message import sanitize_address

class MailgunEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return
        num_sent = 0
        for email_message in email_messages:
            if not email_message.recipients():
                return
            encoding = email_message.encoding or settings.DEFAULT_CHARSET
            from_email = sanitize_address(email_message.from_email, encoding)
            recipients = [sanitize_address(addr, encoding) for addr in email_message.recipients()]
            try:
                resp = requests.post(
                    "https://api.mailgun.net/v3/sandbox075b55521f59465c82d4d87856d6f43c.mailgun.org/messages",
                    auth=("api", "key-e1518fd3e6d897d250e23581f295417c"),
                    data={"from": "<postmaster@sandbox075b55521f59465c82d4d87856d6f43c.mailgun.org>",
                          "to": recipients,
                          "subject": email_message.subject,
                          "text": email_message.body})
            except Exception as e:
                if  self.fail_silently:
                    pass
            else:
                if resp.ok:
                    num_sent += 1
        return num_sent