from email.charset import BASE64
from operator import imod
import parallel, subprocess, time, traceback
from Telegram.settings import BASE_DIR
from utils import run_cmd
from home.models import User_avds
from home.conf import APPIUM_SERVER_HOST,APPIUM_SERVER_PORT,WAIT_TIME
from ppadb.client import Client as AdbClient
from main import LOGGER
from utils import get_installed_packages
from utils import get_random_file_name
from utils import run_cmd, log_activity
from home.cyberghostvpn import CyberGhostVpn
from exceptions import AccountLimitedException, AccountSuspendedException
from exceptions import CannotRegisterThisPhoneNumberException, CannotGetSms
from exceptions import CannotStartDriverException
from exceptions import PhoneRegisteredException
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver
import os,random,time
import difflib, requests
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait




timeout = 10

class Telegram_bot:
    def __init__(self, emulator_name, start_appium=True, start_adb=True,
                 appium_server_port=APPIUM_SERVER_PORT, adb_console_port=None):
        self.emulator_name = emulator_name
        self.user_avd = User_avds.objects.get(avdname=emulator_name)
        self.eml_name1 = emulator_name
        self.app_driver = None
        self.adb = AdbClient() if start_adb else None
        self.device = None
        self.wait_time = WAIT_TIME
        self.start_driver_retires = 0
        # parallel running configration
        self.appium_server_port = appium_server_port
        if not parallel.get_listening_adb_pid():
            run_cmd('adb start-server')
        parallel.start_appium(port=self.appium_server_port)
        #  parallel.start_appium_without_exit()
        if not adb_console_port:
            self.adb_console_port = str(
                parallel.get_one_available_adb_console_port())
            self.system_port = str(parallel.get_one_available_system_port(
                int(self.adb_console_port)))
        else:
            self.adb_console_port = adb_console_port
        self.system_port = str(parallel.get_one_available_system_port(
            int(self.adb_console_port)))
        self.emulator_port = self.adb_console_port
        self.parallel_opts = self.get_parallel_opts()
        self.countries_vpn = 'Hong kong'
        self.logger = LOGGER
        self.secound_permission = 0
        

    def get_parallel_opts(self):
        return {
                'appium:avd': self.emulator_name,
                'appium:avdArgs': ['-port', str(self.adb_console_port)] + self.get_avd_options(),
                'appium:systemPort': self.system_port,
                'appium:noReset': True,
                #  'appium:skipLogCapture': True,
            }



    def get_avd_options(self):
        emulator_options = [
            # Set the emulation mode for a camera facing back or front
            #  '-camera-back', 'emulated',
            #  '-camera-front', 'emulated',

            #  '-phone-number', str(self.phone) if self.phone else '0',

        ]

        # if self.user_avd.timezone:
        #     emulator_options += ['-timezone', f"{self.user_avd.timezone}"]
        LOGGER.debug(f'Other options for emulator: {emulator_options}')
        return emulator_options


    @staticmethod
    def create_avd(avd_name, package=None, device=None):
        default_package = "system-images;android-28;default;x86"

        try:
            if not package:
                cmd = f'avdmanager create avd --name {avd_name} --package "{default_package}"'
                package = default_package
            else:
                cmd = f'avdmanager create avd --name {avd_name} --package "{package}"'

            if device:
                #  cmd += f" --device {device}"
                cmd += f" --device \"{device}\""

            # install package
            if package not in get_installed_packages():
                LOGGER.info(f'Install or update package: {package}')
                cmd1 = f'sdkmanager "{package}"'
                p = subprocess.Popen(cmd1, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, shell=True, text=True)
                # print live output
                while True:
                    output = p.stdout.readline()
                    if p.poll() is not None:
                        break
                    if output:
                        print(output.strip())

            LOGGER.info(f'AVD command: {cmd}')
            #  result = run_cmd(cmd)
            #  return result
            p = subprocess.Popen(
                [cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL
            )
            time.sleep(1)
            p.communicate(input=b"\n")
            p.wait()
            return True

        except Exception as e:
            LOGGER.error(e)
            return False

    def install_apk(self, port, app_name):
        try:
            if app_name.lower() == "telegram":
                cmd = f"adb -s emulator-{port} install {os.path.join(BASE_DIR, 'apk/Telegram.apk')}"
                log_activity(
                    self.user_avd.id,
                    action_type="InstallTelegramApk",
                    msg=f"Installation of Telegram apk",
                    error=None,
                )
                p = subprocess.Popen(
                    [cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL
                )
                p.wait()
            elif app_name.lower() == "cyberghost":
                cmd = f"adb -s emulator-{port} install {os.path.join(BASE_DIR, 'apk/cyberghost.apk')}"
                log_activity(
                    self.user_avd.id,
                    action_type="InstallcyberghostApk",
                    msg=f"Installation of cyberghost apk",
                    error=None,
                )
                p = subprocess.Popen(
                    [cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL
                )
                p.wait()
            else:
                return False

            return True
        except Exception as e:
            print(e)
            return False

    def check_apk_installation(self):
        # LOGGER.debug('Terminate cyberghost vpn')
        vpn = CyberGhostVpn(self.driver())
        LOGGER.debug('Check if telegram is installed')
        if not self.app_driver.is_app_installed("org.telegram.messenger.web"):
            LOGGER.debug('telegram is not installed, now install it')
            self.install_apk(self.adb_console_port, "Telegram")
            log_activity(
                self.user_avd.id,
                action_type="Installtelegram",
                msg=f"telegram app installed successfully.",
                error=None,
            )
        if not self.app_driver.is_app_installed("de.mobileconcepts.cyberghost"):
            LOGGER.debug('cyberghost is not installed, now install it')
            self.install_apk(self.adb_console_port, "cyberghost")
            log_activity(
                self.user_avd.id,
                action_type="Installcyberghost",
                msg=f"cyberghost app installed successfully.",
                error=None,
            )
        LOGGER.debug('Check if telegram is installed')
    def start_driver(self):
        try:
            opts = {
                "platformName": "Android",
                #  "platformVersion": "9.0",    # comment it in order to use other android version
                "automationName": "UiAutomator2",
                "noSign": True,
                "noVerify": True,
                "ignoreHiddenApiPolicyError": True,
                # "newCommandTimeout": 30,#Don't use this
                #  "systemPort": "8210",
                #  'isHeadless': True,
                # "udid": f"emulator-{self.emulator_port}",
            }

            opts.update(self.parallel_opts)

            #  LOGGER.debug('Start appium driver')
            LOGGER.debug(f'Driver capabilities: {opts}')
            LOGGER.debug(f"Driver url: http://{APPIUM_SERVER_HOST}:{self.appium_server_port}/wd/hub")

            self.app_driver = webdriver.Remote(
                f"http://{APPIUM_SERVER_HOST}:{self.appium_server_port}/wd/hub",
                desired_capabilities=opts,
                #  keep_alive=True,
            )
            self.start_driver_retires = 0
            log_activity(
                self.user_avd.id,
                action_type="ConnectAppium",
                msg=f"Driver started successfully",
                error=None,
            )
        except Exception as e:
            LOGGER.warning(type(e))
            LOGGER.warning(e)

            if not parallel.get_avd_pid(name=self.emulator_name,
                                        port=self.adb_console_port):
                self.adb_console_port = str(
                    parallel.get_one_available_adb_console_port())
                adb_console_port = self.adb_console_port
            else:
                adb_console_port = str(
                    parallel.get_one_available_adb_console_port())
            self.system_port = str(parallel.get_one_available_system_port(
                int(adb_console_port)))
            self.parallel_opts = self.get_parallel_opts()
            if not parallel.get_listening_adb_pid():
                run_cmd('adb start-server')
            parallel.start_appium(port=self.appium_server_port)

            tb = traceback.format_exc()
            if self.start_driver_retires > 5:
                LOGGER.info("================ Couldn't start driverCouldn't start driver")
                log_activity(
                    self.user_avd.id,
                    action_type="ConnectAppium",
                    msg=f"Error while connecting with appium server",
                    error=tb,
                )
                raise CannotStartDriverException("Couldn't start driver")
            #  print("killed in start_driver")
            #  self.kill_bot_process(True, True)
            #  self.service = self.start_appium(port=4724)

            self.start_driver_retires += 1
            LOGGER.info(f"appium server starting retries: {self.start_driver_retires}")
            log_activity(
                self.user_avd.id,
                action_type="ConnectAppium",
                msg=f"Error while connecting with appium server",
                error=f"Failed to connect with appium server retries_value: {self.start_driver_retires}",
            )
            self.driver()

    def driver(self, check_verification=True):
        #  LOGGER.debug('Get driver')
        #  assert self.get_device(), "Device Didn't launch."

        try:
            if not self.app_driver:
                self.start_driver()
            session = self.app_driver.session
        except CannotStartDriverException as e:
            raise e
        except Exception as e:
            #  tb = traceback.format_exc()
            #  log_activity(
            #      self.user_avd.id,
            #      action_type="ConnectAppium",
            #      msg=f"Connect with Appium server",
            #      error=tb,
            #  )
            LOGGER.warning(e)
            self.start_driver()

        # check and bypass google captcha
        #  random_sleep()
        # self.perform_verification()
        # popup = self.app_driver.find_elements_by_android_uiautomator(
        #     'new UiSelector().text("Wait")'
        # )
        # popup[0].click() if popup else None
        return self.app_driver


    def kill_bot_process(self, appium=False, emulators=False):
        from selenium.common.exceptions import InvalidSessionIdException
        LOGGER.debug(f'Start to kill the AVD: {self.emulator_name}')

        if self.app_driver:
            LOGGER.info(f'Stop the driver session')
            try:
                self.app_driver.quit()

            except InvalidSessionIdException as e:
                LOGGER.info(e)

        name = self.emulator_name
        port = self.adb_console_port
        parallel.stop_avd(name=name, port=port)

    def delete_avd(self):
        try:
            LOGGER.info(f'Deleting the avd named {self.emulator_name}')
            cmd = f'avdmanager delete avd --name {self.emulator_name}'
            p = subprocess.Popen([cmd], stdin=subprocess.PIPE, shell=True, stdout=subprocess.DEVNULL)
        except Exception as e:
            pass

    def connect_to_vpn(self, fail_tried=0, vpn_type='cyberghostvpn',
                       country='', city=""):
        # self.check_apk_installation()
        self.countries_vpn = country
        if vpn_type == 'cyberghostvpn':
            ghost_vpn_countries = difflib.get_close_matches(country, CyberGhostVpn.get_server_list())
            country = random.choice(ghost_vpn_countries)
            LOGGER.info('Connect to CyberGhost VPN')
            vpn = CyberGhostVpn(self.driver())
            reconnect = True
            #  country = 'United States' if not vpn_country else vpn_country
            return vpn.start_ui(reconnect=reconnect, country=country, city=city)

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
                wait_obj = WebDriverWait(self.driver(), timeout)
                ele = wait_obj.until(
                        condition_func((locator_type, locator),
                            *condition_other_args))
            else:
                self.logger.debug(f'Timeout is less or equal zero: {timeout}')
                ele = self.driver().find_element(by=locator_type,
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


    
    def click_element(self, element, locator, locator_type=By.XPATH,
            timeout=timeout,page=None):
        time.sleep(3)
        
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout,page=page)
        if ele:
            ele.click()
            LOGGER.debug(f'Clicked the element: {element}')
            return ele

    def input_text(self, text, element, locator, locator_type=By.XPATH,
            timeout=timeout, hide_keyboard=True,page=None):
        time.sleep(3)
        
        """Find an element, then input text and return it, or return None"""
        try:
            if hide_keyboard :
                self.logger.debug(f'Hide keyboard')
                try:self.driver().hide_keyboard()
                except:None

            ele = self.find_element(element, locator, locator_type=locator_type,
                    timeout=timeout,page=page)
            if ele:
                ele.clear()
                ele.send_keys(text)
                self.logger.debug(f'Inputed "{text}" for the element: {element}')
                return ele
        except Exception as e :
            self.logger.info(f'Got an error in input text :{element} {e}')

    def restart_avd(self):
        self.kill_bot_process(True,True)
        self.delete_avd()
        # avd_details = User_avds.objects.filter(avdname=self.emulator_name).first()
        # avd_details.delete()
        self.create_avd(self.emulator_name) 
        self.start_driver()
        self.check_apk_installation()
        return

    def starting_permission(self):
        start_messaging_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.FrameLayout/android.widget.TextView'
        continue_contact_xpt = '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView'
        call_permission_deny_xp = 'com.android.permissioncontroller:id/permission_allow_button'
        call_permission_dont_ask_again_xp = 'com.android.permissioncontroller:id/permission_deny_and_dont_ask_again_button'
        self.click_element('start messages', start_messaging_xpath ,timeout=3)
        self.click_element('Start message','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView',By.XPATH)
        self.click_element('continue to allow receive calls btn', continue_contact_xpt, By.XPATH,timeout=3)
        self.click_element('access call logs','com.android.permissioncontroller:id/permission_deny_button',By.ID,timeout=2)
        self.click_element('call permission',call_permission_deny_xp,By.ID,timeout=3)
        self.click_element('dont ask again the permission on call', call_permission_dont_ask_again_xp,By.ID,timeout=3)
        return

    def secound_time_permission(self):
        self.click_element('ask for call permission','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TextView',timeout=1)
        self.click_element('deny for permission of call','com.android.permissioncontroller:id/permission_deny_and_dont_ask_again_button',By.ID,timeout=1)
        self.click_element('access call logs','com.android.permissioncontroller:id/permission_deny_button',By.ID,timeout=1)
        self.click_element('permission manage call','com.android.packageinstaller:id/permission_deny_button',By.ID,timeout=1)
        self.click_element('deny access call logs','com.android.packageinstaller:id/permission_deny_button',By.ID,timeout=1)
        return

    def create_account(self):
        self.driver()
        # /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.FrameLayout/android.widget.TextView

        
        country_code_xpth = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.EditText[1]'
        number_xpth = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.EditText[2]'
        continue_btn_after_number_xpth = '//android.widget.FrameLayout[@content-desc="Done"]'
        
        country_code = 0
        self.countries_vpn = 'Hong kong'  # for temprarory
        if self.countries_vpn == 'Hong kong':country_code = 852
        elif self.countries_vpn == 'south africa':country_code = 27
        elif self.countries_vpn == 'indonesia':country_code = 62
        elif self.countries_vpn == 'macau':country_code = 853
        elif self.countries_vpn == 'vietnam':country_code = 84
        elif self.countries_vpn == 'philippines':country_code = 63
        elif self.countries_vpn == 'argentina':country_code = 54

        self.number = 0
        from home.management.commands.functions_file.function_msg import get_sms,get_number,ban_number
        try:self.app_driver.activate_app('org.telegram.messenger.web')
        except Exception as e:LOGGER.error(e)
        

        
        
        total_acc = 0
        while total_acc <3:
            while True:
                self.starting_permission()
                self.app_driver.activate_app('org.telegram.messenger.web')

                all_ele_li = self.app_driver.find_elements_by_xpath('//*')
                mobile_number_page = False
                for ele in all_ele_li:
                    if ('confirm' and 'phone' and 'number') in ele.get_attribute('text'):
                        mobile_number_page = True
                        break

                if mobile_number_page or  self.find_element('confirm phone number page','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView[2]',By.XPATH,timeout=3):
                    
                    self.number = str(get_number())
                    self.croped_number = str(self.number)[3:]
                    print(self.number,'====================================================')
                    self.input_text(country_code,'country code',country_code_xpth,By.XPATH)
                    self.input_text(self.croped_number,'mobile number',number_xpth,By.XPATH)
                    self.click_element('dont ask again box','com.android.packageinstaller:id/do_not_ask_checkbox',By.ID,timeout=1)
                    self.click_element('deny permssion to make calls','com.android.packageinstaller:id/permission_deny_button',By.ID,timeout=1)
                    self.click_element('dont ask again box','com.android.packageinstaller:id/do_not_ask_checkbox',By.ID,timeout=1)
                    self.click_element('deny access call logs','com.android.packageinstaller:id/permission_deny_button',By.ID,timeout=1)
                    self.click_element('continue after enter number',continue_btn_after_number_xpth,timeout=1)

                    if self.secound_permission < 3:
                        self.secound_time_permission()
                        self.secound_permission += 1
                        
                    if self.find_element('Banned number popup','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView',By.XPATH,timeout=5):
                        self.click_element('Ok btn for banned number','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.TextView[2]',By.XPATH)
                        continue

                    if self.find_element('Too many attempts for otp','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView',By.ID,timeout=1):
                        self.restart_avd()
                        continue


                    all_otp_input = self.app_driver.find_elements(By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/*')
                    self.click_element('get code via sms','/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView[3]')
                    self.otp=0
                    self.otp = get_sms(self.number)
                    print(self.otp,'-======================================')
                    try:self.otp = int(self.otp)
                    except Exception as e:None
                    if type(self.otp) == int:
                        for otp_input in range(len(all_otp_input)):
                            all_otp_input[otp_input].send_keys(self.otp[otp_input])



                        self.click_element('permission for contacts','com.android.permissioncontroller:id/permission_allow_button',By.ID,timeout=4)
                        self.click_element('permission of file access','com.android.permissioncontroller:id/permission_allow_button',By.ID)
                        self.click_element('deny for upgrade app','/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.TextView',By.XPATH)
                        break
                    
                    else:
                        ban_number(self.number)
                        self.click_element('back btn','//android.widget.ImageView[@content-desc="Go back"]')
                        self.click_element('stop to process on this number')
                        continue


                    # if # forget pass word aave tyare
                    
                # else:
                    # self.app_driver.start_activity('org.telegram.messenger.web','org.telegram.ui.LaunchActivity')


            triple_row_xpth = '//android.widget.ImageView[@content-desc="Open navigation menu"]'
            add_account_row_xpth = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]'

            all_ele_menuxpath= '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[1]/androidx.recyclerview.widget.RecyclerView/*'

            self.click_element('Menu btn',triple_row_xpth)
            self.click_element('accounts viwer',add_account_row_xpth)

            try:
                all_menu_ele = self.app_driver.find_elements(all_ele_menuxpath)
                for ele in all_menu_ele:
                    if ele.get_attribute('text') == 'Add Account':
                        ele.click()
                        total_acc +=1
                        
                        break
            except Exception as e:LOGGER.error(e)



        # self.app_driver.start_activity('de.mobileconcepts.cyberghost','de.mobileconcepts.cyberghost.view.app.AppActivity')
        time.sleep(10)


    def Test(self):

        
        
        login = requests.get(f'http://127.0.0.1:8000/login/{self.number}')
        
        
        
        try:
            self.app_driver.activate_app('org.telegram.messenger.web')
            time.sleep(2)
        except Exception as e:print(e)







        self.app_driver.find_elements(By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/androidx.recyclerview.widget.RecyclerView/*')[0].click()
        
        time.sleep(2)
        all_message = self.app_driver.find_elements(By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/*')[-1]
        otp_texts=''
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


        login_confirm = requests.get(f'http://127.0.0.1:8000/application/{otp}')


        return otp
