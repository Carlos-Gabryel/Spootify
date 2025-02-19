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
        print(f'Erro ao iniciar o webdriver com o proxy especificado')
        return None

def login_amazon(driver):
    sign_in_button = pyautogui.moveTo(1815, 228, 2)
    pyautogui.click()
    time.sleep(2)
    email_input = driver.find_element(By.XPATH, '//*[@id="ap_email"]').send_keys('testespootify1@gmail.com')
    continue_button = driver.find_element(By.XPATH, '//*[@id="continue"]').click()
    time.sleep(2)
    password_input = driver.find_element(By.XPATH, '//*[@id="ap_password"]').send_keys('spootify2025')
    login_button = driver.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()

def find_playlist(driver):
    time.sleep(2)
    pyautogui.moveTo(743, 152, 2)
    pyautogui.moveTo(743, 220, 2)
    pyautogui.click()
    pyautogui.moveTo(116, 317, 2)
    pyautogui.click()
    

if __name__ == "__main__":
    driver = config_webdriver('https://music.amazon.com.br/')
    pyautogui.moveTo(1870, 151, 2)
    pyautogui.click()
    wait = WebDriverWait(driver, 10)
    login_amazon(driver)
    find_playlist(driver)
    
    
