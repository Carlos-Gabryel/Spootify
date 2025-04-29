from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import multiprocessing
from fake_useragent import UserAgent
import time
import random
import gc
from solveCaptcha import solve_captcha

ua = UserAgent(
    browsers=['Chrome', 'Firefox', 'Edge', 'Opera'], 
    os=['Windows', 'Linux', 'Mac'],
    platforms=['desktop', 'mobile']
)

def funcao_principal(porta, conta):
    driver = setup_webdriver("https://accounts.spotify.com/pt-BR/login", porta)

    if driver:
        login_spotify(driver, conta)
        fechar_cookies(driver)
        time.sleep(random.uniform(1, 4))
        random_behavior(driver)
        time.sleep(random.uniform(5, 10))

        # identificação do iframe que contem plano de ofertas
        try:
            fechar_iframeOfertas(driver)
        except: 
            print("Iframe de ofertas não encontrado, seguindo com o fluxo do programa...")
            pass
        
        musica_atual = ""
        contador_plays = 0

        while True: 
            try:
                # tocar playlist1 
                tocar_playlist(driver, "Brisa Pernambucana")
                inicio_playlist1 = time.time()

                while time.time() - inicio_playlist1 < random.uniform(3300,3600): # loop com variacao de tempo entre 55 a 60min
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

                while time.time() - inicio_playlist2 < random.uniform(3300,3600): # loop com variacao de tempo entre 55 a 60min
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

    # Configuração do SOCKS5 Proxy
    options.add_argument(f"--proxy-server=socks5://localhost:{porta}")
    
    # Configuração para rodar em segundo plano (opcional)
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized") # inicializa em tela cheia
    options.add_argument("--disable-extensions") # desabilita as extensoes do chrome
    options.add_argument("--disable-application-cache") # desabilita o cache do chrome
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)  
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f"user-agent={ua.random}") # randomiza o user agent com as definições do fake_useragent

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        print(f"Webdriver iniciado na porta {porta}.")
        return driver

    except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {porta}: {e}')
        
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
        try:
            captcha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//main[@id="encore-web-main-content"]//h1[@data-encore-id="type"]')))
            print(f"Captcha encontrado: {captcha.text}")

            if "Precisamos" in captcha.text:
                sitekey = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="g-recaptcha"]'))).get_attribute("data-sitekey")
                url = driver.current_url()

                result = solve_captcha(sitekey, url)
                if result:
                    code = result['code']
                    driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % code)
                    driver.find_element(By.XPATH, '//main[@id="encore-web-main-content"]//button[@data-encore-id="buttonPrimary"]').click()
        except Exception as e:
            print(f"Erro ao lidar com o captcha: {e}")
            time.sleep(40000)
            driver.quit()

def fechar_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container'))).click()
        print("Barra de cookies fechada")

    except:
        print("Barra de cookies não encontrada ou já fechada anteriormente, continuando...")
        pass

def fechar_iframeOfertas(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//html[@dir="auto"]//button[@data-click-to-action-action="DISMISS"]'))).click()
        print("Iframe de ofertas fechado")

    except:
        print("Iframe de ofertas não encontrado ou já fechado anteriormente, continuando...")

def tocar_playlist(driver, nome_playlist):
    try:
        # Clica na playlist com base no nome
        playlist = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f'//div[@aria-label="Sua Biblioteca"]//div[@role="row" and .//button[contains(@aria-label, "Tocar {nome_playlist}")]]'
                )))
        playlist.click()
        print(f"Playlist encontrada: {nome_playlist}")
    except:
        print(f"Não selecionou a playlist {nome_playlist}")

    time.sleep(10)
    try:
        botao_play = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((
                By.XPATH, f'//div[@aria-label="Sua Biblioteca"]//div[@role="group" and @data-encore-id="listRow"]//button[@data-encore-id="buttonTertiary" and @aria-label="Tocar {nome_playlist}"]'
                )))
        botao_play.click()
        print(f"Playlist '{nome_playlist}' tocada com sucesso.")
    

        
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
    portas = [34568, 34569, 34570, 34571, 35002, 35003, 35004, 35555]
    contas = [('vobopo1052@macho3.com','testespootify1'),
              ('niratem674@macho3.com','testespootify1'),
              ('tiham93205@deenur.com','testespootify1'),
              ('feton72780@provko.com','testespootify1'),
              ('vadaraj698@movfull.com','testespootify1'),
              ('doxex93700@bariswc.com','testespootify1'),
              ('tifose9833@movfull.com','testespootify1'),
              ('vocixo9528@provko.com','testespootify1')
              ]

    processos = []
   
    for porta, conta in zip(portas, contas):
        p = multiprocessing.Process(target=funcao_principal, args=(porta, conta))
        processos.append(p)
        p.start()
    
    for p in processos:
        p.join()
    print("Todos os processos foram concluídos.")











