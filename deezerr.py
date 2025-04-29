from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from fake_useragent import UserAgent
import time
import random

ua = UserAgent(
        browsers=['Chrome', 'Firefox', 'Edge', 'Opera'], 
        os=['Windows', 'Linux', 'Mac'],
        platforms=['desktop', 'mobile']
    )

# ssh -D 34567 -N -q -f root@191.252.38.91
PORTA = 34567

"""
Este bot utiliza o firefox na inicialização do seu webdriver
"""


def setup_webdriver(url):
    """Função principal responsável pelas configurações e inicialização do webdriver."""

    options=Options()
    service=Service()

    # configurações de instalação do widevine (server para o funcionamneto do DRM)
    options.set_preference("media.eme.enabled", True)
    options.set_preference("media.gmp-widevinecdm.visible", True)
    options.set_preference("media.gmp-widevinecdm.enabled", True)
    options.set_preference("media.gmp-manager.updateEnabled", True)
    options.set_preference("media.gmp-provider.enabled", True)

    # configurações de proxys e rede
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", 'localhost')
    options.set_preference("network.proxy.socks_port", PORTA)
    options.set_preference("network.proxy.socks_version", 5) 
    options.set_preference("network.proxy.socks_remote_dns", True)
    
    # configurações gerais
    options.set_preference("useAutomationExtension", False)
    options.set_preference("general.useragent.override", ua.random)
    # options.add_argument("-headless")  # executar firefox no modo headless

    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url)
        print(f"Webdriver iniciado na porta {PORTA}.")
        return driver
    
    except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {PORTA}: {e}')
        driver.quit()

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
            time.sleep(random.uniform(0.2, 0.5))

        print(f"Email {email} digitado.")

        send_pass = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@data-cy="input-field-password"]')))
        # iteração para simular digitação humana
        for char in password:
            send_pass.send_keys(char)
            time.sleep(random.uniform(0.2, 0.5))

        print("Senha digitada.")

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-testid="login-button"]')))
        login_button.click()
        print("Login bem-sucedido.")

    except Exception as e:
        print(f"Procedimento de login não efetuado com sucesso: {e}")
        driver.quit()

if __name__ == "__main__":
    driver=setup_webdriver("https://account.deezer.com/pt-br/login/")
    login_deezer(driver)
