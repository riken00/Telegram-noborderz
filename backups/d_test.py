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

    def fake_name(self):
        from faker import Faker
        fake = Faker()
        name = fake.name()
        name_li = str(name).split(' ')
        fname = name_li[0]
        lname = name_li[-1]
        return name,fname, lname

    def next_move(self):
        while True:
            all_ele_li = self.app_driver.find_elements_by_xpath('//*')
            mobile_number_page = False
            for ele in all_ele_li:
                if ('confirm' and 'phone' and 'number') in ele.get_attribute('text'):
                    mobile_number_page = True
                    break

            # create_account = True if len(dicts['current']) == 0 else False
            # if len(dicts['current']) == 0:
                # pass
            country_code = 852
            start_messaging_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.FrameLayout/android.widget.TextView'
            continue_contact_xpt = '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView'
            call_permission_deny_xp = 'com.android.permissioncontroller:id/permission_allow_button'
            country_code_xpth = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.EditText[1]'
            number_xpth = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.EditText[2]'
            continue_btn_after_number_xpth = '//android.widget.FrameLayout[@content-desc="Done"]'
            call_permission_dont_ask_again_xp = 'com.android.permissioncontroller:id/permission_deny_and_dont_ask_again_button'
            # if create_account :
            if mobile_number_page or  self.find_element('confirm phone number page','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView[2]',By.XPATH,timeout=3):
                
                self.number = str(get_number())
                self.croped_number = str(self.number)[3:]
                # if self.starting_permission < 4:
                #     self.click_element('ask for call permission','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView',timeout=1)
                #     self.click_element('deny for permission of call','com.android.permissioncontroller:id/permission_deny_and_dont_ask_again_button',By.ID,timeout=1)
                #     self.click_element('all to recevie calls','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView',By.XPATH,timeout=2)
                #     self.click_element('permission manage call','com.android.packageinstaller:id/permission_deny_button',By.ID,timeout=1)

                print(self.number,'====================================================')
                self.input_text(country_code,'country code',country_code_xpth,By.XPATH)
                self.input_text(self.croped_number,'mobile number',number_xpth,By.XPATH)
                # if self.starting_permission < 5:
                #     self.click_element('deny permssion to make calls','com.android.packageinstaller:id/permission_deny_button',By.ID,timeout=1)
                #     self.click_element('deny access call logs','com.android.packageinstaller:id/permission_deny_button',By.ID,timeout=1)
                #     self.click_element('continue after enter number',continue_btn_after_number_xpth,timeout=1)

                # if self.starting_permission < 5:
                #     self.click_element('ask for call permission','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView',timeout=1)
                #     self.click_element('deny for permission of call','com.android.permissioncontroller:id/permission_deny_and_dont_ask_again_button',By.ID,timeout=1)
                #     self.click_element('access call logs','com.android.permissioncontroller:id/permission_deny_button',By.ID,timeout=1)
                #     self.click_element('permission manage call','com.android.packageinstaller:id/permission_deny_button',By.ID,timeout=1)
                #     self.click_element('deny access call logs','com.android.packageinstaller:id/permission_deny_button',By.ID,timeout=1)
                    # self.starting_permission += 1

                if self.find_element('Banned number popup','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView',By.XPATH,timeout=5):
                    self.click_element('Ok btn for banned number','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.TextView[2]',By.XPATH)
                    self.starting_permission = 0
                    self.secound_permission = 0
                    # continue

                if self.find_element('Too many attempts for otp','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView',By.ID,timeout=1):
                    self.restart_avd()
                    # continue
                    
                    # /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.EditText[1]

                all_otp_input = self.app_driver.find_elements(By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/*')
                self.click_element('get code via sms','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView[3]')
                self.otp=0
                self.otp = get_sms(self.number)
                print(self.otp,'-======================================')

                if self.otp == False:
                    ban_number(self.number)
                    self.click_element('back btn','//android.widget.ImageView[@content-desc="Go back"]',By.XPATH)
                    self.click_element('stop to process on this number','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.TextView[1]',By.XPATH)
                    # continue

                try:
                    self.otp = int(self.otp)
                except Exception as e:None
                if type(self.otp) == int:
                    for otp_input in range(5):
                        input_field= self.input_text(str(self.otp)[otp_input],f'otp input {otp_input+1}',f'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.EditText[{otp_input+1}]')
                        # all_otp_input[otp_input].send_keys(str(self.otp)[otp_input])

                    if self.starting_permission < 4:
                        self.click_element('permission of file access','com.android.permissioncontroller:id/permission_allow_button',By.ID)
                        self.click_element('deny for upgrade app','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.TextView',By.XPATH)
                        # break
                    
                    # dicts['current'].append(self.number)
                # else:
                #     ban_number(self.number)
                #     self.click_element('back btn','//android.widget.ImageView[@content-desc="Go back"]',By.XPATH)
                #     self.click_element('stop to process on this number','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.TextView[1]',By.XPATH)
                #     continue
            # else:continue
            self.outer_loop = False
            time.sleep(3)

            all_ele_li = self.app_driver.find_elements_by_xpath('//*')
            for ele in all_ele_li:
                if ele.get_attribute('text') == 'PHONE_NUMBER_OCCUPIED':
                    self.click_element('Ok btn in "PHONE_NUMBER_OCCUPIED"','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.TextView',By.XPATH,timeout=1)
                    self.outer_loop = True

                    break
            
                elif ele.get_attribute('text') == 'Forgot password?':
                    self.click_element('back tn from','//android.widget.ImageView[@content-desc="Go back"]',By.XPATH)
                    self.outer_loop = True
                    break
            # if self.outer_loop == True:continue

            if self.find_element('Name page of new user','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView',By.XPATH,timeout=5):
                name,self.fname,self.lname = self.fake_name()
                self.input_text(self.fname,'First name','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.widget.EditText[1]',By.XPATH)
                self.input_text(self.lname,'Last name','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.widget.EditText[2]',By.XPATH)
                self.click_element('Continue btn','//android.widget.FrameLayout[@content-desc="Done"]/android.widget.ImageView',By.XPATH)
                if self.starting_permission < 4:
                    self.click_element('permission for contacts','com.android.permissioncontroller:id/permission_allow_button',By.ID,timeout=2)
                    self.click_element('permission of file access','com.android.permissioncontroller:id/permission_allow_button',By.ID,timeout=2)
                self.outer_loop = False
                time.sleep(3)
                # all_ele_li = self.app_driver.find_elements_by_xpath('//*')
                # for ele in all_ele_li:
                #     if ele.get_attribute('text') == 'PHONE_NUMBER_OCCUPIED':
                #         self.click_element('Ok btn in "PHONE_NUMBER_OCCUPIED"','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.TextView',By.XPATH,timeout=1)
                #         self.outer_loop = True
                #         break
                
                #     elif ele.get_attribute('text') == 'Forgot password?':
                #         self.click_element('back tn from','//android.widget.ImageView[@content-desc="Go back"]',By.XPATH)
                #         break
            # else:continue


                # if self.outer_loop == True:
                #     continue
                # else:
                #     None
            


            # if self.find_element('Forget password','')
                
            # else:
                # self.app_driver.start_activity('org.telegram.messenger.web','org.telegram.ui.LaunchActivity')
            if self.starting_permission < 4:
                self.click_element('Access of contacts','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView[2]',By.XPATH,timeout=2)
                self.click_element('access for contacts','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView[2]',By.XPATH,timeout=2)
                if self.click_element('all access of contacts','com.android.permissioncontroller:id/permission_allow_button',By.ID,timeout=2):None
                else:self.click_element('all access of contacts','com.android.packageinstaller:id/permission_allow_button',By.ID,timeout=2)
                if self.click_element('all access of files','com.android.permissioncontroller:id/permission_allow_button',By.ID,timeout=2): None
                else :self.click_element('all access of files','com.android.packageinstaller:id/permission_allow_button',By.ID,timeout=2)



            triple_row_xpth = '//android.widget.ImageView[@content-desc="Open navigation menu"]'
            add_account_row_xpth = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]'
            try:self.app_driver.start_activity('org.telegram.messenger.web','org.telegram.ui.LaunchActivity')
            except Exception as e:None
            self.click_element('deny for upgrade app','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.TextView',By.XPATH,timeout=2)
            all_ele_menuxpath= '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/androidx.recyclerview.widget.RecyclerView/*'
                
            


if __name__ == "__main__":
    driver = CyberGhost()

