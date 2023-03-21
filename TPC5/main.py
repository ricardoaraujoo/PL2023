import ply.lex as lex
import re

money= (0,0)
flag = 0

tokens = (
    'ligado',
    'desligado',
    'abortado',
    'dinheiro',
    'fone'
)

t_ignore  = ' \t'

def t_ligado(t) :
    r'LEVANTAR'  
    global flag
    flag = 1
    print("Bem vindo!")


def t_desligado(t): 
    r'POUSAR' 
    global flag
    flag = 0
    
    ne,nc = money
    print( f'troco: {ne}e{nc}c .Volte sempre!!')

def t_abortado(t) :
    r'ABORTAR'
    global flag
    flag = 2
    
    print("Abortado!")

def custoChamada(tuple2):
    global money
    er,ce = money
    print(tuple2)
    print(money)
    eur2, cent2 = tuple2

    centimos1 = er*100 + ce
    centimos2 = eur2*100 + cent2

    centimos1= centimos1 - centimos2
    e = centimos1//100
    c= centimos1 %100

    money = (e,c)

def saldo(eur,cent):
    global money
    er,ce = money
    e = er + sum(eur) +(sum(cent)+ce)//100
    c = (sum(cent)+ce)%100
    money = (e,c)
    return (e,c)

def numeroTelefonico(n):
    global money
    e,c = money
    custo = (0,0)
    print("O saldo disponível é:" + str(money))
    if (len(n) == 11) and (n[:2] == "00"):
        if e<1:
            print("Saldo insufeciente, é necessário 1,5e")
            return None
        elif e==1 and c<50:
            print("Saldo insufeciente, é necessário 1,5e")        
            return None
        else:
            custo= (1,50)
            custoChamada(custo)
            print("Chamada efetuada")
            return n
    elif len(n)==9 and (n[:3]== "601" or n[:3]== "641"):
            print("Chamada Bloqueada")
            return None
    elif len(n)==9 and (n[:1]== "2"):
        if e==0:
            if c<25:
                print("Saldo insufeciente, é necessário 25centimos")        
                return None
        custo = (0,25)
        custoChamada(custo)
        print("Chamada efetuada")
        return n
    elif len(n)==9 and n[:3]== "808" :
        if e==0:
            if c<10:
                print("Saldo insufeciente, é necessário 10centimos")        
                return None
        custo = (0,10)
        custoChamada(custo)
        print("Chamada efetuada")
        return n
    elif len(n)==9 and n[:3]== "800":
        print("Chamada efetuada")
        return n
    else:
        print("Erro")
        return None

#1c 2c 5c 10c 20c 50c 1e 2e
def t_dinheiro(t):
    r'MOEDA .+'
    global flag
    if flag != 1:
        print("Antes de inserir moedas precisa de levantar o telefone!")
        return t
    
    cent =[0]
    eur = [0]
    matches = re.findall(r'\b(50|20|10|5|2|1)c',t.value)
    if matches != None:
        for match in matches:
            cent.append(int(match))

    matches2 = re.findall(r'\b(2|1)e',t.value)
    if matches2 != None:
        for match2 in matches2:
            eur.append(int(match2))
    e = sum(eur) + sum(cent)//100
    c = sum(cent)%100
    t.value = (e,c)
    print("Saldo carregado com" + str(t.value))
    return t

def t_fone(t):
    r'T=\d{9,11}'
    global flag
    if flag != 1:
        print("Antes de ligar precisa de levantar o telefone!")
        return t
    
    match = re.match(r'T\=(\d{9,11})',t.value).group(1)
    print("O numero marcado foi: " + match)
    n =numeroTelefonico(match)
    if(n==None):
        return t
    t.value = n
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()

data = """
LEVANTAR
ABORTAR
LEVANTAR
MOEDA 20c, 2c 10c, 1e, 3e 25c
MOEDA 1e.
T=00934662832
T=00934662832
POUSAR"""

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    

lexer.token()



