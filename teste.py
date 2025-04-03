from gerenciador_tuneis import verificar_e_recriar_tunel
from selenium import webdriver
from selenium.webdriver.firefox.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import multiprocessing
import random

# ps aux | grep ssh | awk '{print $1}' | xargs kill -9 (bash para tirar todos os tuneis de uma só vez)

ua = UserAgent()

PORTAS = (34567, 34568, 34569, 34570, 34571, 35000, 35001, 35002, 35003)

IPS = (
    "191.252.38.73", "191.252.38.74", "191.252.38.75",
    "191.252.38.78", "191.252.38.79", "191.252.38.84",
    "191.252.38.86", "191.252.38.88", "191.252.38.93"
)

CONTAS = (
'vopaje2986@oronny.com',
'tiham93205@deenur.com',
'jemiho6565@infornma.com',
'yogak72926@motivue.com',
'gewepo9698@oronny.com',
'wapasif996@birige.com',
'sejiv37959@dizigg.com',
'vobopo1052@macho3.com',
'niratem674@macho3.com'
)

SENHA = "testespootify1"

# Configuração do WebDriver
def setup_webdriver(url, porta, ip):
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
        print(f'Erro ao iniciar o webdriver na porta {porta}. Reiniciando o túnel...')
        verificar_e_recriar_tunel(porta, ip)
        
        try:
            driver = webdriver.Firefox(service=service, options=options)
            driver.get(url)
            print(f"Webdriver reiniciado na porta {porta}.")
            return driver
        except Exception:
            print(f"Falha ao reiniciar WebDriver na porta {porta}.")
            driver.quit()
            return None

def login_spotify(driver, email):

    try:
        # digitar email na pagina de login
        digitar_email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'login-username'))
        )
        for char in email:
            digitar_email.send_keys(char)
            time.sleep(random.uniform(0.2, 0.7))

        # digitar senha na pagina de login
        digitar_senha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="login-password"]'))
        )
        for char in SENHA:
            digitar_senha.send_keys(char)
            time.sleep(random.uniform(0.2, 0.7))

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

    time.sleep(3)
    # redireciona para playlist desejada
    driver.get("https://open.spotify.com/playlist/1sIOdW3sClje78CM4SlAZM")
    print("Redirecionado para página da playlist")

    time.sleep(random.randrange(5, 8))
    try:
        nome_playlist = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[5]/div/div[2]/div[1]/div/main/section/div[1]/div[3]/div[3]/span[2]/h1")
    except Exception as e:
        print("Não foi possível identificar o nome da playlist.")

    try:
        play = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='play-button']")))
        play.click()
        print(f"Reproduzindo a playlist -> {nome_playlist.text}")
    except Exception as e:
        print(f"Erro ao tentar iniciar a playlist.")

def executar_bots(porta, ip, conta):
    driver = setup_webdriver("https://accounts.spotify.com/pt-BR/login", porta, ip)

    if driver:
        login_spotify(driver, conta)
        buscar_playlist(driver)
            
        musica_atual = ""
        contador_plays = 0

        #buscar a quantidade de musicas que tem na playlist
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

if __name__ == "__main__":
    processos = []

    for porta, ip, conta in zip(PORTAS, IPS, CONTAS):
        p = multiprocessing.Process(target=executar_bots, args= (porta, ip, conta))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()
    
    
    
        
    
    
