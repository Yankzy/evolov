
from graphene import String, Mutation, List, ObjectType
from observer.utils import follow_unfollow
from users.models import Activity
from users.types import ActivityType
from observer import Notify
from django.forms import ValidationError


class FollowUser(Mutation):
    to_return = List(ActivityType)

    class Arguments:
        email = String(required=True)
        uid = String(required=True)
        event_type = String(required=True)
        user_id = String(required=True) # my ID
        following = String(required=True) # ID of the user I want to follow or unfollow

    def mutate(self, info, **kwargs):
        if kwargs.get('event_type') not in ['follow_user', 'unfollow_user']:
            raise ValidationError("Wrong event_type")

        trigger = Notify(event_type=kwargs["event_type"], callback=follow_unfollow).subscribe()
        trigger(kwargs["event_type"], kwargs)

        all_followed = Activity.objects.filter(following__follower=kwargs['user_id'])

        return FollowUser(to_return=all_followed)


class FollowMutations(ObjectType):
    follow_user = FollowUser.Field()
