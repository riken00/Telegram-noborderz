from collections import UserList
from pprint import pprint
from urllib.request import DataHandler
from django.core.management.base import BaseCommand
from home.models import user_details
from .functions_file.function_msg import *
import pandas as pd 

class Command(BaseCommand):
    help = 'send message as per csv'

    def add_arguments(self, parser):
        parser.add_argument('group',type=str,help = 'Group name')
    
    def handle(self,*args, **kwargs):
        group = kwargs['group']
        data = user_details.objects.all()
        data = [[i.number,i.api_id,i.api_hash] for i in data]
        data_length = len(data)
        chat = pd.read_csv('chat.csv')
        username = chat['Username']
        conversation = chat['Dialogue']
        chat_zip = zip(username,conversation)
        user_count = 0
        dict = {}
        banned = False
        username_list = []
        banned = False

        for i in username:
            if not isinstance(i,float):
                i = i.replace(' ','')
                if i != '':
                    if not i in username_list:
                        username_list.append(i)
        if data_length < len(username_list):
            print(data_length,username_list)
            print('There is not enough user in Data base as required users to start this chat')
        else:
            for i in username_list:
                if not i in dict :
                    user_cred = True
                    while user_cred == True:
                        banned = user_banned(data[user_count][0],data[user_count][1],data[user_count][2])
                        if data_length <= user_count:
                            print('not enough user')
                            user_cred = False
                        else:
                            if not banned:
                                dict [i] = {
                                    'number' : data[user_count][0],
                                    'apiid' : data[user_count][1],
                                    'apihash' : data[user_count][2]
                                }
                                user_cred = False
                            user_count +=1
            pprint(dict)
            if len(username_list) > len(dict):
                print('There is not enough users in database to send messages')
            else:   
                for i,ia in chat_zip:
                    if isinstance(i,str):
                        i = i.replace(' ','')
                        if not i in dict:
                            dict [i] = {
                                'number' : data[user_count][0],
                                'apiid' : data[user_count][1],
                                'apihash' : data[user_count][2]
                            }
                            user_count +=1
                        number = dict[i]['number']
                        id  = dict[i]['apiid']
                        hash = dict[i]['apihash'] 
                        if number and id and hash:
                            banned = user_banned(number,id,hash)
                            if banned:
                                dict[i] = {
                                    'number' : data[user_count][0],
                                    'apiid' : data[user_count][1],
                                    'apihash' : data[user_count][2]
                                }
                                user_count +=1
                            banned = False
                        
                        complete_process = False
                        while not complete_process:
                                         
                            number = dict[i]['number']
                            id  = dict[i]['apiid']
                            hash = dict[i]['apihash'] 
                            complete,temp_banned = script_chat(i,number,id,hash,ia,group)
                            if complete:
                                complete_process = True
                            if (not complete) and (temp_banned == True):
                                if user_count >= data_length:
                                    print('There is not enough Users replace user in DATABASE ! ')
                                    complete_process = True
                                    return print('Please add enough Users in DATABASE According to Required Users')  
                                dict [i] = {
                                    'number' : data[user_count][0],
                                    'apiid' : data[user_count][1],
                                    'apihash' : data[user_count][2]
                                }
                                user_count +=1
                            
