# Generated by Django 4.0.4 on 2022-06-01 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_user_details_comment_user_details_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_details',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='views',
        ),
    ]
