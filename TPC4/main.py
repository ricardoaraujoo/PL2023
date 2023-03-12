import re
import json
import sys

file = sys.argv[1]
listJson = []
fPattern= re.compile(r"(?P<Numero>[^,]+),(?P<Nome>[^,]+),(?P<Curso>[^,]+),?(?P<Notas>[^{,]+)?(?P<Int>\{\d(?:,\d)?\})?(?:::)?(?P<Agreg>[^,]+)?")
with open(file,'r') as fileObj:
    dicT = {}
    primeiraLinha = fileObj.readline()[:-1]
    cabecalho = (fPattern.match(primeiraLinha).groupdict())
    linhas = fileObj.readlines()
    for linha in linhas:
        listDados = linha.replace('\n', '').split(',')

        if(cabecalho['Numero']is not None):
            dicT['Numero'] = listDados[0]
        if(cabecalho['Nome']is not None):
            dicT['Nome'] = listDados[1]
        if(cabecalho['Curso']is not None):
            dicT['Curso'] = listDados[2]

        listSum = []
        if(cabecalho['Notas']is not None):
            if(cabecalho['Int']is not None):
                intPattern = re.compile(r"{(?P<pN>\d),?(?P<uN>\d)?}")
                numeros= (intPattern.match(cabecalho['Int']).groupdict())
                pN = int(numeros['pN'])
                if(cabecalho['Agreg']is not None):
                    soma = 0
                    if cabecalho['Agreg'] == 'sum':
                        if(numeros['uN'] is not None):
                            uN = int(numeros['uN'])
                            for i in range(0,uN):
                                if(listDados[i+3].isdigit()):
                                    soma += int(listDados[i+3])
                        else:
                            for i in range(0,pN):  
                                if(listDados[i+3].isdigit()):
                                    soma += int(listDados[i+3])  
                        dicT['Nota'] = soma
                    else:
                        m=0
                        if(numeros['uN'] is not None):
                            uN = int(numeros['uN'])
                            for i in range(0,uN):
                                if(listDados[i+3].isdigit()):
                                    soma += int(listDados[i+3])
                                    m+=1
                        else:
                            for i in range(0,pN):  
                                if(listDados[i+3].isdigit()):
                                    soma += int(listDados[i+3])
                                    m+=1
                        dicT['Nota'] = soma/m

                else:
                    if(numeros['uN'] is not None):
                        uN = int(numeros['uN'])
                        for i in range(0,uN):
                            listSum.append(listDados[i+3])
                    else:
                        for i in range(0,pN):
                            listSum.append(listDados[i+3])
                    dicT['Nota'] = listSum
            else:
                dicT['Nota'] = listDados[3]
        listJson.append(dicT)
        dicT = {}
        listSum = []


print(listJson)
with open("data.json", "w") as outfile:
    json.dump(listJson,outfile,indent=4, ensure_ascii = False)