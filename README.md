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
  
## Ejemplo 1: Suma Simple
```bash
Archivo: ejemplo.futbol
jugador sumar(a, b):
    remate a pase b

jugador principal():
    remate sumar(10, 20)
```
- ** Explicación: **

jugador sumar(a, b): define una función llamada sumar que recibe dos parámetros.
remate a pase b retorna la suma de a y b (usa pase para la suma).
jugador principal(): define la función principal que llama a sumar con los argumentos 10 y 20.
Resultado esperado: 30.

## Ejemplo 2: Cuadrado y Suma de Cuadrados
Archivo: ejemplo2.futbol
```bash
jugador cuadrado(x):
    remate x tiro x

jugador sumaCuadrados(a, b):
    remate cuadrado(a) pase cuadrado(b)

jugador principal():
    remate sumaCuadrados(3, 4)
```

- ** Explicación: **

jugador cuadrado(x): define una función que calcula el cuadrado de x (usa tiro para la multiplicación).
jugador sumaCuadrados(a, b): retorna la suma de los cuadrados de a y b.
jugador principal(): llama a sumaCuadrados(3, 4).
Resultado esperado: 9 + 16 = 25.

## Ejemplo 3: Cálculo del Promedio
Archivo: ejemplo3.futbol

```bash
jugador promedio(a, b):
    remate (a pase b) intercepcion 2

jugador principal():
    remate promedio(10, 20)
```
- Explicación:

jugador promedio(a, b): calcula el promedio de a y b sumándolos (a pase b) y dividiendo el resultado entre 2 (intercepcion 2).
jugador principal(): invoca promedio(10, 20).
Resultado esperado: 15.

## Ejemplo 4: Operación Compuesta con Funciones Anidadas
Archivo: ejemplo4.futbol
```bash
jugador suma(a, b):
    remate a pase b

jugador resta(a, b):
    remate a regate b

jugador operacion(x, y):
    remate suma(x, resta(x, y))

jugador principal():
    remate operacion(10, 3)
```
- Explicación:

Se definen dos funciones básicas:
suma(a, b) para sumar.
resta(a, b) para restar.
jugador operacion(x, y): realiza una operación compuesta: primero resta y de x y luego suma el resultado a x.
jugador principal(): llama a operacion(10, 3).
Resultado esperado: 10 + (10 - 3) = 17.
