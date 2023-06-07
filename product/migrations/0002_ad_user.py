# Generated by Django 3.2.7 on 2022-11-19 05:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='user',
            field=models.ManyToManyField(related_name='user_ads', to=settings.AUTH_USER_MODEL),
        ),
    ]