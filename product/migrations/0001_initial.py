# Generated by Django 3.2.7 on 2022-11-19 05:15

from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.CharField(default=users.models.get_str, editable=False, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('SOLD', 'Sold'), ('REVIEW', 'Review')], default='ACTIVE', max_length=25)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('facilities', models.JSONField(blank=True, default=dict, null=True)),
                ('nearby', models.JSONField(blank=True, default=dict, null=True)),
                ('details', models.JSONField(blank=True, default=dict, null=True)),
                ('features', models.JSONField(blank=True, default=dict, null=True)),
                ('stripe_product_id', models.CharField(blank=True, max_length=255, null=True)),
                ('stripe_price_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ('published_date',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.CharField(default=users.models.get_str, editable=False, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('category_name', models.CharField(blank=True, max_length=40)),
                ('facilities', models.JSONField(blank=True, default=dict, null=True)),
                ('nearby', models.JSONField(blank=True, default=dict, null=True)),
                ('details', models.JSONField(blank=True, default=dict, null=True)),
                ('features', models.JSONField(blank=True, default=dict, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.CharField(default=users.models.get_str, editable=False, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('sub_category_name', models.CharField(blank=True, max_length=40, null=True)),
                ('price', models.IntegerField(default=0)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='ImageUrl',
            fields=[
                ('id', models.CharField(default=users.models.get_str, editable=False, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('category_image', models.CharField(blank=True, max_length=250, null=True)),
                ('sub_category_image', models.CharField(blank=True, max_length=250, null=True)),
                ('ad_gallery', models.JSONField(blank=True, default=dict, null=True)),
                ('ad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.ad')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category')),
                ('sub_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.subcategory')),
            ],
        ),
        migrations.AddField(
            model_name='ad',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_category', to='product.subcategory'),
        ),
    ]
