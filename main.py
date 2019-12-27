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
    matFes.timer('mjx-mrow', 5, driver, By.CLASS_NAME)
    question = driver.find_element_by_class_name('mjx-mrow')
    print("\n" + str(solved + 1) + '.)')

    try:
        try:
            fracs = question.find_elements_by_xpath('//*[@class="mjx-mfrac"]')
            fractest = fracs[0].text
            ans = matFes.fracsolver(question.text, fracs)
        except:
            equation = question.find_element_by_class_name('mjx-mrow').text
            try:
                ans = matFes.solver(equation)
            except:
                print('Failed to run solver')
    except:
        try:
            equation = question.find_element_by_class_name('question-text-content').text
            print ('Unknown error')
        except:
            print('Failed to resolve text')



    print("Svar: " + str(ans))


    if ansMeth.upper() == "A":
        ansFound = False
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
    if not ansFound:
        print('Kunne ikke finde den rigtige valgmulighed :(')
        allFound = False


    time.sleep(3)

#------------------------------------------------Mangeler stadig at aflevere opg---------------------------
    if solved + 1 == questNum:
        print("done")
        if allFound:
            print('Aflevere opgave')
            driver.find_element_by_class_name('three-d-button progress-bar-button').click()
            driver.find_element_by_xpath("//*/button[2]").click()
        break

    #driver.find_element_by_xpath("//button[@class='arrow-button arrow-button-right']").click()
