import requests
from bs4 import BeautifulSoup
import time
import json
import time


'''
    "SubGrupo" : {
        "definicion": "String"
        "cuentas" : []
    }
    '''
def getSubGrupo(url):
    jsonSubGrupo = {}
    

    time.sleep(2) # avoid site ban for too much traffic requests
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    definicion = soup.find("td", id="npy_celda_definicion")
    sigCuentas = soup.find("td", id="npy_celda_cuentasSig")
    
    if sigCuentas != None:
        arrUrlCuentas = sigCuentas.find_all("a", href=True)
        arrCuentas = []
        for url in arrUrlCuentas:            
            cuenta = getCuenta(url["href"])
            arrCuentas.append(cuenta)
        jsonSubGrupo["definicion"] = definicion.text
        jsonSubGrupo["cuentas"] = arrCuentas
    return jsonSubGrupo

    '''
    "cuenta" : {
        "definición" : "String",
        "movDebe" : "String",
        "movHaber" : "String",
        "ejemplos" : "url"
        "cuentasRelacionadas": [
            url
        ]
    }
    '''
def getCuenta(url):
    cuenta = {}
    time.sleep(2) # avoid site ban for too much traffic requests
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    nombreCuenta = soup.find("h1")
    definicion = soup.find("td", id="npy_celda_definicion")
    movDebe = soup.find("td", id="npy_celda_debe")
    movHaber = soup.find("td", id="npy_celda_haber")
    ejemplos = soup.find("td", id="npy_celda_asientos")
    cuentasRelacionadas = soup.find("td", id="npy_celda_cuentas")

    cuenta = {}
    if nombreCuenta != None:
        cuenta['codigo'] = str(nombreCuenta.text).split()[0].replace(".", "")
        cuenta['nombre'] = " ".join(str(nombreCuenta.text).split()[1:])
    if definicion != None:
        #print("Definicion: ",definicion.text, "\n")
        cuenta['definición'] = definicion.text
    if movDebe != None: 
        #print("movDebe: ",movDebe.text, "\n")
        cuenta['movDebe'] = movDebe.text
    if movHaber != None:
        #print("movHaber: " ,movHaber.text, "\n")
        cuenta['movHaber'] = movHaber.text
    if ejemplos != None:
        arrEjemplos = ejemplos.find_all("a", href=True)
        #print("Ejemplos: \n" )
        if not arrEjemplos :
            jsonEjemplos = {}
            for ejemplo in arrEjemplos:
                #print(ejemplo.text, ejemplos["href"], "\n")
                jsonEjemplos[ejemplo.text] = ejemplos['href']
            cuenta['ejemplos'] = jsonEjemplos
            '''
    if cuentasRelacionadas != None:
        masCuentas = cuentasRelacionadas.find_all("a", href=True)
        arrCuentasRelacionadas = []
        for cuenta in masCuentas:
            print(cuenta.text, "\n")
            arrCuentasRelacionadas.append(cuenta.text)
        cuenta['cuentasRelacionadas'] = arrCuentasRelacionadas
        '''
          
        
    return cuenta

startTime = time.time()

url = ""

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

content = soup.find(id="web")

table = soup.find("table", id="npy_tabla_cuentaPGC")

groupName = soup.find("h1")
definicion = table.find("td", id="npy_celda_definicion")

'''
cuentasRelacionadas = table.find("td", id="npy_celda_cuentas")

print("cuentas relacionadas", cuentasRelacionadas)
cuentasRelacionadas = []
if cuentasRelacionadas != None:
    masCuentas = cuentasRelacionadas.find_all("a", href=True)
    jsonCuentasRelacionadas = {}
    for idx, cuenta in enumerate(masCuentas):
        print(cuenta.text, cuenta['href'])
        jsonCuentasRelacionadas[idx] = cuenta.text
        cuentasRelacionadas.append(jsonCuentasRelacionadas)
'''

subGruposSiguientes = table.find("td", id="npy_celda_cuentasSig")

if subGruposSiguientes != None:
    urlSubGrupo = subGruposSiguientes.find_all("a", href=True)
    arrSubGrupos = []
    for url in urlSubGrupo:
        time.sleep(2) # avoid site ban for too much traffic requests
        subGrupo = getSubGrupo(url["href"])
        arrSubGrupos.append(subGrupo)
    

    #json
    group = {}

    g1 = table.find_all("a", href=True)
    
    '''
    grupo = {
    "código" : groupName.text,
    "definición" : definicion,
    "subGrupos" : {
        #array
    },
        #"cuentasRelacionadas" :  cuentasRelacionadas
    }
    '''

    group["codigo"] = groupName.text
    group["definicion"] = definicion.text
    group["subGroups"] = arrSubGrupos

    with open('grupo.txt', 'w', encoding="utf-8") as outfile:
        json.dump(str(group), outfile)

print("Scrapped in %s seconds" % (time.time() - startTime)) 

