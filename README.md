# Futbolang ⚽

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

**Futbolang** es un lenguaje de programación experimental que combina la sintaxis de Python con terminología futbolística. ¡Convierte tus algoritmos en un emocionante partido de código!

```python
# Ejemplo: Sistema de Evaluación de Becas
tarjeta nombre == "__jugador_principal__":
    alumnos = [
        {"edad": 22, "ingreso": 4000, "promedio": 95},
        {"edad": 17, "ingreso": 3000, "promedio": 88}
    ]
    
    delantero alumno en alumnos:
        tarjeta alumno["edad"] < 19 o alumno["edad"] > 24:
            golazo.imprimir("✖ Edad no válida")
        expulsado:
            golazo.imprimir("✓ ¡Beca aprobada!")
```
Tabla de Contenidos
Características

Instalación

Uso

Sintaxis

Ejemplos

Roadmap

Contribuir

Licencia

Características 🏆
Terminología futbolística: Estructuras de control con nombres de acciones del fútbol

Traducción a Python: Ejecuta código a través de Python 3.6+

Tipado dinámico: Soporta todos los tipos de datos de Python

Manejo de errores: Mensajes claros con seguimiento de excepciones

F-strings: Soporte completo para cadenas formateadas

Instalación ⚙️
Clona el repositorio:
git clone https://github.com/tuusuario/futbolang.git
cd futbolang

Ejecuta los programas .futbol:

python futbolang.py ejemplo.futbol

Uso 🚀
Ejecutar un programa:
python futbolang.py programa.futbol
Ejemplo interactivo con entrada de usuario:
python futbolang.py becas_input.futbol

Sintaxis 📖
Futbolang	Python	Ejemplo
tarjeta	if	tarjeta x > 5:
amonestacion	elif	amonestacion x < 0:
expulsado	else	expulsado:
delantero	for	delantero i en range(5):
golazo.imprimir	print	golazo.imprimir("Gol!")
entrenador.leer_texto	input	edad = entrenador.leer_texto("Edad: ")
Verdadero/Falso	True/False	rechazado = Falso
F"texto"	f-strings	F"Alumno {nombre}"
