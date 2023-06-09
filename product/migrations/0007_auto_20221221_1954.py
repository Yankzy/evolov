# Generated by Django 3.2.7 on 2022-12-21 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0006_alter_ad_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imageurl',
            old_name='ad_gallery',
            new_name='gallery',
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.CharField(default=users.models.get_str, editable=False, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('REVIEW', 'Review')], default='ACTIVE', max_length=25)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('personal_information', models.JSONField(blank=True, default=dict, null=True)),
                ('work_experience', models.JSONField(blank=True, default=dict, null=True)),
                ('skills', models.JSONField(blank=True, default=dict, null=True)),
                ('languages', models.JSONField(blank=True, default=dict, null=True)),
                ('education', models.JSONField(blank=True, default=dict, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resume', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('published_date',),
            },
        ),
    ]
