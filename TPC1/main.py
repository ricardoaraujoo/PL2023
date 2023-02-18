import matplotlib.pyplot as plt

def parsing(ficheiro):
    with open(ficheiro) as my_file:
        listaLinhas = my_file.readlines()
        inicio=0
        infoDict= dict()
        infoDict["idade"]      = []
        infoDict["sexo"]       = []
        infoDict["tensao"]     = []
        infoDict["colesterol"] = []
        infoDict["batimento"]  = []
        infoDict["temDoenca"]  = []
        for linha in listaLinhas:
            linha = linha[:-1]
            if(inicio==0):
                inicio +=1
                continue
            idade,sexo,tensao,colesterol,batimento,temDoenca = linha.split(',')
            infoDict["idade"].append(int(idade))
            infoDict["sexo"].append(sexo)
            infoDict["tensao"].append(int(tensao))
            infoDict["colesterol"].append(int(colesterol))
            infoDict["batimento"].append(int(batimento))
            infoDict["temDoenca"].append(int(temDoenca))
    return infoDict

def doencaSexo(infoDict):
    dictDoencaSexo = {}

    i,f,m,fTotal,mTotal =0,0,0,0,0
    for element in infoDict["sexo"]:
        if(element == "M"):
            if((infoDict["temDoenca"][i])==1):
                m +=1
            mTotal +=1
        else:
            if((infoDict["temDoenca"][i])==1):
                f +=1
            fTotal +=1
        i+=1

    dictDoencaSexo["M"]= m/mTotal *100
    dictDoencaSexo["F"]= f/fTotal *100
    return dictDoencaSexo

def doencaEtario(infoDict):
    dictEtario = {}
    idadeMin = min(infoDict['idade'])
    idadeMax =max(infoDict['idade'])
    limMin = (idadeMin//5) *5
    i=0

    while(limMin <= idadeMax):
        n,nT,i = 0,0,0
        
        limMin4 = limMin +4
        for l in infoDict['idade']:
            if(l>=limMin and l<=limMin4):
                nT +=1
                if((infoDict['temDoenca'][i])==1):
                    n+=1
            i+=1
        dictEtario[f'{limMin}-{limMin4}']= (n/nT) *100
        
        limMin +=5
    return dictEtario

def doencaColesterol(infoDict):
    dictColesterol = {}
    colMin = min([x for x in infoDict['colesterol'] if x != 0])
    colMax = max(infoDict['colesterol'])

    while(colMin <= colMax):
        n,nT,i = 0,0,0
        colMin9 = colMin +9
        for l in infoDict['colesterol']:
            if(l>=colMin and l<=colMin9):
                nT +=1
                if((infoDict['temDoenca'][i])==1):
                    n+=1
            i+=1    
        if(nT !=0):
            dictColesterol[f'{colMin}-{colMin9}'] = (n/nT) *100
        else:
            dictColesterol[f'{colMin}-{colMin9}'] = 0
        colMin +=10
    return dictColesterol

def imprimeTabela(dictI):
    max=0
    for key in dictI:
        maxValue= len(f'|{key}|{dictI[key]}|')
        if(maxValue>max):
            max=maxValue
            
    sFinal=""
    sI=""
    sF=""
    i=0
    while(i<max):
            sI += "_"
            sF += "─"  
            i+=1
    for key in dictI:
        sLinha=f'|{key}|{dictI[key]}|' 
        sFinal+=f'{sI}\n{sLinha}\n{sF}\n'
    print(sFinal)

def grafos(dictInfo):
    x = []
    lastX = 0.5
    for key in dictInfo.keys():
        x.append(lastX)
        lastX+=1

    height = list(dictInfo.values())

    plt.bar(x, height,color="red")
    plt.xticks(x, list(dictInfo.keys()), rotation="vertical")
    plt.subplots_adjust(bottom=0.15)
    plt.show()





dictInfo = parsing("tpc1csv.csv")
dictDoencaSexo = doencaSexo(dictInfo)

dictEtario = doencaEtario(dictInfo)
#print(dictEtario)

dictColes = doencaColesterol(dictInfo)
#print(dictColes)

print("Por Sexo:")
imprimeTabela(dictDoencaSexo)
print("Por Faixa Etaria:")
imprimeTabela(dictEtario)
print("Por Nivel de Colesterol:")
imprimeTabela(dictColes)

grafos(dictDoencaSexo)
grafos(dictEtario)
grafos(dictColes)