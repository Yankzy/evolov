
from users.models import Company, Employee
from users.models import User
from typing import Any
from .exceptions import PermissionDenied, GraphQLError
from django.utils.functional import SimpleLazyObject
from payments.models import PaymentTransaction
from datetime import timedelta

from users.models import Company, Employee
from graphql.error import GraphQLError
from users.models import User
from .exceptions import PermissionDenied


class BasePermission:
    @staticmethod
    def has_permission(context):
        return True
        


class IsAuthenticated(BasePermission):
    """
    permission to check for user authentication
    """
    @classmethod
    def has_permission(cls, context):
        return context.user and context.user.is_authenticated


class IsCompany(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user

        if not user or not user.is_authenticated:
            return False
        
        try:
            company = Company.objects.get(user=user)
        except Company.DoesNotExist:
            return False
            
        return user.is_authenticated and user.is_company


class IsEmployee(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user

        if not user or not user.is_authenticated:
            return False
        
        try:
            employee = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            return False

        return user.is_authenticated and user.is_employee


class CanPostAD(BasePermission):
    @staticmethod
    def has_permission(context):
        user = context.user

        if IsEmployee.has_permission(context):
            user = user.employee.company.user
        
        transactions = PaymentTransaction.objects.filter(user=user, status='COMPLETED')

        if transactions.exists():
            return True

        return False


class InstancePermission:
    @classmethod
    def check_instance_owner(cls, instance: Any, user: User, user_field_name = 'user') -> bool:
        """
        check if the given intance is owned by the passed user

        Args:
            instance (Object, Any): the object to check for permission
            user (User): the owner
            user_field_name (str, optional): the field on the instance that maps to the user. Defaults to 'user'.

        Raises:
            utils.exceptions.PermissionDenied: permission denied if the instance is not owned by the user

        Returns:
            bool: if the instance is owned by the user
        """
        try:
            if getattr(instance, user_field_name) == user:
                return True
        except AttributeError:
            pass

        raise PermissionDenied("Permission Denied for the current opperation")


def permission_checker(permissions: list):
    def wrap_decorator(func):
        def inner(cls, info, *args, **kwargs):
            if check_permission(permissions, info.context):
                return func(cls, info, **kwargs)
            
            raise GraphQLError("Permission Denied")
        
        return inner
    
    return wrap_decorator


def check_permission(permissions, context):
    return all(permission.has_permission(context) for permission in permissions)
    # for permission in permissions:
    #     if not permission.has_permission(context):
    #         return False
    
    # return True
