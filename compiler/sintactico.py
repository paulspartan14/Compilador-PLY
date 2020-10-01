import ply.yacc as yacc
import sys
from lexical import Lexical


class Sintactic(object):
    
    # aqui ira la precedence
    precedence = ()

    # dictionary of names (for storing variables)
    names = {}
    functions = {}
    vars = list()
    errors = list()
    tokens = Lexical.tokens
    errsemcount = 0
    errsint = 0

    # PROGRAM #
    def p_program(self, p):
        ''' program : S '''
    pass

    # START
    def p_start_prod_or_sep(self, p):
        ''' S : production S 
                | production SEP1 S '''
        print("tengo ;")
    pass

    def p_start_only_prod(self, p):
        ' S : production '
        print("soy produccion")
        pass

    # PRODUCTIONS #
    def p_production_decl_sep(self, p):
        ' production : declaracion SEP1 '
        print("estoy entrando a declaracion SEP1")
        pass

    def p_expressions(self, p):
        ' production : expression SEP1 '
        print("entro a expresion ;")
        pass

    def p_functions(self, p):
        ' production : function '
        print('funcion')
        pass

    # ITERATORS #

    def p_iterators(self, p):
        ' production : iterators '
        print('iterador')
        pass

    # DECLARATIONS #

 # aqui se puede poner el error de tipo de dato diferente, ej: string a = 12; ( ya se evalua ./ ) y evalua correctamente
    def p_var_declarations(self, p):
        ' declaracion : types ID AS1 expression '

        td = None # value type

        # metodos para reutilizar valor correcto y el error
        def type_correcto():
            self.names[p[2]] = {
                'value': td,
                'vartype': p[1],
                'line': p.lineno(2),
                'pos': p.lexpos(2)
                }
            p[0] = p[4]
        
        def type_incorrecto():
            print('Incompatible Types')
            self.errsemcount += 1
            self.errors.append({
                'line': p.lineno(2),
                'value': p[1],
                'desc': "incompatible types",
                'type': f"ERRSEM{self.errsemcount}",
                'pos': p.lexpos(2)
                })
            p[0] = 0
            pass

        # INICIA EVALUACION AL DECLARAR VARIABLES    
        if p[1] == 'int':
            # evalua si es numero entero
            if isinstance(p[4], int):
                print(f'variable INT declarada')
                td = int(p[4])
                type_correcto()                
            else:
                type_incorrecto()
                
        elif p[1] == 'float':
            # evalua si es numero float
            if isinstance(p[4], float):
                print(f'variable FLOAT declarada')
                td = float(p[4])
                type_correcto()
            else:
                type_incorrecto()

        elif p[1] == 'boolean': # aun no evaluamos booleanos
            td = bool(p[4])
            type_correcto()

        elif p[1] == 'string':            
            if isinstance(p[4], str):
                print(f'variable STR declarada')
                td = str(p[4])
                type_correcto()
            else:
                type_incorrecto()

    #ej: in3t a = 12;  toma in3t como variable y no como type y a como id
    def p_var_declarations_error(self, p):
        ' declaracion : ID ID AS1 expression '
        print('1.-ERROR DE REDECLARACION ID:', p[1])
        self.errors.append({
            'line': p.lineno(1),
            'value': p[1],
            'desc': 'type error',
            'type': 'ERRLXTD',
            'pos': p.lexpos(1)
        })

    # EXPRESSIONS #

    def p_expression_binop(self, p):
        ''' expression : expression OPAR1 expression
                    | expression OPAR2 expression
                    | expression OPAR3 expression
                    | expression OPAR4 expression
                    | expression OPAR5 expression '''
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
    
    def p_expression_group(self, p):
        'expression : DEL1 expression DEL2'
        p[0] = p[2]

    # valida si el id existe, si no da un lookuperror
    def p_expression_name(self, p):
        ' expression : ID '
        try:
            p[0] = self.names[p[1]]['value']
            print(self.names[p[1]]['value'])
        except LookupError:
            print(f"Variable {p[1]!r} no definida")
            self.errsemcount += 1
            self.errors.append({
                'line': p.lineno(1),
                'value': p[1],
                'desc': "Undefined name",
                'type': f"ERRSEM{self.errsemcount}",
                'pos': p.lexpos(1)
            })
            p[0] = 0

    # valida error con redefinicion de valor intenta cambiarlo (falta que sea tipo de dato)
    def p_expression_name_assign(self, p):
        ' expression : ID AS1 expression '

        try:
            self.names[p[1]]['value'] = p[3]
            print("variable redefinida")
        except LookupError:
            print(f"Variable {p[1]!r} no definida")
            self.errsemcount += 1
            self.errors.append({
                'line': p.lineno(1),
                'value': p[1],
                'desc': "Undefined name",
                'type': f"ERRSEM{self.errsemcount}",
                'pos': p.lexpos(1)
            })
            p[0] = 0
   
    
    def p_expression_number(self, p):
        ' expression : CNE '
        p[0] = p[1]

    def p_expression_string(self, p):
        ' expression : VAL '
        p[0] = p[1]

    def p_expression_empty(self, p):
        'expression : '
        pass

    # FUNCTIONS #
    def p_function(self, p):
        ' function : types ID DEL1 argv DEL2 DEL3 S DEL4 '
        self.functions[p[2]] = 0

    # error de id duplicada
    def p_function_error(self, p):
        ' function : ID ID DEL1 argv DEL2 DEL3 S DEL4'
        print(p[1], p[2])
        self.functions[p[2]] = 0

    def p_argv(self, p):
        '''  argv : argv_rec
                  |  '''
        pass

    def p_argv_rec(self, p):
        ''' argv_rec : types ID SEP2 argv_rec 
                    | types ID '''
        value = None
        if p[1] == 'int':
            value = 0
        elif p[1] == 'float':
            value = 0
        elif p[1] == 'boolean':
            value = false
        elif p[1] == 'string':
            value = ''
        self.names[p[2]] = {
            'value': value,
            'vartype': p[1],
            'line': p.lexpos(2)
        }
    
    def p_types(self, p):
        ''' types : TD1
                  | TD2
                  | TD3
                  | TD4
                  | TD5 '''
        p[0] = p[1]
    
    # ITERADORES
    def p_whileStmt(self, p):
        ' iterators : IT1 DEL1 expr DEL2 DEL3 S DEL4 '
        print(p[1])

    def p_expr(self, p):
        'expr : expr_rec'
        pass

    def p_expr_rec(self, p):
        ''' expr_rec : val relational val
                      | val logical val                      
                      | val logical expr_rec                      
                      | val relational expr_rec
                      | val '''
        pass
    
    def p_val(self, p):
        ''' val : ID 
                | CNE'''
        p[0] = p[1]
    
    def p_relational(self, p):
        ''' relational : OPRE1
                    | OPRE2
                    | OPRE3
                    | OPRE4
                    | OPRE5
                    | OPRE6 '''
        p[0] = p[1]

    def p_logical(self, p):
        ''' logical : OPL1 
                    | OPL2
                    | OPL3'''
        p[0] = p[1]


    # errores

    def p_error(self, p):
        print(f"Unespected token '{p.value}'")  
        self.errsint +=1
        self.errors.append({
            'line': p.lineno,
            'value': p.value,
            'desc': "Unespected token",
            'type': f"ERRLEX{self.errsint}",
            'pos': p.lexpos
        })
        pass

    def __init__(self):
        self.errors = list()
        self.errsemcount = 0
        self.lexer = Lexical()
        self.parser = yacc.yacc(module=self)

    def compile(self, program):
        self.parser.parse(program)
        return self.errors, self.names

# MAIN

if __name__ == "__main__":
    try:
        f = open(sys.argv[1], 'r')
        program = f.read()
        f.close
        ERR, NM = Sintactic().compile(program)
        print(f"\n{NM}\n") # imprime nombres con valores
        print(ERR) # imprime errores
    except IndexError:
        while True:
            try:
                s = input('compilador > ')
            except EOFError:
                break
            Sintactic().parser.parse(s)





    



























'''precedence = (
    ('right', 'AS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'EQUALS'),
    ('left', 'LPARENT', 'RPARENT') 
    # en la precedencia se mira de abajo hacia arria
    # abajo es el mas importante, arriba menos importante
)
'''
'''

    Rule 0       program -> S
    Rule 1       S -> produccion S
    Rule 2       S -> produccion END_LINE S
    Rule 3       S -> produccion
    Rule 4       produccion -> declaracion END_LINE
    Rule 5       produccion -> expresion END_LINE
    Rule 6       produccion -> funcion
    Rule 7       declaracion -> TD1 ID AS1 expresion
    Rule 8       expresion -> expresion OPAR1 expresion --
    Rule 9       expresion -> DEL1 expresion DEL2
    Rule 10      expresion -> CNE
    Rule 11      expresion -> <empty> --
    Rule 12      expresion -> ID ---
    Rule 13      expresion -> ID AS1 expresion
    Rule 14      funcion -> TD1 ID DEL1 argumento DEL2 DEL3 S DEL4
    Rule 15      argumento -> argumento_dec
    Rule 16      argumento -> <empty>
    Rule 17      argumento_dec -> TD1 ID SEP1 argumento_dec
    Rule 18      argumento_dec -> T1 ID

    falta iteradores

    program = block
    block = const-decl var-decl proc-decl statement
    const-decl = CONST const-asigment-list | e

 '''
# sentencias #
# Producciones #
# no terminales, terminales y producciones vacias #

