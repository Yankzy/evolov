from django.db import models
from users.models import get_str, Activity
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings


class Category(models.Model):
    id = models.CharField(primary_key=True, unique=True, editable=False, default=get_str, max_length=40)
    category_name = models.CharField(max_length=40, blank=True, null=False)
    facilities = models.JSONField(default=dict, null=True, blank=True)
    nearby = models.JSONField(default=dict, null=True, blank=True)
    details = models.JSONField(default=dict, null=True, blank=True)
    features = models.JSONField(default=dict, null=True, blank=True)
    benefits = models.JSONField(default=dict, null=True, blank=True)
    positions = models.JSONField(default=dict, null=True, blank=True)


    def __str__(self):
        return self.category_name
        

class SubCategory(models.Model):
    id = models.CharField(primary_key=True, unique=True, editable=False, default=get_str, max_length=40)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    sub_category_name = models.CharField(max_length=40, blank=True, null=True)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.sub_category_name


class Ad(models.Model): 

    status_choices = (
        ('ACTIVE', 'Active'),
        ('DELETED', 'Deleted'),
        ('SOLD', 'Sold'),
        ('REVIEW', 'Review'),
        ('UNPUBLISHED', 'Unpublished'),
    )
    
    id = models.CharField(primary_key=True, unique=True, editable=False, default=get_str, max_length=40)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_ads", blank=False)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, related_name="sub_category", blank=False, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    status = models.CharField(max_length=25, choices=status_choices, default='ACTIVE')
    published_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    facilities = models.JSONField(default=dict, null=True, blank=True)
    nearby = models.JSONField(default=dict, null=True, blank=True)
    details = models.JSONField(default=dict, null=True, blank=True)
    features = models.JSONField(default=dict, null=True, blank=True)
    benefits = models.JSONField(default=dict, null=True, blank=True)
    positions = models.JSONField(default=dict, null=True, blank=True)
    statistics = models.JSONField(default=dict, null=True, blank=True)
    likes = GenericRelation(Activity)

    stripe_product_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        ordering = ('published_date', )


    def __str__(self):
        return str(self.sub_category)


class Resume(models.Model): 
    status_choices = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('REVIEW', 'Review'),
    )
    id = models.CharField(primary_key=True, unique=True, editable=False, default=get_str, max_length=40)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resume", null=True, blank=False)
    status = models.CharField(max_length=25, choices=status_choices, default='ACTIVE')
    published_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    personal_information = models.JSONField(default=dict, null=True, blank=True)
    work_experience = models.JSONField(default=dict, null=True, blank=True)
    skills = models.JSONField(default=dict, null=True, blank=True)
    languages = models.JSONField(default=dict, null=True, blank=True)
    education = models.JSONField(default=dict, null=True, blank=True)
    documents = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        ordering = ('last_updated', )
        get_latest_by = 'last_updated'


    def __str__(self):
        return str(self.user)
    
    @classmethod
    def get_fields(cls, user=None):
        return 'id', 'user', 'published_data', 'last_updated', 'personal_information', 'work_experience', 'skills', 'languages', 'education'




class ImageUrl(models.Model):
    id = models.CharField(primary_key=True, unique=True, editable=False, default=get_str, max_length=40)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    category_image = models.CharField(max_length=250, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    sub_category_image = models.CharField(max_length=250, null=True, blank=True)
    ad = models.ForeignKey(Ad, on_delete=models.SET_NULL, null=True)
    gallery = models.JSONField(default=dict, null=True, blank=True)
