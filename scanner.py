# Implementación de un scanner mediante la codificación de un Autómata
# Finito Determinista como una Matríz de Transiciones# Autor: Dr. Santiago Conant, Agosto 2014 (modificado en Agosto 2015)
# Lucia Cantú-Miller A01194199
# Héctor Luis Díaz Aceves A01176866
# Ivan Alejandro Anguiano Leal A00817460


import sys

# tokens
INT = 100  # Número entero
FLT = 101  # Número de punto flotante
OPB = 102  # Operador binario
LRP = 103  # Delimitador: paréntesis izquierdo
RRP = 104  # Delimitador: paréntesis derecho
END = 105  # Fin de la entrada
EQL = 106  # Simbolo '='
QST = 107  # Simbolo '?'
DPS = 108  # Simbolo d':'
OPL = 109  # Operadores relacionales
IDE = 110  # Identificadores (letras minusculas)
EXC = 111  # Simbolo '!'
ERR = 200  # Error léxico: palabra desconocida

# Matriz de transiciones: codificación del AFD
# [renglón, columna] = [estado no final, transición]
# Estados > 99 son finales (ACEPTORES)
# Caso especial: Estado 200 = ERROR
#      dig   op   (    )  raro  esp  .  =  ?    :   opr  let  !   $
MT = [[  1, OPB, LRP, RRP,   4,   0, 4,EQL,QST,DPS, OPL, IDE, EXC,END], # edo 0 - estado inicial
      [  1, INT, INT, INT, INT, INT, 2,INT,INT,INT, INT, INT, INT,INT], # edo 1 - dígitos enteros
      [  3, ERR, ERR, ERR,   4, ERR, 4,ERR,ERR,ERR, ERR, ERR, ERR,ERR], # edo 2 - primer decimal flotante
      [  3, FLT, FLT, FLT, FLT, FLT, 4,FLT,FLT,FLT, FLT, FLT, FLT,FLT], # edo 3 - decimales restantes flotante
      [ERR, ERR, ERR, ERR,   4, ERR, 4,ERR,ERR,ERR, ERR, ERR, ERR,ERR]] # edo 4 - estado de error

# Filtro de caracteres: regresa el número de columna de la matriz de transiciones
# de acuerdo al caracter dado
def filtro(c):
    """Regresa el número de columna asociado al tipo de caracter dado(c)"""
    if c == '0' or c == '1' or c == '2' or \
       c == '3' or c == '4' or c == '5' or \
       c == '6' or c == '7' or c == '8' or c == '9': # dígitos
        return 0
    elif c == '+' or c == '-' or c == '*' or \
         c == '/': # operadores
        return 1
    elif c == '(': # delimitador (
        return 2
    elif c == ')': # delimitador )
        return 3
    elif c == ' ' or ord(c) == 9 or ord(c) == 10 or ord(c) == 13: # blancos
        return 5
    elif c == '.': # punto
        return 6
    elif c == '=': # simbolo =
        return 7
    elif c == '?': # simbolo ?
        return 8
    elif c == ':':  # simbolo :
        return 9
    elif c == '<' or c == '>' or c == '>=' or c == '==': # operadores relacionales
        return 10
    # identificadores (letras minusculas)
    elif c == 'a' or c == 'b' or c == 'c' or c == 'd' or c == 'e' or c == 'f' or \
        c == 'g' or c == 'h' or  c == 'i' or c == 'j' or  c == 'k' or c == 'l' or \
        c == 'm' or c == 'n' or c == 'o' or c == 'p' or c == 'q' or c == 'r' or \
        c == 's' or c == 't' or c == 'u' or c == 'v' or c == 'w' or c == 'x' or \
        c == 'y' or c == 'z':
        return 11
    elif c == '!': # simbolo !
        return 12
    elif c == '$':  # fin de entrada
        return 13
    else: # caracter raro
        return 4

# Función principal: implementa el análisis léxico
def scanner():
    """Implementa un analizador léxico: lee los caracteres de la entrada estándar"""
    edo = 0 # número de estado en el autómata
    lexema = "" # palabra que genera el token
    tokens = []
    leer = True # indica si se requiere leer un caracter de la entrada estándar
    while (True):
        while edo < 100:    # mientras el estado no sea ACEPTOR ni ERROR
            if leer: c = sys.stdin.read(1)
            else: leer = True
            edo = MT[edo][filtro(c)]
            if edo < 100 and edo != 0: lexema += c
        if edo == INT:    
            leer = False # ya se leyó el siguiente caracter
            print("Entero", lexema)
        elif edo == FLT:   
            leer = False # ya se leyó el siguiente caracter
            print("Flotante", lexema)
        elif edo == OPB:   
            lexema += c  # el último caracter forma el lexema
            print("Operador", lexema)
        elif edo == LRP:   
            lexema += c  # el último caracter forma el lexema
            print("Delimitador", lexema)
        elif edo == RRP:  
            lexema += c  # el último caracter forma el lexema
            print("Delimitador", lexema)
        elif edo == EQL:
            lexema += c # el ultimo caracter forma el lexema
            print("Delimitador", lexema)
        elif edo == QST:
            lexema += c # el ultimo caracter forma el lexema
            print("Delimitador", lexema)
        elif edo == DPS:
            lexema += c # el ultimo caracter forma el lexema
            print("Delimitador", lexema)
        elif edo == OPL:
            lexema += c # el ultimo caracter forma el lexema
            print("Operadores", lexema)
        elif edo == IDE:
            lexema += c # el ultimo caracter forma el lexema
            print("caracter", lexema)
        elif edo == EXC:
            lexema += c # caracter final
            print("Simbolo", lexema)
        elif edo == ERR:   
            leer = False # el último caracter no es raro
            print("ERROR! palabra ilegal", lexema)
        tokens.append(edo)
        if edo == END: return tokens
        lexema = ""
        edo = 0
