# from asyncio import events
# from pydoc import cli
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
# from telethon.tl.
# from telethon.tl.functions.messages import rea
# from pyrogram.raw.functions.messages import GetMessageReactionsList

# number = 919978911838
# id_ = 14251965
# hash_ = '5e489dc4ddfdf6b48db7240a20d84c57'
number = 85262550512
id_ = 15451024
hash_ = '6fb9eb2518d1bd451682c56ddc348be3'
client = TelegramClient(f'./sessions/{number}',id_,f'{hash_}')
client.connect()

if client.get_me():
    print('Script is started !')
else:
    aaa= client.send_code_request(number)
    print(aaa,'**************************')
    client.sign_in(number,input('Enter the OTP: '))

from pyrogram.raw.functions.messages import send_reaction

# client(JoinChannelRequest('piyush_0012'))
# channel = client.get_entity('piyush_0012')
client(JoinChannelRequest('xana_1'))
channel = client.get_entity('xana_1')
# client._get_peer(channel)
peer_id = client.get_peer_id(channel)
print(peer_id,'=========')
# for msg in    client.iter_messages(channel):
#     print(msg.getHistory,'----------')
# print( i.id for i in client.get_messages(channel))
print(channel)


for message in client.iter_messages(channel):
    print(message.reply_markup,'----',message.id,'----', message.text)
    # print(message)


from pyrogram import Client
app = Client(
    f'sdgfsgfsg3',
    api_id=id_,
    api_hash=f'{hash_}'
)
# app.send_code(str(number))
# app.(phone_number=str(number))
# code_otp = input('Enter otp:')
# app.sign_in(phone_number=number)

# chat_id = -123456789

chat_id = 1705305623
# app.run()
print(channel.id,'------------')
# with app:
app.start()
# app.sign_in()
aaa = app.send_code(str(number))
print(aaa)
# app.send_code(str(number))
# app.send_code(str(number))
app.sign_in(phone_number=str(number),phone_code_hash=(app.send_code(str(number))['phone_code_hash']),phone_code=input('Enter code :'))

# app.sign_in(phone_number=)
# aa = app.send_reaction(peer_id,2,'🤔')
# print(aa,'********************')
# with app :
#     for message in app.iter_history(chat_id=channel.id):
#         reactions = app.send(
#             GetMessageReactionsList(
#                 peer=peer_id,
#                 id=message.message_id,
#                 limit=100
#             )
#         )


# for msg in client.iter_h(channel):
#     print(msg.reactions)


# print( client.iter_messages(channel)[0].id)
# from telethon.tl.functions.messages import 
# from telethon.tl.functions.stickers import CreateStickerSetRequest
# CreateStickerSetRequest("Patricia_a12201",title='qwerty',short_name='sdfsd',stickers=['🤔'])

# for message in client.iter_messages(channel):
#     print(message.reply_markup,'----',message.id,'----', message.text)
#     print(message)

# print('\n\n',message,'----------')
    # try:
    #     client.send_message(channel, '🔥',message.id)
    # except Exception as e:
    #     print(e)
        # client.send_message(channel, 'Great update!',reply_to=message.id)
        # print(message.getAvailableReactions)
    # print(message)

# client.send_message(channel, '🔥',comment_to=42)

# client.
# client.send_message(channel, '❤️🔥👍🏻',reply_to=24)


# print('\n\n',client.iter_messages(channel),'\n\n')
# app = client
# with app:
#     peer = app.peer(1705305623)

#     for message in app.iter_history(chat_id=4):
#         print(message.reactions)


# @events.register(events.NewMessage)
# def handler(event):
#     message_id = event.id
#     print(message_id)


# posts = client.GetHistoryRequest(
#         peer='xana_text',
#         limit=1,
#         offset_date=None,
#         offset_id=0,
#         max_id=0,
#         min_id=0,
#         add_offset=0,
#         hash=0)
# aaaa = client.send_message(channel, message='fsdhgfbdash kjbafd',reply_to=4)
# print(aaaa.id,aaaa)
# client.send_message(channel, message="❤️", comment_to=client.get_messages(channel)[-1])
# print(channel.chat)
# print(client.iter_messages(
#     channel,limit=2,reverse=True
# ))