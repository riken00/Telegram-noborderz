from email import message
from django.db import models
import random, subprocess

from home.conf import AVD_DEVICES,AVD_PACKAGES
from utils import LOGGER
# Create your models here.

class user_details(models.Model):
    STATUS = (
        ("ACTIVE", "ACTIVE"),
        ("NOT AUTHORIZED", "NOT AUTHORIZED"),
        ("FLOOD WAIT","FLOOD WAIT"),
        ("BANNED","BANNED"),
        ("DELETED","DELETED"),
        ("NEED PASSWORD","NEED PASSWORD"),
    )
    emulator = models.CharField(max_length=255)
    number = models.IntegerField()
    comment = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    api_id = models.CharField(max_length=255)
    api_hash = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    reaction = models.IntegerField(default=0)
    status = models.CharField(max_length=255,choices=STATUS,default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self) :
        return str(self.number)

class comment_view(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    comment = models.TextField(default='-')
    views = models.IntegerField(default=0)
    comment_on = models.CharField(default='-',max_length=255)
    view_on = models.CharField(default='-',max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

class comments(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    comment = models.TextField(default='-')
    comment_on = models.CharField(default='-',max_length=255)
    message_on = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

class view(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    views_on = models.CharField(default='-',max_length=255)
    # message_on = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

class Engagements(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    reaction = models.CharField(default='-',max_length=255)
    engagement_on = models.CharField(default='-',max_length=255)
    message_on = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

class inactive_user(models.Model):
    STATUS = (
        ("NOT AUTHORIZED", "NOT AUTHORIZED"),
        ("FLOOD WAIT","FLOOD WAIT"),
        ("BANNED","BANNED"),
        ("DELETED","DELETED"),
        ("NEED PASSWORD","NEED PASSWORD"),
    )
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    status = models.CharField(max_length=255,choices=STATUS,default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    
    def __str__(self) :
        return str(self.user)

class User_avds(models.Model):
    avdname = models.CharField(max_length=255)
    port = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True,null=True,blank=True)
    # created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)


    def __str__(self) -> str:
        return str(f'{self.avdname} : {self.port}')


from django.db.models.signals import post_save, pre_delete

def create_better_avd(sender, instance, **kwargs):
    created = kwargs.get('created')

    if created:
        LOGGER.info('Start to create AVD')
        try:
            from home.bot import Telegram_bot
            telegram_bot = Telegram_bot(instance.avdname, start_appium=False, start_adb=False)

            device = random.choice(AVD_DEVICES)  # get a random device
            package = random.choice(AVD_PACKAGES)  # get a random package
            telegram_bot.create_avd(avd_name=instance.avdname, package=package,
                             device=device)

            LOGGER.info(f"**** AVD created with name: {instance.avdname} and port: {instance.port} ****")

        except Exception as e:
            instance.delete()
            LOGGER.error(f"Couldn't create avd due to the following error \n")
            LOGGER.error(e)
            print('Start to create AVD')


def delete_avd(sender, instance, **kwargs):
    try:
        LOGGER.info(f'Deleting the avd named {instance.avdname}')
        cmd = f'avdmanager delete avd --name {instance.avdname}'
        p = subprocess.Popen([cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL)
    except Exception as e:
        pass


post_save.connect(create_better_avd, sender=User_avds)
pre_delete.connect(delete_avd, sender=User_avds)