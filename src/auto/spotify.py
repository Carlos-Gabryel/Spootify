from selenium import webdriver
from selenium.webdriver.firefox.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import multiprocessing
import random

ua = UserAgent()

PORTAS = [34567, 34568, 34569, 34570]
CONTAS = ['wapasif996@birige.com', 'sejiv37959@dizigg.com', 'jemiho6565@infornma.com', 'yogak72926@motivue.com']

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

    # options.add_argument('-headless')
    
    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url)
        print(f"Webdriver iniciado na porta {porta}.\n")
        return driver
    
    except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {porta}\n')
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

        print(f"Login bem-sucedido e webplayer selecionado.")

    except Exception as e:
        print(f'Erro ao tentar fazer login na conta')

def buscar_playlist(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container'))).click() # fecha a barra de cookies
        print("Barra de cookies fechada")

    except:
        print("Barra de cookies não encontrada ou já fechada anteriormente, continuando...")
        pass

    # redireciona para playlist desejada
    # driver.get("https://open.spotify.com/playlist/6EmDufy5m126IOWrr8tCr9")
    # print("Redirecionado para página da playlist")

    # time.sleep(random.randrange(4, 8))
    # # dar play na playlist
    # try:
    #     play = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[5]/div/div[2]/div[2]/div/main/section/div[2]/div[2]/div[2]/div/div/div[1]/button")
    #     play.click()
    #     print("Playlist selecionada com sucesso")
    # except Exception as e:
    #     print(f"Erro ==> {e} <==")

def executar_bots(porta, conta):
    driver = setup_webdriver("https://accounts.spotify.com/en/login", porta)

    if driver:
        login_spotify(driver, conta)
        buscar_playlist(driver)
            
        musica_atual = ""
        contador_plays = 0

        #buscar a quantidade de musicas que tem na playlist
        # qtd_musicas = WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.XPATH, '//*[@id="main"]/div/div[2]/div[5]/div/div[2]/div[2]/div/main/section/div[1]/div[3]/div[3]/div/div[2]/span[1]'))
        # valor = int(qtd_musicas.text.replace(" músicas", ""))
        # print(f"Foram encontradas {valor} músicas na playlist.")

        # while driver:
        #     time.sleep(15)

        #     try:
        #         buscar_musica = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/footer/div/div[1]/div/div[2]/div[1]/div').text

        #         if buscar_musica != musica_atual:
        #             contador_plays+=1
        #             musica_atual = buscar_musica
        #             print(f"Nova faixa encontrada play número {contador_plays}")       

        #     except Exception as e:
        #         print(f'Erro ao buscar música: {e}')

if __name__ == "__main__":
    processos = []

    for porta, conta in zip(PORTAS, CONTAS):
        p = multiprocessing.Process(target=executar_bots, args= (porta, conta))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()
    
    
    
        
    
    
