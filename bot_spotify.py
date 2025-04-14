from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import multiprocessing
import time
import random
import gc

def funcao_principal(porta, conta):
    driver = setup_webdriver("https://accounts.spotify.com/pt-BR/login", porta)

    if driver:
        login_spotify(driver, conta)
        fechar_cookies(driver)
        time.sleep(random.uniform(1, 4))
        random_behavior(driver)
        time.sleep(random.uniform(5, 10))
        
        musica_atual = ""
        contador_plays = 0

        playlists = ["Brisa Pernambucana", "Entre o Pop e a Poesia"]

        while True: 
            try:
                # tocar playlist1 
                tocar_playlist(driver, "Entre o Pop e a Poesia")
                inicio_playlist1 = time.time()

                while time.time() - inicio_playlist1 < random.uniform(3300, 3600): # loop com variacao de tempo entre 55 a 60min
                    time.sleep(15)
                    try:
                        buscar_musica = driver.find_element(By.CSS_SELECTOR, '[data-testid="now-playing-widget"]').text
                        buscar_musica = buscar_musica.replace("Tocando agora", "").strip()

                        if buscar_musica != musica_atual:
                            contador_plays += 1
                            musica_atual = buscar_musica
                            print(f"Nova faixa encontrada play: {contador_plays}")
                    except Exception as e:
                        print(f'Erro ao buscar música na Playlist 1: {e}')
                  
                # tocar Playlist 2
                gc.collect()
                tocar_playlist(driver, "Brisa Pernambucana")
                print("Tocando Playlist 2...")
                inicio_playlist2 = time.time()

                while time.time() - inicio_playlist2 < random.uniform(3300, 3600): # loop com variacao de tempo entre 55 a 60min
                    time.sleep(15)
                    try:
                        buscar_musica = driver.find_element(By.CSS_SELECTOR, '[data-testid="now-playing-widget"]').text
                        buscar_musica = buscar_musica.replace("Tocando agora", "").strip()

                        if buscar_musica != musica_atual:
                            contador_plays += 1
                            musica_atual = buscar_musica
                            print(f"Nova faixa encontrada play: {contador_plays}")
                    except Exception as e:
                        print(f'Erro ao buscar música na Playlist 2: {e}')

            except Exception as e:
                print(f"Erro no loop principal: {e}")
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
    # options.add_argument("-headless")
    
    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url)
        print(f"Webdriver iniciado na porta {porta}.")
        return driver

    except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {porta}: {e}')
        driver.quit()

def login_spotify(driver, conta):
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

        print(f"Login realizado com sucesso no email: {email}")
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

def tocar_playlist(driver, nome_playlist):
    try:
        # Clica na playlist com base no nome
        playlist = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f'//li[.//span[contains(text(), "{nome_playlist}")]]')))
        playlist.click()
        print(f"Playlist encontrada: {nome_playlist}")

        time.sleep(10)
        botao_play = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((
                By.XPATH,  f'//div[@data-testid="action-bar"]//button[@data-testid="play-button" and contains(@aria-label, "Tocar {nome_playlist}")]'
                )))
        botao_play.click()
        
    except Exception as e:
        print(f"Erro ao dar play na playlist '{nome_playlist}': {e}")

def random_behavior(driver):
    action = random.randint(2, 3)

    if action == 2:
        try:
            button_profile = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='user-widget-link']")))
            button_profile.click()
            time.sleep(random.uniform(2.1, 5.4))

            config_button = driver.find_element(By.XPATH, '//a[span[text()="Configurações"]]')
            config_button.click()

        except Exception as e:
            print(f"Erro na ação 2: {e}")
   
    elif action == 3:
        try:
            # clicar na barra de busca
            search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="search-input"]'))
            )
            time.sleep(random.uniform(1.2, 4.5))

            # digitar o artista/gênero aleatório
            chave = random.choice([
                "funk", "Sertanejo", "Pagode", "rap", "Rock", "mpb", "Eletrônica",
                "Caetano Veloso", "Djavan", "Legião Urbana", "Luan Santana",
                "Marília Mendonça", "Guilherme Arantes", "Gilberto Gil", "Elis Regina",
                "Anitta", "Ivete Sangalo", "Wesley Safadão", "Zezé Di Camargo",
                "Chitãozinho e Xororó", "Fernando e Sorocaba", "Bruno e Marrone",
                "Jorge e Mateus", "Henrique e Juliano", "Matheus e Kauan",
                "Maiara e Maraisa", "Joyce Alane", "Ana Carolina", "Adriana Calcanhotto",
                "Maria Gadú", "Ana Vilela", "Ana Cañas", "Piseiro", "Forró",
                "Samba", "Bossa Nova", "Rock Nacional", "Rock Internacional",
                "Pop Nacional", "Pop Internacional", "João Gomes", "João Neto e Frederico",
                "João Bosco e Vinícius", "João Carlos", "João do Morro", "João e Rafael",
                "The Score", "The Killers", "The Strokes"
            ])

            print(f"Buscando por: {chave}")
            # aguardar e digitar na caixa de busca
            for char in chave:
                search_input.send_keys(char)
                time.sleep(random.uniform(0.1, 0.4))

            # melhoria => selecionar card ou ouvir musica aleatoria da tela 

        except:
            print("Nenhuma música clicável encontrada ou card não tinha faixa")


if __name__ == "__main__":
    portas = [34568, 34571, 35002]
    contas = [
        ('vopaje2986@oronny.com', 'testespootify1'),
        ('vadaraj698@movfull.com', 'testespootify1'),
        ('tifose9833@movfull.com', 'testespootify1')
    ]

    processos = []
   
    for porta, conta in zip(portas, contas):
        p = multiprocessing.Process(target=funcao_principal, args=(porta, conta))
        processos.append(p)
        p.start()
    
    for p in processos:
        p.join()
    print("Todos os processos foram concluídos.")

