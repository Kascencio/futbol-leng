# Futbolang

**Futbolang** es un lenguaje de programación conceptual inspirado en Python y en el fútbol. Utiliza términos futbolísticos para definir la sintaxis y la semántica, haciendo que funciones, operaciones y estructuras de control tengan nombres relacionados con el mundo del fútbol. Este repositorio incluye un intérprete básico escrito en Python utilizando [PLY (Python Lex-Yacc)](http://www.dabeaz.com/ply/), que permite ejecutar un subconjunto de Futbolang.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Ejemplos](#ejemplos)
  - [Ejemplo 1: Suma Simple](#ejemplo-1--suma-simple)
  - [Ejemplo 2: Cuadrado y Suma de Cuadrados](#ejemplo-2--cuadrado-y-suma-de-cuadrados)
  - [Ejemplo 3: Cálculo del Promedio](#ejemplo-3--cálculo-del-promedio)
  - [Ejemplo 4: Operación Compuesta con Funciones Anidadas](#ejemplo-4--operación-compuesta-con-funciones-anidadas)


## Características

- **Sintaxis futbolística:**  
  - `jugador` para definir funciones (equivalente a `def` en Python).
  - `remate` para retornar valores (equivalente a `return`).
  - Operadores aritméticos con nombres futbolísticos:
    - `pase` → suma.
    - `regate` → resta.
    - `tiro` → multiplicación.
    - `intercepcion` → división.

- **Intérprete Básico:**  
  Utilizando PLY, el intérprete traduce el código de Futbolang a un AST (Árbol de Sintaxis Abstracta) y luego lo evalúa.

## Requisitos

- **Python 3.x**
- **PLY (Python Lex-Yacc):**  
  Puedes instalarlo con pip:
  ```bash
  pip install ply
