from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from telethon import TelegramClient
from home.models import User_avds, user_details

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        User_avds.objects.all().delete()