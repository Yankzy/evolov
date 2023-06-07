from hypothesis import given
from hypothesis.strategies import text
from users.models import User, Activity
from product.models import Ad
from django.contrib.contenttypes.models import ContentType
from users.query.user_queries import UserQueries
from users.types import ActivityType


@given(user_id=text())
def test_likes_filter_returns_list_of_activity_type_objects(user_id):
    # create a test user and a few test activity objects
    user = User(id=user_id)
    content_type = ContentType(model='Ad')
    activities = [Activity(content_type=content_type, user=user, activity_type='LIKE') for _ in range(2)]
    
    # call the likes_filter method and assert that it returns a list of activity objects
    result = UserQueries.likes_filter(user_id=user_id, activities=activities)
    assert isinstance(result, list)
    assert all(isinstance(x, ActivityType) for x in result)

@given(user_id=text())
def test_likes_filter_filters_by_content_type(user_id):
    # create a test user and a few test activity objects with different content types
    user = User(id=user_id)
    content_type1 = ContentType(model='Ad')
    content_type2 = ContentType(model='BlogPost')
    activities = [
        Activity(content_type=content_type1, user=user, activity_type='LIKE'),
        Activity(content_type=content_type2, user=user, activity_type='LIKE')
    ]
    
    # call the likes_filter method and assert that it only returns activity objects with the correct content type
    result = UserQueries.likes_filter(user_id=user_id, activities=activities)
    assert all(x.content_type == content_type1 for x in result)

@given(user_id=text())
def test_likes_filter_filters_by_activity_type(user_id):
    # create a test user and a few test activity objects with different activity types
    user = User(id=user_id)
    content_type = ContentType(model='Ad')
    activities = [
        Activity(content_type=content_type, user=user, activity_type='LIKE'),
        Activity(content_type=content_type, user=user, activity_type='DISLIKE')
    ]
    
    # call the likes_filter method and assert that it only returns activity objects with the correct activity type
    result = UserQueries.likes_filter(user_id=user_id, activities=activities)
    assert all(x.activity_type == 'LIKE' for x in result)

@given(user_id=text())
def test_likes_filter_returns_empty_list_if_no_matches(user_id):
    # create a test user and a few test activity objects with different content types and activity types
    user = User(id=user_id)
    content_type1 = ContentType(model='Ad')
    content_type2 = ContentType(model='BlogPost')
    activities = [Activity(content_type=content_type1, user=user, activity_type='DISLIKE'),]

if __name__ == "__main__":
    test_likes_filter_returns_empty_list_if_no_matches()