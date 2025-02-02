import ply.yacc as yacc
from futbol_lexer import tokens

# Nodo base para el AST
class Nodo:
    def __init__(self, tipo, valor=None, hijos=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = hijos or []

    def __repr__(self):
        return f"{self.tipo}({self.valor}, {self.hijos})"

# Regla inicial
def p_programa(p):
    '''programa : lista_funciones'''
    p[0] = Nodo('programa', hijos=p[1])

def p_lista_funciones(p):
    '''lista_funciones : lista_funciones funcion
                       | funcion'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_funcion(p):
    '''funcion : JUGADOR ID LPAREN parametros RPAREN COLON bloque'''
    p[0] = Nodo('funcion', valor=p[2], hijos=[p[4], p[7]])

def p_parametros(p):
    '''parametros : parametros COMMA ID
                  | ID
                  | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
            
def p_bloque(p):
    '''bloque : instruccion
              | bloque instruccion'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_instruccion_remate(p):
    '''instruccion : REMATE expresion'''
    p[0] = Nodo('retorno', hijos=[p[2]])

def p_expresion_binaria(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion TIMES expresion
                 | expresion DIVIDE expresion'''
    p[0] = Nodo('bin_op', valor=p[2], hijos=[p[1], p[3]])

def p_expresion_group(p):
    '''expresion : LPAREN expresion RPAREN'''
    p[0] = p[2]

def p_expresion_numero(p):
    '''expresion : NUMBER'''
    p[0] = Nodo('numero', valor=p[1])

def p_expresion_id(p):
    '''expresion : ID'''
    p[0] = Nodo('identificador', valor=p[1])

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
    else:
        print("Error de sintaxis al final del input")

parser = yacc.yacc()

if __name__ == '__main__':
    data = '''
    jugador sumar(a, b):
        remate a pase b
    '''
    resultado = parser.parse(data)
    print(resultado)
