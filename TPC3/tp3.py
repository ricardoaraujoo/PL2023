import re
import collections
import json

def processarFile():
    with open("processos.txt","r") as file_D:
        linhas = file_D.readlines()

        pattern= re.compile(r"^(?P<Pasta>\d+)::(?P<Data>\d{4}\-\d{2}\-\d{2})?::(?P<Nome>[a-zA-Z \,\.\(\)]+)?::(?P<Pai>[a-zA-Z \,\.\(\)]+)?::(?P<Mae>[a-zA-Z \,\.\(\)]+)?::(?P<Observacoes>(\s*.*\s*)*)?::$")
        processedLinhas = []
        for linha in linhas:
            processedLinhas.append(pattern.match(linha).groupdict())

    return processedLinhas

def processosAno(lista):
    dic = {}
    pattern = re.compile(r"(\d{4})")
    for l in lista:
        data = l['Data']
        ano = pattern.match(data).group(0)
        if(ano in dic):
            dic[ano] +=1
        else:
            dic[ano] =1

    sorted_dic = dict(sorted(dic.items()))
    return sorted_dic


def processaNomes(lista):
    dic = {}
    patternAno = re.compile(r"(\d{4})")
    patternNome = re.compile(r"[a-zA-Z]+")
    for l in lista:

        if l['Nome'] is not None:
            nome = patternNome.findall(l['Nome'])

        if l['Pai'] is not None:
            nomePai = patternNome.findall(l['Pai'])
       
        if l['Mae'] is not None:
            nomeMae = patternNome.findall(l['Mae'])
        
        ano = patternAno.match(l['Data']).group(0)
        seculo = int(int(ano)/100 +1)

        if seculo not in dic:
                dic[seculo] = collections.defaultdict(int)
        if len(nome) !=0:
            dic[seculo][nome[0]] +=1
            dic[seculo][nome[-1]]+=1
        if len(nomePai) !=0:
            dic[seculo][nomePai[0]]+=1
            dic[seculo][nomePai[-1]] +=1
        if len(nomeMae) !=0:
            dic[seculo][nomeMae[0]]+=1
            dic[seculo][nomeMae[-1]]+=1
    dic = collections.OrderedDict(sorted(dic.items()))
    dicResultado = {}
    for k in dic.keys():
        dic[k] = collections.OrderedDict(sorted(dic[k].items(), key=lambda x: x[1], reverse=True))
    
        lista = list(dic[k].keys())[0:5]
        dicResultado[k] = lista

    return dicResultado

def relacoesFreq(lista):
    dicResultado = {}
    pattern = re.compile(r",((?:Pai|Filho|Irmao|Avo|Neto|Tio|Sobrinho|Meio|Primo])s?\b\s*[^.\d\(\)]*).")
    for l in lista:
        if l['Observacoes'] is not None:
            for m in re.finditer(pattern,l['Observacoes']):
                relacoes = m.group(1)
                print(relacoes)
                if (relacoes not in dicResultado):
                    dicResultado[relacoes]=0
                else:
                    dicResultado[relacoes]+=1
    return dicResultado
  

def processarParaJson(lista):
    with open('registos.json','w') as file:
        l = lista[0:20]
        json.dump(l,file)


processosAno(processarFile())
processaNomes(processarFile())
relacoesFreq(processarFile())
processarParaJson(processarFile())