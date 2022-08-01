import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from telethon import TelegramClient
from home.models import User_avds, user_details
from home.bot import Telegram_bot
import time

from home.conf import COUNTRY


class Command(BaseCommand):
    help = 'Create random users'


        # parser.add_argument('emulator', type=str, help='emulator of New user')

    def handle(self, *args, **kwargs):
        while True:
            try:
                ports = list(
                            filter(
                                lambda y: not User_avds.objects.filter(port=y).exists(),
                                map(
                                    lambda x: 5550 + x, range(1, 5000)
                                )
                            )
                        )
                devices = list(
                    filter(
                        lambda y: not User_avds.objects.filter(avdname=y).exists(),
                        map(
                            lambda x: f"telegram_{x}", range(1, 5000)
                        )
                    )
                )

                emulator = random.choice(devices)
                port = random.choice(ports)
                aa = User_avds.objects.create(
                    avdname=emulator,
                    port=port,
                )
                
                tg = Telegram_bot(aa.avdname)
                tg.start_driver()
                tg.check_apk_installation()
                # tg.connect_to_vpn(country=COUNTRY)
                breakpoint()
                tg.create_account()

            except Exception as e:
                print(e)
            finally:
                tg.kill_bot_process(True, True)
