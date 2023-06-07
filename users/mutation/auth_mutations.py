import graphene
from users.models import User, UserAuthToken
from users.types import AuthLoginType
from firebase_admin import auth
from firebase_admin.exceptions import NotFoundError
from django.contrib.auth import authenticate
from graphql.error import GraphQLError


class AuthorizationToken(graphene.Mutation):
    to_return = graphene.Field(AuthLoginType)

    class Arguments:
        email = graphene.String(required=True)
        uid = graphene.String(required=True)
    
    def mutate(self, info, **kwargs):
        try:
            firebase_user = auth.get_user_by_email(kwargs['email'])
        except NotFoundError as e:
            raise GraphQLError("Firebase Authentication Failed") from e

        
        if firebase_user.uid != kwargs['uid']:
            raise GraphQLError("Firebase Authentication Failed")

        user = authenticate(email=kwargs['email'], password=kwargs['uid'])

        if not user:
            try:
                user = User.objects.get(email=kwargs['email'])
                user.set_password(kwargs['uid'])
                user.save()
            except User.DoesNotExist as e:
                raise GraphQLError("Invalid Credentials Provided") from e

        token, _ = UserAuthToken.objects.get_or_create(user=user)
        return AuthorizationToken({
            'token': token.token,
            'user': user
        })


class Authorization(graphene.ObjectType):
    authorize_token = AuthorizationToken.Field()
