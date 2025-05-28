import json
import time
import random
import multiprocessing
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_webdriver(porta):
    service = Service()
    options = Options()
    # Configura proxy SOCKS5
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", "localhost")
    options.set_preference("network.proxy.socks_port", porta)
    options.set_preference("network.proxy.socks_version", 5)
    options.set_preference("network.proxy.socks_remote_dns", True)

    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://accounts.spotify.com/pt-BR/login")
    return driver
def login_spotify(driver, conta):
    email, senha = conta
    # Exemplificação: ajustar seletores conforme necessidade
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-username'))).send_keys(email)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password'))).send_keys(senha)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login-button'))).click()
    # Aguarda redirecionamento ao webplayer
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='web-player-link']"))).click()
def tocar_playlist(driver, nome_playlist="PURO SUCO DO BRASIL"):
    # Ajustar XPath ou CSS conforme layout
    playlist = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((
            By.XPATH,
            f"//button[contains(@aria-label, 'Tocar {nome_playlist}')]"
        ))
    )
    playlist.click()


def logout_spotify(driver):
    driver.get("https://accounts.spotify.com/pt-BR/logout")
    time.sleep(2)
def worker(porta, contas):
    index = 0
    while True:
        conta = contas[index]
        print(f"[Porta {porta}] Ciclo conta: {conta[0]}")
        driver = setup_webdriver(porta)
        try:
            login_spotify(driver, conta)
            tocar_playlist(driver)
            # Espera randômico entre 5 e 10 minutos
            wait_time = random.uniform(300, 310)
            print(f"[Porta {porta}] Aguardando {wait_time/60:.2f} minutos")
            time.sleep(wait_time)
        except Exception as e:
            print(f"[Porta {porta}] Erro: {e}")
        finally:
            logout_spotify(driver)
            driver.quit()
            print(f"[Porta {porta}] Driver encerrado. Alternando conta.")
            # Próxima conta
            index = (index + 1) % len(contas)
            # Pequena pausa antes de reabrir
            time.sleep(5)
if __name__ == '__main__': 
    with open('config.json') as f:
        config = json.load(f)

    processos = []
    for porta_str, cfg in config.items():
        porta = int(porta_str)
        contas = cfg['contas']
        p = multiprocessing.Process(target=worker, args=(porta, contas))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()