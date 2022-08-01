import asyncio
import sys
# from django.forms import Input
from telethon.sync import TelegramClient
number = 85262550512
# number = +85262517703
id_ = 15451024
hash_ = '6fb9eb2518d1bd451682c56ddc348be3'
tclient = TelegramClient(f'./sessions/{number}',id_,hash_)
# phone = input('phone ; ')
# if not tclient.is_user_authorized():
#     y = tclient.send_code_request(number)
# # tclient = TelegramClient(f'./sessions/{number}',api_id,api_hash)
# if tclient.start(phone=number,code_callback=int(input('Otp :'))):
#     # user_details.objects.create(number=number,api_id=api_id,api_hash=api_hash,username='Rrfgju',emulator='-')
#     print('User Exists in database ')
# else:
#     print('Please Enter Valid Credentials or OTP !')

number = 85262550512
id_ = 15451024
hash_ = '6fb9eb2518d1bd451682c56ddc348be3'
client = TelegramClient(f'./sessions/{number}',id_,f'{hash_}')
client.connect()

if client.get_me():
    print('Yessss')
else:
    client.send_code_request()
    client.sign_in(number,input('Enter the OTP: '))