# schema.py
import graphene
from graphql import GraphQLError
from django.contrib.auth.models import Group,User
from graphene_django_crud.types import DjangoCRUDObjectType, resolver_hints
from django.contrib.auth import get_user_model
# from users.models import User

# User = get_user_model()
class UserTypes(DjangoCRUDObjectType):
    class Meta:
        model = User
        exclude_fields = ("password",)
        input_exclude_fields = ("last_login", "date_joined")

    full_name = graphene.String()


    @resolver_hints(
      only=["first_name", "last_name"]
    )
    @staticmethod
    def resolve_full_name(parent, info, **kwargs):
        return parent.get_full_name()

    @classmethod
    def get_queryset(cls, parent, info, **kwargs):
        # if info.context.user.is_authenticated:
        return User.objects.all()

    @classmethod
    def mutate(cls, parent, info, instance, data, *args, **kwargs):
        # if not info.context.user.is_staff:
        #     raise GraphQLError('not permited, only staff user')

        # if "password" in data.keys():
        #     instance.set_password(data.pop("password"))
        return super().mutate(parent, info, instance, data, *args, **kwargs)

class GroupType(DjangoCRUDObjectType):
    class Meta:
        model = Group

class NewQuery(graphene.ObjectType):

    me = graphene.Field(
        UserTypes,
        email=graphene.String(),
        uid=graphene.String(),
    )
    user = UserTypes.ReadField()
    users = UserTypes.BatchReadField()

    group = GroupType.ReadField()
    groups = GroupType.BatchReadField()

    def resolve_me(self, info, **kwargs):
        # return info.context.user if info.context.user.is_authenticated else None
        return User.objects.all()

class NewMutation(graphene.ObjectType):

    user_create = UserTypes.CreateField()
    user_update = UserTypes.UpdateField()
    user_delete = UserTypes.DeleteField()

    group_create = GroupType.CreateField()
    group_update = GroupType.UpdateField()
    group_delete = GroupType.DeleteField()

class Subscription(graphene.ObjectType):

    user_created = UserTypes.CreatedField()
    user_updated = UserTypes.UpdatedField()
    user_deleted = UserTypes.DeletedField()

    group_created = GroupType.CreatedField()
    group_updated = GroupType.UpdatedField()
    group_deleted = GroupType.DeletedField()

