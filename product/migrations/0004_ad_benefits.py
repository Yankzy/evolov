# Generated by Django 3.2.7 on 2022-12-04 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_category_benefits'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='benefits',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]