from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os


load_dotenv()
USER_NAME=os.getenv('USER_NAME')
PASSWORD=os.getenv('PASSWORD')

# proxie_options = {
#     'proxy': {
#         'http': 'socks5://127.0.0.1:9050',
#         'https': 'socks5://127.0.0.1:9050',
#         'no_proxy':'localhost,127.0.0.1'
#     }
# }

# Configuração do WebDriver
def setup_webdriver(url):
    service = Service() 
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36')
    # options.add_argument('--headless')
    options.add_experimental_option('detach', True)
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        return driver
    except Exception as e:
        print(f'Erro ao iniciar o webdriver')
        return None

def login_spotify(driver):
    try:
        usuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-username')))
        usuario.send_keys(USER_NAME) # digitar email

        senha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password')))
        senha.send_keys(PASSWORD) # digitar senha

        botao_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login-button')))
        botao_login.click() # botao clicavel de login

        web_player = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='web-player-link']")))
        web_player.click() # botao clicavel do webplayer

    except Exception as e:
        print(f'Erro ao tentar fazer login no spotify {e}')

def buscar_playlist(driver):
    barra_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container')))
    barra_cookies.click() # fecha a barra de cookies

    # selecionar_playlist = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Desktop_LeftSidebar_Id"]/nav/div/div[1]/div[2]/div[2]/div/div/ul/div/div[2]/li/div/div/div[1]')))
    # selecionar_playlist.click() # seleciona a primeira playlist que está salva na conta
    botao_play = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="play-button"]')))
    botao_play.click()
    
    
if __name__ == "__main__":
    driver = setup_webdriver("https://accounts.spotify.com/en/login")
    login_spotify(driver)
    time.sleep(2)
    buscar_playlist(driver)
    time.sleep(5)
    
    # determinando 48h de execução
    tempo_execucao = 300
    tempo_inicio = time.time()

    musicas_tocadas = []
    musica_atual = ""

    while(time.time() - tempo_inicio) < tempo_execucao:
        time.sleep(20)
        try:
            buscar_musica = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/footer/div/div[1]/div/div[2]/div[1]/div').text
            if buscar_musica != musica_atual:
                musica_atual = buscar_musica
                musicas_tocadas.append(musica_atual)
                print(f"Nova faixa encontrada {buscar_musica} e adicionada a lista de faixas")
            else:
                    print("Nova faixa ainda não encontrada.")
        except Exception as e:
            print(e)
        
    print(f"A quantidade de plays foi de {len(musicas_tocadas)}")
    driver.quit()
        
    
    
