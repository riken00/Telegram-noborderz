



import click
from telethon.sync import TelegramClient
number = 85262550512
id_ = 15451024
hash_ = '6fb9eb2518d1bd451682c56ddc348be3'

client = TelegramClient(f'./sessions/{number}',id_,hash_)

client.connect()
client.get_me()
client.send_message(client.get_entity('xanaofficial'),message='v.good',comment_to=269)
client.disconnect()


number = 85262550512
id_ = 15451024
hash_ = '6fb9eb2518d1bd451682c56ddc348be3'
from pyrogram import Client
app = Client(
    f'{number}_p',
    api_id=id_,
    api_hash=f'{hash_}',
    phone_number=str(number),
    )

app.connect()
# app.start()

abc = app.get_messages('xanaofficial',269)
app.cansen
print(abc.sender_chat)
# aaa = app.send_reaction('xanaofficial',269,'👍')
# aaa = app.send_comment(
#     'xanaofficial',269,'👍'
# )
# print(aaa)
# with app:print(app.get_me())
app.disconnect()