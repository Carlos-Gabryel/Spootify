import json
import time
import random
import multiprocessing
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_webdriver(proxy_host, proxy_port, proxy_user, proxy_pass):
    options = Options()
    # Flags para minimizar detecção de bot
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--enable-unsafe-webgpu")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=pt-BR")
    # options.add_argument("--headless")  # Descomente para rodar sem interface gráfica

    # User-Agent customizado (opcional)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    # Remove a flag de automação
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Desabilita WebRTC para evitar vazamento de IP real
    options.add_argument("--disable-webrtc")

    seleniumwire_options = {
        'proxy': {
            'http': f'socks5://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
            'https': f'socks5://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }

    driver = webdriver.Chrome(options=options, seleniumwire_options=seleniumwire_options)

    # Executa JS para remover propriedades de automação
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.navigator.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt']});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        """
    })

    driver.get("https://accounts.spotify.com/pt-BR")
    return driver

def login_spotify(driver, conta):
    email, senha = conta
    print(f"Fazendo login na conta: {email}")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'login-username'))).send_keys(email)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password'))).send_keys(senha)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login-button'))).click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='web-player-link']"))).click()

playlists = [
            'Léo Foguete 2025  🚀 As Melhores | Obrigado Deus | Última Noite | Cópia Proibida | Quem de Nós Dois', 
            'Léo Foguete 🚀 2025 - Dona - O Coração Que Você Quer Entrar Tem Dona - Cópia Proibida - É Hit'
        ]

def tocar_playlist(driver, nome_playlist=random.choice(playlists)): 
    try:
        # Clica na playlist com base no nome
        playlist = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f'//div[@aria-label="Sua Biblioteca"]//div[@role="row" and .//button[contains(@aria-label, "Tocar {nome_playlist}")]]'
                )))
        playlist.click()
        print(f"Playlist encontrada: {nome_playlist}")
    except Exception as e:
        print(f"Não foi possível selecionar a playlist {nome_playlist} - {e}")

    time.sleep(random.uniform(8, 12))
    try:
        botao_play = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((
                By.XPATH, f'//div[@aria-label="Sua Biblioteca"]//div[@role="group" and @data-encore-id="listRow"]//button[@data-encore-id="buttonTertiary" and @aria-label="Tocar {nome_playlist}"]'
                )))
        botao_play.click()
        print(f"Playlist '{nome_playlist}' tocada com sucesso.")
    except Exception as e:
        print(f"Erro ao tocar a playlist '{nome_playlist}': {e}")
        driver.quit()

def logout_spotify(driver, email=None):
    if email:
        print(f"Fazendo logout da conta: {email}")

    driver.get("https://accounts.spotify.com/pt-BR/logout")
    time.sleep(2)

def worker(proxy_info):
    proxy_host = proxy_info["host"]
    proxy_port = proxy_info["port"]
    proxy_user = proxy_info["username"]
    proxy_pass = proxy_info["password"]
    contas = proxy_info["contas"]
    index = 0

    while True:
        conta = contas[index]
        print(f"[Proxy {proxy_host}:{proxy_port}] Ciclo conta: {conta[0]}")
        driver = setup_webdriver(proxy_host, proxy_port, proxy_user, proxy_pass)
        musica_atual = ""
        contador_plays = 0
        try:
            login_spotify(driver, conta)
            tocar_playlist(driver)
            wait_time = random.uniform(3600, 4000)
            print(f"[Proxy {proxy_host}:{proxy_port}] Aguardando {wait_time/60:.2f} minutos")

            start_time = time.time()
            while time.time() - start_time < wait_time:
                try:
                    buscar_musica = driver.find_element(By.CSS_SELECTOR, '[data-testid="now-playing-widget"]').text
                    buscar_musica = buscar_musica.replace("Tocando agora", "").strip()
                    if buscar_musica != musica_atual:
                        contador_plays += 1
                        musica_atual = buscar_musica
                        print(f"[Proxy {proxy_host}:{proxy_port}] Nova faixa encontrada play: {contador_plays}")
                except Exception as e:
                    print(f'[Proxy {proxy_host}:{proxy_port}] Erro ao buscar música: {e}')
                time.sleep(10)  # Ajuste o intervalo conforme necessário

        except Exception as e:
            print(f"[Proxy {proxy_host}:{proxy_port}] Erro: {e}")
        finally:
            logout_spotify(driver)
            driver.quit()
            print(f"[Proxy {proxy_host}:{proxy_port}] Driver encerrado. Alternando conta.")
            index = (index + 1) % len(contas)
            time.sleep(5)

if __name__ == '__main__':
    with open('config.json') as f:
        config = json.load(f)

    processos = []
    for proxy_info in config["proxies"]:
        p = multiprocessing.Process(target=worker, args=(proxy_info,))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()