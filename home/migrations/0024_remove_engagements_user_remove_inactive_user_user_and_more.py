# Generated by Django 4.0.4 on 2022-06-14 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_inactive_user_engagements_comment_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engagements',
            name='user',
        ),
        migrations.RemoveField(
            model_name='inactive_user',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='reaction',
        ),
        migrations.DeleteModel(
            name='comment_view',
        ),
        migrations.DeleteModel(
            name='Engagements',
        ),
        migrations.DeleteModel(
            name='inactive_user',
        ),
    ]