from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from playwright.sync_api import sync_playwright
import pytesseract
from PIL import Image


porta = 34567
conta = 'doxex93700@bariswc.com'

# configuração do webdriver com Chrome
def setup_webdriver(url):
    service = Service()  
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f'--proxy-server=socks5://localhost:{porta}')  
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--mute-audio')
    options.add_argument('--remote-debugging-port=9222')  

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        print(f"Webdriver iniciado na porta {porta}.")
        return driver

    except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {porta}: {e}')
        driver.quit()

def login_spotify(driver):
    try:
        digitar_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-username')))
        digitar_login.send_keys(conta)

        digitar_senha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password')))
        digitar_senha.send_keys('testespootify1')

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

def buscar_playlist(driver):
    # Fechar a barra de cookies com Selenium
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container'))).click()
        print("Barra de cookies fechada")
    except:
        print("Barra de cookies não encontrada ou já fechada anteriormente, continuando...")

    # Usar Playwright para identificar e clicar na playlist
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")  # Conecta ao navegador já aberto pelo Selenium
            page = browser.contexts[0].pages[0]  # Obtém a aba atual

            # Captura uma screenshot da área onde o botão da playlist está
            screenshot_path = "playlist_button.png"
            page.screenshot(path=screenshot_path, full_page=True)

            # Usar OCR para identificar o botão da playlist
            image = Image.open(screenshot_path)

            # Melhorar a imagem para OCR (opcional)
            image = image.convert("L")  # Converter para escala de cinza
            text = pytesseract.image_to_string(image, lang="eng")  # Definir idioma como inglês

            print(f"Texto identificado pelo OCR: {text}")  # Log para depuração

            if "TOP 10 Joyce Alane 2025" in text:  # Verifica se o texto está na imagem
                print("Botão da playlist identificado com OCR.")
                # Simula o clique no botão da playlist
                page.click('text="TOP 10 Joyce Alane 2025"')  # Seleciona o botão pelo texto
            else:
                print("Botão da playlist não encontrado com OCR.")
    except Exception as e:
        print(f"Erro ao buscar playlist com Playwright e OCR: {e}")

if __name__ == "__main__":
    driver = setup_webdriver("https://accounts.spotify.com/pt-BR/login")

    if driver:
        login_spotify(driver)
        buscar_playlist(driver)
        time.sleep(100)
        
        # musica_atual = ""
        # contador_plays = 0

        # try:
        #     qtd_musicas = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@data-testid='now-playing-widget']"))
        #     )
        #     valor = int(qtd_musicas.text.replace(" músicas", ""))
        #     print(f"Foram encontradas {valor} músicas na playlist.")
        # except:
        #     valor = 0
        #     print("Não foi possível contar as músicas.")

        # while driver:
        #     time.sleep(15)
        #     try:
        #         buscar_musica = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/footer/div/div[1]/div/div[2]/div[1]/div').text

        #         if buscar_musica != musica_atual:
        #             contador_plays += 1
        #             musica_atual = buscar_musica
        #             print(f"Nova faixa encontrada, play número {contador_plays}")
        #     except Exception as e:
        #         print(f'Erro ao buscar música: {e}')