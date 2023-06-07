import glob
from django.conf import settings
from config import celery_app
from django.core.mail import EmailMessage
import time

def send_one_email(**kwargs):
    # see https://gist.github.com/Yankzy/154970e4de0d50aff9140117f7d4fd0d
    msg = EmailMessage()

    msg.subject = kwargs.get("subject")
    msg.from_email = settings.DEFAULT_FROM_EMAIL
    msg.to = [kwargs.get("email")]
    msg.body = kwargs.get('body')

    if filename := kwargs.get("attachment"):
        msg.attach_file(filename)
    
    msg.send()


@celery_app.task()
def welcome_email(**kwargs):
    print("Sending Email Started")
    # time.sleep(60)
    send_one_email(
        name=kwargs.get("first_name"),
        email=kwargs.get("email"),
        subject="Thank you",
        body="Thanks for registering!\nRegards, The DevNotes team",
        attachment=kwargs.get('attachment')
    )
    print("Email Sent")
    print("------------------------")


def thanks_for_upgrading(**kwargs):
    send_one_email(
        name=kwargs.get("first_name"),
        email=kwargs.get("email"),
        subject="Thank you for upgrading to adminstrator",
        body="Thanks for upgrading! You're gonna love it. \nRegards, The DevNotes team",
        attachment=glob.glob('/Users/mac/Documents/W-4 Susana.pdf')
    )
