from ast import Break, While
from curses import KEY_PPAGE
from email import message
from pydoc import allmethods
from telethon.sync import TelegramClient

import os.path
import zipfile
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from tiktok_bot.settings import BASE_DIR
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
# from Telegram.settings import BASE_DIR
def driver_options(profile_dir):
    options = webdriver.ChromeOptions()
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    # print(software_names, operating_systems,)
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

    useragent = user_agent_rotator.get_random_user_agent()

    # options = Options() 
    options = webdriver.ChromeOptions() 

    # options.add_extension("CyberGhost_VPN.crx")#crx file path
    # options.add_argument('--no-sandbox')
    # options.add_argument('--autoplay-policy=no-user-gesture-required')
    options.add_argument('--start-maximized')    
    # options.add_argument('--single-process')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--disable-blink-features")
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--enable-javascript")
    # options.add_argument("--disable-notifications")
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument("--enable-popup-blocking")
    # # options.add_argument('--user-data-dir=./profiles/')
    # # options.add_argument(f"--profile-directory={'1_'+str(username__)}")
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_experimental_option("excludeSwitches", [
    #     "enable-logging",
    #     "enable-automation",
    #     "ignore-certificate-errors",
    #     "safebrowsing-disable-download-protection",
    #     "safebrowsing-disable-auto-update",
    #     "disable-client-side-phishing-detection"])
    # options.add_argument("disable-infobars")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--autoplay-policy=no-user-gesture-required')
    # options.add_argument('--start-maximized')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--disable-blink-features")
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--enable-javascript")
    # options.add_argument("--disable-notifications")
    # options.add_argument("disable-infobars")
    # options.add_argument('--no-proxy-server')
    # options.add_argument('--disable-gpu')
    # options.add_argument("--disable-popup-blocking")
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument("--disable-web-security")
    # options.add_argument("--allow-running-insecure-content")
    # options.add_experimental_option('useAutomationExtension', True)
    # options.add_experimental_option("excludeSwitches", [
    #     "enable-logging",
    #     "enable-automation",
    #     "ignore-certificate-errors",
    #     "safebrowsing-disable-download-protection",
    #     "safebrowsing-disable-auto-update",
    #     "disable-client-side-phishing-detection"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-data-dir=./profiles/')
    options.add_argument(f"--profile-directory={profile_dir}")
    # prefs = {"credentials_enable_service": True,
    #          "profile.password_manager_enabled": True}
    # options.add_experimental_option("prefs", prefs)
    # options.headless = True
    options.add_extension(os.path.join("/home/riken/Desktop/Workspace/Telegram/Telegram-noborderz/CyberGhost_VPN.crx"))

    return options,useragent
import random, time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def connect_vpn(driver):

    driver.switch_to.window(driver.window_handles[0])
    driver.get('chrome-extension://ffbkglfijbcbgblgflchnbphjdllaogb/index.html')
    time.sleep(3)

    # Disconnect if already connected
    try:
        driver.execute_script('document.querySelector("body > app-root > main > app-home > div > div.spinner > app-switch > div > div.spinner > div.spinner-inner").click()')
    except Exception as e:print(e)
    time.sleep(3)
    try:
        connected_btn = driver.find_element(By.CLASS_NAME, 'dark outer-circle connected')
        connected_btn[0].click() if connected_btn else None
    except Exception as e:print(e) # document.querySelector("body > app-root > main > app-home > div > div.spinner > app-switch > div > div.spinner > div.spinner-inner").click()

    # Select country
    countries_drop_down_btn = driver.find_elements(By.TAG_NAME, 'mat-select-trigger')
    countries_drop_down_btn[0].click() if countries_drop_down_btn else None

    # randomly select a country name from a list
    country_list = ['United States','Romania','Netherlands','Germany']
    # country_list = ['Romania','Neth0erlands']
    vpn_country = random.choice(country_list)

    total_option_country = driver.find_elements(By.TAG_NAME, 'mat-option')
    for i in total_option_country:
        i_id = i.get_attribute('id')
        country_text_ele = i.find_element(By.XPATH, f"//*[@id='{i_id}']/span")
        country_text = country_text_ele.text
        
        # checking if the country is whether same or not and click on it
        if vpn_country == country_text:
            country_text_ele.click()
            break

    # Checking is the VPN connected or not
    try:
        connect_btn = driver.find_element(By.XPATH, '//div[@class="dark disconnected outer-circle"]')
        connect_btn.click()
    except Exception as e:print(e)

def get_driver(profile_dir='profile_dir'):
    
    options,useragent = driver_options(profile_dir)
    # service = Service()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # driver = webdriver.Chrome()

    # stealth(driver,
    #         languages=["en-US", "en"],
    #         user_agent=useragent,
    #         vendor="Google Inc.",
    #         platform="Win32",
    #         webgl_vendor="Intel Inc.",
    #         renderer="Intel Iris OpenGL Engine",
    #         fix_hairline=True,
    #     )
    # connect_vpn(driver)
    
        
    return driver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

number = 919953990018
id_ = 9032170
hash_ = '0a5c0443b0e3aa7337274d30ec2f012f'

client = TelegramClient(f'./sessions/{number}',id_,hash_)


client.connect()




driver = get_driver(profile_dir=number)  

driver.get('https://web.telegram.org/k/#@xanaofficial')
time.sleep(4)
# driver.execute_script('')

# recentList = list(driver.find_elements(By.CLASS_NAME,"message"))

# for list in recentList :
#     driver.execute_script("arguments[0].scrollIntoView();", list )
#     time.sleep(1)

# viewed_message = []
# message_len = client.iter_messages(client.get_entity('xanaofficial'))
# print(message_len)
# msg_count = 0
# for i in message_len:
#     msg_count+=1


action = ActionChains(driver)
# all_message_elements = list(driver.find_elements(By.CLASS_NAME,"bubble-content"))

# action.click(all_message_elements[0])
time.sleep(2)
# print(msg_count,'='*100)

# chat_container = driver.find_element(By.CLASS_NAME,'chats-container')
# action.click(chat_container).perform()
# for i in range(msg_count*2):
while True:
    time.sleep(0.5)
    try:
        driver.find_element(By.XPATH,'//*[@id="column-center"]/div/div[2]/div[2]/div[1]/button').click()
    except Exception as e: ...
    time.sleep(0.5)
        
    
    scrollable_ele = list(driver.find_elements(By.CLASS_NAME,'scrollable-y'))[1]
    print('-----------------------1-------------------')
    
    action.key_down(Keys.PAGE_UP,scrollable_ele).perform()

# all_message_elements = list(driver.find_elements(By.CLASS_NAME,"bubble-content"))
# while True:
#     time.sleep(3)
#     if len(all_message_elements) > 0:
#         print('----------------------1---------------------')
#         for message_element in all_message_elements:
#             if not message_element in viewed_message:
#                 print('----------------------2---------------------')
#                 driver.execute_script("arguments[0].scrollIntoView(true);", message_element )
#                 viewed_message.append(message_element)
#                 time.sleep(1)
    
    
#     time.sleep(1)
#     print('----------------------3---------------------')
#     all_message_elements = list(driver.find_elements(By.CLASS_NAME,"bubble-content"))
    
#     if len(viewed_message) >= msg_count:
#         break
    ...    

# ------------------------------------

# print('1111')
# driver.execute_script("window.scrollTo(-1100,-1100);")

# ------------------------------------

# last_height = driver.execute_script("return document.body.scrollHeight")
# print(last_height,'------------------')
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
    
# ------------------------------------
# while True:
    # all_element = list(driver.find_elements(By.CLASS_NAME,"message"))
    # all_element.reverse()
    # driver.execute_script("arguments[0].scrollIntoView();", all_element[0])
    # time.sleep(3)
# ------------------------------------
input('Enter :')
driver.quit()







# for i in client.iter_admin_log(client.get_entity('mrkhadela')):
#     print(i)

# for i in client.iter_messages(client.get_entity('mrkhadela')): 
#     print(client.send_read_acknowledge(client.get_entity('mrkhadela'),message=i))

# print(client.send_read_acknowledge(client.get_entity('mrkhadela'),message=messs),'--=-=-')




















# iter_MSG = list(client.iter_messages(client.get_entity('mrkhadela')))
# all_message_len = len(iter_MSG)
    
# driver = get_driver(profile_dir=number)     
# driver.get('https://web.telegram.org/k/#@mrkhadela')
# time.sleep(4)





# msg_elements = list(driver.find_elements(By.CLASS_NAME,'message'))
# print(type(msg_elements),'--------------------')
# print(msg_elements,'--------------------')
# viewd_msg_count = 0
# viewd_msg_list = []
# action = ActionChains(driver=driver)
# while True:
#     time.sleep(1)
#     print(msg_elements,'============')
#     message_ele = msg_elements.pop()
#     if message_ele in viewd_msg_list:
#         continue
#     if action.scroll_to_element(message_ele):
#         viewd_msg_list.append(message_ele)
#         viewd_msg_count += 1
#     msg_elements = list(driver.find_elements(By.CLASS_NAME,'message'))
    
#     if viewd_msg_count >= all_message_len:break
    




# input("Enter :")

# driver.quit()
# client.disconnect()