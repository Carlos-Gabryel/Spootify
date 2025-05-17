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

ua = UserAgent(
    browsers=['Chrome', 'Firefox', 'Edge', 'Opera'], 
    os=['Windows', 'Linux', 'Mac'],
    platforms=['desktop', 'mobile']
)

portas = [
        34569,
        34567,
        34568,
        34570,
        34571,
        # 35000,
        # 35001,
        # 35002,
        # 35003,
        # 35004
        ]
contas = [
        ('kipima2102@benznoi.com', 'testespootify1'),
        ('sasiro4082@benznoi.com', 'testespootify1'),
        ('jawonel871@idoidraw.com', 'testespootify1'),
        ('tefako3759@javbing.com', 'testespootify1'),
        ('fipofe8836@exitings.com', 'testespootify1'),
        # ('tisoweb560@nutrv.com', 'testespootify1'),
        # ('biradi6712@nutrv.com', 'testespootify1'),
        # ('disebak433@firain.com', 'testespootify1'),
        # ('cegexi1890@firain.com', 'testespootify1'),
        # ('gelox24223@idoidraw.com', 'testespootify1')
        ]

def funcao_principal(porta, conta):
    driver = setup_webdriver("https://accounts.spotify.com/pt-BR/login", porta)

    if driver:
        login_spotify(driver, conta)

        try:
            fechar_iframeOfertas(driver)
        except: 
            print("Banner de ofertas não encontrado")
            pass

        fechar_cookies(driver)
        time.sleep(random.uniform(1, 4))
        random_behavior(driver)
        time.sleep(random.uniform(5, 10))
        
        musica_atual = ""
        contador_plays = 0

        while True:
            try:
                fechar_iframeOfertas(driver)
            except: 
                print("Banner de ofertas não encontrado.")
                pass
            
            try:
                # tocar playlist1 
                tocar_playlist(driver, "Léo Foguete 2025  🚀 As Melhores | Obrigado Deus | Última Noite | Cópia Proibida | Quem de Nós Dois")
                print(f"Tocando Playlist 1...")
                inicio_playlist1 = time.time()

                while time.time() - inicio_playlist1 < random.uniform(3300, 3600): # looping com variacao de tempo para trocar de playlist
                    time.sleep(15)

                    try:
                        buscar_musica = driver.find_element(By.CSS_SELECTOR, '[data-testid="now-playing-widget"]').text
                        buscar_musica = buscar_musica.replace("Tocando agora", "").strip()
                        if buscar_musica != musica_atual:
                            contador_plays += 1
                            musica_atual = buscar_musica
                            print(f"Nova faixa encontrada play: {contador_plays}")
                    except Exception as e:
                                print(f'Erro ao buscar música na Playlist 1 {e}')

                # tocar Playlist 2
                try:
                    gc.collect()
                    print(f"Garbage collector limpo!")
                except:
                    print(f"Erro ao limpar o garbage collector ")
                
                tocar_playlist(driver, "Pausar Rock Brasileiro: Anos 2000")
                print(f"Tocando Playlist 2...")
                inicio_playlist2 = time.time()

                while time.time() - inicio_playlist2 < random.uniform(50, 60): # loop com variacao de tempo entre 55 a 60min
                    time.sleep(15)
                    try:
                        buscar_musica = driver.find_element(By.CSS_SELECTOR, '[data-testid="now-playing-widget"]').text
                        buscar_musica = buscar_musica.replace("Tocando agora", "").strip()

                        if buscar_musica != musica_atual:
                            contador_plays += 1
                            musica_atual = buscar_musica
                            print(f"Nova faixa encontrada play {contador_plays}")
                    except Exception as e:
                        print(f'Erro ao buscar música na Playlist 2{e}')

            except Exception as e:
                print(f"Erro no loop principal {e}")
                break

# configuração do webdriver com Chrome
def setup_webdriver(url, porta):
    service = Service()  
    options = webdriver.ChromeOptions()

    # configurando ip da vpn 
    options.add_argument(f"--proxy-server=socks5://localhost:{porta}")
    
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu") # desabilita o uso da gpu
    options.add_argument("--no-sandbox") # desabilita o sandbox do chrome 
    options.add_argument("--disable-dev-shm-usage") # desabilita o uso do dev-shm
    options.add_argument("--start-maximized") # inicializa em tela cheia
    options.add_argument("--disable-extensions") # desabilita as extensoes do chrome
    options.add_argument("--disable-application-cache") # desabilita o cache do chrome
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) # desabilita o modo automatizado do chrome
    options.add_argument('--disable-blink-features=AutomationControlled') # desabilita o modo automatizado do chrome
    options.add_argument(f"user-agent={ua.random}") # randomiza o user agent com as definições do fake_useragent
    options.add_argument('--ignore-certificate-errors') # ignora os erros de certificado (ssl por exemplo)

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
        print(f"Erro ao fazer login no Spotify {email} => {e} <=")
        driver.quit()

    try:
        # seleção de webplayer
        webplayer = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='web-player-link']")))
        webplayer.click()
    except Exception as e:
        # espaço reservado para a solução do recaptcha
        print(f"PEGOU NAO ESSA PORRAAAA ({porta}) {e}")
        # driver.quit()

def fechar_iframeOfertas(driver):
    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//html[@dir="auto"]//button[@data-click-to-action-action="DISMISS"]'))).click()
        print("Banner de ofertas fechado")

    except:
        print("Banner de ofertas não encontrado.")

def fechar_cookies(driver):
    try:
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container'))).click()
        print(f"Barra de cookies fechada.")

    except:
        print(f"Barra de cookies não encontrada ou já fechada anteriormente, continuando...")

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
    processos = []
   
    for porta, conta in zip(portas, contas):
        p = multiprocessing.Process(target=funcao_principal, args=(porta, conta))
        processos.append(p)
        p.start()
    
    for p in processos:
        p.join()
    print("Todos os processos foram concluídos.")

