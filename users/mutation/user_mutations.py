from graphene import ID, String, Mutation, List, ObjectType, Boolean, Int
from observer.utils import create_or_update_user
from users.models import Activity, Following, User, Company, Employee, UserAuthToken
from users.types import CompanyType, EmployeeType, UserType, AuthLoginType
from django.forms import ValidationError
from observer import Notify
from firebase_admin import auth
from firebase_admin.exceptions import NotFoundError
from django.contrib.auth import authenticate
import graphene 
from graphql.error import GraphQLError
from utils.permissions import IsAuthenticated, IsCompany, permission_checker
from firebase_admin import auth



class CreateUser(Mutation):
    to_return = List(UserType)

    class Arguments:
        email = String(required=True)
        uid = String(required=True)
        event_type = String(required=True)
        first_name = String(required=True)
        last_name = String(required=True)
        phone = String(required=True)
        street_address = String()
        city = String()
        zip_code = String()
        state = String()
        country = String(required=True)
        notification_is_on = Boolean()
        is_company = Boolean(required=True)
        is_employee = Boolean(required=True)
        corporation_name = String()
        corporation_id = ID()
        user_bio = String()
        company_id = String() # Required if the user being created is an employee
        employee_position = String() # Required if the user being created is an employee


    def mutate(self, info, **kwargs):
        if kwargs.get('event_type') != 'create_user':
            raise ValidationError("Wrong event_type")

        if kwargs.get('is_employee'):
            user = auth.create_user(
                email=kwargs['email'],
                email_verified=False,
                phone_number=kwargs['phone'],
                password=kwargs['uid'],
                display_name=f"{kwargs['first_name']} {kwargs['last_name']}",
                disabled=False
            )
            kwargs['uid'] = user.uid

        Notify(
            event_type="create_user", 
            callback=create_or_update_user,
            data=kwargs
        ).subscribe()()

        return CreateUser(to_return=User.objects.filter(email=kwargs['email']))



class UpdateUser(Mutation):
    to_return = List(UserType)

    class Arguments:
        email = String(required=True)
        uid = String(required=True)
        event_type = String(required=True)
        first_name = String()
        last_name = String()
        is_active = Boolean()
        is_verified = Boolean()
        notification_is_on = Boolean()
        phone = String()
        street_address = String()
        city = String()
        zip_code = Int()
        state = String()
        country = String()
        user_bio = String()

    def mutate(self, info, **kwargs):
        if kwargs.get('event_type') != 'update_user':
            raise ValidationError("Wrong event_type")
        
        trigger = Notify(
            event_type="create_user", 
            callback=create_or_update_user,
            data=kwargs
        ).subscribe()
        trigger()
        return UpdateUser(to_return=User.objects.filter(email=kwargs['email']))


class UpdateEmployee(Mutation):
    to_return = List(EmployeeType)

    class Arguments:
        email = String(required=True)
        event_type = String(required=True)
        employee_id = String(required=True)
        employee_position = String()
        show_employee = Boolean()
        first_name = String()
        last_name = String()
        phone = String()
        street_address = String()
        city = String()
        zip_code = String()
        state = String()
        country = String()
        phone = String()
        is_company = Boolean()
        is_employee = Boolean()
        user_bio = String()

    def mutate(self, info, **kwargs):
        if kwargs.get('event_type') != 'update_employee':
            raise ValidationError("Wrong event_type")

        Notify(
            event_type="update_user", 
            callback=create_or_update_user,
            data=kwargs
        ).subscribe()()
        
        employee = Employee.objects.filter(user=kwargs['employee_id'])
        
        employee.update(
            employee_position=pos if (pos := kwargs.get('employee_position')) else list(employee)[0].employee_position,
            show_employee=list(employee)[0].show_employee if (val := kwargs.get('show_employee')) is None else val
        )
        
        return UpdateEmployee(to_return=employee)



class DeleteUser(Mutation):
    to_return = graphene.Field(UserType)
    class Arguments:
        user_id = graphene.ID(required=True)
    

    @permission_checker([IsAuthenticated, IsCompany])
    def mutate(self, info, *args, **kwargs):
        try:

            user = User.objects.get(id=kwargs['user_id'])

            user.is_active = False
            user.save()
            return DeleteUser(user)

        except User.DoesNotExist as e:
            raise GraphQLError("User does not exist.") from e




class UserMutations(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    update_employee = UpdateEmployee.Field()
    delete_user = DeleteUser.Field()
