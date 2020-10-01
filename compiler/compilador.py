from lexical import Lexical
from sintactico import Sintactic
import sys
import re




if __name__ == "__main__":
    filetabla = open("output/tablafile.txt", "w+")
    tokensfilear = open("output/tokens.txt", "w+")
    errorsfile = open("output/errors.txt", "w+")

    f = open(sys.argv[1], 'r')
    datos = f.read()
    f.close()

    JL = Lexical()
    JP = Sintactic()

    tokensFile, simbolTable = JL.tokenizer(datos)
    errors, names = JP.compile(datos)
    for t in simbolTable:
        if re.match(r'ID', t['type']):
            try:
                t['vartype'] = names[t['value']]['vartype']

            except Exception as err:
                print(err)



    # metiendo datos a las diferentes tablas
    filetabla.write("   TABLA DE SIMBOLOS \n \n")
    filetabla.write("  LEXEMA    TOKEN       TIPO \n \n")

    for x in range(0,len(simbolTable)):
        if 'vartype' in simbolTable[x]:
            filetabla.write('{:^10}{:^10}{:^10}\n'.format(f"{simbolTable[x]['value']}", f"{simbolTable[x]['type']}",f"{simbolTable[x]['vartype']}"))
        else:
            filetabla.write('{:^10}{:^10}\n'.format(f"{simbolTable[x]['value']}", f"{simbolTable[x]['type']}"))
            
                       

    # TABLA DE TOKENS
    for x in range(0,len(tokensFile)):
        if tokensFile[x]['type'] == 'SEP1':
            tokensfilear.write(tokensFile[x]['type'] + '\n')
        elif tokensFile[x]['type'] == 'DEL3':
            tokensfilear.write(tokensFile[x]['type'] + '\n')
        elif tokensFile[x]['type'] == 'DEL4':
            tokensfilear.write(tokensFile[x]['type'] + '\n')
        else:
            tokensfilear.write(tokensFile[x]['type'] + ' ')

    
    #TABLA DE ERRORES(errores sintacticos)
    errorsfile.write("  ERROR      LEX       LINE        DESC \n \n")
    for x in range(0,len(errors)):
        errorsfile.write('{:^10}{:^10}{:^10}{:^10}\n'.format(f"{errors[x]['type']}", f"{errors[x]['value']}",f"{errors[x]['line']}",f"{errors[x]['desc']}"))

    filetabla.close()
    tokensfilear.close()
    errorsfile.close()


