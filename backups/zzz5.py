from telethon.sync import TelegramClient
number = 85262550512
id_ = 15451024
hash_ = '6fb9eb2518d1bd451682c56ddc348be3'

client = TelegramClient(f'./sessions/{number}',id_,hash_)


client.connect()
for msg in client.iter_messages('xanaofficial'):
    print(msg.id)
    
client.disconnect()