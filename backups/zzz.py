# from asyncio import events
# from pydoc import cli
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
# from telethon.tl.functions.
# from telethon.tl.
# from telethon.tl.functions.messages import rea
# from pyrogram.raw.functions.messages import setChatAvailableReactions#

# number = 919978911838
# id_ = 14251965
# hash_ = '5e489dc4ddfdf6b48db7240a20d84c57'
# number = 85262550512
# id_ = 15451024
# hash_ = '6fb9eb2518d1bd451682c56ddc348be3'
# client = TelegramClient(f'./sessions/{number}',id_,f'{hash_}')
number = 85260353503
id_ = 11066996	
hash_ = '9695c347d1f1dc652df716d5df325e42'
client = TelegramClient(f'{number}',id_,hash_)
# client = TelegramClient(f'./sessions/{number}',id_,hash_)
client.connect()



if client.get_me():
    print('Script is started !')
else:
    phone_code_hash= client.send_code_request(number).phone_code_hash
    # print(phone_code_hash,'***************************')
    client.sign_in(number,input('Enter the OTP: '))
channel = client.get_entity('xana_1')
client(JoinChannelRequest(channel))

Telegram = client.get_entity('telegram')
# print(Telegram,'======================')
# print(client.get_dialogs()[0].message)
telegram_msg = client.get_dialogs()[0].message
print(str(telegram_msg.text).replace('**Login code:**','').split(' ')[1].replace('.',''))
try:
    otp__ = str(telegram_msg.text).replace('**Login code:**','').split(' ')[1].replace('.','')
except Exception as e:otp__=''
# for i in telegram_msg:
#     print()
# for message in client.get_messages:
#     print(message.reply_markup,'----',message.id,'----', message.text)
#     break
#     
from pyrogram import Client
app = Client(
    f'sdgfsgfsg3aqa',
    api_id=id_,
    api_hash=f'{hash_}',
    phone_number=str(number),
    

)
# count = 0
# for message in client.iter_messages('Telegram'):
#     if count > 5:
#         break
#     else:
#         count += 1
#     print(message.reply_markup,'----',message.id,'----', message.text)
    

# if otp__:
#     phone_code_hash= client.send_code_request(number).phone_code_hash


app.connect()
# aa = app.send_code()
# print(aa)
print(app.get_me())
# with app:app.sign_in(phone_number=str(number),phone_code_hash=phone_code_hash,phone_code=otp__)


