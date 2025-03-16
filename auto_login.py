# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005480DB4C7655137F465F9BF1F4BD46C077EFDF834464BC1454A4D50AFAFD2AAB6A7C4538E9E23AC22501B8EB1A1CC074EF96ECC4CFBFBCFACAD59EC522743C8BD23465F9D6AACB88DCDD31213E130CD24DAE4ACD97826009E185B4105418A1997829422059746C82FCC0CA0F9A671401DE50BE63844ED4EAC6530667A68BB9A4F91477A498C922FA3DEE1A927A7F8BA34529BD8A39261D5C9316202F43665B9BAEE56C0442B1DBE03869EEA885CFC273F83306DEB33B3E87FEEFA146DCBB8522E719526BB88046E587A6FE10E56BE90046259FAA470805D38B86ECA3C85D47EA23D5E9B772DD008B98DE73D988C2216E2C03B39924626A5FC0EC936DD6BE0D0EF3D073D446EB494CD8106101FD45ED865DE8E9FDCB64B76EED8A65C3EC1CCCBF5801B7354D15EDD9EFB67D45916C82DF1D394E048E53AEDF23F287C08CF9B3E3875A23299E702D0EF2BC33171EE68F4BF39A4F7DE91A77587A5BE0D7EC27D90C"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
