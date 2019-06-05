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



# Get user
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
matFes.timer('//*[@id="frame"]/article/div[1]/article/div[3]/div[8]', 15, driver, By.XPATH)
driver.find_element_by_xpath('//*[@id="frame"]/article/div[1]/article/div[3]/div[8]').click()
matFes.timer('//*[@id="lightPopup_9"]/div[2]/div[1]/div[2]/a', 5, driver, By.XPATH)
driver.find_element_by_xpath('//*[@id="lightPopup_9"]/div[2]/div[1]/div[2]/a').click()
# Answer the questions
question = "??"
while True:
    matFes.timer('//*[@id="MathJax-Span-2"]', 5, driver, By.XPATH)
    questionTest = driver.find_element_by_xpath('//*[@id="MathJax-Span-2"]').text
    if questionTest != question:
        question = questionTest
        print("New Slide")
        print(matFes.solver(question))
    time.sleep(1)
