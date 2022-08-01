



from telethon.sync import TelegramClient



number = 85262550512
id_ = 15451024
hash_ = '6fb9eb2518d1bd451682c56ddc348be3'
client = TelegramClient(f'{number}',id_,hash_)

client.connect()
channel = client.get_entity('xanaofficial')
print(client.get_messages(channel)[0].date)
count_ = 0


definer_ = '''XANA has sold out its first metaverse avatar wearable NFTs by Hiroko Koshino, the world-renowned designer.**

XANA produced 10 looks and 29 items from the 2022 Spring/Summer collection by Hiroko Koshino, a top international fashion designer, into 3D wearables for XANA avatars'''
import datetime
from datetime import  timedelta, time
import datetime
import pytz

utc=pytz.UTC
for message in client.iter_messages(channel):

    # if datetime.datetime.now().day > message.date.day > datetime.datetime.now().day - datetime.timedelta(days=4).days:
    # if message.date.month < datetime.datetime.now().month:
        # print(datetime.date.today().day)
        aaa = datetime.datetime.now() - datetime.timedelta(days=4)
        if utc.localize(aaa) <  message.date:
        # if aaa.day > message.date.day > datetime.date.today().day :
            print(message.date.day)
            print(message.id)

print(datetime.datetime.now().month,':',datetime.datetime.now() - datetime.timedelta(days=4))
    # if definer_ in str(message.text):
    #     msg_id = message.id
    #     print(msg_id,'=====================')