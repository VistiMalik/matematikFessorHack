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

def solver(equation):
    # Replace things in the equation
    regex = '([0-9])([x])'
    res = re.findall(regex, equation)
    equation = equation.encode('utf-8','ignore')
    equation = equation.replace('−', '-')
    equation = equation.replace('⋅', '*')
    equation = equation.replace(':', '/')
    equation = re.sub("\d+\n\d+", lambda x:x.group(0).replace("\n", '**'), equation)
    equation = equation.replace('\n', '')
    equation = re.sub("(?<=\d)x", "*x", equation)
    equation = re.sub("=$", '=x', equation)
    # Calculation of the equation
    x = sympy.Symbol('x')
    try:
        left, right = equation.split('=')
        eq = sympy.Eq(eval(left), eval(right))
        answer = sympy.solve(eq, x)[0]
        return(answer)
    except:
        return 0

def fracsolver(equation, fracs):
    amnt = 0
    equation = equation.replace("\n", '')
    while True:
        try:
            num = fracs[amnt].find_element_by_class_name('mjx-numerator').text
            dnum = fracs[amnt].find_element_by_class_name('mjx-denominator').text
            num = num.replace("\n", '')
            dnum = dnum.replace("\n", '')
            equation = equation.replace(num + dnum, '(' + num + ')' + '/' + '(' + dnum + ')')
            amnt += 1
        except:
            break
    return solver(equation)
