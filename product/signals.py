from django.dispatch import receiver
# from django.db.models.signals import post_save
from config import celery_app
from payments.api.stripe import stripe_api
from . import models


# @receiver(post_save, sender=models.Ad)
def ad_signal(instance: models.Ad, *args, **kwargs):
    create_stripe_product.delay(instance.id)


@celery_app.task()
def create_stripe_product(ad_id):
    ad = models.Ad.objects.get(id=ad_id)

    if not ad.stripe_product_id:
            product = stripe_api.create_product(
                name=ad.details.get('title') or "Evolov Test Product",
                description=ad.details.get('description') or "Evolov Test Product Details",
            )
            ad.stripe_product_id = product.id

            price = stripe_api.create_price(
                price=ad.details['price'],
                product_id=product.id
            )
            ad.stripe_price_id = price.id

            ad.save()