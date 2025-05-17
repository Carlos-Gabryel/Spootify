from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

porta = 35000
url='https://accounts.spotify.com/pt-BR/login'  

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
 
try:
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)
    print(f"Webdriver iniciado na porta {porta}.")

except Exception as e:
        print(f'Erro ao iniciar o webdriver na porta {porta}: {e}')
       
