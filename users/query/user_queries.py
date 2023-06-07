import graphene
from graphene_django.types import ObjectType
from users.models import User, Activity
from users.types import UserType, ActivityType
from product.models import Ad
from django.contrib.contenttypes.models import ContentType


class UserQueries(ObjectType):

    user_filter = graphene.List(UserType, user_id=graphene.String(required=True))
    likes_filter = graphene.List(ActivityType, user_id=graphene.String(required=True))

    def resolve_user_filter(self, info, user_id):
        return User.objects.filter(pk=user_id)


    # def resolve_likes_filter(self, info, user_id):
    #     user = User.objects.get(id=user_id)
    #     content_type = ContentType.objects.get_for_model(Ad)
    #     return Activity.objects.filter(content_type=content_type, user=user, activity_type='LIKE')

    def resolve_likes_filter(self, info, user_id):
        user = User.objects.get(id=user_id)
        content_type = ContentType.objects.get_for_model(Ad)
        likes = Activity.objects.filter(content_type=content_type, user=user, activity_type='LIKE')
        ad_ids = likes.values_list('object_id', flat=True)
        ads = Ad.objects.filter(id__in=ad_ids)
        activities = []
        for like in likes:
            ad = ads.get(id=like.object_id)
            activity = ActivityType(
                id=like.id,
                user=like.user,
                activity_type=like.activity_type,
                object_id=like.object_id,
            )
            activities.append(activity)
        return activities
