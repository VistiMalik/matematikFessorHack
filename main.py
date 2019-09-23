# -*- coding: utf-8 -*-
# imports
import matFes
import time
import getpass
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Get user info
uniUserName = raw_input("Skriv dit uni-login brugernavn: ")
uniPassword = getpass.getpass("Skriv dit uni-login password: ")


# Config driver
chromeDriverVersion = matFes.getChromeDriver()
options = webdriver.ChromeOptions()
options.add_argument('---ignore-certificate-errors')
options.add_argument("--test-type")
driver = webdriver.Chrome(
    ChromeDriverManager(chromeDriverVersion).install(),
    chrome_options=options
)
# Choose url
driver.get('https://matematikfessor.dk/ext/unilogin/login/?r=https%3A%2F%2Fwww.matematikfessor.dk%2F')

# login
matFes.timer('user', 5, driver, By.ID)
driver.find_element_by_name('user').send_keys(uniUserName)
driver.find_element_by_name('pass').send_keys(uniPassword)
driver.find_element_by_name('login').click()

# open the module
#matFes.timer('//div[@class="testBar hideTime ready"]', 15, driver, By.XPATH)
#driver.find_element_by_xpath('//div[@class="testBar hideTime ready"]/span[@class="wrapper"]/span[@class="title"]').click()
#matFes.timer('//*[@id="lightPopup_9"]/div[2]/div[1]/div[2]/a', 10, driver, By.XPATH)
#driver.find_element_by_xpath('//*[@id="lightPopup_9"]/div[2]/div[1]/div[2]/a').click()

input(":")
# Find and solve the equations
matFes.timer('//*[@id="MJXc-Node-6"]/span', 100000, driver, By.XPATH)
questNum = 1
while True:
    questPath = '//*[@id="MathJax-Element-' + str(questNum) + '-Frame"]'
    matFes.timer(questPath, 5000, driver, By.XPATH)
    quest = driver.find_element_by_xpath(questPath).text
    print (matFes.solver(quest))
    questNum += 8
