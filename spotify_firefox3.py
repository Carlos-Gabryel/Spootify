from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import multiprocessing
import subprocess
from fake_useragent import UserAgent
import time
import random
import gc

ua = UserAgent(
    browsers=['Chrome', 'Firefox', 'Edge', 'Opera'], 
    os=['Windows', 'Linux', 'Mac'],
    platforms=['desktop', 'mobile']
)

def funcao_principal(porta, conta):
    driver = setup_webdriver("https://accounts.spotify.com/pt-BR/login", porta)

    if driver:
        login_spotify(driver, conta, porta)

        try:
            fechar_iframeOfertas(driver, porta)
        except: 
            print(f"Banner de ofertas não encontrado {porta}")
            pass

        fechar_cookies(driver)
        time.sleep(random.uniform(1, 4))
        
        musica_atual = ""
        contador_plays = 0

        while True:
            try:
                fechar_iframeOfertas(driver)
            except: 
                print(f"Banner de ofertas não encontrado {porta}.")
                pass
            
            time.sleep(15)
            try:
                # tocar playlist1 
                tocar_playlist(driver, "Léo Foguete 2025  🚀 As Melhores | Obrigado Deus | Última Noite | Cópia Proibida | Quem de Nós Dois")
                print(f"Tocando Playlist 1... {porta}")
                inicio_playlist1 = time.time()

                while time.time() - inicio_playlist1 < random.uniform(3300, 3600): # looping com variacao de tempo para trocar de playlist
                    time.sleep(15)

                    try:
                        buscar_musica = driver.find_element(By.CSS_SELECTOR, '[data-testid="now-playing-widget"]').text
                        buscar_musica = buscar_musica.replace("Tocando agora", "").strip()
                        if buscar_musica != musica_atual:
                            contador_plays += 1
                            musica_atual = buscar_musica
                            print(f"Nova faixa encontrada play {porta}: {contador_plays}")
                    except Exception as e:
                                print(f'Erro ao buscar música na Playlist 1 ({porta}) {e}')

                # tocar Playlist 2
                try:
                    gc.collect()
                    print(f"Garbage collector limpo! {porta}")
                except:
                    print(f"Erro ao limpar o garbage collector {porta}")
                
                tocar_playlist(driver, "PURO SUCO DO BRASIL")
                print(f"Tocando Playlist 2 {porta}...")
                inicio_playlist2 = time.time()

                while time.time() - inicio_playlist2 < random.uniform(50, 60): # loop com variacao de tempo entre 55 a 60min
                    time.sleep(15)
                    try:
                        buscar_musica = driver.find_element(By.CSS_SELECTOR, '[data-testid="now-playing-widget"]').text
                        buscar_musica = buscar_musica.replace("Tocando agora", "").strip()

                        if buscar_musica != musica_atual:
                            contador_plays += 1
                            musica_atual = buscar_musica
                            print(f"Nova faixa encontrada play {porta} {contador_plays}")
                    except Exception as e:
                        print(f'Erro ao buscar música na Playlist 2 {porta}{e}')

            except Exception as e:
                print(f"Erro no loop principal {porta} {e}")
                break

# configuração do webdriver com Chrome
def setup_webdriver(url, porta):
    service = Service()  
    options = Options()

    # Configuração do DRM
    options.set_preference("media.eme.enabled", True)
    options.set_preference("media.gmp-widevinecdm.visible", True)
    options.set_preference("media.gmp-widevinecdm.enabled", True)
    options.set_preference("media.gmp-manager.updateEnabled", True)
    options.set_preference("media.gmp-provider.enabled", True)
    
    # Configuração do SOCKS5
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", 'localhost')
    options.set_preference("network.proxy.socks_port", porta)
    options.set_preference("network.proxy.socks_version", 5) 
    options.set_preference("network.proxy.socks_remote_dns", True)
    options.add_argument("-headless")
    
    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url)
        print(f"Webdriver iniciado na porta {porta}.")
        return driver

    except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {porta}: {e}')
        driver.quit()

def login_spotify(driver, conta, porta):
    try:
        email, senha = conta
        digitar_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-username')))

        for char in email:
            digitar_login.send_keys(char)
            time.sleep(random.uniform(0.1, 0.4))

        digitar_senha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password')))
        for char in senha:
            digitar_senha.send_keys(char)
            time.sleep(random.uniform(0.1, 0.4))

        botao_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login-button')))
        botao_login.click()

        print(f"Login realizado com sucesso no email: {email} na porta {porta}")
    except Exception as e:
        print(f"Erro ao fazer login no Spotify {e}")
        driver.quit()

    try:
        # seleção de webplayer
        webplayer = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='web-player-link']")))
        webplayer.click()
    except Exception as e:
        print(f"PEGOU NAO ESSA PORRAAAA {e}")

def tocar_playlist(driver, nome_playlist):
    try:
        # Clica na playlist com base no nome
        playlist = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f'//div[@aria-label="Sua Biblioteca"]//div[@role="row" and .//button[contains(@aria-label, "Tocar {nome_playlist}")]]'
                )))
        playlist.click()
        print(f"Playlist encontrada: {nome_playlist}")
    except:
        print(f"Webdriver não conseguiu selecionar a playlist {nome_playlist}")

    time.sleep(10)
    try:
        botao_play = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((
                By.XPATH, f'//div[@aria-label="Sua Biblioteca"]//div[@role="group" and @data-encore-id="listRow"]//button[@data-encore-id="buttonTertiary" and @aria-label="Tocar {nome_playlist}"]'
                )))
        botao_play.click()
        print(f"Playlist '{nome_playlist}' tocada com sucesso.")
    
    except Exception as e:
        print(f"Erro ao dar play na playlist{nome_playlist} => {e} <=")

def fechar_iframeOfertas(driver, porta):
    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//html[@dir="auto"]//button[@data-click-to-action-action="DISMISS"]'))).click()
        print(f"Banner de ofertas fechado {porta}")

    except:
        print(f"Banner de ofertas não encontrado {porta}.")

def fechar_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container'))).click()
        print("Barra de cookies fechada")

    except:
        print("Barra de cookies não encontrada ou já fechada anteriormente, continuando...")

if __name__ == "__main__":
    
    caminho_tuneis = "C:/Users/Spootify/dev/Spootify/scripts-tuneis/tuneis_firefox3.sh"

    try:
        print("Iniciando tuneis SSH...")
        subprocess.run(["bash", caminho_tuneis], check=True)
        print("Túneis SSH iniciados com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao iniciar os túneis SSH: {e}")
        exit(1)

    portas = [
        35555, 35557, 35558, 35559
        ]
    # 35556,
    contas = [
        ("bokehox847@hazhab.com", "testespootify1"),
        # ("mocal26211@inkight.com", "testespootify1"), # conta banida
        ("hipat16822@magpit.com", "testespootify1"),
        ("tagava8450@bamsrad.com", "testespootify1"),
        ("vehape5044@daupload.com", "testespootify1")
        ]

    processos = []

    for porta, conta in zip(portas, contas):
        p = multiprocessing.Process(target=funcao_principal, args=(porta, conta))
        processos.append(p)
        p.start()
    
    for p in processos:
        p.join()
    print("Todos os processos foram concluídos.")

