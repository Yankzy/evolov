import graphene
from graphene_django import DjangoObjectType
from . import models


class StripeTransactionType(DjangoObjectType):
    class Meta:
        model = models.StripeTransaction
