#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

from selenium import webdriver
import getpass
import time
import datetime
import logging
import os

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

print("Getting transaction data from your ASB account")

print("Enter your ASB online username:")
asbUsername = input()

asbPassword = getpass.getpass("Enter your ASB online password: ")

print("Launching browser...")
options = webdriver.ChromeOptions()
options.add_argument("download.default_directory=" + os.getcwd())

browser = webdriver.Chrome(chrome_options=options)

browser.get('https://online.asb.co.nz/auth/?fm=header:login')

usernameBox = browser.find_element_by_id('dUsername')
usernameBox.send_keys(asbUsername)
passwordBox = browser.find_element_by_id('password')
passwordBox.send_keys(asbPassword)
loginButton = browser.find_element_by_id('loginBtn')
loginButton.click()
time.sleep(2)
print("Current URL: " + browser.current_url)
token = browser.current_url.split('/')[5]
print("Token: " + token)

todaysDate = datetime.datetime.now()
# TODO: Loop through and just get all the transactions ever
monthYear = todaysDate.strftime('%b %Y')
print("type: {0}, value: {1}".format(type(monthYear), monthYear))
csvURL = "https://online.asb.co.nz/fnc/{0}/Statements/export.ashx?paging=250&\
FROMDAY=2&\
FROMMMYY=Mar 2017&\
TODAY={1}&\
TOMMYY={2}&\
FORMAT=CSV - Generic&\
AccountNumber=12-0000-0000000-00&\
AccountType=0".format(token,todaysDate.day,todaysDate.strftime('%b %Y'))

logging.debug("CSV download URL: " + csvURL)

browser.get(csvURL)

time.sleep(5)
browser.quit()
