from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from random_user_agent.user_agent import UserAgent
import signal
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
options.add_argument('--window-size=960,800')
options.add_argument('--incognito')
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_window_position(300, 300, windowHandle='current')

def signal_handler(sig, frame):
    driver.quit()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)


def input_word(word):
    for i in word:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"button.key[data-key='{i}']"))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.key[data-key='enter']"))).click()
    

def get_states():
    board_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "board")))
    tiles = WebDriverWait(board_element, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tile")))
    

if __name__ == '__main__':
    try:
        driver.get('https://word.rodeo/?utm_source=share#bVPah5aVC4fNMZfw0BEkFg/e9EnA7X9pVKlmHTFwSw8GLI2J3KDdRdIRMYuuobhRjnjLg3lQiLEf3Kgptm91c2VyuCo7Y43T')
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-panel"]/div[1]/button')))
        button.click()

        input_word('acuea')

        time.sleep(100)

    except KeyboardInterrupt:
        driver.quit()
        sys.exit(0)
    except Exception as e:
        print("Error:", e)
