from twilio.rest import Client
from django.conf import settings
from config import celery_app


@celery_app.task()
def send_sms(to, text, _from = settings.TWILIO_DEFAULT_SENDER):
    print(f"sending SMS, {to}, {_from}")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
                                body=text,
                                from_=_from,
                                to=to
                            )
    print(message.__dict__)
