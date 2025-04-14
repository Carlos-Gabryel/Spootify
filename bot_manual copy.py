from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import gc

porta = 35556
conta = 'capiva5647@buides.com'

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
    # options.add_argument("-headless")
    
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

        for char in conta:
            digitar_login.send_keys(char)
            time.sleep(random.uniform(0.1, 0.4))

        digitar_senha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password')))
        for char in 'testespootify1':
            digitar_senha.send_keys(char)
            time.sleep(random.uniform(0.1, 0.4))

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
   
if __name__ == "__main__":
    driver = setup_webdriver("https://accounts.spotify.com/pt-BR/login")

    if driver:
        login_spotify(driver)
        fechar_cookies(driver)

        musica_atual = ""
        contador_plays = 0


        while True: 
            try:
                # tocar Playlist 1
                gc.collect()
                driver.delete_all_cookies()

                tocar_playlist(driver, "Brisa Pernambucana")
                inicio_playlist1 = time.time()

                while time.time() - inicio_playlist1 < 55 * 60: # loop por 55 minutos
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
                tocar_playlist(driver, "Entre o Pop e a Poesia")
                print("Tocando Playlist 2...")
                inicio_playlist2 = time.time()

                while time.time() - inicio_playlist2 < 55 * 60: 
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

def random_behavior (driver):
    action = random.randint(1, 5)

    if action == 1:
        # apos logar, clicar no botao home e selecionar algum card
        print ("Ação 1 selecionada")
        try:
            driver.get("https://www.spotify.com/")
            time.sleep(random.uniform(5.7, 10.2))

            for _ in range(random.randint(3,6)):
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(random.uniform(1.3, 5.5))

            # clicar em algum card de alguma seção
            card = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='card']")))

            card.click()
            print("Clicou no card")

        except Exception as e:
            print(f"Erro na ação 1: {e}")

    elif action == 2:
        # clica no perfil do usuario e depois em configuracoes e em seguida, rola a página e volta para a playlist
        print ("Ação 2 selecionada")
        try:
            button_profile = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='user-widget']")))
            button_profile.click()
            time.sleep(random.uniform(4.2, 8.5))

            for _ in range(random.randint(4,9)):
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(random.uniform(2.4, 6.9))
                
            driver.back()
            print("Voltou para a playlist")
            time.sleep(random.uniform(3.1, 7.8))

        except Exception as e:
            print(f"Erro na ação 2: {e}")

    elif action == 3:
        # Ação 3: fazer busca por um artista/gênero aleatório, clicar em algum card, escutar uma música e sair
        print("Ação 3 selecionada")
        try:
            # clicar na barra de busca
            buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='search-button']"))
            )
            buscar.click()
            time.sleep(random.uniform(3.1, 7.8))

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
            campo_busca = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "input"))
            )
            for char in chave:
                campo_busca.send_keys(char)
                time.sleep(random.uniform(0.1, 0.4))

            time.sleep(random.uniform(2.5, 4.0))

            # clicar no primeiro card de resultado
            card = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='card']"))
            )
            card.click()
            print("Entrou no card do resultado")
            time.sleep(random.uniform(4.9, 7.3))

            # tentar tocar uma faixa se estiver disponível
            try:
                musica = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tracklist-row']"))
                )
                musica.click()
                print("Tocando uma música aleatória do resultado")
                time.sleep(random.uniform(10, 20))  # escuta um pouco antes de sair
            except:
                print("Nenhuma música clicável encontrada ou card não tinha faixa")

            # volta para a tela anterior
            driver.back()
            time.sleep(random.uniform(2.1, 4.2))

        except Exception as e:
            print(f"Erro na ação 3: {e}")

    elif action == 4:
    # acao 4: comportamento humano fora do player - exploração casual do app
        print("Comportamento aleatório 4: explorando o Spotify como um humano curioso...")

        try:
            # ir para a aba de busca
            botao_busca = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='search-button']"))
            )
            botao_busca.click()
            print("Entrou na aba de busca.")
            time.sleep(random.uniform(3.2, 5.1))

            # rolar pela aba de busca como se estivesse explorando gêneros
            corpo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']"))
            )

            for _ in range(random.randint(2, 4)):
                scroll_px = random.randint(200, 600)
                driver.execute_script(f"arguments[0].scrollBy(0, {scroll_px});", corpo)
                print(f"Rolou {scroll_px}px na aba de busca.")
                time.sleep(random.uniform(1.5, 3.9))

            # Simular um clique aleatório num gênero
            generos = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='genre-card']")
            if generos:
                genero_escolhido = random.choice(generos)
                driver.execute_script("arguments[0].scrollIntoView(true);", genero_escolhido)
                genero_escolhido.click()
                print("Clicou num gênero aleatório.")
                time.sleep(random.uniform(4.6, 8.1))

                # Rolar um pouco mais dentro da página do gênero
                for _ in range(random.randint(1, 3)):
                    scroll_px = random.randint(150, 400)
                    driver.execute_script(f"window.scrollBy(0, {scroll_px});")
                    print(f"Rolou {scroll_px}px dentro da página do gênero.")
                    time.sleep(random.uniform(2.3, 4.5))

        except Exception as e:
            print(f"Ação 4 falhou: {e}")

    elif action == 5:
        # ação 5: clicar em uma playlist e adicionar uma musica aleatória a biblioteca
        
        print("Ação 5 selecionada")
        try:
            # clicar na aba de playlists
            botao_playlist = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='library-button']"))
            )
            botao_playlist.click()
            time.sleep(random.uniform(3.2, 5.1))

            # rolar pela aba de playlists como se estivesse explorando playlists
            corpo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']"))
            )

            for _ in range(random.randint(2, 4)):
                scroll_px = random.randint(200, 600)
                driver.execute_script(f"arguments[0].scrollBy(0, {scroll_px});", corpo)
                print(f"Rolou {scroll_px}px na aba de playlists.")
                time.sleep(random.uniform(1.5, 3.9))

            # Simular um clique aleatório numa playlist
            playlists = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='playlist-card']")
            if playlists:
                playlist_escolhida = random.choice(playlists)
                driver.execute_script("arguments[0].scrollIntoView(true);", playlist_escolhida)
                playlist_escolhida.click()
                print("Clicou numa playlist aleatória.")
                time.sleep(random.uniform(4.6, 8.1))

                # Rolar um pouco mais dentro da página da playlist
                for _ in range(random.randint(1, 3)):
                    scroll_px = random.randint(150, 400)
                    driver.execute_script(f"window.scrollBy(0, {scroll_px});")
                    print(f"Rolou {scroll_px}px dentro da página da playlist.")
                    time.sleep(random.uniform(2.3, 4.5))

        except Exception as e:
            print(f"Ação 5 falhou: {e}")