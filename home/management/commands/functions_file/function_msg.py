from distutils.log import error
from email import message
import time
import random
from requests import request
from telethon import TelegramClient
from telethon.sync import TelegramClient
from home.driver.driver import get_driver
from home.models import Engagements, comment_view, inactive_user, user_details, view
import telethon,os
from telethon import errors
from telethon.tl.functions.channels import JoinChannelRequest
from pyrogram import Client
from pyrogram import errors as p_errors
from main import LOGGER
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from utils import random_sleep


def add_group(view_group,groupname,Message,number,apiid,apihash):
    try:
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        user = user_details.objects.filter(number=number).first()
        client.connect()
        if client.is_user_authorized():
            me = client.get_me()
            client(JoinChannelRequest(groupname))
            time.sleep(0.3)
            entity = client.get_entity(view_group)
            if client.send_read_acknowledge(entity):
                view.objects.create(
                    user = user,   views_on= groupname
                )
                user.views += 1
                LOGGER.info(f"{me.first_name} {number} have Marked as seen in {view_group}'s chat")
            else : 
                LOGGER.info(f"{me.first_name} {number} have No new messages in {view_group}'s chat")
            # if client.send_message(groupname,Message):
            #     user.comment += 1
            #     LOGGER.info(f'+{number} {me.first_name} has sent a message in {groupname}')
            # else:
            #     LOGGER.info(f"+{number} {me.first_name} couldn't sent Message in {groupname}")
            # time.sleep(random.randint(60, 70))
            # user.save()
        else:
            user.status = "NOT AUTHORIZED"
            user.save()
            LOGGER.info(f'{number} is not authorized So please authorized it')    
        client.disconnect()
    except Exception as e :
        client.disconnect()
        LOGGER.info(e)

def send_messages(view_group,groupname,Message,number,apiid,apihash):
    try:
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        user = user_details.objects.filter(number=number).first()
        view_counts = comment_view.objects.create(user=user,comment_on=groupname,view_on=view_group)
        client.connect()
        if client.is_user_authorized():
            me = client.get_me()
            client(JoinChannelRequest(groupname))
            entity = client.get_entity(view_group)
            if client.send_read_acknowledge(entity):
                user.views += 1
                view_counts.views += 1
                user.save()
                view_counts.save()
                view.objects.create(
                    user = user,   views_on= groupname
                )
                LOGGER.info(f"{me.first_name} {number} have Marked as seen in {view_group}'s chat")
            else : 
                LOGGER.info(f"{me.first_name} {number} have No new messages in {view_group}'s chat")
            if client.send_message(groupname,Message):
                user.comment += 1
                view_counts.comment = Message
                user.save()
                view_counts.save()
                LOGGER.info(f'+{number} {me.first_name} has sent a message in {groupname}')
            else:
                LOGGER.info(f"+{number} {me.first_name} couldn't sent Message in {groupname}")
            time.sleep(0.2)
            # time.sleep(random.randint(60, 70))
        else:
            user.status = "NOT AUTHORIZED"
            user.save()
            LOGGER.info(f'{number} is not authorized So please authorized it')    
        client.disconnect()
    except errors.FloodWaitError as e:
        user.status = "TEMP BANNED"
        user.save()
    except errors.UserBannedInChannelError as e:
        user.status = "BANNED"
        user.save()

    except Exception as e :
        client.disconnect()
        LOGGER.info(e)

    

def view_chat(groupname,number,apiid,apihash):
    try:
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        client.connect()
        user = user_details.objects.filter(number=number).first()
        if client.is_user_authorized():
            me = client.get_me()
            client(JoinChannelRequest(groupname))
            entity = client.get_entity(groupname)
            if client.send_read_acknowledge(entity):
                view.objects.create(
                    user = user,   views_on= groupname
                )
                LOGGER.info(f"{me.first_name} {number} have Marked as seen in {groupname}'s chat")
            else : 
                LOGGER.info(f"{me.first_name} {number} have No new messages in {groupname}'s chat")
        else:
            user.status = "NOT AUTHORIZED"
            user.save()
            LOGGER.info(f'{number} is not authorized So please authorized it')    
        # time.sleep(random.randint(3,5))
        time.sleep(0.5)
        client.disconnect()
    except Exception as e :
        client.disconnect()
        LOGGER.info(e)

def user_banned(number,apiid,apihash):
    try:
        banned = False
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_(phone=number)
                client.sign_in(code=(input(f'Please Enter the OTP of {number} : ')))
                client.disconnect()
                return banned
            except telethon.errors.rpcerrorlist.PhoneNumberBannedError:
                LOGGER.info(f'Phone number {number} is banned !')
                if os.path.exists(f'./sessions/{number}.session'):
                    banned = True
                    os.remove(f'./sessions/{number}.session')
                    user_details.objects.filter(number=number).delete()
                LOGGER.info(f'{number} is deleted from DATABASE')
                banned = True
                client.disconnect()
                return banned
        else: 

            client.disconnect()
            return banned
    except Exception as e :
        client.disconnect()
        LOGGER.info(e)


def script_chat(i,number,id,hash,msg,group):
    if str(msg) == "nan" :
        return True, False

    try:
        complete = False 
        temp_banned = False
        try:
            client = TelegramClient(f'./sessions/{number}',id,hash)
            client.connect()
            # client(JoinChannel(group))
            # entity = client.get_entity(group)
            # client.send_message(entity,msg)
            f_name = client.get_me().first_name
            LOGGER.info(f"{number} : {f_name} --- sent a message {msg}")
            time.sleep(random.randint(0,1))
            # time.sleep(random.randint(60,70))
            client.disconnect()
            complete = True
            return complete,temp_banned
        except errors.FloodWaitError as e:
            client.disconnect()
            LOGGER.info(f'{number} can not send message till',e.seconds,'secounds') 
            temp_banned = True
            return complete,temp_banned
    except Exception as err :
        LOGGER.info(err)   
        return complete,temp_banned



def pyrogram_authorization(number,apiid,apihash,client_=''):
    user = user_details.objects.filter(number=number).first()
    client_ = TelegramClient(f'./sessions/{number}',apiid,apihash)
    try:
        client_.connect()
        app = Client(f'./sessions/{number}_p',api_id=f"{apiid}",api_hash=f"{apihash}",phone_number=str(number))
        app.connect()
        is_authorized = False
        try:is_authorized = True if app.get_me() else False
        except Exception as e:...

        if is_authorized:...
        else:
            sent_code = app.send_code(phone_number=str(number))
            phone_code_hash_ = sent_code.phone_code_hash
            time.sleep(4)
            telegram_msg = client_.get_dialogs()[0].message
            try:otp__ = str(telegram_msg.text).replace('**Login code:**','').split(' ')[1].replace('.','')
            except Exception as e:otp__=''
            app.sign_in(phone_number=str(number),phone_code_hash=phone_code_hash_,phone_code=f"{otp__}")
        
        app.disconnect()
        client_.disconnect()
    except p_errors.SessionPasswordNeeded as e:
        user.status = 'NEED PASSWORD'
        user.save()
    except p_errors.PhoneNumberBanned as e:
        user.status = 'BANNED'
        user.save()
    except p_errors.AuthKeyUnregistered as e:
        user.status = 'BANNED'
        user.save()
    except Exception as e:LOGGER.info(e)

from datetime import  timedelta, time
import datetime
import pytz

def engagement_msg_id(groupname,all_message = False):
    
    
    last_few_days= datetime.datetime.now() - datetime.timedelta(days=2)
    msg_id = 0
    utc=pytz.UTC
    msg_id_li = []
    for i in range(15):
        if msg_id_li: return msg_id_li
        
        user = user_details.objects.filter(status="ACTIVE").order_by('?').first()
        try:
            client = TelegramClient(f'./sessions/{user.number}',user.api_id,user.api_hash)
            client.connect()
            if client.is_user_authorized():
                me = client.get_me()
                client(JoinChannelRequest(groupname))
                message_count = 0
                msg_id_li = [ message.id for message in client.iter_messages(groupname) ] if all_message == True else [ message.id for message in client.iter_messages(groupname) if utc.localize(last_few_days) <  message.date ]
                # for message in client.iter_messages(groupname):
                #     if utc.localize(last_few_days) <  message.date:
                #         msg_id = message.id
                #         msg_id_li.append(msg_id)

                    # if message_count > 50 : break
                    # message_count += 1

            else:
                LOGGER.info(f'{user.number} is not authorized So please authorized it engagement msg id')    
                user.status = "NOT AUTHORIZED"
                user.save()
                
        except p_errors.SessionPasswordNeeded as e:

            LOGGER.error(f'there {user.number} is SessionPasswordNeeded error')
            if not inactive_user.objects.filter(user=user).exists():
                inactive_user.objects.create(
                    user = user,
                    status = 'NEED PASSWORD'
                )
            user.status = 'NEED PASSWORD'
            user.save()
        except p_errors.PhoneNumberBanned as e:
            LOGGER.error(f'there {user.number} is PhoneNumberBanned error')
            if not inactive_user.objects.filter(user=user).exists():
                inactive_user.objects.create(
                    user = user,
                    status = 'BANNED'
                )
            user.status = 'BANNED'
            user.save()
        except p_errors.AuthKeyUnregistered as e:
            LOGGER.error(f'there {user.number} is AuthKeyUnregistered error')
            if not inactive_user.objects.filter(user=user).exists():
                inactive_user.objects.create(
                    user = user,
                    status = 'NOT AUTHORIZED'
                )
            user.status = 'NOT AUTHORIZED'
            user.save()
        except errors.AuthBytesInvalidError as e:
            LOGGER.error(f'there {user.number} is AuthBytesInvalidError error')
        except errors.FloodWaitError as e:
            LOGGER.error(f'there {user.number} is FloodWaitError error')
            if not inactive_user.objects.filter(user=user).exists():
                inactive_user.objects.create(
                    user = user,
                    status = "TEMP BANNED"
                )
            user.status = "TEMP BANNED"
            user.save()
        except errors.UserBannedInChannelError as e:
            LOGGER.error(f'there {user.number} is UserBannedInChannelError error')

            LOGGER.error('This user is banned from the channel / group')
        except Exception as e :
            client.disconnect()
            LOGGER.info(e)

    return msg_id_li

def engagement(groupname,Message_id,number,apiid,apihash,random_=0):
    action_status = False 
    reaction_list = ["❤️","👍","🔥"]   
    view_nu = 0
    user = user_details.objects.filter(number=number).first()
    try:
        client = TelegramClient(f'./sessions/{number}',apiid,apihash)
        pyrogram_authorization(number,apiid,apihash,client)
        client.connect()
        if client.is_user_authorized():
            me = client.get_me()
            client(JoinChannelRequest(groupname))
            entity = client.get_entity(groupname)
            peer_name = entity.title
            if client.send_read_acknowledge(entity):
                user.views += 1
                user.save()
                view.objects.create(user = user,   views_on= groupname)
                view_nu += 1
                LOGGER.info(f"{me.first_name} {number} have Marked as seen in {groupname}'s chat")
            else : 
                LOGGER.info(f"{me.first_name} {number} have No new messages in {groupname}'s chat")
            dr_bot = view_on_post(number,peer_name,groupname,entity.id,Message_id)
            message_len = client.iter_messages(entity=entity)
            msg_count = 0
            for i in message_len:
                msg_count+=1
            dr_bot.login(client,msg_count)

            # p_client = Client(f'./sessions/{number}_p',api_id=f"{apiid}",api_hash=f"{apihash}",phone_number=str(number))
            # p_client.connect()

            # if p_client.get_me():
            #     message_id_len = 0

            #     # if not random_ :
            #     #     message_id_len = len(Message_id)
            #     #     Message_id = random.sample(Message_id,k=message_id_len)
            #     # else: 
            #         # random_ > len(Message_id)
            #         # Message_id = random.sample(Message_id,k=random_)
            #         # else:
            #         #     message_id_len = len(Message_id)
            #         #     Message_id = random.sample(Message_id,k=message_id_len)


            #     for msg in Message_id:
            #         # print(p_client.get_messages(groupname,msg))
            #         # reactioner_msg = p_client.get_messages(groupname,msg).id
            #         # reactioner_msg.
            #         # p_client.send_reaction(reactioner_msg.id)

            #         reaction = random.choice(reaction_list)
            #         if not Engagements.objects.filter(user = user,engagement_on = groupname,message_on = int(msg)).exists():
            #             try:

            #                 if p_client.send_reaction(groupname,msg,reaction):
            #                     Engagements.objects.create(
            #                         user = user,
            #                         reaction = reaction,
            #                         engagement_on = groupname,
            #                         views = view_nu,
            #                         message_on = int(msg)
            #                     )
            #                     user.reaction += 1
            #                     user.save()
            #                     LOGGER.info(f"{me.first_name} has send reaction {reaction} on message id : {msg} of {groupname} channel / group.")
            #                     action_status = True
            #                 else:
            #                     LOGGER.info(f"{me.first_name} couldn't send reaction {reaction} on message id : {msg} of {groupname} channel / group.")
            #             except Exception as e:LOGGER.error(e)
            #         else:
            #             LOGGER.info(f"{me.first_name} have already sent the reaction {reaction} on message id : {msg} of {groupname} channel / group and can not sent reaction again.")
            #         # time.sleep(2)
            # p_client.disconnect()
        else:
            if not inactive_user.objects.filter(user=user).exists():
                inactive_user.objects.create(
                    user = user,
                    status = 'NEED PASSWORD'
                )
            user.status = "NOT AUTHORIZED"
            user.save()
            LOGGER.info(f'{number} is not authorized So please authorized it main engagement')    
        client.disconnect()
    except p_errors.SessionPasswordNeeded as e:
        LOGGER.error(f'there {number} is SessionPasswordNeeded error')
        if not inactive_user.objects.filter(user=user).exists():
            inactive_user.objects.create(
                user = user,
                status = 'NEED PASSWORD'
            )
        user.status = 'NEED PASSWORD'
        user.save()
    except p_errors.PhoneNumberBanned as e:
        LOGGER.error(f'there {number} is PhoneNumberBanned error')
        if not inactive_user.objects.filter(user=user).exists():
            inactive_user.objects.create(
                user = user,
                status = 'BANNED'
            )
        user.status = 'BANNED'
        user.save()
    except p_errors.AuthKeyUnregistered as e:
        LOGGER.error(f'there {number} is AuthKeyUnregistered error')
        if not inactive_user.objects.filter(user=user).exists():
            inactive_user.objects.create(
                user = user,
                status = 'NOT AUTHORIZED'
            )
        user.status = 'NOT AUTHORIZED'
        user.save()
    except errors.AuthBytesInvalidError as e:
        LOGGER.error(f'there {number} is AuthBytesInvalidError error')
    except errors.FloodWaitError as e:
        LOGGER.error(f'there {number} is FloodWaitError error')
        if not inactive_user.objects.filter(user=user).exists():
            inactive_user.objects.create(
                user = user,
                status = "TEMP BANNED"
            )
        user.status = "TEMP BANNED"
        user.save()
    except errors.UserBannedInChannelError as e:
        LOGGER.error(f'there {number} is UserBannedInChannelError error')

        LOGGER.error('This user is banned from the channel / group')

    except Exception as e :
        client.disconnect()
        LOGGER.info(e)

    return action_status


class view_on_post():
    
    def __init__(self,number,groupname,groupusername,groupid,msg_id) -> None:
        self.number = number
        self.driver = get_driver(profile_dir=number)
        self.driver.get('https://web.telegram.org/k/')
        self.driver.refresh()
        self.logger = LOGGER
        self.viewed_msg_timestemps = []

        self.groupusername = groupusername
        self.groupid = groupid
        self.msg_id = msg_id

        ...


        

    def find_element(self, element, locator, locator_type=By.XPATH,
            page=None, timeout=10,
            condition_func=EC.presence_of_element_located,
            condition_other_args=tuple()):
        """Find an element, then return it or None.
        If timeout is less than or requal zero, then just find.
        If it is more than zero, then wait for the element present.
        """
        time.sleep(3)
        try:
            if timeout > 0:
                wait_obj = WebDriverWait(self.driver, timeout)
                ele = wait_obj.until(
                        condition_func((locator_type, locator),
                            *condition_other_args))
            else:
                self.logger.debug(f'Timeout is less or equal zero: {timeout}')
                ele = self.driver.find_element(by=locator_type,
                        value=locator)
            if page:
                self.logger.debug(
                        f'Found the element "{element}" in the page "{page}"')
            else:
                self.logger.debug(f'Found the element: {element}')
            return ele
        except (NoSuchElementException, TimeoutException) as e:
            if page:
                self.logger.debug(f'Cannot find the element "{element}"'
                        f' in the page "{page}"')
            else:
                self.logger.debug(f'Cannot find the element: {element}')
            
            return False

    def click_element(self, element, locator, locator_type=By.XPATH,
            timeout=10,page=None):
        time.sleep(3)
        
        """Find an element, then click and return it, or return None"""
        try:
            ele = self.find_element(element, locator, locator_type, timeout=timeout,page=page)
            if ele:
                ele.click()
                LOGGER.debug(f'Clicked the element: {element}')
                return ele

            else:return False
        except Exception as e:print(e)

    def input_text(self, text, element, locator, locator_type=By.XPATH,
            timeout=10, page=None):
        time.sleep(3)
        
        """Find an element, then input text and return it, or return None"""
        try:
            
            ele = self.find_element(element, locator, locator_type=locator_type,
                    timeout=timeout,page=page)
            if ele:
                ele.clear()
                ele.send_keys(text)
                self.logger.debug(f'Inputed "{text}" for the element: {element}')
                return ele
        except Exception as e :
            self.logger.info(f'Got an error in input text :{element} {e}')
            
            return False

    def new_tab(self):
        self.driver.execute_script("window.open('https://web.telegram.org/k/')")
        self.driver.switch_to.window(self.driver.window_handles[0]) 
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0]) 
        self.driver.refresh()

   

    def login(self,client,message_len):
        try:
            for i in range(2):
                try:
                    self.driver.set_page_load_timeout(30)
                    self.driver.get('https://web.telegram.org/k/')
                    break
                except TimeoutException :
                    LOGGER.error('The driver got timeout error')

            for i in range(2):
                self.new_tab()
                random_sleep(6,7)
                if self.find_element('number btn','//*[@id="auth-pages"]/div/div[2]/div[2]/div/div[2]/button',By.XPATH):
                    login_need = True
                    break
                all_ele = False
                # if self.find_element('Authentication Page','auth-pages',By.ID,page='login'):
                #     login_need = True
                #     break
                try:all_ele = self.driver.find_elements(By.XPATH,'//*')
                except Exception as e:...
                login_need = False
                if all_ele:
                    for ele in all_ele:
                        # print(ele.text)
                        if "log in by phone number" in str(ele.text).lower():
                            login_need = True
                            break 
                        elif "log in to telegram by" in str(ele.text).lower():
                            login_need = True
                            break 
            action = ActionChains(self.driver)

            if self.find_element('Note','note',By.CLASS_NAME,timeout=4):
                self.click_element('Find btn','auth-number-edit',By.CLASS_NAME)

            for i in range(5):  
                if login_need == True:
                    try:
                        self.new_tab()
                        random_sleep(2,3)
                        self.click_element('phone number','c-ripple',By.CLASS_NAME)
                        self.input_text(self.number,'phone number field','//*[@id="auth-pages"]/div/div[2]/div[1]/div/div[3]/div[2]/div[1]')
                        random_sleep(2,3)
                        self.click_element('Next btn','//*[@id="auth-pages"]/div/div[2]/div[1]/div/div[3]/button[1]',By.XPATH,timeout=12,page='Login')
                        random_sleep(3,4)
                        client.connect()
                        telegram_msg = client.get_dialogs()[0].message
                        try:otp__ = str(telegram_msg.text).replace('**Login code:**','').split(' ')[1].replace('.','')
                        except Exception as e:otp__=''
                        client.disconnect()
                        try:self.input_text(otp__,'Otp input','//*[@id="auth-pages"]/div/div[2]/div[3]/div/div[3]/div/input',By.XPATH,timeout=40)
                        except Exception as e:LOGGER.error(e)
                        element__=self.find_element('home page','//*[@id="folders-container"]/div/div[1]/ul/li[1]/div[1]',By.XPATH,timeout=20)
                        if element__ :
                            action.click(element__).perform()
                        
                        self.new_tab()
                        all_ele = False
                        try:all_ele = self.driver.find_elements(By.XPATH,'//*')
                        except Exception as e:...
                        if all_ele:
                            for ele in all_ele:
                                # print(ele.text)
                                if "log in by phone number" in str(ele.text).lower():
                                    login_need = True
                                    break 
                                elif "log in to telegram by" in str(ele.text).lower():
                                    login_need = True
                                    break
                                else: login_need = False
                        
                    except : 
                        self.new_tab()
                        ...
                else : break
            
            client.connect()
            client(JoinChannelRequest(self.groupusername))
            
            client.disconnect()
            # self.driver.get('https://web.telegram.org/z/#-1665674176')
            # self.driver.get('https://web.telegram.org/z/#-1781322808')
            time.sleep(3)
            self.driver.refresh()
            random_sleep(2,3)
            print(f'------------0-------------------{self.groupusername}')
            self.click_element('go to the latest post','src-components-middle-FloatingActionButtons-module__root src-components-middle-FloatingActionButtons-module__revealed src-components-middle-FloatingActionButtons-module__no-extra-shift',By.CLASS_NAME)
            

            self.driver.get(f"https://web.telegram.org/k/#@{self.groupusername}")
            client.connect()
            print(f'------------1-------------------{self.groupusername}')
            from datetime import datetime
            all_msg = {}
            for i in client.iter_messages(client.get_entity(self.groupusername)) :
                print('------------2-------------------')
                    
                msg_id = i.id
                msg_datetime = i.date
                import pytz
                epoch_time = datetime(1970, 1, 1, 0, 0, 0).replace(tzinfo=pytz.UTC)
                msg_time_dates = (msg_datetime.year, msg_datetime.month, msg_datetime.day, int(msg_datetime.strftime("%H")), int(msg_datetime.strftime("%M")), int(msg_datetime.strftime("%S")))
                msg_time_dates = datetime(*msg_time_dates).replace(tzinfo=pytz.UTC)
                delta = (msg_datetime - epoch_time)
                secound_timestemp = int(delta.total_seconds())
                all_msg [secound_timestemp] = msg_id
                
            user = user_details.objects.filter(number = self.number).first()

            print('------------3-------------------')
            client.disconnect()
            
            
            print('------------4-------------------')
            self.driver.get(f"https://web.telegram.org/k/#@{self.groupusername}")
            print('---------------------------0',self.groupusername)
            total_sent_view = view.objects.filter(user = user, views_on = self.groupusername ).count()  
            displayed_msgs_eles = []
            for _ in range(len(all_msg)):
                print(len(all_msg) ,total_sent_view ,'==========================5========================')
                random_sleep(7,10)
                displayed_msgs_eles = self.get_message_elements()
                for msg_ele in displayed_msgs_eles :
                    timestemp = msg_ele[1]
                    if not timestemp in self.viewed_msg_timestemps :self.viewed_msg_timestemps.append(timestemp)
                    else : continue
                    time.sleep(1)
                    try:self.driver.find_element(By.XPATH,'//*[@id="page-chats"]/div[1]/div[5]/div[2]/button[5]').click()
                    except Exception as e: ...
                    # action.scroll_to_element(msg_ele[0]).perform()
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView();", msg_ele[0])
                        
                    except Exception as e: 
                        print('-------------------------------11111111111111111')
                        
                    if not Engagements.objects.filter(user = user,engagement_on = self.groupusername,message_on = int(all_msg[timestemp])).exists():
                    
                        reaction_list = [1,3,4,13,14,5,6,9]
                        reaction = reaction_id = random.choice(reaction_list)
                        if reaction == 1: reaction = "👍"
                        elif reaction == 3: reaction = "❤️"
                        elif reaction == 4: reaction = "🔥"
                        elif reaction == 12: reaction = "🤩"
                        elif reaction == 13: reaction = "🎉"
                        elif reaction == 5: reaction = "🥰"
                        elif reaction == 6: reaction = "👏"
                        elif reaction == 9: reaction = "🤯"

                        
                        action.context_click(msg_ele[0]).perform()
                        time.sleep(3)
                        try:
                            self.driver.execute_script(f'document.querySelector("#column-center > div > div > div.btn-menu-reactions-container.btn-menu-reactions-container-vertical > div > div > div:nth-child({reaction_id})").click()')
                            user.reaction += 1
                            user.save()
                            
                            Engagements.objects.create(
                                user_id = user.id,
                                views = 1,
                                reaction = reaction,
                                engagement_on = self.groupusername,
                                message_on = all_msg[timestemp]
                            )
                        except Exception as e: 
                            ...
                        # try:
                        #     self.driver.execute_script(f'document.querySelector("#column-center > div > div > div.btn-menu-reactions-container.btn-menu-reactions-container-vertical > div > div > div:nth-child({reaction_id})").click()')
                        # except Exception as e: 
                        #     ...
                            
                        
                    if not view.objects.filter(user = user, message_on = all_msg[timestemp]).exists():
                        view.objects.create(
                            user = user ,
                            views_on = self.groupusername,
                            message_on = all_msg[timestemp]
                        )
                        user.views += 1
                        user.save()
                    random_sleep()
                time.sleep(2)
                if msg_ele:action.key_down(Keys.PAGE_UP,msg_ele[0]).perform()
                else : 
                    msg_ele_0 = self.find_element('scrollable ele','scrollable scrollable-y',By.CLASS_NAME)
                    action.key_down(Keys.PAGE_UP,msg_ele_0).perform()
                total_sent_view = view.objects.filter(user = user, views_on = self.groupusername ).count()  
            
            client.disconnect()
            
            self.driver.refresh()
            random_sleep(2,3)
            

            random_sleep(4,5)
        except KeyboardInterrupt :
            LOGGER.error('There was an keyboard interrupt...')
        except Exception as e:
            LOGGER.error(e,'------Error\n------Error\n------Error\n------Error\n------Error\n------Error\n')
            # self.driver.quit()
        # self.driver.quit()
        try:
            self.driver.quit()
        except Exception as e: ...     
        time.sleep(3)



    def get_message_elements(self):
        message_ele = []
        time.sleep(3)
        channels_post = list(self.driver.find_elements(By.CLASS_NAME,'channel-post'))
        # print(len(channels_post),'------------------\n\n\n\n\n')
        # for ele in channels_post :
            # print(ele,'---------------7--------------------')
        for ele in self.driver.find_elements(By.CLASS_NAME,'channel-post') :
            # print(ele,'------------------6----------------')
            timestemp = ele.get_attribute('data-timestamp')
            if timestemp:
                if not timestemp in self.viewed_msg_timestemps :
                    message_ele.append(ele)
                # break

        message_ele.reverse()

        all_time_stemps = []

        for msg in message_ele :
            time_stemp = int(msg.get_attribute('data-timestamp'))
            all_time_stemps.append(time_stemp)
        all_time_stemps.sort()
        all_time_stemps.reverse()
        message_list = []
        for time_stemp in all_time_stemps :
            for msg in message_ele :
                if time_stemp == int(msg.get_attribute('data-timestamp')) :
                    message_list.append([msg, time_stemp])
                    break
        return message_list





import requests



import time
# import s

from urllib.parse import urlencode


def get_number(pid='10',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"

    while True:
        try:
            payload = {
                "action": "getmobile",
                "username": "pay@noborders.net",
                "token": "87269a810f4a59d407d0e0efe58185e6",
                "pid": pid,
                "cocode":country
            }
            payload = urlencode(payload)
            full_url = str(url) + str(payload)
            
            response = requests.post(url=full_url)
            response = response.content.decode("utf-8")
            # LOGGER.info(response)
            # time.sleep(1000)

            try:response = int(response);break
            except Exception as e:LOGGER.info(e)
            
            # if str(response) == ('Message|Capture Max mobile numbers,you max is 5' or 'Message|unavailable'):
            #     continue
            # else:break
        except Exception as e:LOGGER.info(e)
    return response

def get_sms(phone_number, pid='10',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"
    payload = {
        "action": "getsms",
        "username": "pay@noborders.net",
        "token": "87269a810f4a59d407d0e0efe58185e6",
        "pid": pid,
        "mobile": phone_number,
        "author": "pay@noborders.net",
        "cocode":country
    }
    payload = urlencode(payload)
    full_url = url + payload
    for x in range(15):
        response = requests.post(url=full_url).text
        LOGGER.info(response,'=================================')
        if 'telegram' in str(response).lower():
            response = str(response).split('Telegram code:')[-1]
            otp = response.split(' ')[1].replace("You",'')
            return otp
        time.sleep(4)

    return False

def ban_number(phone_number, pid='10',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"
    payload = {
        "action": "addblack",
        "username": "pay@noborders.net",
        "token": "87269a810f4a59d407d0e0efe58185e6",
        "pid": pid,
        "mobile": phone_number,
        "author": "pay@noborders.net",
        "cocode":country
    }
    payload = urlencode(payload)
    full_url = url + payload
    response = requests.post(url=full_url)
    LOGGER.info(response.text)
    return response
