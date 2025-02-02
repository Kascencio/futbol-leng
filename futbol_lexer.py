import ply.lex as lex

# Lista de tokens
tokens = (
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'COLON', 'COMMA',
)

# Palabras reservadas en Futbolang-Funcional
reserved = {
    'jugador': 'JUGADOR',
    'remate': 'REMATE',
    'tarjeta': 'TARJETA',
    'amonestacion': 'AMONESTACION',
    'expulsado': 'EXPULSADO',
    # Agrega aquí más palabras clave según tu lenguaje
}

tokens = tokens + tuple(reserved.values())

# Reglas de expresiones regulares simples para tokens
t_PLUS    = r'pase'
t_MINUS   = r'regate'
t_TIMES   = r'tiro'
t_DIVIDE  = r'intercepcion'
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
    r'[A-Za-z_][A-Za-z_0-9]*'
    # Comprueba si es una palabra reservada
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':
    data = '''
    jugador sumar(a, b):
        remate a pase b
    '''
    lexer.input(data)
    for token in lexer:
        print(token)
