# Generated by Django 4.0.4 on 2022-05-24 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_user_details_emulator'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_avds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avdname', models.CharField(max_length=255)),
                ('port', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
