# Generated by Django 3.2.7 on 2022-12-16 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20221205_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('SOLD', 'Sold'), ('REVIEW', 'Review')], default='ACTIVE', max_length=25),
        ),
    ]
