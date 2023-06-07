
import contextlib
from product.filter_options import category_options
from users.forms import UserForm
from users.models import Following, User
from django.utils import timezone
from product.models import Ad, Category, ImageUrl, SubCategory, Resume
from graphql import GraphQLError
import logging
import traceback
from utils import to_snake_case

kw = []


def create_or_update_user(**data):
    kwargs = data['data']
    kw.append(kwargs)
        

    if kwargs.get('event_type') == 'create_user':
        kwargs.setdefault("date_joined", timezone.now())
        kwargs.setdefault("last_login", timezone.now())
        kwargs.setdefault("password", kwargs['uid'])
        if kwargs.get('is_employee') and (not kwargs.get('employee_position') or not kwargs.get('company_id')):
            raise GraphQLError("employee_position and company_id are required")

        form = UserForm(kwargs)
        if form.is_valid():
            user = form.save()
    else:
        try:
            user = User.objects.get(email=kwargs['email'])
        except User.DoesNotExist:
            return {'success': False, 'error': 'User does not exist'}

        fields = [field.name for field in User._meta.get_fields()]
        for field, value in kwargs.items():
            if field in fields:
                setattr(user, field, value)

        user.save()

        
    return user


def follow_unfollow(**kwargs):
    with contextlib.suppress(Exception):
        is_following = Following.objects.filter(follower=kwargs['user_id'], followed=kwargs['following'])
        if is_following.exists() and kwargs.get('event_type') == 'unfollow_user': 
            is_following.delete()
        elif not is_following.exists() and kwargs.get('event_type') == 'follow_user':
            ff = Following(follower=kwargs['user_id'], followed=kwargs['following'])
            ff.follow.create(activity_type='FOLLOW')
            ff.save()


def manage_category(**data):
    kwargs = data['data']
    options = category_options(kwargs['category_name'])
    try:
        category = Category.objects.filter(category_name=kwargs['category_name'])
        if category.exists() and kwargs.get('event_type') == 'delete_category': 
            category.delete()
        elif not category.exists() and kwargs.get('event_type') == 'create_category': 
            cat = Category.objects.create(
                category_name=kwargs['category_name'],
                details=options.get('details', {}),
            )
            ImageUrl.objects.create(category=cat, category_image=kwargs['category_image_url'])
        elif category.exists() and kwargs.get('event_type') == 'update_category': 
            category.update(
                category_name=kwargs['category_name'],
                details=options.get('details', {}),
            )
            ImageUrl.objects.filter(category=category.first()).update(category_image=kwargs['category_image_url'])
            
    except Exception as e:
        raise GraphQLError(e) from e


def manage_sub_category(**data):
    kwargs = data['data']
    try:
        sub_category = SubCategory.objects.filter(sub_category_name=kwargs['sub_category_name'])
        if sub_category.exists() and kwargs.get('event_type') == 'delete_sub_category': 
            sub_category.delete()
        elif not sub_category.exists() and kwargs.get('event_type') == 'create_sub_category': 
            cat = Category.objects.get(category_name=kwargs['category_name'])
            sub = SubCategory.objects.update_or_create(
                category=cat, 
                sub_category_name=kwargs['sub_category_name'], 
            )
            ImageUrl.objects.create(sub_category=sub, category=cat, sub_category_image=kwargs['sub_category_image_url'])
        elif sub_category.exists() and kwargs.get('event_type') == 'update_sub_category':
            cat = Category.objects.get(category_name=kwargs['category_name'])
            sub_category.update(
                category=cat, 
                sub_category_name=kwargs['sub_category_name'], 
            )
            ImageUrl.objects.filter(sub_category=sub_category.first()).update(sub_category_image=kwargs['sub_category_image_url'])
    except Exception as err:
        GraphQLError(err)

def create_update_ad(**data):
    kwargs = data['data']

    try:
        sub = SubCategory.objects.get(sub_category_name=kwargs['sub_category_name'])
        if kwargs.get('event_type') == "create_ad":
            ad = Ad.objects.create(
                sub_category=sub,
                details=kwargs.get('details', None),
                features=kwargs.get('features', {}),
                benefits=kwargs.get('benefits', {}),
                nearby=kwargs.get('nearby', {}),
                facilities=kwargs.get('facilities', {}),
                statistics={"reviews": 0, "views": 0, "likes": 0, "shares": 0},
            )
            ad.user.add(kwargs['user'])
            ImageUrl.objects.create(ad=ad, gallery=kwargs.get('gallery', None))
            return ad

        ad = list(Ad.objects.filter(id=kwargs['ad_id']))[0]
        ad.update(
            facilities=kwargs.get('facilities', ad['facilities']),
            details=det if (det := kwargs.get('details')) else ad['details'],
            near_by=near if (near := kwargs.get('near_by')) else ad['near_by'],
            status= ad['status'] if (val := kwargs.get('status')) is None else val,
            is_active= ad['is_active'] if (val := kwargs.get('is_active')) is None else val,
        )
        return ad
    except Exception as e:
        tb = ''.join(traceback.format_exception(None, e, e.__traceback__))
        logging.getLogger('error_logger').error(f"{timezone.now()}: \n{tb}")
        raise GraphQLError(e) from e




def create_update_resume(**data):
    kwargs = data['data']
    try:
        if kwargs.get('event_type') == "create_resume":
            Resume.objects.create(
                user=kwargs['user'],
                personal_information=kwargs.get('personal_information', {}),
                skills=kwargs.get('skills', {}),
                work_experience=kwargs.get('work_experience', {}),
                education=kwargs.get('education', {}),
                languages=kwargs.get('languages', {}),
            )
            return Resume.objects.filter(user=kwargs['user']).last()
    except Exception as e:
        tb = ''.join(traceback.format_exception(None, e, e.__traceback__))
        logging.getLogger('error_logger').error(f"{timezone.now()}: \n{tb}")
        raise GraphQLError(e) from e

    
