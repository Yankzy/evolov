import graphene
from graphene_django.types import ObjectType
from users.models import User, Employee
from users.types import UserType, EmployeeType
from django.contrib.auth import authenticate
from django.forms import ValidationError
from firebase_admin import auth
from utils.permissions import permission_checker, IsAuthenticated


class EmployeeQueries(ObjectType):

    all_employees = graphene.List(
        EmployeeType, 
        company_id=graphene.String(required=True)
    )

    def resolve_all_employees(self, info, company_id):
        return Employee.objects.filter(company_id=company_id, user_id__is_active=True)
