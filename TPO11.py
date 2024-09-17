# Se importa "emoji" para darle una calidad mayor a la salida por consola.
# Se importa el archivo "Funciones.py" para importar las funciones
import emoji
from Funciones import validate_guess, remove_accents, play_game, \
    cargar_palabras


# PROGRAMA PRINCIPAL
# Cargar la lista de palabras desde el archivo
LISTA_PALABRAS_POSIBLES = cargar_palabras('palabras.txt')

# Número máximo de intentos
INTENTOS_MAXIMO = 6

# Iniciar el juego
play_game(LISTA_PALABRAS_POSIBLES, INTENTOS_MAXIMO)

# Mensaje de bienvenida
print(
    f"\n{emoji.emojize(':robot:')} " f"BIENVENIDO A STRINGLE!"
    f"{emoji.emojize(':thinking_face:')}"
    )

bandera = True

while bandera:
    modo_normal = play_game(LISTA_PALABRAS_POSIBLES, INTENTOS_MAXIMO)
    restart = input("\nLe gustaría volver a jugar? (Y/N): ")
    restart = restart.upper()

    while restart != "Y" and restart != "N":
        restart = input("\nValor ingresado no reconocido. "
                        "Le gustaría volver a jugar? (Y/N): ")
        restart = restart.upper()

    if restart == "Y":
        bandera = True
    else:
        bandera = False
        print(f"\nGracias por jugar! {emoji.emojize(':people_hugging:')}\n")
