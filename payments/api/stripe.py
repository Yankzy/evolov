import stripe
from django.conf import settings


class StripeAPI:
    def __init__(self) -> None:
        stripe.api_key = settings.STRIPE_KEY
    
    def create_product(self, name, description):
        return stripe.Product.create(name=name, description=description)

    def create_price(self, price, product_id):
        return stripe.Price.create(
            unit_amount=int(price) * 100,
            currency='usd',
            product=product_id
        )
    
    def create_intent(self, price):
        return stripe.PaymentIntent.create(
            amount=price,
            currency='USD',
            automatic_payment_methods={
                'enabled': True,
            },
        )
    
    def get_or_create_link(self, price):
        link = stripe.PaymentLink.create(
            line_items=[
                {
                    'price': price,
                    'quantity': 1,
                }
            ]
        )

        return link

    def send_invoice(self, email, price):
        customer = stripe.Customer.create(
            email=email,
            description="Customer to invoice",
        )
    
        customer_id = customer.id


        stripe.InvoiceItem.create(
            customer=customer_id,
            price=price,
        )

        invoice = stripe.Invoice.create(
            customer=customer_id,
            collection_method='send_invoice',
            days_until_due=30,
        )

        stripe.Invoice.send_invoice(invoice.id)
        return invoice


stripe_api = StripeAPI()
