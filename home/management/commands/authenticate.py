from collections import UserList
from pprint import pprint
from urllib.request import DataHandler
from django.core.management.base import BaseCommand
from home.models import user_details
from .functions_file.function_msg import *
import pandas as pd 

class Command(BaseCommand):
    help = 'send message as per csv'

    def handle(self,*args, **kwargs):

        count = 0
        all_user = user_details.objects.all()

        for user in all_user:
            client = TelegramClient(f'./sessions/{user.number}',user.api_id,user.api_hash)
            client.connect()
            chat2 = client.get_dialogs()
            # chat2 = client.get_entity('Telegram')
            # chat2 = client.get_messages(chat2)
            # chat2 = client.iter_messages('Telegram')
            # for i in chat2:
                # print(i)
            print(chat2)
            client.disconnect()
            input('Enter :')
