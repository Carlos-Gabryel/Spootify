from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    botao_fazer_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signInButton"]'))).click()
    digitar_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ap_email"]'))).send_keys('testespootify1@gmail.com')
    botao_continuar = driver.find_element(By.XPATH, '//*[@id="continue"]').click()
    digitar_senha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ap_password"]'))).send_keys('spootify2025')
    botao_login = driver.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()

# def selecionar_playlist(driver):
#     clicar_biblioteca = WebDriverWait(driver, 10).until(EC.element_to_be_selected((By.XPATH, "//*[@id="contextMenuHoverButton"]//button")))

if __name__ == "__main__":
    driver = config_webdriver('https://music.amazon.com/')
    login_amazon(driver)
    
    
    
