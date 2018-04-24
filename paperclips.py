# versao 002 do codigo, tudo bem baguncado, depois componentizar
# threads dao problema com o Selenium, conflito de IO.

from selenium import webdriver
import os
import time
import thread
import random

# responde se o gap de tempo for maior que 10s
def isGapSec(lasttime=0, gap=10):
    now = time.time()
    if (lasttime == 0):
        return False, now
    elif (lasttime + 10 < now):
        return True, now
    else:
        return False, lasttime


browser = webdriver.Firefox()
url = "http://www.decisionproblem.com/paperclips/index2.html"
browser.get(url)


# define os objetos da pagina
def finder(elem):
    temp = browser.find_element_by_id(elem)
    return temp


paperclips = finder("clips")
def paperclipsnum():
    tmptxt = paperclips.text
    tmpnum = tmptxt.replace(",", "")
    return int(tmpnum)
makeclipbtn = finder("btnMakePaperclip")
wireCostDiv = finder("wireCost")
def wirecost():
    return float(wireCostDiv.text)
btnBuyWire = finder("btnBuyWire")
autoclipper = finder("btnMakeClipper")
projectListTop = finder("projectListTop")
fundsDiv = finder("funds")
def funds(): 
    return float(fundsDiv.text)
unsoldClipsDiv = finder("unsoldClips")
def unsoldClips():
    return float(unsoldClipsDiv.text)
btnLowerPrice = finder("btnLowerPrice")
btnRaisePrice = finder("btnRaisePrice")
btnExpandMarketing = finder("btnExpandMarketing")
#clipmakerRate2Div = finder("clipmakerRate2")
clipmakerRateDiv = finder("clipmakerRate")
def clipRPS():
    return float(clipmakerRateDiv.text)
#nanoWireDiv = finder("nanoWire")
wireDiv = finder("wire")
def remWire():
    wiretxt = wireDiv.text
    wirenum = wiretxt.replace(",", "")
    return int(wirenum)
clipperCostDiv = finder("clipperCost")
def clipperCost():
    return float(clipperCostDiv.text)
btnAddProc = finder("btnAddProc")
btnAddMem = finder("btnAddMem")
trustDiv = finder("trust")
processorsDiv = finder("processors")
memoryDiv = finder("memory")


def crescerComp():
    tr = float(trustDiv.text)
    pr = float(processorsDiv.text)
    me = float(memoryDiv.text)
    if (tr > (pr + me)):
        if (random.random() > 0.4):
            btnAddMem.click()
        else:
            btnAddProc.click()
        #print("-- --")
        #print("-- eh possivel crescer memoria ou CPU --")
        #print("-- comandos: --")
        #print("-- btnAddProc.click()")
        #print("-- btnAddMem.click()")
        #beeper(0.1, 880)
    

# define os objetos do projeto
# https://github.com/jgmize/paperclips

def tentaprojetos(qtdmax=1, minimo=1, maximo=219):
    qtde = 0
    for elem in range(minimo, maximo+1):
        if (qtde >= qtdmax):
            break
        try:
            exec("prj=projectListTop.find_element_by_id('projectButton{0}')".format(str(elem)))
            if (prj.is_enabled()):
                qtde += 1
                print("-- projeto escolhido: {0}".format(prj.text))
                prj.click()
        except:
            pass


# tenta projets e verifica comp a cada 5s

def prjcpuinfinito(cooldown=5, paperclipsmin=2000):
    if (paperclipsnum() < paperclipsmin):
        pass
    else:
        tentaprojetos()
        crescerComp()
    #time.sleep(cooldown)


# gera as logs
def getts():
    ts = time.localtime()
    return ts

def gethumantime():    
    ts = getts()
    return time.strftime("%Y-%m-%d %H:%M:%S", ts)

def logger():
    tmp = []
    tmp.append(gethumantime())
    tmp.append("paperclips: '{0}'".format(str(paperclipsnum())))
    tmp.append("funds: '{0}'".format(fundsDiv.text))
    tmp.append("unsoldClips: '{0}'".format(unsoldClipsDiv.text))
    return tmp

def record_logs():
    with open('logpaper.txt', 'a') as f:
        f.write(str(logger())+"\n")
    

# regras de negocio
# so compra fio se precisar

def buywire(minval=14):
    wirecst = wirecost()
    remwire = remWire()
    cliprps = clipRPS()
    if (remwire < 500*cliprps and wirecst <= minval):
        btnBuyWire.click()
    elif (remwire < 50*cliprps and wirecst <= minval+2):
        btnBuyWire.click()
    elif (remwire < 10*cliprps and wirecst <= minval+5):
        btnBuyWire.click()
    elif (remwire == 0):
        btnBuyWire.click()

def fazbuyinfinito():
    buywire()
    makeclipbtn.click()

def fazerclips(qtde=100):
    for n in range(qtde):
        makeclipbtn.click()
        if (n % 99 == 0): print("-- 100 --")

def fazbuy(qtde, minval=14):
    for n in range(qtde):
        buywire(minval)
        makeclipbtn.click()
        if (n % 99 == 0): print("-- 100 --")
    beeper()

def beeper(secs=0.5, freqs=440):
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (secs, freqs))

def goodstart(qtde):
    for n in range(qtde):        
        makeclipbtn.click()
        if (funds() >= 5.0):
            autoclipper.click()
    beeper(0.2, 660)
    beeper(0.4, 440)

def autoclip(qtde=5, intervalo=1):
    for n in range(qtde):        
        autoclipper.click()
    #time.sleep(intervalo)
    #beeper(0.2, 660)
    #beeper(0.2, 440)
    #beeper(0.4, 880)

print("-- inicio --")

def iniciorapido():
	# reduzir taxa para 18 pct
	for n in range(7):
	    makeclipbtn.click()
	    btnLowerPrice.click()

	print("-- preco reduzido para $ 0.18 --")
	print("-- aguarde 200 iteracoes...   --")

	# comeca jogando 85
	goodstart(85)

	# retorna taxa para 25 pct
	for n in range(7):
	    btnRaisePrice.click()
	    makeclipbtn.click()

	print("-- preco de volta em $ 0.25 --")


def threaders():

	time.sleep(0.5)

	# thread logger
	try:
	    thread.start_new_thread(record_logs,())
	except:
	    print("++ ERRO em: ")
	    print("-- thread.start_new_thread(record_logs,())")

	time.sleep(0.5)

	try:
	    thread.start_new_thread(prjcpuinfinito,())
	except:
	    print("++ ERRO em: ")
	    print("-- thread.start_new_thread(prjcpuinfinito,())")

	time.sleep(0.5)

	try:
	    thread.start_new_thread(fazbuyinfinito,())
	except:
	    print("++ ERRO em: ")
	    print("-- thread.start_new_thread(fazbuyinfinito,())")


## pseudo-threader

isAlive = True
isFazBuy = True
logTime = 0
cpumemTime = 0
comandos = []

def p(entra):
    global comandos
    comandos.append(entra)
    print("-- {0} cadastrado. existem {1} comandos na fila.".format(entra, str(len(comandos))))

def pseudothreader():
    global isAlive
    global isFazBuy
    global logTime
    global cpumemTime
    global comandos

    while(isAlive):
        boolLog, logTime = isGapSec(logTime, 10)
        if (boolLog):
            record_logs()
            boolLog = False
        boolMem, cpumemTime = isGapSec(cpumemTime, 12)
        if (boolMem):
            prjcpuinfinito()
            boolMem = False
        while (len(comandos) > 0):
            try:
                exec(comandos.pop())
            except:
                print("++ algo deu errado com um dos comandos !!!")
        if (isFazBuy):
            fazbuyinfinito()


thread.start_new_thread(pseudothreader,())

beeper(0.2, 440)
beeper(0.2, 660)
beeper(0.4, 440)

print("-- jogar --")

print("-- --")
print("-- comandos uteis: --")
#print("-- thread.start_new_thread(autoclip, (qtde=5, intervalo=1))")
#print("-- thread.start_new_thread(tentaprojetos, (qtdmax=1, minimo=1, maximo=219))")
print("-- isFazBuy = False --")
print("-- p("btnRaisePrice.click()") --")
print("-- p("btnLowerPrice.click()") --")
print("-- p("autoclip(qtde=1)") --")
print("-- p("btnExpandMarketing.click()") --")

print("-- --")
print("-- gaps: --")
print("-- auto-comprar memoria e CPU: --")

# fim
