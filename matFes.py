# -*- coding: utf-8 -*-
import re
import requests
from subprocess import check_output
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import sympy
import fractions
import solvers
import time

def getChromeDriver():
    out = check_output(["google-chrome", "--version"])
    chromeVersion = re.search('(\d+)', out).group(0)
    r = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + chromeVersion)
    chromeDriverVersion = r.text
    return chromeDriverVersion

def timer(path, time, driver, argument):
    try:
        WebDriverWait(driver, time).until(EC.presence_of_element_located((argument, path)))
    except TimeoutException:
        print("Site not loaded")
        driver.close()
        exit(1)

def solver(equation, fracs, type):
    if type == 'dec':
        return solvers.decSolver(equation)
    elif type == 'frac':
        return solvers.fracSolver(equation, fracs)
    elif type == 'txt':
        return solvers.txtSolver(equation)

def autoAns(driver, ans):
    ansFound = False
    try:
        driver.find_element_by_xpath("//input[@class='number-input-field input-field-answer-input-field']").send_keys(str(ans) + "\n")
        ansFound = True
    except:
        answers = driver.find_elements_by_class_name('multiple-choice-answer-label')
        i = 0
        for possibilities in answers:
            answer = answers[i].text.replace("\n",'')
            answer = answer.encode('utf-8','ignore')
            answer = answer.replace('−','-')
            answer = (re.findall(r'([-,\d+])', answer))
            answer = ''.join(answer)
            if answer == str(ans):
                answers[i].click()
                ansFound = True
                driver.find_element_by_xpath("//*[@class='three-d-button answer-button']").click()
                break
            i += 1
    return ansFound
