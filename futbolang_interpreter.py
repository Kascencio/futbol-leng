#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import ply.lex as lex
import ply.yacc as yacc

###############################################################################
#                                LEXER                                        #
###############################################################################

# Palabras reservadas (incluyendo operadores y palabras de control)
reserved = {
    'jugador': 'JUGADOR',
    'remate': 'REMATE',
    'pase': 'PLUS',
    'regate': 'MINUS',
    'tiro': 'TIMES',
    'intercepcion': 'DIVIDE',
    'tarjeta': 'IF',
    'amonestacion': 'ELIF',
    'expulsado': 'ELSE',
    'delantero': 'FOR',
    'en': 'EN',
    'rango': 'RANGE',
    'y': 'AND',
    'nada': 'NOP'
}

# Lista de tokens (se incluye STRING para literales y demás tokens)
tokens = (
    'NUMBER',
    'ID',
    'STRING',
    'GT',
    'LT',
    'GE',
    'LE',
    'EQ',
    'ASSIGN',
    'NEWLINE',
    'LPAREN',
    'RPAREN',
    'COLON',
    'COMMA',
) + tuple(reserved.values())

# Definición de tokens fijos para paréntesis, dos puntos y coma
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COLON   = r':'
t_COMMA   = r','

# Otros símbolos
t_ASSIGN  = r'='
t_GT      = r'>'
t_LT      = r'<'
t_GE      = r'>='
t_LE      = r'<='
t_EQ      = r'=='
# Ignoramos espacios, tabulaciones y retornos de carro (\r)
t_ignore  = ' \t\r'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    # Remover las comillas de apertura y cierre
    t.value = t.value[1:-1]
    return t

# Permite que los identificadores incluyan puntos (por ejemplo, "entrenador.leer_texto")
def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

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
        self.value = value          # Valor (número, nombre, operador, etc.)
        self.children = children or []  # Lista de nodos hijos

    def __repr__(self):
        return f"Node({self.type}, {self.value}, {self.children})"

###############################################################################
#                            PARSER (GRAMÁTICA)                               #
###############################################################################

# Precedencia para operadores aritméticos y lógicos
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
    'function : JUGADOR ID LPAREN param_list RPAREN COLON NEWLINE block'
    # p[2]: nombre de la función, p[4]: lista de parámetros, p[8]: bloque de sentencias
    p[0] = Node("function", value=p[2], children=[p[4], p[8]])

def p_param_list(p):
    '''param_list : param_list COMMA ID
                  | ID
                  | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]

# Un bloque es una o más sentencias separadas por NEWLINE
def p_block(p):
    '''block : statement
             | block NEWLINE statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# --- Sentencias ---
# Asignación: variable = expresión
def p_statement_assign(p):
    'statement : ID ASSIGN expression'
    p[0] = Node("assign", value=p[1], children=[p[3]])

# Sentencia de retorno
def p_statement_return(p):
    'statement : REMATE expression'
    p[0] = Node("return", children=[p[2]])

# Sentencia condicional (if/elif/else)
def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN COLON NEWLINE block opt_if'''
    # p[3]: condición; p[8]: bloque "if"; p[9]: cláusulas opcionales (elif/else)
    p[0] = Node("if", children=[p[3], p[8], p[9]])

def p_opt_if(p):
    '''opt_if : ELIF LPAREN expression RPAREN COLON NEWLINE block opt_if
              | ELSE COLON NEWLINE block
              | empty'''
    if len(p) == 8:
        p[0] = [("elif", p[3], p[7])] + p[8]
    elif len(p) == 6:
        p[0] = [("else", None, p[4])]
    else:
        p[0] = []

# Sentencia de bucle: for variable en rango(expression) : NEWLINE block
def p_statement_for(p):
    'statement : FOR ID EN RANGE LPAREN expression RPAREN COLON NEWLINE block'
    p[0] = Node("for", value=p[2], children=[p[6], p[10]])

# Sentencia de expresión (para llamadas que se usan como sentencia)
def p_statement_expr(p):
    'statement : expression'
    p[0] = Node("expr", children=[p[1]])

# Sentencia NOP: la palabra "nada" se interpreta como una sentencia vacía (equivalente a "pass")
def p_statement_nop(p):
    'statement : NOP'
    p[0] = Node("nop")

# --- Expresiones ---
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = Node("binop", value=p.slice[2].type, children=[p[1], p[3]])

def p_expression_compare(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression'''
    p[0] = Node("compare", value=p.slice[2].type, children=[p[1], p[3]])

def p_expression_and(p):
    'expression : expression AND expression'
    p[0] = Node("and", children=[p[1], p[3]])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Node("number", value=p[1])

def p_expression_string(p):
    'expression : STRING'
    p[0] = Node("string", value=p[1])

def p_expression_id(p):
    'expression : ID'
    p[0] = Node("var", value=p[1])

def p_expression_fun_call(p):
    'expression : ID LPAREN arg_list RPAREN'
    p[0] = Node("fun_call", value=p[1], children=p[3])

def p_arg_list(p):
    '''arg_list : arg_list COMMA expression
                | expression
                | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]

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

# Diccionario global para funciones definidas por el usuario
global_functions = {}

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

def eval_expr(node, env):
    if node.type == "number":
        return node.value
    elif node.type == "string":
        return node.value
    elif node.type == "var":
        if node.value in env:
            return env[node.value]
        else:
            raise Exception(f"Variable '{node.value}' no definida")
    elif node.type == "binop":
        left = eval_expr(node.children[0], env)
        right = eval_expr(node.children[1], env)
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
    elif node.type == "compare":
        left = eval_expr(node.children[0], env)
        right = eval_expr(node.children[1], env)
        op = node.value
        if op == "GT":
            return left > right
        elif op == "LT":
            return left < right
        elif op == "GE":
            return left >= right
        elif op == "LE":
            return left <= right
        elif op == "EQ":
            return left == right
        else:
            raise Exception(f"Operador de comparación desconocido: {op}")
    elif node.type == "and":
        return eval_expr(node.children[0], env) and eval_expr(node.children[1], env)
    elif node.type == "fun_call":
        func_name = node.value
        args = [eval_expr(arg, env) for arg in node.children]
        # Funciones integradas para entrada/salida
        if func_name == "entrenador.leer_texto":
            prompt = args[0] if args else ""
            return input(prompt)
        elif func_name == "golazo.imprimir":
            print(*args)
            return None
        elif func_name in global_functions:
            func_def = global_functions[func_name]
            params = func_def.children[0]  # lista de parámetros
            block = func_def.children[1]   # bloque de sentencias
            if len(params) != len(args):
                raise Exception(f"La función '{func_name}' espera {len(params)} argumentos, se dieron {len(args)}")
            new_env = env.copy()
            for param, arg_val in zip(params, args):
                new_env[param] = arg_val
            return exec_block(block, new_env)
        else:
            # Soporte para funciones básicas integradas: int, float, str
            if func_name == "int":
                return int(args[0])
            elif func_name == "float":
                return float(args[0])
            elif func_name == "str":
                return str(args[0])
            else:
                raise Exception(f"Función '{func_name}' no definida")
    else:
        raise Exception(f"Nodo de expresión no soportado: {node}")

def exec_statement(stmt, env):
    if stmt.type == "assign":
        env[stmt.value] = eval_expr(stmt.children[0], env)
    elif stmt.type == "return":
        raise ReturnException(eval_expr(stmt.children[0], env))
    elif stmt.type == "if":
        if eval_expr(stmt.children[0], env):
            return exec_block(stmt.children[1], env)
        else:
            for option in stmt.children[2]:
                tipo, cond, block = option
                if tipo == "elif":
                    if eval_expr(cond, env):
                        return exec_block(block, env)
                elif tipo == "else":
                    return exec_block(block, env)
    elif stmt.type == "for":
        iterations = eval_expr(stmt.children[0], env)
        var = stmt.value
        result = None
        for i in range(int(iterations)):
            new_env = env.copy()
            new_env[var] = i
            try:
                result = exec_block(stmt.children[1], new_env)
            except ReturnException as ret:
                result = ret.value
                break
        return result
    elif stmt.type == "expr":
        return eval_expr(stmt.children[0], env)
    elif stmt.type == "nop":
        return None
    else:
        raise Exception(f"Sentencia no soportada: {stmt}")

def exec_block(block, env):
    result = None
    for stmt in block:
        try:
            result = exec_statement(stmt, env)
        except ReturnException as ret:
            return ret.value
    return result

def exec_program(ast):
    # Registrar funciones definidas globalmente
    for func in ast.children:
        if func.type == "function":
            global_functions[func.value] = func
    if "principal" in global_functions:
        try:
            result = eval_expr(Node("fun_call", value="principal", children=[]), {})
            print("Resultado de 'principal':", result)
        except ReturnException as ret:
            print("Resultado de 'principal':", ret.value)
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
    ast = parser.parse(data)
    if ast is None:
        print("Error al parsear el archivo fuente.")
        sys.exit(1)
    print("AST generado:")
    print(ast)
    print("--------------------------------------------------")
    exec_program(ast)

if __name__ == '__main__':
    main()
