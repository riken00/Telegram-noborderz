from cgi import print_directory
from itertools import count
from telethon.sync import TelegramClient



number = 85262550512
id_ = 15451024
hash_ = '6fb9eb2518d1bd451682c56ddc348be3'
client = TelegramClient(f'{number}',id_,hash_)
# # client = TelegramClient(f'./sessions/{number}',id_,hash_)
client.connect()
channel = client.get_entity('xanaofficial')
print(client.get_messages(channel))
count_ = 0
# print(client.iter_messages(channel))
definer_ = '''XANA has sold out its first metaverse avatar wearable NFTs by Hiroko Koshino, the world-renowned designer.**

XANA produced 10 looks and 29 items from the 2022 Spring/Summer collection by Hiroko Koshino, a top international fashion designer, into 3D wearables for XANA avatars'''
for message in client.iter_messages(channel):
    # print(message.reply_markup,'----',message.id,'----', message.text,)
    if definer_ in str(message.text):
        msg_id = message.id
        print(msg_id,'=====================')
        break

    
    # if count_ > 100:break
    # count_ += 1
    # break
    # print(message)