# OGUsers Notifer
import configparser, time, warnings, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Disable python logging to console
warnings.filterwarnings("ignore")
clear = lambda: os.system('cls')
clear()
# Setup web-driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--hide-scrollbars')
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
browser = webdriver.Chrome(chrome_options=options)
clear()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        # Goes to login page and user details from config.ini
        browser.get(('https://ogusers.com/member.php?action=login'))
        browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Username/Email:'])[1]/following::input[1]").send_keys(self.username)
        browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[1]").send_keys(self.password)
        browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[3]").click()
        time.sleep(1)

    def update(self):
        browser.get(('https://ogusers.com'))
        PM_alert = browser.find_element_by_xpath("//div[@class='pm_alert']")
        alertPM = PM_alert.get_attribute('innerHTML')
        # Get html: alertPM.strip()
        soup = BeautifulSoup(alertPM.strip())
        tags = soup.find_all('a')
        pm_from = tags[1].text
        pm_from_link = tags[1].attrs['href']
        pm_title = tags[2].text
        pm_link = tags[2].attrs['href']
        print(pm_from)
        print(pm_from_link)
        print(pm_title)
        print(pm_link)
        time.sleep(10)

# Read config file and grab username/password
config = configparser.ConfigParser()
config.read('config.ini')

# Set user details
OGU = User(config['user']['username'], config['user']['password'])
# Start bumping
print('[-] Logging in..')
OGU.login()
print('[+] Logged in..')
print('[+] Starting notifer..')
OGU.update()