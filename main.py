from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from random_user_agent.user_agent import UserAgent
import urllib.parse
import subprocess
import threading
import signal
import json
import sys
import time

user_agent = UserAgent().get_random_user_agent()
print(user_agent)

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'--user-agent={user_agent}')
options.add_argument('--incognito')
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

def signal_handler(sig, frame):
    driver.quit()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

decrypted_word = ""
node_finished_event = threading.Event()

def input_word(word):
    for i in word:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"button.key[data-key='{i}']"))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.key[data-key='enter']"))).click()
    
def run_node_script(encrypted_text):
    global decrypted_word
    output = subprocess.check_output(['node', 'index.js', encrypted_text], text=True)
    print("\nNode.js script output:\033[1m", output, "\033[0m")
    json_start_index = output.find('{')
    if json_start_index != -1:
        json_data = output[json_start_index:]
        decrypted_data = json.loads(json_data)
        decrypted_word = decrypted_data.get('word', '')
    node_finished_event.set()


if __name__ == '__main__':
    try:
        driver.minimize_window()

        url = input('\nEnter a URL:  ')

        driver.maximize_window()

        parsed_url = urllib.parse.urlparse(url)
        encrypted_text = parsed_url.fragment

        node_thread = threading.Thread(target=run_node_script, args=(encrypted_text,))
        node_thread.start()

        driver.get(url)
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-panel"]/div[1]/button')))
        button.click()

        node_finished_event.wait()
        input_word('tengo')
        input_word('llama')
        input_word('estar')
        input_word('adios')
        input_word(decrypted_word)

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'show-solved')]")))
        print("\033[32m\033[1mSuccessful!\033[0m\033[37m")

        time.sleep(9999)

    except KeyboardInterrupt:
        driver.quit()
        sys.exit(0)
    except TimeoutException:
        print("maybe check internet connection?")
    except Exception as e:
        print("Error:", e)

