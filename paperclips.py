# versao 001 do codigo, tudo bem baguncado, depois componentizar

from selenium import webdriver
import os

browser = webdriver.Firefox()
url = "http://www.decisionproblem.com/paperclips/index2.html"
browser.get(url)
makeclipbtn = browser.find_element_by_id("btnMakePaperclip")
wirecost = browser.find_element_by_id("wireCost")
btnBuyWire = browser.find_element_by_id("btnBuyWire")
autoclipper = browser.find_element_by_id("btnMakeClipper")
projectListTop = browser.find_element_by_id("projectListTop")

def buywire(minval=14):
    if (int(wirecost.text) <= minval):
        btnBuyWire.click()

def fazerclips(qtde=100):
    for n in range(qtde):
        makeclipbtn.click()

def fazbuy(qtde):
    for n in range(qtde):
        buywire()
        makeclipbtn.click()
    beeper()

def beeper(secs=0.5, freqs=440):
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (secs, freqs))
