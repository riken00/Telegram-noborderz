# Generated by Django 4.0.4 on 2022-06-17 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_inactive_user_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='inactive_user',
        ),
    ]
