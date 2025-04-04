from selenium import webdriver
from selenium.webdriver.firefox.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import random

ua = UserAgent()

porta = 34567
conta = 'doxex93700@bariswc.com'

# configuracao do webdriver
def setup_webdriver(url):
    service = Service() 
    options = webdriver.FirefoxOptions()

    # configuracao para forçar atualizado do widevine
    options.set_preference("media.eme.enabled", True)
    options.set_preference("media.gmp-widevinecdm.visible", True)
    options.set_preference("media.gmp-widevinecdm.enabled", True)
    options.set_preference("media.gmp-manager.updateEnabled", True)
    options.set_preference("media.gmp-provider.enabled", True)
    options.add_argument("--start-maximized")
    
    # configuracao do socks5
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", 'localhost')
    options.set_preference("network.proxy.socks_port", porta)
    options.set_preference("network.proxy.socks_version", 5) 
    options.set_preference("network.proxy.socks_remote_dns", True)
    # options.add_argument('-headless')
    
    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url)
        print(f"Webdriver iniciado na porta {porta}.")
        return driver
    
    except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {porta}.')
        driver.quit()

def login_spotify(driver):

    try:
        # digitar email na pagina de login
        digitar_email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'login-username'))
        ).send_keys(conta)

        # digitar senha na pagina de login
        digitar_senha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'login-password'))
        ).send_keys('testespootify1')   

        # clicar no botao de login após digitação de usuario e senha
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'login-button'))
        ).click()

        print("Login bem sucedido!")

        try:
        # clica no botao webplayer para abrir a interface principal do spotify
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='web-player-link']"))
            ).click()

            print("Webplayer selecionado, seguindo para playlists...")
        except:
            print("Webplayer não encontrado, devido a recaptcha")

    except Exception as e:
        print(f'Erro ao tentar fazer login na conta')
        driver.quit()

def buscar_playlist(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container'))).click() # fecha a barra de cookies
        print("Barra de cookies fechada")

    except:
        print("Barra de cookies não encontrada ou já fechada anteriormente, continuando...")
        pass

    # da play na primera playlist
    botao_play = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/div[3]/nav/div/div[1]/div[2]/div[1]/div/div[2]/ul/div/div[2]/li[1]/div/div[1]')))
    botao_play.click()

    time.sleep(5)
    try:
        play = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='play-button']")))
        play.click()
        print(f"Reproduzindo a playlist.")
    except Exception as e:
        print(f"Erro ao tentar iniciar a playlist.")

if __name__ == "__main__":
    driver = setup_webdriver("https://accounts.spotify.com/pt-BR/login")

    if driver:
        login_spotify(driver)
        buscar_playlist(driver)
            
        musica_atual = ""
        contador_plays = 0

        # buscar a quantidade de musicas que tem na playlist
        qtd_musicas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='now-playing-widget']")))
        valor = int(qtd_musicas.text.replace(" músicas", ""))
        print(f"Foram encontradas {valor} músicas na playlist.")

        while driver:
            time.sleep(15)

            try:
                buscar_musica = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/footer/div/div[1]/div/div[2]/div[1]/div').text

                if buscar_musica != musica_atual:
                    contador_plays+=1
                    musica_atual = buscar_musica
                    print(f"Nova faixa encontrada play número {contador_plays}")

            except Exception as e:
                print(f'Erro ao buscar música: {e}')
    
    
