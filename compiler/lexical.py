import ply.lex as lex
import re
import sys

# Palabras reservadas

reserved = (
    'int',
    'string',
    'boolean',
    'float',
    'void',

    'while',# iterador 1
    'for',
    'print' # reservado para imprimir valores
    #'return' falta evaluar retunrns
)

tok_variables = (
        'ID',          # x
        'CNE',         # 12 

)

# clase lexical del analizador sintactico
class Lexical(object):

    # Tokens
    tokens = (
        'TD1',       # Tipo de dato
        'TD2',
        'TD3',
        'TD4',
        'TD5',
        'OPAR1',      # +
        'OPAR2',      # -
        'OPAR3',      # *
        'OPAR4',      # /
        'OPAR5',      # % NO TOQUENIZA ESTE

        'OPRE1',       # >=
        'OPRE2',       # <=
        'OPRE3',       # ==
        'OPRE4',       #/ !=      
        'OPRE5',       # <
        'OPRE6',       # >
        'FLECHA',     # =>


        'OPL1',        # &&
        'OPL2',        # ||
        'OPL3',        #/ !

        'AS1',         # =
        'DEL1',        # (
        'DEL2',        # )
        'DEL3',        # {
        'DEL4',        # }
        'SEP1',        # ; 
        'SEP2',        # ,
        'VAL',         # valor de string: $"hello word"
        'PRT',         # reservado para imprimir valores
    
        'STRINGS',     # "SoyString"
        'FLOATNUM',    # 12.0
        'IT1',         # instruccion iterativa
        'IT2'

       #        ------ RECORDATORIO ------
       # 'TD',   # Tipos de datos: int, string, float, void
       # 'OP',   # Operadores aritmeticos: +, -, *, /
       # 'DEL',  # Delimitadores:  (, )
       # 'SEP',  # Misceláneos:  ,
       # 'ID',   # Identificadores:  Variables y nombres de funciones
       # 'CNE',  # Constantes numéricas:  0, 1, 23, 24
       # 'AS',   # Operador asignación:  =
       # 'IC',   # Ciclos:  while, for
       # 'OL'    # Operadores lógicos: >, <, <=, >=, == 

    ) + tok_variables

    # variables aux
    counters = {}
    names = {}
    error_count = 0
    errors = []    

    # declaración de tokens


    # Operadores Aritmeticos
    t_OPAR1 = r'\+'
    t_OPAR2 = r'-'
    t_OPAR3 = r'\*'
    t_OPAR4 = r'/'
    T_OPAR5 = r'\%'

    # Operadores Relacionales
    t_OPRE1 = r'>='
    t_OPRE2 = r'<='
    t_OPRE3 = r'=='
    t_OPRE4 = r'!='
    t_OPRE5 = r'<'
    t_OPRE6 = r'>'
    t_FLECHA = r'=>'

    # Operadores Lógicos
    t_OPL1 = r'&&'
    t_OPL2 = r'(\|\|)'
    t_OPL3 = r'!'

    # more..


    t_AS1 = r'='
    t_DEL1 = r'\('
    t_DEL2 = r'\)'
    t_DEL3 = r'\{'
    t_DEL4 = r'\}'
    t_SEP1 = r';'
    t_SEP2 = r','

    # dato que ignora espacios y tabs
    t_ignore = ' \t\v'

    # funcion para valores de strings
    def t_STRINGS(self, t):
        r'\"([^\\\n]|(\\(.|\n)))*?\"'
        t.type = 'VAL'
        t.value = str(t.value)
        return t

    # Función para los identificadores.
    def t_ID(self, t):
        r'[a-zA-Z_]\w*'
        # if para tokenizar TD, IT
        if t.value in reserved:
            if t.value == 'while':
                t.type = 'IT1'
            elif t.value == 'for':
                t.type = 'IT2'
            elif t.value == 'print':
                t.type = 'PRT'
            else:
                t.type = 'TD' + str(reserved.index(t.value) + 1)
        return t

    # Función para numeros flotantes (acepta: 12.212 | 12.)
    # NO HACE LOS FLOATS TIPO .12
    def t_FLOATNUM(self, t):
        r'([0-9]+\.\d*)'
        t.type = 'CNE'
        t.value = float(t.value)
        return t    

    # Función para numeros enteros. NOTIQUALS
    def t_CNE(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t    

    # Función para una contar las lineas saber donde esta el elemento actual
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    # Función para comentarios.
    def t_COMMENT(self, t):
        r'\#.*'
        pass

    # Función para token no valido. por cada error aumenta contador
    def t_error(self, t):
        line = t.lexer.lineno
        self.error_count += 1
        t.type = 'LXERR' + str(self.error_count)
        t.value = t.value[0]
        print ("Caracter ilegal %s en la linea %d" % (t.value[0], line))
        t.lexer.skip(1) # salta el token
        return t

    def __init__(self, **kwargs):
        # función inicial

        # contadores de tokens multiples
        for t in tok_variables:
            self.counters[t] = 0
        
        # inicializar los errores en vacio
        self.errors = list()
        self.lexer = lex.lex(module=self, **kwargs)

    def tokenizer(self, data):
        # recibe el codigo

        # archivo de tokens, tabla de simbolos y tokens multiples
        tokenFile = list()
        seen = set()
        simtable = list()

        # abrir archivos TXT
        filetabla = open("output/tablafile.txt", "w+") 
        #filetokens = open("output/tokensfile.txt", "w+") 

        # Titulos de la tabla de simbolos
        filetabla.write("   TABLA DE SIMBOLOS \n \n")
        filetabla.write("  LEXEMA    TOKEN       TIPO \n \n")

        self.lexer.input(data)

        while True:
            #mientras haya tokens insertalos
            token = self.lexer.token()
            if not token:
                break

            # ---- ver los tokens en la lista de tokens ----
            #print(token, token.lineno, token.type, token.value)

            if token.value not in seen:
                # si el tokens no esta duplicado agregalo
                seen.add(token.value)
                if token.type in tok_variables:
                    # si es token multiple
                    # aumenta el contador
                    self.counters[token.type] += 1
                    token.type += str(self.counters[token.type])
                    self.names[token.value] = token.type
                
                # escribir en tabla de simbolos txt
                filetabla.write('{:^10}{:^10}\n'.format(f'{token.value}', f'{token.type}'))
                simtable.append({
                    'line': token.lineno,
                    'type': token.type,
                    'value': token.value,
                    'pos': token.lexpos
                })
            elif token.type in tok_variables:
                # si ya esta repetido asignar el token existente
                token.type = self.names[token.value]
            
            # agregarlo a la lista de tokens
            tokenFile.append({
                'line': token.lineno,
                'type': token.type,
                'value': token.value,
                'pos': token.lexpos
            })
            # escribir un salto de linea o espacio en el archivo
            #if token.type == 'SEP1':
                #filetokens.write(token.type + '\n')
            #elif token.type == 'DEL3':
                #filetokens.write(token.type + '\n')
            #elif token.type == 'DEL4':
                #filetokens.write(token.type + '\n')
            #else:
                #filetokens.write(token.type + ' ')
            
        
        # cerrar archivos
        filetabla.close()
        #filetokens.close()
        return tokenFile, simtable


# Main
if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    datos = f.read()
    f.close()
    JL = Lexical()
    TF, ST = JL.tokenizer(datos)

    print("\n Tabla de simbolos \n")
    for simtable in ST:
        print(simtable)
    

    print("\n Tokens de tokenFile \n")
    for tokenfile in TF:
        print(tokenfile)
