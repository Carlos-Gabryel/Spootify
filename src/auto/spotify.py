from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gc
import time

# Configuração do WebDriver
def setup_webdriver(url):
    service = Service() 
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36')
    options.add_argument('--headless=new')
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        print("Webdriver iniciado.")

        return driver
    except Exception as e:
        print(f'Erro ao iniciar o webdriver.')
        return None

def login_spotify(driver):
    try:
        usuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-username')))
        usuario.send_keys('testespootify1@gmail.com') # digitar email

        senha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password')))
        senha.send_keys('testespootify1') # digitar senha

        botao_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login-button')))
        botao_login.click() # botao clicavel de login

        web_player = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='web-player-link']")))
        web_player.click() # botao clicavel do webplayer

        print("Login bem-sucedido e webplayer selecionado.")

    except Exception as e:
        print(f'Erro ao tentar fazer login no Spotify {e}')

def buscar_playlist(driver):
    try:
        barra_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container')))
        barra_cookies.click() # fecha a barra de cookies

        print("Barra de cookies fechada.")
    except:
        print("Barra de cookies não encontrada ou já fechada anteriormente, continuando...")
        pass

    botao_play = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="play-button"]')))
    botao_play.click()
    
    print("Playlist encontrada e selecionada.")

if __name__ == "__main__":
    driver = setup_webdriver("https://accounts.spotify.com/en/login")
    if driver:
        login_spotify(driver)
        time.sleep(2)
        buscar_playlist(driver)
        
        # determinando 48h de execução
        tempo_execucao = 172800
        tempo_inicio = time.time()
        
        musica_atual = ""
        contador_plays = 0

        while(time.time() - tempo_inicio) < tempo_execucao:
            time.sleep(20)
            try:
                buscar_musica = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[4]/footer/div/div[1]/div/div[2]/div[1]/div').text

                if buscar_musica != musica_atual:
                    contador_plays+=1
                    musica_atual = buscar_musica
                    print(f"Nova faixa encontrada play número {contador_plays}")
                
                if contador_plays%5 == 0:
                    gc.collect()
                    print("Garbage collector limpo")

            except Exception as e:
                print(e)

        driver.quit()
    print(f"A quantidade de plays foi de {len(contador_plays)}")
    
        
    
    
