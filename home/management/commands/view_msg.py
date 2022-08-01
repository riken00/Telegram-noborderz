from django.core.management.base import BaseCommand
from home.models import user_details
from .functions_file.function_msg import *

class Command(BaseCommand):
    help = 'run in order to join'

    def add_arguments(self, parser):
        parser.add_argument('group',type=str,help = 'Group name')
    def handle(self,*args, **kwargs):
        group = kwargs['group']
        while True:
            for i in user_details.objects.all():
                number = i.number
                api_id = i.api_id
                api_hash = i.api_hash 
                client = TelegramClient(f'./sessions/{number}',api_id,api_hash)

                banned = user_banned(client,number,api_id,api_hash) 
                if banned:
                    print('yes !',banned)
                else :
                    print('no !',banned)
                    view_chat(group,client,number)
                    