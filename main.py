# -*- coding: utf-8 -*-
# imports
import matFes
import time
import re
import getpass
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import traceback

# Get user info
login = ["",""]
try:
    f = open('login', 'r')
    login = f.readlines()
    f.close()
except:
    login[0] = raw_input("Skriv dit uni-login brugernavn: ")
    login[1] = getpass.getpass("Skriv dit uni-login password: ")
    f = open('login', 'w+')
    f.write(login[0]+"\t"+login[1]+"\n")
    print(login)


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
driver.find_element_by_name('user').send_keys(login)


# open the module
#matFes.timer('//div[@class="testBar hideTime ready"]', 15, driver, By.XPATH)
#driver.find_element_by_xpath('//div[@class="testBar hideTime ready"]/span[@class="wrapper"]/span[@class="title"]').click()
#matFes.timer('//*[@id="lightPopup_9"]/div[2]/div[1]/div[2]/a', 10, driver, By.XPATH)
#driver.find_element_by_xpath('//*[@id="lightPopup_9"]/div[2]/div[1]/div[2]/a').click()


# potenser har mjx-sup som class
# kvadratrod er mjx-surd
#questions = driver.find_elements_by_class_name('card-scroller-child')


matFes.timer('question-header', 214783600, driver, By.CLASS_NAME)
matFes.timer('question-content', 15, driver, By.CLASS_NAME)


# Answer the questions
ansMeth = 'A'
allFound = True
questNum = int((re.findall(r'/ (\d+)', driver.find_element_by_xpath('//*[@class="question-index-indicator"]').text))[0])
for solved in range(questNum):
    print('input')
    ans = None
    ansFound = False
    matFes.timer('question-text-content', 5, driver, By.CLASS_NAME)
    print("\n" + str(solved + 1) + '.)')

    try:
        question = driver.find_element_by_class_name('mjx-mrow')
        try:
            fracs = question.find_elements_by_xpath('//*[@class="mjx-mfrac"]')
            fractest = fracs[0].text
            ans = matFes.solver(question.text, fracs, 'frac')
        except:
            equation = question.find_element_by_class_name('mjx-mrow').text
            try:
                ans = matFes.solver(equation, None, 'dec')
            except:
                print('Failed to run solver')
    except:

        try:
            equation = driver.find_element_by_xpath("//div[@class='question-text-content']").text
            ans = matFes.solver(equation, None, 'txt')
        except:
            print('Failed to resolve text')
            ansMeth = None
            allFound = False


    if ans != None:
        print("Svar: " + str(ans))

    if ansMeth == None:
        raw_input('Tryk enter for at komme videre')
    elif ansMeth.upper() == 'A':
        try:
            driver.find_element_by_xpath("//input[@class='number-input-field input-field-answer-input-field']").send_keys(ans + "\n")
            ansFound = True
        except:
            answers = driver.find_elements_by_class_name('multiple-choice-answer-label')
            i = 0
            for possibilities in answers:
                answer = answers[i].text.replace("\n",'')
                answer = answer.encode('utf-8','ignore')
                answer = answer.replace('−','-')
                answer = (re.findall(r'([-\d+])', answer))
                answer = ''.join(answer)
                if answer == str(ans):
                    answers[i].click()
                    ansFound = True
                    driver.find_element_by_xpath("//*[@class='three-d-button answer-button']").click()
                    break
                i += 1

    if not ansFound and ansMeth == 'A':
        allFound = False
        print('Kunne ikke finde den rigtige valgmulighed :(')
        raw_input('Tryk enter for at komme videre')


    time.sleep(3)
    if solved + 1 == questNum:
        print("done")
        if allFound:
            print('Aflevere opgaven')
            driver.find_element_by_xpath('//*[@id="frame"]/article/span/button').click()
            time.sleep(1)
            driver.find_element_by_xpath("//*/button[2]").click()
        break
