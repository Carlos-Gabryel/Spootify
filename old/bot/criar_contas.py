from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import random
import requests
import gc
import csv

ua = UserAgent(
    browsers=["chrome", "firefox", "safari", "edge"],
    os=["Windows", "Mac", "Linux"],
    platforms=["desktop", "mobile"],
)

senha_padrao = "testespootify1"

def funcao_geral():
    global email_gerado

    driver = setup_driver("https://temp-mail.io/en")

    if driver:
        try:
            # Espera até que o campo contenha um e-mail válido
            email_presente = WebDriverWait(driver, 20).until(
                lambda d: "@" in d.find_element(By.ID, "email").get_attribute("value")
            )
            if email_presente:
                email_gerado = driver.find_element(By.ID, "email").get_attribute("value")
                print(f"E-mail gerado: {email_gerado}")

                abrir_spotify(driver)

        except Exception as e:
            print(f"Erro ao obter o e-mail: {e}")
        finally:
            driver.quit()


def abrir_spotify(driver):

    try:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://accounts.spotify.com/pt-BR/login")
        print("Navegando para o site do Spotify...")

        cadastro_spotify(driver, email_gerado)

    except Exception as e:
        print(f"Erro ao abrir o Spotify: {e}")


def cadastro_spotify(driver, email_gerado):
    try:
        botao_cadastrar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@data-testid='login-container']//a[@id='sign-up-link']",
                )
            )
        )
        botao_cadastrar.click()
        print("Botão de cadastro clicado.")

        time.sleep(2)

        # Fechar a barra de cookies
        fechar_cookies(driver)

        time.sleep(2)

        digitar_email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        for char in email_gerado:
            digitar_email.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        print("E-mail digitado com sucesso.")

        time.sleep(2)

        botao_avancar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='submit']"))
        )
        botao_avancar.click()

        print("Botão de avançar clicado.")

        time.sleep(2)

        # Etapa 1
        digitar_senha = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "new-password"))
        )

        for char in senha_padrao:
            digitar_senha.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        print("Senha digitada com sucesso.")

        time.sleep(2)

        botao_avancar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='submit']"))
        )
        botao_avancar.click()

        print("Botão de avançar clicado.")

        time.sleep(2)

        # Etapa 2
        nome, sobrenome = obter_nome()
        if not nome or not sobrenome:
            print("Erro ao obter nome e sobrenome.")
            return

        digitar_nome = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "displayName"))
        )

        nome_completo = f"{nome} {sobrenome}"
        for char in nome_completo:
            digitar_nome.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        print(f"Nome e sobrenome digitados com sucesso: {nome_completo}")

        time.sleep(2)

        # Data de Nascimento
        dia = random.randint(1, 28)
        mes = random.randint(1, 12)
        ano = random.randint(1980, 2004)

        digitar_dia = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "day"))
        )
        for char in str(dia):
            digitar_dia.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        print(f"Dia digitado: {dia}")

        time.sleep(2)

        digitar_mes = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "month"))
        )
        selecionar_mes = Select(digitar_mes)
        selecionar_mes.select_by_value(str(mes))
        print(f"Mês digitado: {mes}")

        time.sleep(2)

        digitar_ano = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "year"))
        )
        for char in str(ano):
            digitar_ano.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        print(f"Ano digitado: {ano}")

        time.sleep(2)

        # Gênero
        generos = ["male", "female", "non_binary", "other", "prefer_not_to_say"]
        selecionar_genero = random.choice(generos)

        label_genero = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//label[@for='gender_option_{selecionar_genero}']")
            )
        )
        label_genero.click()
        print(f"Gênero selecionado: {selecionar_genero}")

        time.sleep(2)

        # Avançar
        botao_avancar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='submit']"))
        )
        botao_avancar.click()
        print("Botão de avançar clicado.")

        time.sleep(2)

        # Etapa 3

        aceitar_termos = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//label[@for='terms-conditions-checkbox']")
            )
        )
        aceitar_termos.click()
        print("Checkbox de termos marcado com sucesso.")

        time.sleep(2)

        botao_inscrever = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='submit']"))
        )
        botao_inscrever.click()
        print("Botão de avançar clicado.")

        time.sleep(5)

        if conta_criada(driver):
            # Verifica se a conta foi criada com sucesso
            print("Conta criada com sucesso!")
        else:
            print("Conta não foi criada.")

    except Exception as e:
        print(f"Erro ao preencher o cadastro: {e}")

def conta_criada(driver, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: (
                d.current_url.startswith("https://accounts.spotify.com/pt-BR/status")
                or d.find_elements(By.XPATH, "//button[@data-testid='user-widget-link']")
            )
        )
        return True
    except:
            return False


def setup_driver(url):
    service = Service()
    options = Options()

    options.add_argument(f"user-agent={ua.random}")
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", 'localhost')
    options.set_preference("network.proxy.socks_port", porta)
    options.set_preference("network.proxy.socks_version", 5) 
    options.set_preference("network.proxy.socks_remote_dns", True)

    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url)
        print(f"WebDriver iniciado com sucesso: {driver}")
        return driver

    except Exception as e:
        print(f"Erro ao iniciar o WebDriver: {e}")


def fechar_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-close-btn-container"))
        ).click()
        print("Barra de cookies fechada")

    except Exception as e:
        print(
            "Barra de cookies não encontrada ou já fechada anteriormente, continuando..."
        )


def obter_nome():
    try:
        response = requests.get("https://randomuser.me/api/")
        response.raise_for_status()
        data = response.json()
        nome = data["results"][0]["name"]["first"]
        sobrenome = data["results"][0]["name"]["last"]
        print(f"Nome obtido: {nome} {sobrenome}")
        return nome, sobrenome

    except Exception as e:
        print(f"Erro ao obter nome: {e}")
        return None, None


def salvar_dados_csv(id_conta, email, senha):
    nome_arquivo = "contas_criadas2.csv"
    try:
        arquivo_existe = False
        try:
            with open(nome_arquivo, "r", newline="", encoding="utf-8") as arquivo:
                arquivo_existe = True
        except FileNotFoundError:
            pass

        with open(nome_arquivo, "a", newline="", encoding="utf-8") as arquivo:
            escritor_csv = csv.writer(arquivo)

            if not arquivo_existe:
                escritor_csv.writerow(["ID", "Email", "Senha"])

            escritor_csv.writerow([id_conta, email, senha])
            print(f"Dados salvos no CSV: ID={id_conta}, Email={email}, Senha={senha}")

    except Exception as e:
        print(f"Erro ao salvar os dados no CSV: {e}")


if __name__ == "__main__":
    id_conta = 1
    while True:
        try:
            print(f"Iniciando criação da conta ID={id_conta}...")
            funcao_geral()

            salvar_dados_csv(id_conta, email_gerado, senha_padrao)

            print(
                f"Conta ID={id_conta} criada com sucesso! Reiniciando para criar outra conta...\n"
            )
            id_conta += 1
            time.sleep(5)
            gc.collect()

        except Exception as e:
            print(f"Erro durante a criação da conta ID={id_conta}: {e}")
            print("Reiniciando o processo...\n")
            time.sleep(5)
