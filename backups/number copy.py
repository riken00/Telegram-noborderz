import time
import requests

from urllib.parse import urlencode


# # def get_insta_number(pid='8'):
# def get_insta_number(pid='8',country = 'hk'):

#     url = "http://api.getsmscode.com/vndo.php?"

#     payload = {
#         "action": "getmobile",
#         "username": "pay@noborders.net",
#         "token": "87269a810f4a59d407d0e0efe58185e6",
#         "pid": pid,
#         "cocode":country
#     }

#     payload = urlencode(payload)
#     full_url = url + payload
#     response = requests.post(url=full_url)
#     response = response.content.decode("utf-8")
#     # print(response)
#     # time.sleep(1000)

#     return response[3:]


# def get_insta_sms(phone_number, pid='8'):
def get_insta_sms(phone_number, pid='8',country = 'hk'):

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
        print(response,'=================================')
        if 'telegram' in str(response).lower():
            response = str(response).split('Telegram code:')[-1]
            otp = response.split(' ')[1].replace("You",'')
            return otp
        time.sleep(4)

    return False


# def ban_number(phone_number, pid='8',country = 'hk'):
#     url = "http://api.getsmscode.com/vndo.php?"
#     payload = {
#         "action": "addblack",
#         "username": "pay@noborders.net",
#         "token": "87269a810f4a59d407d0e0efe58185e6",
#         "pid": pid,
#         "mobile": phone_number,
#         "author": "pay@noborders.net",
#         "cocode":country
#     }
#     payload = urlencode(payload)
#     full_url = url + payload
#     response = requests.post(url=full_url)
#     print(response.text)
#     return response


if __name__ == '__main__':
    # number = get_insta_number()
    # print(number)
    # aa = input('Enter :')

    # if aa == 1:
        # ban_number(number)
    # else:
    sms = get_insta_sms('85260544727')
        # print(sms)
    # input('Enter :')

    # import pdb;pdb.set_trace()