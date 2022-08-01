# Generated by Django 4.0.4 on 2022-05-30 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_user_avds'),
    ]

    operations = [
        migrations.CreateModel(
            name='inactive_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.user_details')),
            ],
        ),
    ]
