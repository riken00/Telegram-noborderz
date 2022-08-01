import random
import time, string
from turtle import title
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from selenium.webdriver.common.by import By
from home.models import user_details
from home.driver.driver import get_driver
# Create your views here.

driver = ''
class login(View):
    def get(self,request,number):
        links = [
            'https://www.facebook.com',
            'https://www.google.com/',
            'https://www.linkedin.com/',
            'https://twitter.com/?lang=en',
            'https://en.wikipedia.org/wiki/Twitter',
            'https://apps.apple.com/us/app/twitter/id333903271',
            'https://play.google.com/store/apps/details?id=com.twitter.android&hl=en_US&gl=US',
            'https://www.linkedin.com/authwall?trk=ripf&trkInfo=AQG4YbQ8-momcAAAAYEoWKjgqXb97_VxGwm3PMo9kqw1Rj_TVvpHPhHJk7SaIJ4y-I7ZL3nrsfkTX51yZGkGQBJPrljYGZ0onYcBRAWxQO60_H6XIiYquLc2_qhJT4M38h1PI5s=&original_referer=https://www.google.com/&sessionRedirect=https%3A%2F%2Fwww.linkedin.com%2Fcompany%2Ftwitter',
            'https://mashable.com/category/twitter',
            'https://www.apple.com/',
            'https://mashable.com/category/space',
            'https://mashable.com/tech',
            'https://mashable.com/life',
            'https://mashable.com/category/social-good',
            'https://mashable.com/entertainment',
            'https://mashable.com/deals',
            # 'https://www.apple.com/iphone-13-pro/',
            'https://www.apple.com/ipad-air/',
            'https://www.apple.com/apple-events/',
            'https://www.apple.com/iphone-13/'
        ]
        global driver
        driver = get_driver()
        sucsess = False
        for i in range(len(links)):
            driver.get(links[i])
        time.sleep(5)
        driver.get('https://www.google.com/')
        driver.get('https://my.telegram.org/auth')
        try:
            driver.find_element(By.ID,'my_login_phone').send_keys(str(number))
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="my_send_form"]/div[2]/button').click()
            sucsess = True
        except Exception as e:driver.quit();print(e)

        data = {'sucsess' : sucsess}

        return JsonResponse(data=data)


class testing(View):
    def get(self,request,otp):
        success = False
        app_api_id = ''
        app_api_hash = ''
        try:
            print(driver.find_element_by_id('app_edit_form').is_displayed(),'=======================')
        except Exception as e:None
        # driver.get('https://www.google.com')
        try:
            try:
                driver.find_element(By.ID,'my_password').send_keys(str(otp))
                # driver.find_element(By.NAME,'remember').click()
                driver.find_element_by_name('remember').click()
                driver.find_element(By.XPATH,'//*[@id="my_login_form"]/div[4]/button').click()
                time.sleep(5)
                driver.refresh()
                time.sleep(3)
                driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/ul/li[1]/a').click()
                time.sleep(5)
                driver.refresh()
                time.sleep(3)
            except Exception as e:None


            for i in range(20):
                try:
                    if driver.find_element_by_xpath('//*[@id="app_edit_form"]/h3').get_attribute('text') == 'Available MTProto servers': break
                except Exception as e:None
                try:
                    if driver.find_element_by_id('app_edit_form').is_displayed():break
                except Exception as e:None
                # elif driver.find_element_by_id('app_create_form').is_displayed():continue

                    # elif driver.f 
                length = random.randint(8,13)
                titles = ''.join(random.choices(string.ascii_lowercase,k=length))
                short_name = titles[:int(length/2)]
                app_title = driver.find_element(By.ID,'app_title')
                app_title.clear()
                app_title.location_once_scrolled_into_view
                app_title.send_keys(titles)
                app_shortname = driver.find_element(By.ID,'app_shortname')
                app_shortname.clear()
                app_shortname.send_keys(short_name)
                try:
                    driver.execute_script('document.querySelector("#app_create_form > div:nth-child(6) > div > div:nth-child(8) > label > input[type=radio]").click()')
                except Exception as e:None
                # driver.find_element(By.NAME,'app_platform').click()
                # driver.find_element(By.NAME,'app_platform').click()
                time.sleep(1)
                driver.find_element(By.ID,'app_save_btn').click()
                time.sleep(2)
                # driver.refresh()
                try:
                    driver.switch_to.alert.accept() 
                except Exception as e:None
                try:
                    if driver.find_element_by_id('app_edit_form').is_displayed():break
                    elif driver.find_element_by_id('app_create_form').is_displayed():continue
                    else:continue
                except Exception as e:None
            time.sleep(5)



            

            
        except Exception as e:None
        try:
            driver.refresh()
            app_api_id = driver.find_element(By.XPATH,'//*[@id="app_edit_form"]/div[1]/div[1]/span').get_attribute('innerText')
            app_api_hash = driver.find_element(By.XPATH,'//*[@id="app_edit_form"]/div[2]/div[1]/span').get_attribute('innerText')
            driver.find_element_by_id('app_save_btn').click()
            time.sleep(4)
            driver.execute_script('document.querySelector("#app_save_btn").click()')
            # driver.find_element_by_class_name('btn btn-link').click()
            time.sleep(3)
            driver.execute_script('document.querySelector("#app_edit_form > div:nth-child(14) > div > a").click()')
            driver.refresh()
            time.sleep(3)
            driver.execute_script('document.querySelector("body > div.tl_page_wrap > div.container.tl_page_container > div > div > div > div > div.col-md-8 > div > ul > li:nth-child(3) > a").click()')
            driver.refresh()
            # driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/ul/li[3]/a').click()
            time.sleep(2)
        except Exception as e:None
        if app_api_id and app_api_hash:
            success = True
        else:success = False
        data = {
            'sucsess' : success,
            'app_api_id' : app_api_id,
            'app_api_hash' : app_api_hash,
        }


        driver.quit()
        return JsonResponse(data=data)

class application(View):
    def get(self,request,otp):
        success = False
        app_api_id = ''
        try:
            print(driver.find_element_by_id('app_edit_form').is_displayed(),'=======================')
        except Exception as e:print(e)
        app_api_hash = ''
        # driver.get('https://www.google.com')
        try:
            try:
                driver.find_element(By.ID,'my_password').send_keys(str(otp))
                # driver.find_element(By.NAME,'remember').click()
                driver.find_element_by_name('remember').click()
                driver.find_element(By.XPATH,'//*[@id="my_login_form"]/div[4]/button').click()
                time.sleep(5)
                driver.refresh()
                time.sleep(3)
                driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/ul/li[1]/a').click()
                time.sleep(5)
                driver.refresh()
                time.sleep(3)
            except Exception as e:print(e)


            while True:
                try:
                    if driver.find_element_by_xpath('//*[@id="app_edit_form"]/h3').get_attribute('text') == 'Available MTProto servers': break
                except Exception as e:None
                try:
                    if driver.find_element_by_id('app_edit_form').is_displayed():break
                except Exception as e:print(e)
                # elif driver.find_element_by_id('app_create_form').is_displayed():continue

                    # elif driver.f 
                length = random.randint(8,13)
                titles = ''.join(random.choices(string.ascii_lowercase,k=length))
                short_name = titles[:int(length/2)]
                app_title = driver.find_element(By.ID,'app_title')
                app_title.clear()
                app_title.location_once_scrolled_into_view
                app_title.send_keys(titles)
                app_shortname = driver.find_element(By.ID,'app_shortname')
                app_shortname.clear()
                app_shortname.send_keys(short_name)
                try:
                    driver.execute_script('document.querySelector("#app_create_form > div:nth-child(6) > div > div:nth-child(8) > label > input[type=radio]").click()')
                except Exception as e:print(e)
                # driver.find_element(By.NAME,'app_platform').click()
                # driver.find_element(By.NAME,'app_platform').click()
                time.sleep(1)
                driver.find_element(By.ID,'app_save_btn').click()
                time.sleep(2)
                # driver.refresh()
                try:
                    driver.switch_to.alert.accept() 
                except Exception as e:print(e)
                try:
                    if driver.find_element_by_id('app_edit_form').is_displayed():break
                    elif driver.find_element_by_id('app_create_form').is_displayed():continue
                    else:continue
                except Exception as e:print(e)
            time.sleep(5)



            

            
        except Exception as e:print(e)
        driver.refresh()
        app_api_id = driver.find_element(By.XPATH,'//*[@id="app_edit_form"]/div[1]/div[1]/span').get_attribute('innerText')
        app_api_hash = driver.find_element(By.XPATH,'//*[@id="app_edit_form"]/div[2]/div[1]/span').get_attribute('innerText')
        driver.find_element_by_id('app_save_btn').click()
        time.sleep(4)
        driver.execute_script('document.querySelector("#app_save_btn").click()')
        # driver.find_element_by_class_name('btn btn-link').click()
        time.sleep(3)
        driver.execute_script('document.querySelector("#app_edit_form > div:nth-child(14) > div > a").click()')
        driver.refresh()
        time.sleep(3)
        driver.execute_script('document.querySelector("body > div.tl_page_wrap > div.container.tl_page_container > div > div > div > div > div.col-md-8 > div > ul > li:nth-child(3) > a").click()')
        driver.refresh()
        # driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div/div[2]/div/ul/li[3]/a').click()
        time.sleep(2)
        if app_api_id and app_api_hash:
            success = True
        else:success = False
        data = {
            'sucsess' : success,
            'app_api_id' : app_api_id,
            'app_api_hash' : app_api_hash,
        }


        driver.quit()
        return JsonResponse(data=data)



class test(View):
    def get(self,request):

        return JsonResponse(data={
            'test' : True
        })