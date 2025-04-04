from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

porta = 34567
conta = 'doxex93700@bariswc.com'

# configuração do webdriver com Chrome
def setup_webdriver(url):
    service = Service()  
    options = Options()

    # configuracao do drm
    options.set_preference("media.eme.enabled", True)
    options.set_preference("media.gmp-widevinecdm.visible", True)
    options.set_preference("media.gmp-widevinecdm.enabled", True)
    options.set_preference("media.gmp-manager.updateEnabled", True)
    options.set_preference("media.gmp-provider.enabled", True)
    
    # configuracao do socks5
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", 'localhost')
    options.set_preference("network.proxy.socks_port", porta)
    options.set_preference("network.proxy.socks_version", 5) 
    options.set_preference("network.proxy.socks_remote_dns", True)
    
    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url)
        print(f"Webdriver iniciado na porta {porta}.")
        return driver

    except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {porta}: {e}')
        driver.quit()

def login_spotify(driver):
    try:
        digitar_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-username')))
        digitar_login.send_keys(conta)

        digitar_senha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password')))
        digitar_senha.send_keys('testespootify1')

        botao_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login-button')))
        botao_login.click()

        print(f"Login realizado com sucesso no email: {conta}")
    except Exception as e:
        print(f"Erro ao fazer login no Spotify {e}")
        driver.quit()

    try:
        # seleção de webplayer
        webplayer = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='web-player-link']")))
        webplayer.click()
    except Exception as e:
        print(f"PEGOU NAO ESSA PORRAAAA {e}")
        driver.quit()

def fechar_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container'))).click()
        print("Barra de cookies fechada")

    except:
        print("Barra de cookies não encontrada ou já fechada anteriormente, continuando...")

def buscar_playlist(driver):
    playlist_atual = ""

    try:

        playlist1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//li[@aria-posinset="1"]')))
        playlist1.click()

        time.sleep(10)
        dar_play = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="play-button"]')))
        dar_play.click()
        nome_playlist = dar_play.get_attribute('aria-label')
        print(f"Tocando atualmente: {nome_playlist.replace("Tocar", "")}")

        time.sleep(10)
        playlist2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//li[@aria-posinset="2"]')))
        playlist2.click()

    
   
    except Exception as e:
        print(f"Elemento não encontrado {e}")    


if __name__ == "__main__":
    driver = setup_webdriver("https://accounts.spotify.com/pt-BR/login")

    if driver:
        login_spotify(driver)
        fechar_cookies(driver)
        buscar_playlist(driver)
       
        # musica_atual = ""
        # contador_plays = 0

        # try:
        #     qtd_musicas = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@data-testid='now-playing-widget']"))
        #     )
        #     valor = int(qtd_musicas.text.replace(" músicas", ""))
        #     print(f"Foram encontradas {valor} músicas na playlist.")
        # except:
        #     valor = 0
        #     print("Não foi possível contar as músicas.")

        # while driver:
        #     time.sleep(15)
        #     try:
        #         buscar_musica = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/footer/div/div[1]/div/div[2]/div[1]/div').text

        #         if buscar_musica != musica_atual:
        #             contador_plays += 1
        #             musica_atual = buscar_musica
        #             print(f"Nova faixa encontrada, play número {contador_plays}")
        #     except Exception as e:
        #         print(f'Erro ao buscar música: {e}')
