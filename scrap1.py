import requests
from bs4 import BeautifulSoup
import time
import json

url = ""

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

content = soup.find(id="web")

table = soup.find("table", class_="npy_modTableInt")

arrCuentas = []

data = {}

data['cuentas'] = []

for numero in table.find_all("a", href=True):
    arrCuenta = [numero['href'], numero.text]
    arrCuentas.append(arrCuenta)

    #json
    
    
        
    #Scrap2
    
    time.sleep(3) # avoid site ban for too much traffic requests
    secondPage = requests.get(numero['href'])
    secondSoup = BeautifulSoup(secondPage.content, "html.parser")
    secondContent = secondSoup.find(id="web")
    
    details = secondContent.find("td", id="npy_tabla_cuentaPGC")

    definicion = secondContent.find("td", id="npy_celda_definicion")

    movDebe = secondContent.find("td", id="npy_celda_debe")

    movHaber = secondContent.find("td", id="npy_celda_haber")

    sigCuentas = secondContent.find("td", id="npy_celda_cuentasSig")

    ejemplos = secondContent.find("td", id="npy_celda_asientos")

    cuentasRelacionadas = secondContent.find("td", id="npy_celda_cuentas")

    #falta nota contenido <b>NOTA:</b>
    details = {}
    if definicion != None:
        print("Definicion: ",definicion.text, "\n")
        details['definición'] = definicion.text
    if movDebe != None: 
        print("movDebe: ",movDebe.text, "\n")
        details['movDebe'] = movDebe.text
    if movHaber != None:
        print("movHaber: " ,movHaber.text, "\n")
        details['movHaber'] = movHaber.text
    if sigCuentas != None:
        cuentas = sigCuentas.find_all("a", href=True)
        print("Cuentas siguientes: \n")
        cuentasSiguientes = {}
        for cuenta in cuentas:
            print(cuenta.text, cuenta['href'], "\n")
            cuentasSiguientes[cuenta.text] = cuenta['href']
        details['sigCuentas'] = cuentasSiguientes
    if ejemplos != None:
        arrEjemplos = ejemplos.find_all("a", href=True)
        print("Ejemplos: \n" )
        if not arrEjemplos :
            jsonEjemplos = {}
            for ejemplo in arrEjemplos:
                print(ejemplo.text, ejemplos["href"], "\n")
                jsonEjemplos[ejemplo.text] = ejemplos['href']
            details['ejemplos'] = jsonEjemplos
    if cuentasRelacionadas != None:
        masCuentas = cuentasRelacionadas.find_all("a", href=True)
        jsonMasCuentas = {}
        for cuenta in masCuentas:
            print(cuenta.text, cuenta['href'])
            jsonMasCuentas[cuenta.text] = cuenta['href']
        details['masCuentas'] = jsonMasCuentas

    data['cuentas'].append({
        'codigo' : numero.text,
        'detalles' : details
        }
    )

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)

    
    

#print(arrCuentas)



#print(numeros.prettify())