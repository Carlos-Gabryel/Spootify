from selenium import webdriver
from selenium.webdriver.firefox.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import multiprocessing

ua = UserAgent()

# 191.252.204.214 teste1
# 191.252.219.163 teste2

PORTAS = [34567, 34568]
CONTAS = ['wapasif996@birige.com', 'sejiv37959@dizigg.com']

# Configuração do WebDriver
def setup_webdriver(url, porta):
    service = Service() 
    options = webdriver.FirefoxOptions()

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
        print(f"Webdriver iniciado na porta {porta}.\n")
        return driver
    
    except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {proxy_port}\n')
        driver.quit()
        return None

def login_spotify(driver, email):
    try:
        # digitar email na pagina de login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'login-username'))
        ).send_keys(email)

        # digitar senha na pagina de login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login-password"]'))
        ).send_keys('testespootify1') 

        # clicar no botao de login após digitação de usuario e senha
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'login-button'))
        ).click() 

        # clica no botao webplayer para abrir a interface principal do spotify
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='web-player-link']"))
        ).click()

        print(f"Login bem-sucedido e webplayer selecionado no email: {1} da porta: {1}.")

    except Exception as e:
        print(f'Erro ao tentar fazer login na conta: {1} da porta: {1}')

def buscar_playlist(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container'))).click() # fecha a barra de cookies
        print("Barra de cookies fechada")

    except:
        print("Barra de cookies não encontrada ou já fechada anteriormente, continuando...")
        pass

    driver.get("https://open.spotify.com/playlist/6EmDufy5m126IOWrr8tCr9")

    # nome_playlist = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/span[2]/h1'))).text
    # print(f"Playlist {nome_playlist} encontrada e selecionada")

    # botao de play para iniciar musica
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='play-button']"))).click() 
    
def executar_bots(porta, conta):
    driver = setup_webdriver("https://accounts.spotify.com/en/login", porta)

    if driver:
        try:
            login_spotify(driver, conta)
            buscar_playlist(driver)
            
            musica_atual = ""
            contador_plays = 0

            # buscar a quantidade de musicas que tem na playlist
            qtd_musicas = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/div/div[2]/span[1]')
            valor = int(qtd_musicas.text.replace(" songs", ""))
            print(f"Foram encontradas {valor} músicas na playlist.")

            while driver:
                time.sleep(15)

                try:
                    buscar_musica = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/footer/div/div[1]/div/div[2]/div[1]/div').text

                    if buscar_musica != musica_atual:
                        contador_plays+=1
                        musica_atual = buscar_musica
                        print(f"Nova faixa encontrada play número {contador_plays} - [{{}}]")

                except Exception as e:
                    print(f'[{porta}] Erro ao buscar música: {e}')

            driver.quit()
        except Exception as e:
            print(f"[{porta}] Erro geral: {e} ")

if __name__ == "__main__":
    processos = []

    for porta, conta in zip(PORTAS, CONTAS):
        p = multiprocessing.Process(target=executar_bots, args=(porta, conta))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()
    
    
    
        
    
    
