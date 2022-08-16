from cgi import print_directory
from itertools import count
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from telethon import TelegramClient
from home.management.commands.functions_file.function_msg import engagement, engagement_msg_id
from home.models import Engagements, user_details
from main import LOGGER
import random, os

reaction_list = ["❤️","👍","🔥"]
definer_ = '''XANA has sold out its first metaverse avatar wearable NFTs by Hiroko Koshino, the world-renowned designer.

XANA produced 10 looks and 29 items from the 2022 Spring/Summer collection by Hiroko Koshino, a top international fashion designer, into 3D wearables for XANA avatars. 

The limited edition of 500 NFT sold out in just 45 minutes upon sale.

Through this project, XANA has fully demonstrated to the market the potential of the new "digital fashion" field, a fusion of the fashion industry and the Metaverse.

XANA will continue to actively collaborate with the world's top brands and outstanding independent designers to bring new business opportunities to the fashion industry.'''
# definer_ = '''XANA has sold out its first metaverse avatar wearable NFTs by Hiroko Koshino, the world-renowned designer.**

# XANA produced 10 looks and 29 items from the 2022 Spring/Summer collection by Hiroko Koshino, a top international fashion designer, into 3D wearables for XANA avatars'''
class Command(BaseCommand):
    help = 'For engagement'
    def handle(self, *args, **kwargs):

        all_active_user = list(user_details.objects.filter(status="ACTIVE").order_by('?'))
        # ENGAGEMENT_COUNT = 100
        # AGENT_USER = 'xanaofficial'
        # AGENT_USER = 'xana_1234'

        # for get the message id
        # test_user = all_active_user[0]

        # AGENT_USER = 'qatestingxana'
        AGENT_USER = 'piyush_0012'
        AGENT_USER = 'xanaofficial'
        # AGENT_USER = 'xana_text'
        # AGENT_USER = str(os.getenv('AGENT_USER',''))
        # ENGAGEMENT_COUNT = int(os.getenv('ENGAGEMENT_COUNT',''))
        ENGAGEMENT_COUNT = 1000
        print(ENGAGEMENT_COUNT,'================')
        active_user_count = len(all_active_user)
        if active_user_count < ENGAGEMENT_COUNT:
            ENGAGEMENT_COUNT = active_user_count
            LOGGER.error(f'There is not sufficient user in Database and there are only {active_user_count}, Thus only these user will do the engagement')
            # return
        # if user_details.objects.filter(status="")


        message_id = engagement_msg_id(groupname=AGENT_USER,all_message = True)
        print(message_id)
        count_ = 0
        if message_id:
            # for i in range(ENGAGEMENT_COUNT):
            for i in range(len(all_active_user)):
                user = all_active_user.pop(0)
                count_ += 1
                # print(user)
                # for id in message_id:
                # if not Engagements.objects.filter(user = user,engagement_on = AGENT_USER,message_on = int(id)).exists():
                    
                engagement(random_=2,groupname=AGENT_USER,Message_id=message_id,number=user.number,apiid=user.api_id,apihash=user.api_hash)
                # break
        else:   
            LOGGER.info('We could not find the message of which we are looking for to do engagement.')
        print('\n\n\n\n-----------',count_)
        
        ...

# error -------------

# [WDM] - ====== WebDriver manager ======
# [WDM] - Current google-chrome version is 102.0.5005
# [WDM] - Get LATEST chromedriver version for 102.0.5005 google-chrome
# [WDM] - Driver [/home/eu4/.wdm/drivers/chromedriver/linux64/102.0.5005.61/chromedriver] found in cache
# 2022-06-23 11:33:22,169  function_msg.py  main   INFO     Message: timeout: Timed out receiving message from renderer: -302.901
#   (Session info: chrome=102.0.5005.61)