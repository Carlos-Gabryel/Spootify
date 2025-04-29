from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from solveCaptcha import solve_captcha
import time

url = 'https://www.google.com/recaptcha/api2/demo'

driver = webdriver.Chrome()
driver.get(url)

result = solve_captcha('6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-', url)

code = result['code']
print(code)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "g-recaptcha-response"))
)

driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % code)

time.sleep(150)

# ta repreendido
driver.find_element(By.ID, "recaptcha-demo-submit").click()
    
