import ply.lex as lex
import ply.yacc as yacc
from flask import Flask, render_template, request

# Palabras reservadas
reserved = {
    'for': 'PALABRA_RESERVADA',
    'int': 'TIPO_DATO',
    'programa': 'PALABRA_RESERVADA',
    'read': 'PALABRA_RESERVADA',
    'printf': 'PALABRA_RESERVADA',
    'end': 'PALABRA_RESERVADA'
}

# Lista de tokens
tokens = [
    'IDENTIFICADOR',
    'PAREN_APERTURA',
    'PAREN_CIERRE',
    'LLAVE_APERTURA',
    'LLAVE_CIERRE',
    'PUNTO_COMA',
    'NUMERO',
    'OPERADOR_ASIGNACION',
    'MAS',
    'MENOS',
    'COMA',
    'CADENA'
] + list(reserved.values())

# Reglas de los tokens
t_ignore = ' \t'
t_PAREN_APERTURA = r'\('
t_PAREN_CIERRE = r'\)'
t_LLAVE_APERTURA = r'\{'
t_LLAVE_CIERRE = r'\}'
t_PUNTO_COMA = r';'
t_OPERADOR_ASIGNACION = r'='
t_MAS = r'\+'
t_MENOS = r'-'
t_COMA = r','
t_CADENA = r'\".*?\"'

# Expresión regular para números
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expresiones regulares para palabras reservadas
def t_PALABRA_RESERVADA(t):
    r'\b(for|programa|int|read|printf|end)\b'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')  
    return t

# Expresión regular para identificadores
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

# Manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejar errores léxicos
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Función para realizar el análisis léxico
def lexer_analysis(text):
    lexer.input(text)
    lexer.lineno = 1
    lex_tokens = []
    palabra_reservada_count = 0
    identificador_count = 0
    simbolo_count = 0
    numero_count = 0

    for tok in lexer:
        token_info = {
            'token': tok.value,
            'palabra_reservada': 'x' if tok.type in ['PALABRA_RESERVADA', 'TIPO_DATO'] else '',
            'numero': 'x' if tok.type == 'NUMERO' else '',
            'simbolo': 'x' if tok.type in ['PAREN_APERTURA', 'PAREN_CIERRE', 'LLAVE_APERTURA', 'LLAVE_CIERRE', 'PUNTO_COMA', 'OPERADOR_ASIGNACION', 'MAS', 'MENOS', 'COMA'] else '',
            'identificador': 'x' if tok.type == 'IDENTIFICADOR' else '',
            'tipo': tok.type.replace("_", " ").lower()
        }
        lex_tokens.append(token_info)

        if tok.type in ['PALABRA_RESERVADA', 'TIPO_DATO']:
            palabra_reservada_count += 1
        elif tok.type == 'IDENTIFICADOR':
            identificador_count += 1
        elif tok.type in ['PAREN_APERTURA', 'PAREN_CIERRE', 'LLAVE_APERTURA', 'LLAVE_CIERRE', 'PUNTO_COMA', 'OPERADOR_ASIGNACION', 'MAS', 'MENOS', 'COMA']:
            simbolo_count += 1
        elif tok.type == 'NUMERO':
            numero_count += 1

    return lex_tokens, palabra_reservada_count, identificador_count, simbolo_count, numero_count

# Análisis sintáctico
syntax_errors = []

# Regla principal del programa
def p_program(p):
    '''program : PALABRA_RESERVADA IDENTIFICADOR PAREN_APERTURA PAREN_CIERRE LLAVE_APERTURA instrucciones LLAVE_CIERRE'''
    pass

# Regla de instrucciones
def p_instrucciones(p):
    '''instrucciones : instruccion instrucciones
                     | instruccion
                     | empty'''
    pass

# Regla para instrucciones individuales
def p_instruccion(p):
    '''instruccion : TIPO_DATO lista_identificadores PUNTO_COMA
                   | IDENTIFICADOR OPERADOR_ASIGNACION expresion PUNTO_COMA
                   | PALABRA_RESERVADA IDENTIFICADOR PUNTO_COMA
                   | PALABRA_RESERVADA PAREN_APERTURA CADENA PAREN_CIERRE 
                   | PALABRA_RESERVADA PUNTO_COMA'''  
    pass

# Regla para lista de identificadores
def p_lista_identificadores(p):
    '''lista_identificadores : IDENTIFICADOR
                             | IDENTIFICADOR COMA lista_identificadores'''
    pass

# Regla para expresiones
def p_expresion(p):
    '''expresion : IDENTIFICADOR
                 | NUMERO
                 | expresion MAS expresion
                 | expresion MENOS expresion'''
    pass

# Regla vacía
def p_empty(p):
    'empty :'
    pass

# Manejo de errores sintácticos
def p_error(p):
    if p is None:
        syntax_errors.append("Error de sintaxis: Fin de archivo inesperado")
    else:
        syntax_errors.append(f"Error de sintaxis: Token inesperado '{p.value}' en la línea {p.lineno}")

# Función para realizar el análisis sintáctico
def parser_analysis(text):
    global syntax_errors
    syntax_errors = []
    result = parser.parse(text)
    
    if not syntax_errors:
        syntax_errors.append("Análisis sintáctico correcto")
    
    return syntax_errors

# Inicialización de Flask
app = Flask(__name__)

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    lex_tokens = []
    palabra_reservada_count = 0
    identificador_count = 0
    simbolo_count = 0
    numero_count = 0
    syntax_errors = []
    text = ""

    if request.method == 'POST':
        text = request.form['text']
        lex_tokens, palabra_reservada_count, identificador_count, simbolo_count, numero_count = lexer_analysis(text)
        syntax_errors = parser_analysis(text)

    return render_template('index6.html', text=text, lex_tokens=lex_tokens, palabra_reservada_count=palabra_reservada_count, identificador_count=identificador_count, simbolo_count=simbolo_count, numero_count=numero_count, syntax_errors=syntax_errors) 

# Inicializar el lexer y el parser
lexer = lex.lex()
parser = yacc.yacc()

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)