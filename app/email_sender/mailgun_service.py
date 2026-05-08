import os
import requests


class EmailSenderService:

    def __init__(self):

        self.api_key = os.getenv(
            "MAILGUN_API_KEY"
        )

        self.domain = os.getenv(
            "MAILGUN_DOMAIN"
        )

        self.from_email = os.getenv(
            "MAILGUN_FROM_EMAIL"
        )

    def send_email(
        self,
        subject,
        body
    ):

        to_email = os.getenv(
            "TEST_RECIPIENT_EMAIL"
        )

        html_body = f"""
        <html>
            <body>
                <pre>
{body}
                </pre>
            </body>
        </html>
        """

        response = requests.post(

            f"https://api.mailgun.net/v3/"
            f"{self.domain}/messages",

            auth=(
                "api",
                self.api_key
            ),

            data={

                "from": self.from_email,

                "to": [to_email],

                "subject": subject,

                "html": html_body
            }
        )

        return response