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
    x = sympy.Symbol('x')
    try:
        left, right = equation.split('=')
        eq = sympy.Eq(eval(left), eval(right))
        answer = sympy.solve(eq, x)[0]
        return(answer)
    except:
        print("Sorry can't answer that question :(")
