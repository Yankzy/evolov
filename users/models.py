
import email
from django.db import models
from django.contrib.auth.models import AbstractUser
from observer.sms_listener import send_sms
from users.managers import FirebaseUserManager
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from uuid import uuid4
from django.utils import timezone
from observer.email_listener import welcome_email


def get_str():
    return get_random_string(37)


class Activity(models.Model):
    # https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    activity_type = models.CharField(max_length=250, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=250, blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.activity_type}"

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class User(AbstractUser):
    
    username = None
    id = models.CharField(
        primary_key=True, default=get_str, unique=True, editable=False, max_length=40)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=True, blank=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    is_company = models.BooleanField(default=False, null=True, blank=True)
    is_employee = models.BooleanField(default=False, null=True, blank=True)
    notification_is_on = models.BooleanField(default=False, null=True, blank=True)
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    street_address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=25, null=True, blank=True)
    zip_code = models.CharField(max_length=25, null=True, blank=True)
    state = models.CharField(max_length=25, null=True, blank=True)
    country = models.CharField(max_length=56, null=True, blank=True)
    user_bio = models.TextField(max_length=56, null=True, blank=True)
    profile_image = models.CharField(max_length=560, null=True, blank=True)
    follow = GenericRelation(Activity, related_query_name='Following')

    objects = FirebaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserAuthToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE, related_name='token')
    token = models.UUIDField(default=uuid4)

    created_at = models.DateTimeField(default=timezone.localtime)


class Company(models.Model):
    id = models.CharField(primary_key=True, unique=True, editable=False, default=get_str, max_length=40)
    corporation_name = models.CharField(max_length=25, null=True, blank=True)
    corporation_id = models.CharField(max_length=25, null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company', null=True, blank=True)
    show_employees = models.BooleanField(default=True, null=True, blank=True)


    @receiver(post_save, sender=User)
    def create_company_object(sender, instance, created, **kwargs): 
        if created:
            instance.set_password(instance.password)
            instance.save()
            # welcome_email.delay(first_name=instance.first_name, email=instance.email)
            # send_sms.delay(instance.phone, "Hello There, Welcome To Evolov")

            if instance.is_company and not instance.is_employee:
                from observer.utils import kw
                Company.objects.create(
                    user=instance,
                    corporation_name=kw[0]['corporation_name'],
                    corporation_id=kw[0]['corporation_id'],
                )
            

    def __str__(self):
        return f'{self.name}'


class Employee(models.Model):
    id = models.CharField(primary_key=True, unique=True, editable=False, default=get_str, max_length=40)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='main_company', null=True, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee', null=True, blank=True)
    employee_position = models.CharField(max_length=40, blank=True, null=True)
    show_employee = models.BooleanField(default=True, null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_employee_object(sender, instance, created, **kwargs):
        if created and instance.is_employee:
            from observer.utils import kw
            Employee.objects.create(
                user=instance,
                employee_position=kw[0]['employee_position'],
                company=Company.objects.get(pk=kw[0]['company_id'])
            )

    def __str__(self):
        return self.id


class Following(models.Model):
    """
    A model representing the relationship between two users or a user and a subcategory.
    
    Attributes:
        id (CharField): A unique ID for this relationship.
        follower (CharField): The ID of the user who is following.
        followed (CharField): The ID of the user or subcategory being followed.
        sub_category_name (CharField): The name of the subcategory being followed, if applicable.
        follow (GenericRelation): A generic relation to the `Activity` model representing the follow activity.

    * To add a follow:
        - Get the instance of the Ad  they want to follow: ad_instance = Ad.objects.get(pk="id_string")
        - Get the user instance of the user doing the following: user_instance = User.objects.get(pk="user_id_string")
        - Add the follow to db: Activity.objects.create(content_object=ad_instance, activity_type="Activity.FOLLOW", user=user_instance)

    * To get all the Ads a user liked: 
        - Activity.objects.filter(user="user_id_string", activity_type='FOLLOW')

    * Get all the Likes
        - ad_instance.follow.all()

    * Count the number of likes
        - ad_instance.follow.count()

    * Get the users who liked an ad
        - ad_instance.follow.values_list('user__first_name', flat=True)
    """

    id = models.CharField(primary_key=True, unique=True, editable=False, default=get_str, max_length=40)
    follower = models.CharField(max_length=40, blank=False, null=True)
    followed = models.CharField(max_length=40, blank=True, null=True)
    sub_category_name = models.CharField(max_length=40, blank=True, null=True)
    follow = GenericRelation(Activity, related_query_name='following')


class Like(models.Model):
    from product.models import Ad
    """
    * To add a like:
        - Get the instance of the Ad they like: ad_instance = Ad.objects.get(pk="id_string")
        - Get the user instance of the user doing the liking: user_instance = User.objects.get(pk="user_id_string")
        - Add the like to db: Activity.objects.create(content_object=ad_instance, activity_type="Activity.LIKE", user=user_instance)

    * To get all the Ads a user liked: 
        - Activity.objects.filter(user="user_id_string", activity_type='LIKE')

    * Get all the Likes
        - ad_instance.likes.all()

    * Count the number of likes
        - ad_instance.likes.count()

    * Get the users who liked an ad
        - ad_instance.likes.values_list('user__first_name', flat=True)
    """
    
    id = models.CharField(primary_key=True, unique=True, editable=False, default=get_str, max_length=40)
    user = models.CharField(max_length=40, blank=False, null=True)
    ad_liked = models.CharField(max_length=40, blank=False, null=True)
    likes = GenericRelation(Activity, related_query_name='liked')
