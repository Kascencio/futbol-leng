#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import ply.lex as lex
import ply.yacc as yacc

###############################################################################
#                                LEXER                                        #
###############################################################################

# Definir las palabras reservadas, incluyendo los operadores
reserved = {
    'jugador': 'JUGADOR',
    'remate': 'REMATE',
    'pase': 'PLUS',
    'regate': 'MINUS',
    'tiro': 'TIMES',
    'intercepcion': 'DIVIDE',
}

# Lista de tokens básicos (sin incluir los reservados) y se añaden al final
tokens = (
    'NUMBER',
    'ID',
    'LPAREN',
    'RPAREN',
    'COLON',
    'COMMA',
) + tuple(reserved.values())

# Expresiones regulares para símbolos fijos
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COLON   = r':'
t_COMMA   = r','

# Ignorar espacios y tabulaciones
t_ignore  = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    # Si el identificador coincide con una palabra reservada, se asigna el token correspondiente.
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

###############################################################################
#                              AST (Nodo)                                     #
###############################################################################

class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type            # Por ejemplo: "number", "binop", "function", etc.
        self.value = value          # Valor numérico, nombre de función, operador, etc.
        self.children = children or []  # Lista de nodos hijos

    def __repr__(self):
        return f"Node({self.type}, {self.value}, {self.children})"

###############################################################################
#                            PARSER (GRAMÁTICA)                               #
###############################################################################

# Definir precedencia para los operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# --- Programa y definición de funciones ---

def p_program(p):
    'program : function_list'
    p[0] = Node("program", children=p[1])

def p_function_list(p):
    '''function_list : function_list function
                     | function'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_function(p):
    'function : JUGADOR ID LPAREN param_list RPAREN COLON statement'
    # p[2]: nombre de la función  
    # p[4]: lista de parámetros  
    # p[7]: statement (en este ejemplo, únicamente una instrucción "remate")
    p[0] = Node("function", value=p[2], children=[p[4], p[7]])

def p_param_list(p):
    '''param_list : param_list COMMA ID
                  | ID
                  | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]

def p_statement(p):
    'statement : REMATE expression'
    p[0] = Node("return", children=[p[2]])

# --- Expresiones ---
# Se combina la parte recursiva (operaciones binarias) con la parte "primary".
def p_expression(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | primary
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        # Usamos p.slice[2].type para obtener el tipo del token (por ejemplo, "PLUS")
        p[0] = Node("binop", value=p.slice[2].type, children=[p[1], p[3]])

# Reglas para expresiones "primary" (átomos)
def p_primary_number(p):
    'primary : NUMBER'
    p[0] = Node("number", value=p[1])

def p_primary_id(p):
    'primary : ID'
    p[0] = Node("var", value=p[1])

def p_primary_fun_call(p):
    'primary : ID LPAREN arg_list RPAREN'
    p[0] = Node("fun_call", value=p[1], children=p[3])

def p_primary_paren(p):
    'primary : LPAREN expression RPAREN'
    p[0] = p[2]

def p_arg_list(p):
    '''arg_list : arg_list COMMA expression
                | expression
                | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print("Error de sintaxis en '%s'" % p.value)
    else:
        print("Error de sintaxis al final de la entrada")

parser = yacc.yacc()

###############################################################################
#                          INTERPRETADOR (EJECUCIÓN)                          #
###############################################################################

# Diccionario global para almacenar las definiciones de función
functions = {}

def evaluate_expr(node, env):
    """Evalúa una expresión a partir del AST y un entorno (diccionario de variables)."""
    if node.type == "number":
        return node.value
    elif node.type == "var":
        name = node.value
        if name in env:
            return env[name]
        else:
            raise Exception(f"Variable '{name}' no definida")
    elif node.type == "binop":
        left = evaluate_expr(node.children[0], env)
        right = evaluate_expr(node.children[1], env)
        op = node.value
        if op == "PLUS":
            return left + right
        elif op == "MINUS":
            return left - right
        elif op == "TIMES":
            return left * right
        elif op == "DIVIDE":
            return left / right
        else:
            raise Exception(f"Operador desconocido: {op}")
    elif node.type == "fun_call":
        func_name = node.value
        args = [evaluate_expr(arg, env) for arg in node.children]
        if func_name in functions:
            func_def = functions[func_name]
            params = func_def.children[0]  # Lista de parámetros
            stmt = func_def.children[1]     # El statement (nodo "return")
            if len(params) != len(args):
                raise Exception(f"La función '{func_name}' espera {len(params)} argumentos, se dieron {len(args)}")
            # Crear un nuevo entorno para la llamada (copia del entorno actual)
            new_env = env.copy()
            for param, arg_val in zip(params, args):
                new_env[param] = arg_val
            return evaluate_statement(stmt, new_env)
        else:
            raise Exception(f"Función '{func_name}' no definida")
    else:
        raise Exception(f"Nodo no soportado en evaluación: {node}")

def evaluate_statement(node, env):
    """Evalúa un statement. En este ejemplo, se soporta únicamente 'remate' (return)."""
    if node.type == "return":
        return evaluate_expr(node.children[0], env)
    else:
        raise Exception("Tipo de statement no soportado")

def execute_program(ast):
    """
    Recorre el AST para almacenar todas las definiciones de función en el diccionario
    global 'functions'. Luego, si se definió la función 'principal', se la invoca.
    """
    for func in ast.children:
        if func.type == "function":
            functions[func.value] = func
    if "principal" in functions:
        result = evaluate_expr(Node("fun_call", value="principal", children=[]), {})
        print("Resultado de 'principal':", result)
    else:
        print("No se definió la función 'principal'.")

###############################################################################
#                                  MAIN                                     #
###############################################################################

def main():
    if len(sys.argv) < 2:
        print("Uso: python futbolang_interpreter.py <archivo.futbol>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"El archivo '{filename}' no se encontró.")
        sys.exit(1)

    # Parsear el código fuente y generar el AST
    ast = parser.parse(data)
    print("AST generado:")
    print(ast)
    print("--------------------------------------------------")
    # Ejecutar el programa interpretando el AST
    execute_program(ast)

if __name__ == '__main__':
    main()
