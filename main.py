import json
import time
import subprocess
import urllib.parse

from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome

from random_user_agent.user_agent import UserAgent

user_agent = UserAgent().get_random_user_agent()
print(user_agent)

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'--user-agent={user_agent}')
options.add_argument('--incognito')
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

def run_node_script(encrypted_text):
    output = subprocess.check_output(['node', 'index.js', encrypted_text], text=True)
    json_start_index = output.find('{')
    if json_start_index != -1:
        json_data = output[json_start_index:]
        decrypted_data = json.loads(json_data)
        decrypted_word = decrypted_data.get('word', '')
        return decrypted_word

def main():
    decrypted_word = ""

    driver.minimize_window()
    url = input('Enter a URL:  ')
    driver.maximize_window()

    parsed_url = urllib.parse.urlparse(url)
    encrypted_text = parsed_url.fragment

    decrypted_word = run_node_script(encrypted_text)

    driver.get(url)

    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-panel"]/div[1]/button')))
    button.click()

    for word in ['tengo', 'busca', 'estar', 'adios', 'madre', decrypted_word]:
        input_word(word)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "copy-result")))
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-panel"]/div[1]/button'))).click()
    time.sleep(99999)

def input_word(word):
    for i in word:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"button.key[data-key='{i}']"))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.key[data-key='enter']"))).click()

if __name__ == "__main__":
    main()

