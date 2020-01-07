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
from decimal import Decimal
import math


def round(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def decSolver(equation):
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



def fracSolver(equation, fracs):
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
    return decSolver(equation)


def txtSolver(equation):
    equation = equation.encode('utf-8','ignore')
    if re.match(r"Afrund (\d+),(\d+) til (\d+) decimal", equation) != None:
        eqNums = re.findall(r"Afrund (\d+),(\d+) til (\d+) decimal", equation)
        eqNums = eqNums[0]
        res = (str(round(float(eqNums[0] + "." + eqNums[1]), int(eqNums[2]))).replace('.', ',')).replace(',0', '')
        return res
    elif re.match(r"Hvad bliver (\d+),(\d+) hvis der skal afrundes til nærmeste hele tal?", equation):
        eqNums = re.findall(r"bliver (\d+),(\d+) hvis", equation)
        eqNums = eqNums[0]
        res = (str(round(float(eqNums[0] + '.' + eqNums[1]))).replace('.', ',')).replace(',0', '')
        return res

    else:
        print('Kunne ikke finde en løsning til ' + equation + ':(')
