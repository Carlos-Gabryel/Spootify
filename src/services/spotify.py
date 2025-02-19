from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyautogui
import time

PROXY_HOST = "brd.superproxy.io"
PROXY_PORT = "33335"
PROXY_USER = "brd-customer-hl_7a3a36a2-zone-residential_proxy1"
PROXY_PASS = "8r39pf270ihp"

PROXY = f"{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

def config_webdriver(url):
    service = Service() 
    options = webdriver.ChromeOptions()
    
    options.add_experimental_option('detach', True)
    options.add_argument('--start-maximized')
    options.add_argument('--proxy-server=%s' % PROXY)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        return driver
    except Exception as e:
        print(f'Erro ao iniciar o webdriver com o proxy especificado')
        return None

def login_spotify(driver):
    username_input=driver.find_element(By.XPATH, '//*[@id="login-username"]').send_keys('testespootify1@gmail.com')
    password_input=driver.find_element(By.XPATH, '//*[@id="login-password"]').send_keys('spootify2025')
    login_submit=driver.find_element(By.XPATH, '//*[@id="login-button"]/span[1]').click()
    time.sleep(2)
    web_player_click=driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/button[2]/span[2]').click()

def find_playlist(driver):
 
    search_input=driver.find_element(By.XPATH, '//*[@id="global-nav-bar"]/div[2]/div/div[1]/span/div/form/div[2]/input').send_keys('.')

    time.sleep(2)
    pyautogui.moveTo(49, 293, 1)
    pyautogui.click()
    pyautogui.moveTo(198, 456, 1)
    pyautogui.click()
    pyautogui.moveTo(1864, 976, 1)
    pyautogui.click()
    pyautogui.moveTo(518, 595, 1)
    pyautogui.click()


if __name__ == "__main__":
    driver = config_webdriver('https://accounts.spotify.com/en/login')
    login_spotify(driver)
    time.sleep(2)
    find_playlist(driver)
    