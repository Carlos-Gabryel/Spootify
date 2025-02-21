from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyautogui
import time

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
        driver.find_element(By.ID, 'login-username').send_keys('testespootify1@gmail.com') #login input
        driver.find_element(By.ID, 'login-password').send_keys('spootify2025') #password input
        driver.find_element(By.ID, 'login-button').click() #botao clicavel de login
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/button[2]').click() #botao clicavel do webplayer
        
    except Exception as e:
        print('Erro ao tentar fazer login no spotify')

def find_playlist(driver):
    driver.find_element(By.XPATH, '//*[@id="global-nav-bar"]/div[2]/div/div[1]/span/div/form/div[2]/input').send_keys('.')
    
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
    