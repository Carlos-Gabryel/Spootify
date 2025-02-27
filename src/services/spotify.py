from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36')
    options.add_argument('--headless')
    options.add_experimental_option('detach', True)
    
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
        web_player.click() # botao clicavel do webplayer[

        print('Login realizado com sucesso!')
        
    except Exception as e:
        print(f'Erro ao tentar fazer login no spotify {e}')

def find_playlist(driver):
    driver.find_element(By.XPATH, '//*[@id="global-nav-bar"]/div[2]/div/div[1]/span/div/form/div[2]/input').send_keys('.')
    cookies_bar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="onetrust-close-btn-container"]/button'))).click()
    set_playlist = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Desktop_LeftSidebar_Id"]/nav/div/div[1]/div[2]/div[2]/div/div/ul/div/div[2]/li/div/div/div[1]'))).click()
    playlist_img = driver.find_element(By.XPATH, '//*[@id="Desktop_LeftSidebar_Id"]/nav/div/div[1]/div[2]/div[2]/div/div[2]/ul/div/div[2]/li/div/div[3]/div/div/div[1]/img')
    playlist_name = playlist_img.get_attribute('alt')

    print(f'Playlist selecionada com sucesso!\n{playlist_name}')

if __name__ == "__main__":
    driver = config_webdriver("https://accounts.spotify.com/en/login")
    login_spotify(driver)
    time.sleep(2)
    find_playlist(driver)
    
