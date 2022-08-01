from django.core.management.base import BaseCommand
from home.models import user_details
from .functions_file.function_msg import *

class Command(BaseCommand):
    help = 'run in order to join'

    def add_arguments(self, parser):
        parser.add_argument('view_group',type=str,help = 'view Group name')
        parser.add_argument('group',type=str,help = 'Group name')
        parser.add_argument('msg',type=str,help = 'Message')
    def handle(self,*args, **kwargs):
        msg = kwargs['msg']
        group = kwargs['group']
        view_group = kwargs['view_group']

        while True:
            data = user_details.objects.all()
            for i in data:
                number = i.number
                api_id = i.api_id
                api_hash = i.api_hash
                banned = user_banned(number,api_id,api_hash) 
                if banned == False:
                    send_messages(view_group,group,msg,number,api_id,api_hash)
                    time.sleep(random.randint(3,6))
            print('Time is sleep for some secounds')
            time.sleep(random.randint(6,12))
                    