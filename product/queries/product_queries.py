import graphene
from graphene_django.types import ObjectType
from product.models import Category, Ad
from users.types import CategoryType, CompanyType, UserType, AdType
from firebase_admin import auth
from product import types, models
from utils.paginators import common_pagination
from utils.permissions import IsEmployee, IsCompany, IsAuthenticated, permission_checker
from django.db.models import Q
from graphene_django.filter import DjangoFilterConnectionField
from users.models import Company, Employee, User


class ProductQueries(ObjectType):
    category = graphene.List(CategoryType, email=graphene.String())


    my_ads = graphene.Field(
        types.ADPaginatedType,
        page=graphene.Int(1),
        per_page=graphene.Int(25),
    )

    ad_by_category = DjangoFilterConnectionField(types.AdNode)

    
    user_ads_filter = graphene.List(
        AdType, 
        user_id=graphene.String(required=True), 
        is_vacancy=graphene.Boolean(required=True)
    )

    def resolve_user_ads_filter(self, info, user_id, is_vacancy):
        return Ad.objects.filter(
            Q(user__id=user_id),
            Q(sub_category__sub_category_name='vacancy'),
            ~Q(status='DELETED'),
        ) if is_vacancy else Ad.objects.filter(
            Q(user__id=user_id),
            ~Q(sub_category__sub_category_name='vacancy'),
            ~Q(status='DELETED'),
        ) 
        


    
    def resolve_category(self, info, **kwargs):
        return Category.objects.all()



    def resolve_my_ads(self, info, **kwargs):
        user = info.context.user

        if user is None:
            objects = models.Ad.objects.all()
            # exclude some fields here or move to new object type
        
        if IsCompany.has_permission(info.context):
            company = user.company
            employees = company.main_company.all()
            

            objects = models.Ad.objects.filter(
                Q(user=user) |
                Q(user__employee__in=employees)
            )
        
        if IsEmployee.has_permission(info.context):
            objects = models.Ad.objects.filter(user=user)

        return common_pagination(
            objects=objects,
            page=kwargs['page'],
            per_page=kwargs['per_page'],
        )

