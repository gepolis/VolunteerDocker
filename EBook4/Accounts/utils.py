import random
import time

import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from fake_useragent import UserAgent
import datetime

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Accounts.models import MosRuAuth
from django.conf import settings
ua = UserAgent()
user_agent = ua.ff
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")

if settings.SERV:
    #options.add_argument("--headless")
    #options.add_argument("--start-maximized")
    #options.add_argument("--disable-gpu")
    #options.add_argument("--no-sandbox")
    #options.add_argument("-disable-dev-shm-usage")
    pass
options.add_argument("--disable-blink-features=AutomationControlled")
selpath = "/home/gepolis/PycharmProjects/EBook4/Accounts/chromedriver"
if settings.SERV:
    selpath = "/root/Ebook1/chromedriver"

selpath = "/home/gepolis/Загрузки/geckodriver"


def get_random_proxy():
    f = open(f"{settings.PROXIES_PATH}", "r")
    lines = f.readlines()
    proxy = lines[random.randint(0, len(lines) - 1)]
    f.close()
    return proxy

def get_profile_data(user_login, user_password,uuid):

    db_obj = MosRuAuth.objects.get(uuid=uuid)
    db_obj.status = "wait"
    db_obj.save()
    start = datetime.datetime.now()
    opts = options

    opts.add_argument(f'--proxy-server={get_random_proxy()}')
    try:
        driver = webdriver.Chrome(options=opts,
                                  service=Service(
                                      executable_path=selpath
                                  )
                                  )
        t=1
    except Exception as e:
        print(e)
        db_obj.status = "error"
        db_obj.save()
        t=0


    if t ==1:
        driver.get(
            "https://login.mos.ru/sps/login/methods/password?bo=%2Fsps%2Foauth%2Fae%3Fresponse_type%3Dcode%26access_type"
            "%3Doffline%26client_id%3Ddnevnik.mos.ru%26scope%3Dopenid%2Bprofile%2Bbirthday%2Bcontacts%2Bsnils"
            "%2Bblitz_user_rights%2Bblitz_change_password%26redirect_uri%3Dhttps%253A%252F%252Fschool.mos.ru%252Fv3%252Fauth"
            "%252Fsudir%252Fcallback")
        print("-----------------------")
        print(driver.current_url)
        print("-----------------------------------")

        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.NAME, 'login')))
        #time.sleep(10)
        login = driver.find_element(By.NAME, "login")
        password = driver.find_element(By.NAME, "password")
        button = driver.find_element(By.ID, "bind")
        login.click()
        login.send_keys(user_login)
        password.click()
        password.send_keys(user_password)
        button.click()
        try:
            captcha = driver.find_element(By.CLASS_NAME, "formCaptcha__container")
            captcha_exists = True



        except:
            captcha_exists = False
            pass

        if captcha_exists:
            captcha = driver.find_element(By.CLASS_NAME, "formCaptcha__container")
            captcha_img = captcha.find_element(By.TAG_NAME, "img")
            captcha_url = captcha_img.get_attribute("src")
            db_obj.captcha = True
            db_obj.captcha_url = captcha_url
            db_obj.status="wait_captcha"
            db_obj.save()
        state = True
        timer = 15
        while state:
            if timer == 0:
                break
            if driver.current_url == "https://school.mos.ru/auth/callback":
                state = False

            timer -= 1
            time.sleep(1)
        if not state:
            token = driver.get_cookie("aupd_token")
            if token:
                token = token['value']
                data = requests.get(
                    "https://school.mos.ru/api/family/web/v1/profile",
                    headers={
                        "Authorization": f"{token}",
                        "Auth-Token": f"{token}",
                        "User-Agent": user_agent,
                        "X-mes-subsystem": "familyweb",
                    }
                )
                data = data.json()
                data["token"] = token
                driver.close()
            else:
                data = False

            if data:
                db_obj.token = data.get("token")
                db_obj.data = data
                db_obj.status = "success"
                db_obj.save()
            return data
        else:
            return False
