from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import random

PORTA = 34568
ua = UserAgent(
    browsers=['Chrome', 'Firefox', 'Edge', 'Opera'], 
    os=['Windows', 'Linux', 'Mac'],
    platforms=['desktop', 'mobile']
)

def setup_webdriver(url):
    """Função principal responsável pelas configurações e inicialização do webdriver."""

    options=webdriver.ChromeOptions()
    service=Service()

    options.add_argument("--no-sandbox") # desabilita o sandbox
    options.add_argument("--disable-dev-shm-usage") # desabilita o uso do /dev/shm contornando problemas de memoria
    options.add_argument("--disable-gpu") # desabilita a gpu 
    options.add_argument("--disable-extensions") # desabilita as extensoes do chrome
    options.add_argument("--disable-application-cache") # desabilita o cache do chrome
    options.add_argument("--start-maximized") # inicializa em tela cheia
    options.add_argument(f"user-agent={ua.random}") # randomiza o user agent com as definições do fake_useragent
    options.add_argument(f"--proxy-server=socks5://localhost:{PORTA}") # define o proxy para o socks5 na porta 34567

    # removedores de flag de automação
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 

    try:
        driver = webdriver.Chrome(options=options, service=service)
        driver.get(url)
        print(f"Webdriver iniciado na porta {PORTA}.")
        return driver

    except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {PORTA}: {e}')
        

def login_deezer(driver):
    """Função responsável por realizar login das contas."""

    email = "ximih60717@cotigz.com"
    password = "testespootify1"
    
    try:
        # aceitando cookies da pagina 
        accept_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gdpr-btn-accept-all"]')))
        accept_cookies.click()
        print("Nota sobre cookies encontrada e aceita.")

        switch_to_email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-testid="btn-switch-to-email"]')))
        switch_to_email.click()
        print("Mudado para login por email.")
    
        send_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@data-cy="input-field-email"]')))
        # iteração para simular digitação humana
        for char in email:
            send_email.send_keys(char)
            time.sleep(random.uniform(0.1, 0.55))

        print(f"Email {email} digitado.")

        send_pass = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@data-cy="input-field-password"]')))
        # iteração para simular digitação humana
        for char in password:
            send_pass.send_keys(char)
            time.sleep(random.uniform(0.1, 0.55))

        print("Senha digitada.")

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-testid="login-button"]')))
        login_button.click()
        print("Botão de login clicado. Aguardando redirecionamento para página principal.")

    except Exception as e:
        print(f"Procedimento de login não efetuado com sucesso: {e}")
        driver.quit()

if __name__ == "__main__":
    driver=setup_webdriver("https://account.deezer.com/pt-br/login/")
    login_deezer(driver)
    time.sleep(100)
