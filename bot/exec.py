import json
import time
import random
import multiprocessing
import traceback
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service 
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent

ua = UserAgent()

def comportamento_escrever(element, text, min_delay=0.05, max_delay=0.2):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))


def comportamento_clicar(
    driver, element, min_delay_before_click=0.5, max_delay_before_click=1.5
):
    action = ActionChains(driver)
    action.move_to_element(element).perform() 
    time.sleep(
        random.uniform(min_delay_before_click, max_delay_before_click)
    ) 
    element.click()



def setup_webdriver(proxy_host, proxy_port):

    options = Options()

    # Stealth flags
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--enable-unsafe-webgpu")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=pt-BR")
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--start-maximized")

    # Configuração de proxy com seleniumwire
    seleniumwire_options = {
        'proxy': {
            'http': f'http://{proxy_host}:{proxy_port}',
            'https': f'https://{proxy_host}:{proxy_port}',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    service = Service()

    driver = webdriver.Chrome(
        service=service,
        options=options,
        seleniumwire_options=seleniumwire_options
    )
    return driver


def login_spotify(driver, conta):
    email, senha = conta
    print(f"Fazendo login na conta: {email}")

    input_email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "login-username"))
    )

    if input_email:
        comportamento_escrever(input_email, email) 
        time.sleep(random.uniform(1.0, 3.0)) 

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        comportamento_clicar(driver, login_button)  

    entrar_com_senha = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[@data-encore-id='buttonTertiary']")
        )
    )

    if entrar_com_senha:
        comportamento_clicar(driver, entrar_com_senha)  
        time.sleep(random.uniform(1.5, 3.5)) 

    input_senha = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "login-password"))
    )

    if input_senha:
        comportamento_escrever(input_senha, senha)  
        time.sleep(random.uniform(1.0, 3.0)) 

        final_login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        comportamento_clicar(
            driver, final_login_button
        )  

    WebDriverWait(driver, 25).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-testid='web-player-link']")
        )
    ).click()


playlists = [
    "Léo Foguete 2025 🚀 As Melhores | Obrigado Deus | Última Noite | Cópia Proibida | Quem de Nós Dois",
    "Léo Foguete 🚀 2025 - Dona - O Coração Que Você Quer Entrar Tem Dona - Cópia Proibida - É Hit",
]


def tocar_playlist(driver, nome_playlist=random.choice(playlists)):
    print(f"Login realizado com sucesso. Selecionando a playlist: {nome_playlist}")

    try:
        playlist = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f'//div[@aria-label="Sua Biblioteca"]//div[@role="row" and .//button[contains(@aria-label, "Tocar {nome_playlist}")]]',
                )
            )
        )
        comportamento_clicar(driver, playlist)  
        print(f"Playlist encontrada: {nome_playlist}")
    except Exception as e:
        print(f"Não foi possível selecionar a playlist {nome_playlist} - {e}")
        time.sleep(40000)

    time.sleep(random.uniform(8, 12)) 
    try:
        botao_play = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f'//div[@aria-label="Sua Biblioteca"]//div[@role="group" and @data-encore-id="listRow"]//button[@data-encore-id="buttonTertiary" and @aria-label="Tocar {nome_playlist}"]',
                )
            )
        )
        comportamento_clicar(driver, botao_play) 
        print(f"Playlist '{nome_playlist}' tocada com sucesso.")
    except Exception as e:
        print(f"Erro ao tocar a playlist '{nome_playlist}': {e}")
        driver.quit() 


def logout_spotify(driver, email=None):
    if email:
        print(f"Fazendo logout da conta: {email}")

    driver.get("https://accounts.spotify.com/pt-BR/logout")
    time.sleep(random.uniform(2.0, 4.0)) 

def fechar_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container'))).click()
        print("Barra de cookies fechada")

    except:
        print("Barra de cookies não encontrada ou já fechada anteriormente, continuando...")


def worker(proxy_info):
    proxy_host = proxy_info["host"]
    proxy_port = proxy_info["port"]
    contas = proxy_info["contas"]
    index = 0
    propaganda = False

    start_time= time.time()
    tempo_execucao = 28800

    while time.time() - start_time < tempo_execucao:
        while True:
            conta = contas[index]
            email_atual = conta[0]
            print(f"[Proxy {proxy_host}:{proxy_port}] Ciclo conta: {email_atual}")
            driver = None
            try:
                driver = setup_webdriver(proxy_host, proxy_port)
                musica_atual = ""
                contador_plays = 0

                login_spotify(driver, conta)
                tocar_playlist(driver)

                wait_time = random.uniform(180, 300)
                print(
                    f"[Proxy {proxy_host}:{proxy_port}] Aguardando {wait_time/60:.2f} minutos"
                )

                while time.time() - start_time < wait_time:
                    try:
                        try:
                            buscar_musica = driver.find_element(
                                By.CSS_SELECTOR, '[data-testid="now-playing-widget"]'
                            ).text
                            buscar_musica = buscar_musica.replace(
                                "Tocando agora", ""
                            ).strip()
                            time.sleep(2)
                            propaganda = False
                        except Exception:
                            print("Musica nao encontrada. Relizando verificações.")
                            
                            try:
                                buscar_propaganda = driver.find_element(
                                By.XPATH, '//div[@data-testid="now-playing-widget" and @aria-label="Propaganda"]'
                            )
                                if buscar_propaganda:
                                    propaganda = True
                                    time.sleep(5)
                                    continue

                            except Exception:
                                fechar_cookies(driver)

                        if (buscar_musica != musica_atual) and propaganda is False:
                            contador_plays += 1
                            musica_atual = buscar_musica
                            print(
                                f"[Proxy {proxy_host}:{proxy_port}] Nova faixa encontrada play: {contador_plays}"
                            )

                    except Exception as e:
                        print(
                            f"[Proxy {proxy_host}:{proxy_port}] Erro ao buscar música: {e}"
                        )
                    time.sleep(random.uniform(10, 25))  

            except Exception as e:
                print(
                    f"[Proxy {proxy_host}:{proxy_port}] Erro crítico no ciclo para conta {email_atual}: {e}"
                )
                print(traceback.format_exc())
            finally:
                if driver:
                    logout_spotify(driver, email_atual)
                    driver.quit()
                    print(
                        f"[Proxy {proxy_host}:{proxy_port}] Driver encerrado. Alternando conta."
                    )
                else:
                    print(
                        f"[Proxy {proxy_host}:{proxy_port}] Driver não foi inicializado para conta {email_atual}. Pulando para a próxima."
                    )

                index = (index + 1) % len(contas)
                time.sleep(random.uniform(5, 15))  


if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)

    processos = []
    for proxy_info in config["proxies"]:
        p = multiprocessing.Process(target=worker, args=(proxy_info,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()
