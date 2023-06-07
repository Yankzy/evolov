import graphene
from graphene_django.types import ObjectType
from users.models import User
from users.types import UserType
from django.contrib.auth import authenticate
from django.forms import ValidationError
from firebase_admin import auth
from utils.permissions import permission_checker, IsAuthenticated


def firebase_auth(uid):
    """
    Authenticate user in firebase when they login.
    As long as they remain logged in on the frontend, we will just run local authentication.
    """
    return user if (user := auth.get_user(uid)) else None



class Authenticate(ObjectType):
    auth = graphene.List(
        UserType,
        email=graphene.String(),
        uid=graphene.String()
    )

    list_all_users = graphene.List(
        UserType,
        filters=graphene.JSONString()
    )


    get_me = graphene.Field(UserType)

    # @permission_checker([IsAuthenticated])
    def resolve_get_me(self, info, **kwargs):
        return info.context.user

    # @permission_checker([IsAuthenticated])
    def resolve_list_all_users(self, info, **kwargs):
        return User.objects.filter(**kwargs['filters'])

    def resolve_auth(self, info, **kwargs):
        user = auth.get_user_by_email(kwargs['email'])
        # user = auth.create_user(
        #    i email=kwargs['email'],
        #     email_verified=False,
        #     phone_number='+15555550100',
        #     password='secretPassword',
        #     display_name='John Doe',
        #     photo_url='http://www.example.com/12345678/photo.png',
        #     disabled=False
        # )
        print(user.__dict__)
        # print('Sucessfully created new user: {0}'.format(user.uid))

        # # if "Doesn't exist in FIREBASE", frontend should redirect to SIGNUP 
        # if not firebase_auth(kwargs['uid']):
        #     raise ValidationError("Doesn't exist in firebase")

        # # if "Doesn't exist in DATABASE", frontend should redirect to PROFILE FORM 
        # if not authenticate(username=kwargs['email'], password=kwargs['uid']):
        #     raise ValidationError("Doesn't exist in database")

        return User.objects.filter(email=kwargs['email'])
