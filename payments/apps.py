from django.apps import AppConfig
from django.conf import settings
import stripe

class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'

    # def ready(self):
    #     print('-------- registering stripe webhook --------')
    #     stripe_webhook = settings.STRIPE_WEBHOOK_URL
    #     stripe.api_key = settings.STRIPE_KEY

    #     registered = False

    #     hooks_list = [x.url for x in stripe.WebhookEndpoint.list().data]

    #     if stripe_webhook in hooks_list:
    #         print('-------- webhook endpoint already registered --------')    
    #     else:
    #         stripe.WebhookEndpoint.create(
    #             url=stripe_webhook,
    #             enabled_events=[
    #                 'checkout.session.completed',
    #             ]
    #         )

    #         print(f'-------- new webhook endpoint {stripe_webhook} registered --------')