#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

from selenium import webdriver
import getpass
import time
import os

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

browser.get("https://online.asb.co.nz/fnc/" + token + \
        "/Statements/export.ashx?paging=250&FROMDAY=2&FROMMMYY=Mar 2017&TODAY=22&TOMMYY=Mar 2017&FORMAT=CSV - Generic&AccountNumber=12-3026-0045171-00&AccountType=0")

time.sleep(5)
browser.quit()
