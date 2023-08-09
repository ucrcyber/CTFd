from email.utils import formataddr

import requests

from CTFd.utils import get_app_config, get_config
from CTFd.utils.email.providers import EmailProvider


# Changed to using smtp2go
class MailgunEmailProvider(EmailProvider):
    @staticmethod
    def sendmail(addr, text, subject):
        ctf_name = get_config("ctf_name")
        mailfrom_addr = get_config("mailfrom_addr") or get_app_config("MAILFROM_ADDR")
        mailfrom_addr = formataddr((ctf_name, mailfrom_addr))

        mailgun_base_url = get_config("mailgun_base_url") or get_app_config(
            "MAILGUN_BASE_URL"
        )
        mailgun_api_key = get_config("mailgun_api_key") or get_app_config(
            "MAILGUN_API_KEY"
        )
        # Remove trailing / if exists
        mailgun_base_url = mailgun_base_url[:-1] if mailgun_base_url[-1] == "/" else mailgun_base_url
        mailgun_base_url = mailgun_base_url.strip()
        try:
            r = requests.post(
                mailgun_base_url+"/email/send",
                headers={"Content-Type": "application/json"},
                json={
                    "api_key": mailgun_api_key,
                    "sender": mailfrom_addr,
                    "to": [addr],
                    "subject": subject,
                    "text_body": text,
                },
                timeout=5.0,
            )
        except requests.RequestException as e:
            return (
                False,
                "{error} exception occured while handling your request".format(
                    error=type(e).__name__
                ),
            )

        if r.status_code == 200:
            return True, "Email sent"
        else:
            return False, "smtp2go settings are incorrect"
