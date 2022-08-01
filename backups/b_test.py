from cgi import print_directory
from appium import webdriver
import os.path,random
# from ..main import LOGGER
import time, requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlencode
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from faker import Faker

# from home.models import user_details
fake = Faker()
country_name = 'malaysia'

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
    @staticmethod
    def get_driver():
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
        print(driver)
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
                wait_obj = WebDriverWait(self.app_driver, timeout)
                ele = wait_obj.until(
                        condition_func((locator_type, locator),
                            *condition_other_args))
            else:
                print(f'Timeout is less or equal zero: {timeout}')
                ele = self.app_driver.find_element(by=locator_type,
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
                try:self.app_driver.hide_keyboard()
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
        window_size = self.app_driver.get_window_size()
        width = window_size["width"]
        height = window_size["height"]
        x1 = width*0.7
        y1 = height*(scroll_height/10)
        y2 = height*0.2
        self.app_driver.swipe(
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

    def next_move(self):
        self.number = '85296506664'

        while True:
            # self.click_element('Access of contacts','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView[2]',By.XPATH,timeout=2)

            # self.click_element('access for contacts','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView[2]',By.XPATH,timeout=5)
            # if self.click_element('all access of contacts','com.android.permissioncontroller:id/permission_allow_button',By.ID,timeout=1):None
            # else:self.click_element('all access of contacts','com.android.packageinstaller:id/permission_allow_button',By.ID,timeout=1)
            # if self.click_element('all access of files','com.android.permissioncontroller:id/permission_allow_button',By.ID,timeout=1): None
            # else :self.click_element('all access of files','com.android.packageinstaller:id/permission_allow_button',By.ID,timeout=1)

            triple_row_xpth = '//android.widget.ImageView[@content-desc="Open navigation menu"]'
            add_account_row_xpth = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]'

            login = requests.get(f'http://127.0.0.1:8000/login/{self.number}')

            try:
                self.app_driver.activate_app('org.telegram.messenger.web')
                time.sleep(2)
            except Exception as e:print(e)
            try:
                self.app_driver.find_elements(By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/androidx.recyclerview.widget.RecyclerView/*')[0].click()
            except Exception as e:print(e)

            time.sleep(2)
            all_message = self.app_driver.find_elements(By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/*')
            all_message.reverse()
            otp_texts=''
            print(all_message)
            for message in all_message:
                msg_text = str(message.get_attribute('text'))
                print(msg_text)
                if 'Web login code' in msg_text:
                    otp_texts = msg_text
                    break
            if otp_texts:
                otp_texts = otp_texts.split('\n')
                otp_texts.remove(otp_texts[0])
                otp = otp_texts[0]

                otp_request = requests.get(f'http://127.0.0.1:8000/application/{otp}')
                print(otp_request,'----------------------------')

                # if otp_request['sucsess'] == True:
                #     user_details.objects.create(
                #         emulator =  self.emula
                #     )
            if self.find_element('Menu btn',triple_row_xpth):
                self.click_element('Menu btn',triple_row_xpth)
                self.click_element('accounts viwer',add_account_row_xpth)
                # time.sleep(2)

                if True: # for update username
                    self.click_element('Profile btn','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.view.View',By.XPATH)
                    self.click_element('username btn','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]',By.XPATH)
                    self.input_text('eagfeauff213','username field','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.EditText',By.XPATH)
                    # self.input_text(self.username,'username field','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.EditText',By.XPATH)
                    self.click_element('Done btn','//android.widget.ImageButton[@content-desc="Done"]/android.widget.ImageView',By.XPATH)
                    self.click_element('Back btn','//android.widget.ImageView[@content-desc="Go back"]',By.XPATH)

                    self.click_element('Menu btn',triple_row_xpth)
                    self.click_element('accounts viwer',add_account_row_xpth)

                
                try:
                    all_menu_ele = self.app_driver.find_elements_by_xpath('//*')
                    for ele in all_menu_ele:
                        print(ele.get_attribute('text'))
                        if ele.get_attribute('text') == 'Add Account':
                            ele.click()
                            total_acc +=1
                            print('\n\nCode completed\n\n')
                            break
                except Exception as e:print(e)
            # else:continue
            

        pass


if __name__ == "__main__":
    driver = CyberGhost()

