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
        user = user_details.objects.all()
        for i in user:
            number = i.number
            api_id = i.api_id
            api_hash = i.api_hash
            # number = i.number
            dub = user_details.objects.filter(number = number)
            print('yess',len(dub),dub)
            # if len(dub) > 1:
            #     print('yess',len(dub),dub)
            #     list(user_details.objects.filter(number = number))[-1].delete()

            # tclient = TelegramClient(f'./sessions/{number}',api_id,api_hash)
            # try:
            #     if tclient.start(phone=number):
            #         print('User is already Exists in Database !')
            #         user_details.objects.create(number=number,api_id=api_id,api_hash=api_hash,username='-',emulator='-')
            #     else:print('User Exists in database ')
            # except Exception as e:
            #     i.delete()
            #     print(e)


        # csv_li= [
            
        #     '/media/eu4/49fa581d-6d91-4c0f-886a-2d6d1a2b9857/project/Automation/telegram_avds/office-work/account_csv/Himanshu_Telegram_AC_CSV.csv'
        #     ]

        # for csv in csv_li:
        #     datafram = pd.read_csv(csv)
        #     for data in range(len(datafram)):
        #         number = datafram['number'][data]
        #         apiid =  datafram['app_id'][data]
        #         apihash = datafram['api_hash'][data]
        #         username = datafram['username'][data]
        #         avdname = datafram['emulator'][data]
                
        #         if user_details.objects.filter(number=number).exists():
        #             print('User is already Exists in Database !')
        #         else :
                    
        #             tclient = TelegramClient(f'./sessions/{number}',apiid,apihash)
        #             print(number)
        #             # aa = tclient.connect()
        #             # b = tclient.get_me()
        #             # print(b)
        #             # if not tclient.is_user_authorized():

        #             #     tclient.send_code_request(number)
                        
        #             #     # signing in the client
        #             #     tclient.sign_in(number, input('Enter the code: '))

        #             # print(aa.)
        #             try:
        #                 if tclient.start(phone=number):
        #                     user_details.objects.create(number=number,api_id=apiid,api_hash=apihash,username=username,emulator=avdname)

        #                     print('User Exists in database ')
        #                 else:
        #                     print('Please Enter Valid Credentials or OTP !')
        #             except Exception as e:
        #                 print(e)