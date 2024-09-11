# STRINGLE - Juego de Adivinanza de Palabras

## Descripción

STRINGLE es un juego de adivinanza de palabras inspirado en el famoso juego Wordle. El objetivo del juego es adivinar una palabra secreta de 5 letras en un número limitado de intentos. Cada vez que se hace un intento, el juego proporciona retroalimentación sobre qué letras son correctas y si están en la posición correcta o incorrecta.

El juego también permite finalizar la partida antes de agotar los intentos ingresando `-1`.

## Características

- Palabras de 5 letras.
- 6 intentos para adivinar la palabra.
- Indicaciones en colores:
  - **Verde**: Letra correcta en la posición correcta.
  - **Amarillo**: Letra correcta en la posición incorrecta.
  - **Rojo**: Letra incorrecta.
- Opción para reiniciar el juego después de cada partida.

## Requisitos del Sistema

- Python 3.x
- Librerías adicionales: `emoji`, `colorama`

## Instalación

1. **Clona el repositorio o descarga los archivos:**

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd stringle
## Changelog

### [v1.2.0] - 11-09-2024
- **Archivos:** Se crea el archivo "Funciones.py" donde se agregan las funciones del código y se separan del código principal.

### [v1.2.0] - 10-09-2024
- **README:** Se crea el archivo README para proporcionar al usuario mayor información acerca del proyecto.
- **Mejoras:** Mejoras con Pep8

### [v1.2.0] - 09-09-2024
- **Emojis:** Se importan emojis que se muestran en consola para mayor calidad visual.
- **Cambios:** Cambios menores a la modularización y mas mejoras con Pep8.

### [v1.2.0] - 03-09-2024
- **Mejora:** Se utiliza Pep8 para cumplir con la pautas de estilo propuestos por la misma.
- 
### [v1.2.0] - 02-09-2024
- **Nueva Funcionalidad:** Se agregó la opción de finalizar el juego al ingresar `-1`.
- **Comentarios:** Se implementan comentarios para que el usuario comprenda el codigo fuente.
- **Mejora:** Mejoras en la validación de la entrada del usuario.
- - **Mejora:** Añadido soporte para eliminar tildes en las palabras de entrada.

### [v1.1.0] - 31-08-2024
- **Nueva Funcionalidad:** Colores en la consola usando `colorama`.
- **Lógica principal:** Se implementa la lógica principal del juego.

### [v1.0.0] - 26-08-2024
- **Lanzamiento inicial:** Implementación básica del juego.

- ***Gracias por jugar Stringle***
