import re
import sys
import io
import contextlib
import traceback

class FutbolangInterpreter:
    def __init__(self):
        # Diccionario de traducciones de palabras clave
        self.translations = [
            # Orden importante: más específicas primero
            (r'\bdelantero\s+(\w+)\s+en\s+range\((.+)\):', r'for \1 in range(\2):'),  # Para range
            (r'\bdelantero\s+(\w+)\s+en\s+(\w+):', r'for \1 in \2:'),  # Nueva regla general
            (r'\btarjeta\s+(.+):', r'if \1:'),
            (r'\bamonestacion\s+(.+):', r'elif \1:'),  # Maneja el : existente
            (r'\bexpulsado:', r'else:'),  # Ya estaba correcto
            
            # Otros
            (r'\bgolazo\.imprimir\b', 'print'),
            (r'\bentrenador\.leer_texto\b', 'input'),
            (r'\bnombre\b', '__name__'),
            (r'\b__jugador_principal__\b', '__main__'),
            (r'\bVerdadero\b', 'True'),
            (r'\bFalso\b', 'False'),
            
            # Operadores
            (r'\bo\b', 'or'),
            (r'\by\b', 'and'),
            
            # Banderines para f-strings
            (r'F"(.*?)"', r'f"\1"')
        ]
    
    def translate(self, code):
        """Traduce código Futbolang a Python"""
        try:
            translated_code = code
            
            # Aplicar traducciones
            for pattern, replacement in self.translations:
                translated_code = re.sub(pattern, replacement, translated_code)
            
            # Imprimir código traducido para depuración
            print("--- Código Traducido ---")
            print(translated_code)
            print("--- Fin Código Traducido ---")
            
            return translated_code
        except Exception as e:
            print(f"Error en traducción: {e}")
            traceback.print_exc()
            return ""
    
    def run(self, code):
        try:
            python_code = self.translate(code)
            
            if not python_code:
                print("Error: No se pudo traducir el código")
                return
            
            # Espacio de nombres CORREGIDO
            namespace = {
                '__builtins__': __builtins__,
                '__name__': '__main__'  # <-- ¡Esta línea es crucial!
            }
            
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                exec(python_code, namespace)  # Ahora ejecutará el bloque principal
            
            captured_output = output.getvalue()
            print("--- Salida del Programa ---")
            print(captured_output)
            print("--- Fin Salida ---")
        
        except Exception as e:
            print(f"Error en la ejecución: {e}")
            print("Código traducido:")
            print(python_code)
            traceback.print_exc()

def main():
    # Si se pasa un archivo como argumento
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as file:
                code = file.read()
            
            print(f"Contenido del archivo {sys.argv[1]}:")
            print(code)
            print("--- Fin Contenido ---")
            
            interpreter = FutbolangInterpreter()
            interpreter.run(code)
        except FileNotFoundError:
            print(f"Error: Archivo {sys.argv[1]} no encontrado")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            traceback.print_exc()
    else:
        print("Por favor, proporcione un archivo Futbolang para ejecutar")

if __name__ == '__main__':
    main()