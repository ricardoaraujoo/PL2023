import sys

def lerStdin():
    somaALL= 0
    flag=True
    sOff,sOn,soma ="","","0"
    for line in sys.stdin:
        for letter in line.rstrip():
            sOff,sOn = checkString(letter,sOff,sOn)
            if(sOff == "off"):
                flag=False
                sOff=""
                sOn=""
            if(sOn == "on"):
                flag=True
                sOn=""
                sOff=""
            
            if(letter.isdigit() and flag):
                soma += letter
            else:
                somaALL += int(soma)
                soma="0"
            if letter in ['=']:
                print(somaALL)
        somaALL += int(soma)
        soma="0"

    return somaALL

def checkString(letter,sOff,sOn):
    if letter in ['o', 'O']:
            sOff += letter.lower()
            sOn  += letter.lower()
    if letter in ['f', 'F']:
            sOff += letter.lower()    
    if letter in ['n', 'N']:
            sOn  += letter.lower()
    
    return sOff,sOn

lerStdin()