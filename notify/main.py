# OGUsers Notifer
import configparser, time, warnings, os
from dhooks import Webhook, Embed
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

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
    def __init__(self, username, password, webhook):
        self.username = username
        self.password = password
        self.webhook = webhook

    def login(self):
        # Goes to login page and user details from config.ini
        browser.get(('https://ogusers.com/member.php?action=login'))
        browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Username/Email:'])[1]/following::input[1]").send_keys(self.username)
        browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[1]").send_keys(self.password)
        browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[3]").click()
        time.sleep(1)

    def update(self):
        # Set webhook url
        hook = Webhook(self.webhook)
        # Go to site and check for PM Alerts popup
        already_sent = ''
        while True:
            browser.get(('https://ogusers.com'))
            try:
                PM_alert = browser.find_element_by_xpath("//div[@class='pm_alert']")
                alertPM = PM_alert.get_attribute('innerHTML')
                soup = BeautifulSoup(alertPM.strip())
                tags = soup.find_all('a')
                # Set PM variables
                pm_from = tags[1].text
                pm_from_link = tags[1].attrs['href']
                pm_title = tags[2].text
                pm_link = tags[2].attrs['href']
                
                if pm_link == already_sent:
                    print('[!] Already sent notification, checking again in 60 seconds..')
                else:
                    # Discord webhook stuff
                    embed = Embed(
                        color=0x702c2c,
                        timestamp='now'  # sets the timestamp to current time
                        )
                    embed.set_author(name=pm_from + ' has sent you a PM')
                    embed.add_field(name='Title', value=pm_title)
                    embed.add_field(name='Open DM', value=pm_link)
                    embed.set_footer(text='Created by @braiden')
                    hook.send(embed=embed)
                    already_sent = pm_link
                    print('[!] Sent notification..')
            except NoSuchElementException:
                print('[!] Received no PMs, checking again in 60 seconds..')
            time.sleep(30)

# Read config file and grab username/password
config = configparser.ConfigParser()
config.read('config.ini')

# Set user details
OGU = User(config['user']['username'], config['user']['password'], config['user']['discord_webhook'])
# Start bumping
print('[-] Logging in..')
OGU.login()
print('[+] Logged in..')
print('[+] Starting notifer..')
OGU.update()