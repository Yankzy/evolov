from utils.mixins import PaginatedTypeMixin
from graphene_django.types import DjangoObjectType
import graphene
from . import models


class ADType(DjangoObjectType):
    class Meta:
        model = models.Ad
    

class ADPaginatedType(PaginatedTypeMixin):
    objects = graphene.List(ADType)


class AdNode(DjangoObjectType):
    class Meta:
        model = models.Ad
        filter_fields = {
            'sub_category': ['exact'],
            'sub_category__category': ['exact'],
        }
        interfaces = graphene.relay.Node,
