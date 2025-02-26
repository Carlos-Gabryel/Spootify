from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
from dotenv import load_dotenv
import os

load_dotenv()
USER_NAME=os.getenv('USER_NAME')
PASSWORD=os.getenv('PASSWORD')

# proxie_options = {
#     'proxy': {
#         'http': 'socks5://127.0.0.1:9050',
#         'https': 'socks5://127.0.0.1:9050',
#         'no_proxy':'localhost,127.0.0.1'
#     }
# }

def config_webdriver(url):
    service = Service() 
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_argument('--start-maximized')

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        return driver
    except Exception as e:
        print(f'Erro ao iniciar o webdriver')
        return None

def login_spotify(driver):
    
    try:
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-username')))
        username.send_keys(USER_NAME) # user input

        password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password')))
        password.send_keys(PASSWORD) # password input

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login-button')))
        login_button.click() # botao clicavel de login

        web_player = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div/button[2]')))
        web_player.click() # botao clicavel do webplayer
        
    except Exception as e:
        print(f'Erro ao tentar fazer login no spotify {e}')

def find_playlist(driver):
    
    pyautogui.moveTo(49, 293, 1)
    pyautogui.click()
    pyautogui.moveTo(198, 456, 1)
    pyautogui.click()
    pyautogui.moveTo(1864, 976, 1)
    pyautogui.click()
    pyautogui.moveTo(518, 595, 1)
    pyautogui.click()

if __name__ == "__main__":
    driver = config_webdriver("https://accounts.spotify.com/en/login")
    login_spotify(driver)
    driver.find_element(By.XPATH, '//*[@id="global-nav-bar"]/div[2]/div/div[1]/span/div/form/div[2]/input').send_keys('.')
    time.sleep(2)
    find_playlist(driver)
    
