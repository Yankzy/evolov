import graphene
from graphene_django.types import ObjectType
from users.models import User
from product.models import Ad
from users.types import UserType, AdType
from utils.permissions import permission_checker, IsAuthenticated





class CompanyQueries(ObjectType):

    company = graphene.List(UserType, email=graphene.String())

    # @permission_checker([IsAuthenticated])
    def resolve_company(self, info, **kwargs):
        return User.objects.filter(email=kwargs['email'])