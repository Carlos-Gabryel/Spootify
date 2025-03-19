from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def config_webdriver(url):
    service = Service() 
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('start-maximized')
    # options.add_argument('--headless')
    options.add_experimental_option('detach', True)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        return driver
    except Exception as e:
        print(f'Erro ao iniciar o webdriver com o proxy especificado')
        return None

def login_amazon(driver):
    digitar_email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'ap_email'))
        )
    digitar_email.send_keys('testespootify1@gmail.com')

    botao_continuar = driver.find_element(By.ID, 'continue').click()

    digitar_senha = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'ap_password'))
        )
    digitar_senha.send_keys('spootify2025')

    botao_login = driver.find_element(By.ID, 'signInSubmit').click()

def selecionar_playlist(driver):
    time.sleep(4)
    botao_biblioteca = driver.find_element(By.XPATH, "//button[@aria-label='Biblioteca']")
    botao_biblioteca.click()
    # time.sleep(2)
    # botao_musicas =driver.find_element(By.ID, 'contextMenuOption1')
    # botao_musicas.click()

if __name__ == "__main__":
    driver = config_webdriver('https://music.amazon.com.br/')
    time.sleep(2)
    botao_fazer_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "signInButton"))).click()
    login_amazon(driver)
    time.sleep(2)
    selecionar_playlist(driver)
    
    
    
