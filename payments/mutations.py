from django.conf import settings
import graphene
from . import models
from utils.permissions import *
from product import models as product_models
from .api.stripe import stripe_api
import stripe


class StripeTransaction(graphene.Mutation):
    class Arguments:
        subcategory_id = graphene.ID(required=True)
    
    client_secret = graphene.String()


    # @permission_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):
        try:
            subcategory = product_models.SubCategory.objects.get(id=kwargs['subcategory_id'])
        except product_models.Ad.DoesNotExist as e:
            raise GraphQLError("subcategory not found") from e
        

        stripe_intent = stripe_api.create_intent(subcategory.price)

        payment_transaction = models.PaymentTransaction.objects.create(
            user=info.context.user,
            amount=subcategory.price,
        )

        transaction = models.StripeTransaction.objects.create(
            payment_transaction=payment_transaction,
            stripe_transaction_id=stripe_intent.id,
        )

        return StripeTransaction(stripe_intent.client_secret)


class PremiumAndSponsorPayment(graphene.Mutation):
    client_secret = graphene.String()

    class Arguments:
        sub_category_name = graphene.ID(required=True)
    
    def mutate(self, info, **kwargs):

        stripe.api_key = settings.STRIPE_SECRET

        try:
            subcategory = product_models.SubCategory.objects.get(sub_category_name=kwargs['sub_category_name'])
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=int(15 * 100),
                currency='usd',
                payment_method_types=['card'],
                # automatic_payment_methods={
                #     'enabled': True,
                # },
            )
        except (product_models.Ad.DoesNotExist, ValueError) as e:
            raise GraphQLError(str(e)) from e
                 
        return PremiumAndSponsorPayment(intent['client_secret'])



class PaymentMutations(graphene.ObjectType):
    create_stripe_transaction = StripeTransaction.Field()
    payment = PremiumAndSponsorPayment.Field()
