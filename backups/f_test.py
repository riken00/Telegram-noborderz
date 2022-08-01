from cgi import print_directory
from appium import webdriver
import os.path,random
# from ..main import LOGGER
import time, requests
from flask import jsonify
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlencode
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from telethon.sync import TelegramClient
from faker import Faker

# from home.models import user_details
fake = Faker()
country_name = 'malaysia'

def random_sleep(a,b):
    random_ = random.randint(a,b)
    print(f'time sleep : {random_}')
    time.sleep(random_)

def get_number(pid='8',country = 'hk'):
    url = "http://api.getsmscode.com/vndo.php?"

    payload = {
        "action": "getmobile",
        "username": "pay@noborders.net",
        "token": "87269a810f4a59d407d0e0efe58185e6",
        "pid": pid,
        "cocode":country
    }

    payload = urlencode(payload)
    full_url = url + payload
    response = requests.post(url=full_url)
    response = response.content.decode("utf-8")
    # print(response)
    # time.sleep(1000)

    return response

def get_sms(phone_number, pid='8',country = 'hk'):
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
    for x in range(10):
        response = requests.post(url=full_url).text
        if 'insta' in (response).lower():
            response = response.split(' ')
            otp = response[1]+response[2]
            return otp
        time.sleep(4)

    return False

def ban_number(phone_number, pid='8',country = 'hk'):
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
    print(response.text)
    return response



class CyberGhost:
    timeout = 5
    def __init__(self):
        self.app_driver = self.get_driver()
        self.next_move()
        self.follow_count=0
        # self.logger = LOGGER
        self.timeout = 10
    # @staticmethod
    def get_driver(self):
        """
        Starts appium driver
        """
        path = '/wd/hub'
        port = 4723
        host = "http://localhost"
        opts = {
            "platformName": "Android",
            "automationName": "uiautomator2",
            "noSign": True,
            "noVerify": True,
            "ignoreHiddenApiPolicyError": True,
        }
        url = f"{host}:{port}{path}"
        driver = webdriver.Remote(url, desired_capabilities=opts, keep_alive=True)
        # print(driver)
        self.app_driver = driver

        return driver

    
    
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
                wait_obj = WebDriverWait(self.get_driver(), timeout)
                ele = wait_obj.until(
                        condition_func((locator_type, locator),
                            *condition_other_args))
            else:
                print(f'Timeout is less or equal zero: {timeout}')
                ele = self.get_driver().find_element(by=locator_type,
                        value=locator)
            if page:
                print(
                        f'Found the element "{element}" in the page "{page}"')
            else:
                print(f'Found the element: {element}')
            return ele
        except (NoSuchElementException, TimeoutException) as e:
            if page:
                print(f'Cannot find the element "{element}"'
                        f' in the page "{page}"')
            else:
                print(f'Cannot find the element: {element}')


    
    def click_element(self, element, locator, locator_type=By.XPATH,
            timeout=timeout,page=None):
        time.sleep(3)
        
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout,page=page)
        if ele:
            ele.click()
            return ele

    def input_text(self, text, element, locator, locator_type=By.XPATH,
            timeout=timeout, hide_keyboard=True,page=None):
        time.sleep(3)
        
        """Find an element, then input text and return it, or return None"""
        try:
            if hide_keyboard :
                print(f'Hide keyboard')
                try:self.get_driver().hide_keyboard()
                except:None

            ele = self.find_element(element, locator, locator_type=locator_type,
                    timeout=timeout,page=page)
            if ele:
                ele.clear()
                ele.send_keys(text)
                print(f'Inputed "{text}" for the element: {element}')
                return ele
        except Exception as e :
            print(f'Got an error in input text :{element} {e}')

    def swip_display(self,scroll_height):
        window_size = self.get_driver().get_window_size()
        width = window_size["width"]
        height = window_size["height"]
        x1 = width*0.7
        y1 = height*(scroll_height/10)
        y2 = height*0.2
        self.get_driver().swipe(
            start_x = x1,
            start_y = y1,
            end_x = x1,
            end_y = y2, 
            duration=random.randrange(1050, 1250),
            )

    def try_again_popup(self):
        try:
            
            try_again_ele_id = 'com.instagram.android:id/default_dialog_title'
            try_again_ele_ele = self.find_element('Try again',try_again_ele_id,By.ID,timeout=3)

            if try_again_ele_ele:
                try_again_ok_id = 'com.instagram.android:id/negative_button_row'
                time.sleep(3)
                self.click_element('Ok btn',try_again_ok_id,By.ID,timeout=2)
                self.click_element('Ok btn',try_again_ok_id,By.ID,timeout=2)
                self.click_element('Ok btn',try_again_ok_id,By.ID,timeout=2)
                self.click_element('Ok btn',try_again_ok_id,By.ID,timeout=2)
                return True
            else:
                return False
        except :return False



    def fake_name(self):
        from faker import Faker
        fake = Faker()
        name = fake.name()
        name_li = str(name).split(' ')
        fname = name_li[0]
        lname = name_li[-1]
        return name,fname, lname

    

    def next_move(self):
        print(1)
        import asyncio
        number = 85262550512
        id_ = 15451024
        hash_ = '6fb9eb2518d1bd451682c56ddc348be3'
        client = TelegramClient(f'./sessions/{number}',id_,f'{hash_}')
        client.connect()
        # client = asyncio.run(client_1(number,id_,hash_))
        # await self.client_1()
        print(2)
        # from telethon import TelegramClient, connection

        # client = TelegramClient(
        #     './sessions/{85262550512}',
        #     15451024,
        #     '6fb9eb2518d1bd451682c56ddc348be3',

        #     # Use one of the available connection modes.
        #     # Normally, this one works with most proxies.
        #     connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,

        #     # Then, pass the proxy details as a tuple:
        #     #     (host name, port, proxy secret)
        #     #
        #     # If the proxy has no secret, the secret must be:
        #     #     '00000000000000000000000000000000'
        #     proxy=('mtproxy.example.com', 2002, 'secret')
        # )
        # import os
        # import sys
        # # client = TelegramClient(f'./sessions/{85262550512}',15451024,'6fb9eb2518d1bd451682c56ddc348be3')
        # # with TelegramClient(f'./sessions/{85262550512}',15451024,'6fb9eb2518d1bd451682c56ddc348be3') as client:
        # time.sleep(5)
        if not client.is_user_authorized():
            client.send_code_request(number)

        triple_row_xpth = '//android.widget.ImageView[@content-desc="Open navigation menu"]'

        self.app_driver = self.get_driver()

        self.find_element('Menu btn',triple_row_xpth)

        random_sleep(5,9)
        telegram_otp1 = self.app_driver.find_element(By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]')
        telegram_otp1.click()
        try:
            all_menu_ele = self.app_driver.find_elements_by_xpath('//*')
            for ele in all_menu_ele:
                print(ele.get_attribute('text'))
                if 'Archived' in str(ele.get_attribute('text')).lower() :
                    self.click_element('back btn','//android.widget.ImageView[@content-desc="Go back"]',By.XPATH)
                    self.click_element('telegram chat 2','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]',By.XPATH)
                    # telegram_otp1 = self.app_driver.find_element(By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]')

                    # secound_element = True
                    break
        except Exception as e:print(e)

        all_message = []
        otp_texts=''
        time.sleep(3)

        all_message = self.app_driver.find_elements(By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/*')
        # except Exception as e:print(e)
        all_message.reverse()   
        for message in all_message:
            msg_text = str(message.get_attribute('text'))
            print(msg_text)
            if 'Login code:' in msg_text:
                otp_texts = str(msg_text).replace('Login code:','').strip().split('.')[0]
                print(otp_texts,'======================')
                break
        # if otp_texts:
        #     self.app_driver.back()
        #     otp_texts = otp_texts.split('\n')
        #     otp_texts.remove(otp_texts[0])
        #     otp = otp_texts[0]
        #     print(otp)
        
        

        # client = TelegramClient(f'./sessions/{85262550512}',15451024,'6fb9eb2518d1bd451682c56ddc348be3')
        # if not client.is_user_authorized():
            # client.send_code_request(85262550512)
        
        # asyncio.run(client_login(client=client,otp=otp_texts))
        # asyncio.run()
        # print(33)
        # return
        if not client.is_user_authorized():
            client.sign_in(number,code=otp_texts)
            
        me = client.get_me()
        print(me)
        # if tclient.start(phone=85262550512,max_attempts=5):
# async def client_1(number,id,hash):
#         from telethon import TelegramClient, connection

#         client = TelegramClient(f'./sessions/{number}',id,f'{hash}')
#         # client = TelegramClient(f'./sessions/{85262550512}',15451024,'6fb9eb2518d1bd451682c56ddc348be3')
#         # with TelegramClient(f'./sessions/{85262550512}',15451024,'6fb9eb2518d1bd451682c56ddc348be3') as client:
#         # time.sleep(5)
#         await client.connect()
#         # if not client.is_user_authorized():
#         await client.send_code_request(number)
        
#         return client

# async def client_login(client,otp):
#     print('---------1')
#     # if not await client.is_user_authorized():
#     print('---------1')
#     await client.sign_in(85262550512,code=otp)
#     print('---------2')
#     me = await client.get_me()
#     print(me)
#     return

    

if __name__ == "__main__":
    driver = CyberGhost()

